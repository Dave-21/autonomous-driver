import os
import sys
import json
import time
import signal
import argparse
import subprocess
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import TypedDict, Optional, List

BASE_DIR = Path(r"C:\Users\david\code\autonomous\autonomous-driver").resolve()
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

try:
    from src.agent.guardrails import (
        SHUTDOWN_REQUESTED,
        sandboxed_write_candidate,
        execute_isolated_benchmark,
        save_agent_state,
        ALLOWED_MUTABLE_FILE,
        log_experiment_attempt,
        auto_install_package_if_allowed
    )
    from src.agent.web_search import search_web_knowledge
except (ModuleNotFoundError, ImportError):
    from guardrails import (
        SHUTDOWN_REQUESTED,
        sandboxed_write_candidate,
        execute_isolated_benchmark,
        save_agent_state,
        ALLOWED_MUTABLE_FILE,
        log_experiment_attempt
    )
    from web_search import search_web_knowledge

from langgraph.graph import StateGraph, END

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5-coder:7b-instruct-q8_0"
TRIPLE_BACKTICKS = chr(96) * 3

# -----------------------------------------------------------------------------
# 1. STRICT DATA SCHEMA & TOOL MANIFESTS
# -----------------------------------------------------------------------------
DATA_SCHEMA_MANIFEST = """
============================== STRICT DATA SCHEMA ==============================
RAW INPUT INGREDIENTS GUARANTEED PRESENT IN df_train & df_test:
| Column Name                     | Dtype   | Description                                              |
| :------------------------------ | :------ | :------------------------------------------------------- |
| `timestamp`                     | object  | ISO Datetime string                                      |
| `month`                         | int64   | Calendar month (1 - 12)                                  |
| `day_of_week`                   | int64   | Day of week (0=Mon, ..., 6=Sun)                          |
| `wti_usd_bbl`                   | float64 | WTI crude oil front-month settlement ($/bbl)             |
| `brent_usd_bbl`                 | float64 | Brent crude oil settlement ($/bbl)                       |
| `rbob_wholesale_usd_gal`        | float64 | NYMEX RBOB gasoline wholesale futures ($/gal)            |
| `crude_to_rbob_crack_spread`    | float64 | Refining margin spread: (RBOB * 42) - WTI ($/bbl)        |
| `local_price_spread_usd`        | float64 | Lincoln Rd station price spread ($/gal)                  |
| `tax_floor_usd`                 | float64 | Michigan fuel taxes & environmental floor ($/gal)        |
| `traffic_index`                 | float64 | Upper Peninsula US-41 commercial traffic index           |
| `is_summer_blend`               | int64   | 1 if EPA summer RVP blend active, 0 otherwise            |
| `whiting_refinery_outage_risk`  | float64 | BP Whiting refinery outage risk index (0.0 - 1.0)        |
| `green_bay_terminal_risk`       | float64 | Green Bay pipeline terminal bottleneck risk (0.0 - 1.0)  |
| `national_refinery_outage_risk` | float64 | U.S. nationwide refinery utilization risk (0.0 - 1.0)    |
| `target_escanaba_retail_price`  | float64 | TARGET Y (in df_train only; predict this for test)       |

RULE: All raw input columns you read from must come from this table.
You CAN and SHOULD create new engineered features by combining these ingredients!
================================================================================
"""

TOOL_MANIFEST = """
============================= AGENT TOOL MANIFEST =============================
1. `web_search(query: str) -> str`: DuckDuckGo knowledge lookup for modeling techniques and syntax.
2. `auto_install_package(pkg: str)`: Automatic pip installer for machine learning packages.
3. `ast_static_analyzer(code: str)`: Static syntax tree validation preventing unauthorized OS calls.
4. `walk_forward_evaluator()`: 4-Fold sequential walk-forward time-series backtesting engine.
================================================================================
"""

class AgentCouncilState(TypedDict):
    mode: str
    iteration: int
    max_iterations: int
    retry_count: int
    max_retries: int
    promotions_total: int
    champion_mae: float
    champion_asym_mae: float
    champion_composite_score: float
    champion_code: str
    feature_proposal: str
    web_research_context: str
    candidate_code: str
    last_error: Optional[str]
    candidate_mae: Optional[float]
    candidate_asym_mae: Optional[float]
    candidate_dir_acc: Optional[float]
    candidate_decision_acc: Optional[float]
    candidate_composite_score: Optional[float]
    candidate_model_type: Optional[str]
    candidate_hyperparams: Optional[dict]
    recent_trials_summary: List[str]
    eval_error: Optional[str]
    status: str

def compute_composite_score(mae: float, asym_mae: float, dir_acc: float) -> float:
    dir_acc_norm = max(0.0, min(1.0, dir_acc / 100.0))
    dir_penalty = 1.0 + 0.20 * (1.0 - dir_acc_norm)
    score = (0.50 * mae + 0.50 * asym_mae) * dir_penalty
    return round(score, 4)

def check_ollama_health() -> bool:
    try:
        req = urllib.request.Request("http://localhost:11434/", method="GET")
        with urllib.request.urlopen(req, timeout=3) as resp:
            return resp.status == 200
    except Exception:
        return False

def call_ollama(prompt: str, temperature: float = 0.3, max_retries: int = 3) -> str:
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": temperature}
    }
    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    for attempt in range(1, max_retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                return json.loads(resp.read().decode("utf-8")).get("response", "")
        except urllib.error.URLError as e:
            if attempt == max_retries:
                raise ConnectionError(f"[FATAL] Cannot connect to Ollama at {OLLAMA_URL}.") from e
            time.sleep(2)

def extract_code(llm_output: str) -> str:
    py_marker = TRIPLE_BACKTICKS + "python"
    generic_marker = TRIPLE_BACKTICKS
    if py_marker in llm_output:
        return llm_output.split(py_marker)[1].split(generic_marker)[0].strip()
    elif generic_marker in llm_output:
        return llm_output.split(generic_marker)[1].split(generic_marker)[0].strip()
    return llm_output.strip()

def get_clean_tail_error(full_error: str) -> str:
    lines = [line.strip() for line in full_error.splitlines() if line.strip()]
    return "\n".join(lines[-10:]) if len(lines) > 10 else "\n".join(lines)

def extract_search_query_from_error(full_error: str) -> str:
    lines = [line.strip() for line in full_error.splitlines() if line.strip()]
    for line in reversed(lines):
        if "KeyError:" in line:
            return "python pandas KeyError column not in index fix"
        if any(err in line for err in ["ValueError:", "TypeError:", "NameError:", "AttributeError:", "ModuleNotFoundError:"]):
            clean_err = line.split(":")[-1].strip()
            err_type = line.split(":")[0].strip()
            return f"python {err_type} {clean_err}"[:90]
    return "python scikit-learn model predict error"

def generate_and_save_dashboard(telemetry: dict, candidate_code: str = "") -> str:
    ts = telemetry.get("timestamp", datetime.now().isoformat())
    date_str = ts.split("T")[0]
    metrics = telemetry.get("metrics", {})
    forecast = telemetry.get("forecast_tomorrow", {})
    model_type = telemetry.get("model_type", "Unknown")

    cur_price = forecast.get("current_retail_avg", 0.0)
    pred_price = forecast.get("predicted_tomorrow_retail", 0.0)
    delta = forecast.get("expected_delta_usd", 0.0)
    recommendation = forecast.get("recommendation", "BUY AS NEEDED")

    if delta >= 0.025:
        icon = "🚨"
        analysis = (
            f"Wholesale RBOB futures and terminal rack costs indicate imminent upward price pressure. "
            f"Lincoln Road pump prices are projected to rise by ~+${delta:.2f}/gal within 24-48 hours. "
            f"Fill up today to lock in current rates."
        )
    elif delta <= -0.025:
        icon = "⏳"
        analysis = (
            f"Downstream wholesale costs in Green Bay/Chicago have eased while station margins expanded. "
            f"Lincoln Road pump prices are projected to drop by -${abs(delta):.2f}/gal over the next 1-2 days. "
            f"Hold off on filling up until tomorrow to capture lower prices."
        )
    else:
        icon = "⚖️"
        analysis = (
            f"Wholesale rack costs and local retail prices are in equilibrium. "
            f"No major swings anticipated. Buy fuel as needed."
        )

    dashboard_content = f"""# Escanaba Retail Fuel Intelligence Dashboard
**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | **Data Timestamp:** {ts}

---

## {icon} Driver Recommendation: {recommendation}
**Current Lincoln Rd Average:** ${cur_price:.3f}/gal  
**Projected 24h Retail Price:** ${pred_price:.3f}/gal (**{'+' if delta > 0 else ''}{delta:.3f}/gal**)

### Market Analysis
{analysis}

---

## Model Benchmark Telemetry
- **Active Champion Architecture:** `{model_type}`
- **Walk-Forward Backtest MAE:** `${metrics.get('mae_usd', 0.0):.4f}/gal`
- **Asymmetric Spike Loss (Penalty for Missed Surges):** `${metrics.get('asymmetric_mae_usd', 0.0):.4f}/gal`
- **Directional Trend Accuracy:** `{metrics.get('directional_accuracy_pct', 0.0)}%`
- **Driver Decision Success Rate:** `{metrics.get('decision_success_pct', 0.0)}%`

---
*Autonomous MLOps commit verified by AST Guardrail & LangGraph Council.*
"""

    os.makedirs(BASE_DIR / "dashboards", exist_ok=True)
    date_file = BASE_DIR / "dashboards" / f"{date_str}_escanaba_telemetry.md"
    latest_file = BASE_DIR / "dashboards" / "latest_telemetry.md"

    with open(date_file, "w", encoding="utf-8") as f:
        f.write(dashboard_content)
    with open(latest_file, "w", encoding="utf-8") as f:
        f.write(dashboard_content)

    return str(latest_file)

def check_and_sync_daily_dashboard(champion_code: str):
    """Guarantees today's dashboard is evaluated and synced to GitHub before trials begin."""
    today_str = datetime.now().strftime("%Y-%m-%d")
    date_file = BASE_DIR / "dashboards" / f"{today_str}_escanaba_telemetry.md"

    if not date_file.exists():
        print(f"╭── [DAILY DASHBOARD HEARTBEAT] ─────────────────────────────")
        print(f"│ Syncing today's forecast with active champion model...")
        bench = execute_isolated_benchmark()
        if bench["success"]:
            dash_path = generate_and_save_dashboard(bench["telemetry"], champion_code)
            print(f"│ Published: dashboards/{today_str}_escanaba_telemetry.md")
            
            subprocess.run(["git", "add", "dashboards/", "data/telemetry.json"], cwd=str(BASE_DIR))
            commit_msg = f"Daily Fuel Intelligence: Champion {bench['telemetry']['model_type']} update for {today_str}"
            subprocess.run(["git", "commit", "-m", commit_msg], cwd=str(BASE_DIR))
            push_res = subprocess.run(["git", "push"], cwd=str(BASE_DIR), capture_output=True, text=True)
            if push_res.returncode == 0:
                print("│ GitHub Remote: Synced successfully.")
            else:
                print(f"│ GitHub Remote: Local commit ready ({push_res.stderr.strip()[:40]}).")
        print(f"╰────────────────────────────────────────────────────────────\n")
    else:
        print(f"✓ Daily GitHub forecast dashboard is current for {today_str}.\n")

# -----------------------------------------------------------------------------
# LangGraph Council Nodes
# -----------------------------------------------------------------------------
def feature_engineer_node(state: AgentCouncilState) -> dict:
    current_iter = state["iteration"] + 1
    
    mode_tag = f"[{state['mode'].upper()}]"
    print(f"╭── ITERATION {current_iter} {mode_tag} " + "─" * (48 - len(str(current_iter)) - len(mode_tag)))
    print(f"│ 🔍 Feature Engineer : Researching econometric strategies via DuckDuckGo...")
    
    web_knowledge = search_web_knowledge("retail gasoline price econometric feature engineering spread ratio momentum", max_results=2)

    prompt = (
        f"{DATA_SCHEMA_MANIFEST}\n\n"
        f"EMPIRICAL RESEARCH FINDINGS:\n{web_knowledge}\n\n"
        "TASK:\n"
        "Propose 2 high-impact feature transformations using ONLY columns from the table above.\n"
        "STRICT CONSTRAINT: You CANNOT invent new base column names (e.g. 'proximity_to_escanaba' is FORBIDDEN).\n"
        "Keep your output to 3 concise sentences."
    )
    try:
        proposal = call_ollama(prompt, temperature=0.3)
    except Exception:
        proposal = "Calculate 3-day RBOB price momentum and ratio of crack spread to local price spread."

    # Format proposal cleanly
    clean_lines = [l.strip() for l in proposal.splitlines() if l.strip() and not l.startswith("```")]
    display_prop = " ".join(clean_lines)
    if len(display_prop) > 115:
        display_prop = display_prop[:112] + "..."
    print(f"│ 💡 Proposal         : {display_prop}")

    return {
        "iteration": current_iter,
        "retry_count": 0,
        "last_error": None,
        "web_research_context": web_knowledge,
        "feature_proposal": proposal
    }

def model_architect_node(state: AgentCouncilState) -> dict:
    is_retry = state["retry_count"] > 0
    research_section = ""

    if is_retry and state["last_error"]:
        print(f"│ ⚠️  Model Architect  : Self-repair retry {state['retry_count']}/{state['max_retries']} (DuckDuckGo Diagnostic RAG)...")
        tail_err = get_clean_tail_error(state["last_error"])
        search_query = extract_search_query_from_error(tail_err)
        rag_solution = search_web_knowledge(search_query, max_results=2)

        schema_error_warning = ""
        if "KeyError:" in tail_err:
            bad_col = tail_err.split("KeyError:")[-1].strip()
            schema_error_warning = (
                f"\nCRITICAL COLUMN ERROR:\n"
                f"You tried to access {bad_col}, which DOES NOT EXIST in the raw DataFrame!\n"
                f"You MUST remove {bad_col} and ONLY use columns from the Strict Data Schema!\n"
            )

        research_section = (
            f"ERROR IN PREVIOUS ATTEMPT:\n```\n{tail_err}\n```\n"
            f"{schema_error_warning}\n"
            f"DUCKDUCKGO RAG FIX REFERENCE:\n{rag_solution}\n\n"
        )
    else:
        print(f"│ ⚙️  Model Architect  : Synthesizing candidate architecture & features...")
        research_section = f"DOMAIN BACKGROUND:\n{state.get('web_research_context', '')}\n\n"

    history_context = "\n".join(state["recent_trials_summary"][-3:]) if state["recent_trials_summary"] else "None yet."

    prompt = (
        f"{DATA_SCHEMA_MANIFEST}\n\n"
        f"{TOOL_MANIFEST}\n\n"
        f"{research_section}"
        f"RECENT TRIAL HISTORY:\n{history_context}\n\n"
        f"CURRENT CHAMPION SCORE: {state['champion_composite_score']:.4f} (MAE: ${state['champion_mae']:.4f})\n"
        f"PROPOSED FEATURE STRATEGY:\n{state['feature_proposal']}\n\n"
        f"ARCHITECTURAL INSTRUCTIONS:\n"
        f"To beat the Champion (${state['champion_mae']:.4f} MAE), use regularized regression or shallow gradient boosting:\n"
        f"- Option A: `GradientBoostingRegressor(n_estimators=35, max_depth=2, learning_rate=0.04, subsample=0.85)`\n"
        f"- Option B: `RidgeCV(alphas=np.logspace(-3, 3, 13))` with interaction features\n"
        f"- Option C: `HistGradientBoostingRegressor(max_iter=30, min_samples_leaf=4, l2_regularization=3.0)`\n"
        f"- Option D: `HuberRegressor(alpha=1.0, epsilon=1.35)` with StandardScaler\n\n"
        f"MANDATORY FUNCTION CONTRACT:\n"
        f"1. Define `def extract_features(df: pd.DataFrame) -> pd.DataFrame:`\n"
        f"   - ONLY use columns from the Strict Data Schema table. NEVER invent column names.\n"
        f"   - Return a DataFrame of numeric columns with `.bfill().fillna(0.0)`.\n"
        f"2. Define `def train_and_forecast(df_train: pd.DataFrame, df_test: pd.DataFrame, tomorrow_features: dict) -> dict:`\n"
        f"   - Net margin target: `y_train = df_train['target_escanaba_retail_price'] - df_train['rbob_wholesale_usd_gal'] - df_train['tax_floor_usd']`\n"
        f"   - `X_train = extract_features(df_train); X_test = extract_features(df_test)`\n"
        f"   - Fit model on (X_train, y_train)\n"
        f"   - Predict test retail: `pred_test = df_test['rbob_wholesale_usd_gal'].values + df_test['tax_floor_usd'].values + model.predict(X_test)`\n"
        f"   - Tomorrow forecast: `df_tomorrow = pd.DataFrame([tomorrow_features])`\n"
        f"   - `pred_tomorrow = float(tomorrow_features['rbob_wholesale_usd_gal'] + tomorrow_features['tax_floor_usd'] + float(np.ravel(model.predict(extract_features(df_tomorrow)))[0]))`\n"
        f"   - Return: `{{'model_type': str, 'test_predictions': pred_test.tolist(), 'predicted_tomorrow_retail': round(pred_tomorrow, 3), 'hyperparameters': dict}}`\n\n"
        f"Output ONLY complete, runnable Python code inside {TRIPLE_BACKTICKS}python {TRIPLE_BACKTICKS} blocks."
    )

    code = extract_code(call_ollama(prompt, temperature=0.35))
    return {"candidate_code": code}

def ast_guardrail_node(state: AgentCouncilState) -> dict:
    success, reason = sandboxed_write_candidate(state["candidate_code"])
    if not success:
        print(f"│ 🛡️  AST Guardrail   : BLOCKED - {reason}")
        log_experiment_attempt(
            iteration=state["iteration"],
            model_type="Untrusted_Candidate",
            status="BLOCKED_AST",
            champion_mae=state["champion_mae"],
            feature_proposal=state.get("feature_proposal"),
            error_trace=reason
        )
        return {
            "eval_error": f"AST Violation: {reason}",
            "last_error": reason,
            "retry_count": state["retry_count"] + 1,
            "status": "AST_ERROR"
        }
    print("│ 🛡️  AST Guardrail   : PASSED (Syntax verified, sandbox clean)")
    return {"eval_error": None, "last_error": None, "status": "WRITTEN"}

def benchmark_evaluator_node(state: AgentCouncilState) -> dict:
    print("│ 📊 Benchmark Engine : Running 4-fold walk-forward cross validation...")
    result = execute_isolated_benchmark(timeout_sec=60)

    if not result["success"]:
        err_msg = result["error"]
        if "ModuleNotFoundError: No module named" in err_msg:
            try:
                missing_mod = err_msg.split("No module named '")[1].split("'")[0]
                installed = auto_install_package_if_allowed(missing_mod)
                if installed:
                    print(f"│ 📦 Package Manager  : Installed '{missing_mod}', repeating benchmark...")
                    result = execute_isolated_benchmark(timeout_sec=60)
            except Exception:
                pass

    if not result["success"]:
        err_msg = result["error"]
        tail_err = get_clean_tail_error(err_msg)
        short_err = tail_err.splitlines()[-1] if tail_err else "Benchmark execution halted"
        print(f"│ ❌ Benchmark Error  : {short_err}")
        sandboxed_write_candidate(state["champion_code"])
        log_experiment_attempt(
            iteration=state["iteration"],
            model_type=state.get("candidate_model_type") or "FaultyCandidate",
            status="ERROR",
            champion_mae=state["champion_mae"],
            feature_proposal=state.get("feature_proposal"),
            error_trace=tail_err
        )
        return {
            "eval_error": err_msg,
            "last_error": tail_err,
            "candidate_mae": None,
            "retry_count": state["retry_count"] + 1,
            "status": "BENCHMARK_ERROR"
        }

    telemetry = result["telemetry"]
    mae = telemetry["metrics"]["mae_usd"]
    asym_mae = telemetry["metrics"]["asymmetric_mae_usd"]
    dir_acc = telemetry["metrics"]["directional_accuracy_pct"]
    decision_acc = telemetry["metrics"]["decision_success_pct"]
    model_type = telemetry["model_type"]
    hyperparams = telemetry.get("hyperparameters", {})

    composite = compute_composite_score(mae, asym_mae, dir_acc)

    # Clean comparative metric display
    delta_mae = mae - state["champion_mae"]
    delta_score = composite - state["champion_composite_score"]
    
    print(f"│")
    print(f"│  ┌── CANDIDATE SCORECARD: {model_type}")
    print(f"│  │  MAE:            ${mae:.4f} / gal    (Champ: ${state['champion_mae']:.4f} | {delta_mae:+.4f})")
    print(f"│  │  Asymmetric Loss: ${asym_mae:.4f} / gal    (Champ: ${state['champion_asym_mae']:.4f})")
    print(f"│  │  Directional Acc: {dir_acc:.1f}%            (Champ: {state['candidate_dir_acc'] or 76.9:.1f}%)")
    print(f"│  │  Decision Rate:   {decision_acc:.1f}% profitable actions")
    print(f"│  │  Composite Score: {composite:.4f}           (Target: < {state['champion_composite_score']:.4f} | {delta_score:+.4f})")
    print(f"│  └──")

    return {
        "candidate_mae": mae,
        "candidate_asym_mae": asym_mae,
        "candidate_dir_acc": dir_acc,
        "candidate_decision_acc": decision_acc,
        "candidate_composite_score": composite,
        "candidate_model_type": model_type,
        "candidate_hyperparams": hyperparams,
        "eval_error": None,
        "last_error": None,
        "status": "EVALUATED"
    }

def critic_decision_node(state: AgentCouncilState) -> dict:
    cand_comp = state.get("candidate_composite_score")
    champ_comp = state["champion_composite_score"]
    cand_mae = state.get("candidate_mae")
    cand_asym = state.get("candidate_asym_mae")
    cand_model = state.get("candidate_model_type", "Unknown")

    promoted = False
    if cand_comp is not None and cand_mae is not None:
        if cand_comp < (champ_comp - 0.0010):
            promoted = True
        elif cand_asym < (state["champion_asym_mae"] - 0.015) and cand_mae <= (state["champion_mae"] + 0.01):
            promoted = True

    if promoted:
        diff = champ_comp - cand_comp
        print(f"│ 🏆 Council Decision: PROMOTED! Candidate beat baseline by {diff:+.4f} points.")

        telemetry_file = BASE_DIR / "data" / "telemetry.json"
        with open(telemetry_file, "r", encoding="utf-8") as f:
            telemetry_data = json.load(f)

        dash_path = generate_and_save_dashboard(telemetry_data, state["candidate_code"])

        log_experiment_attempt(
            iteration=state["iteration"],
            model_type=cand_model,
            status="PROMOTED",
            mae=cand_mae,
            rmse=cand_asym,
            directional_acc=state.get("candidate_dir_acc"),
            champion_mae=state["champion_mae"],
            hyperparameters=state.get("candidate_hyperparams"),
            feature_proposal=state.get("feature_proposal")
        )

        subprocess.run(
            ["git", "add", "src/models/model_candidate.py", "data/telemetry.json", "data/model_experiments.jsonl", "dashboards/"],
            cwd=str(BASE_DIR)
        )
        commit_msg = f"Council Champion: {cand_model} Score {cand_comp:.4f} | MAE ${cand_mae:.4f}"
        subprocess.run(["git", "commit", "-m", commit_msg], cwd=str(BASE_DIR))
        push_res = subprocess.run(["git", "push"], cwd=str(BASE_DIR), capture_output=True, text=True)
        
        git_status = "Pushed to GitHub" if push_res.returncode == 0 else "Committed locally"
        print(f"│ 🚀 Deployment      : Model committed ({git_status}).")
        print(f"╰────────────────────────────────────────────────────────────\n")

        save_agent_state(state["iteration"], cand_mae, cand_model)
        trial_note = f"Iteration {state['iteration']}: {cand_model} PROMOTED (Score: {cand_comp:.4f}, MAE: ${cand_mae:.4f})"

        return {
            "promotions_total": state["promotions_total"] + 1,
            "champion_mae": cand_mae,
            "champion_asym_mae": cand_asym,
            "champion_composite_score": cand_comp,
            "champion_code": state["candidate_code"],
            "recent_trials_summary": state["recent_trials_summary"] + [trial_note],
            "status": "PROMOTED"
        }
    else:
        print(f"│ ❌ Council Decision: REJECTED (Score {cand_comp:.4f} >= {champ_comp:.4f}). Baseline retained.")
        print(f"╰────────────────────────────────────────────────────────────\n")
        sandboxed_write_candidate(state["champion_code"])

        if cand_mae is not None:
            log_experiment_attempt(
                iteration=state["iteration"],
                model_type=cand_model,
                status="REVERTED",
                mae=cand_mae,
                rmse=cand_asym,
                directional_acc=state.get("candidate_dir_acc"),
                champion_mae=state["champion_mae"],
                hyperparameters=state.get("candidate_hyperparams"),
                feature_proposal=state.get("feature_proposal")
            )
        trial_note = f"Iteration {state['iteration']}: {cand_model} REVERTED (Score: {cand_comp}, MAE: ${cand_mae})"
        return {
            "recent_trials_summary": state["recent_trials_summary"] + [trial_note],
            "status": "REVERTED"
        }

# -----------------------------------------------------------------------------
# Conditional Routing Supporting Execution Modes
# -----------------------------------------------------------------------------
def route_after_ast(state: AgentCouncilState) -> str:
    if state["status"] == "AST_ERROR":
        if state["retry_count"] <= state["max_retries"]:
            return "model_architect"
        return "critic_decision"
    return "benchmark_evaluator"

def route_after_benchmark(state: AgentCouncilState) -> str:
    if state["status"] == "BENCHMARK_ERROR":
        if state["retry_count"] <= state["max_retries"]:
            return "model_architect"
        return "critic_decision"
    return "critic_decision"

def route_after_critic(state: AgentCouncilState) -> str:
    if SHUTDOWN_REQUESTED:
        print("\n[SYSTEM] Shutdown signal intercepted. Exiting council cleanly.")
        return END

    # Mode 2: Stop immediately when an improvement is achieved
    if state["mode"] == "until_improvement" and state["status"] == "PROMOTED":
        print("🎉 [TARGET REACHED] Improvement achieved under --mode until_improvement. Stopping.")
        return END

    # Mode 1: Stop at iteration boundary
    if state["mode"] == "once" and state["iteration"] >= state["max_iterations"]:
        print(f"✓ Council completed planned cycle ({state['max_iterations']} iterations).")
        return END

    # Mode 3: Continuous runs loop forever
    return "feature_engineer"

def build_council_graph():
    workflow = StateGraph(AgentCouncilState)

    workflow.add_node("feature_engineer", feature_engineer_node)
    workflow.add_node("model_architect", model_architect_node)
    workflow.add_node("ast_guardrail", ast_guardrail_node)
    workflow.add_node("benchmark_evaluator", benchmark_evaluator_node)
    workflow.add_node("critic_decision", critic_decision_node)

    workflow.set_entry_point("feature_engineer")

    workflow.add_edge("feature_engineer", "model_architect")
    workflow.add_edge("model_architect", "ast_guardrail")

    workflow.add_conditional_edges("ast_guardrail", route_after_ast, {
        "model_architect": "model_architect",
        "benchmark_evaluator": "benchmark_evaluator",
        "critic_decision": "critic_decision"
    })

    workflow.add_conditional_edges("benchmark_evaluator", route_after_benchmark, {
        "model_architect": "model_architect",
        "critic_decision": "critic_decision"
    })

    workflow.add_conditional_edges("critic_decision", route_after_critic, {
        "feature_engineer": "feature_engineer",
        END: END
    })

    return workflow.compile()

# -----------------------------------------------------------------------------
# Main Runner with Signal Protection & CLI Argument Handling
# -----------------------------------------------------------------------------
def run_autonomous_council(mode: str = "once", iterations: int = 3):
    print("╔═══════════════════════════════════════════════════════════════╗")
    print("║   ESCANABA RETAIL FUEL - AUTONOMOUS ML COUNCIL                ║")
    print("║   LangGraph Orchestration • DuckDuckGo RAG • AST Guardrail    ║")
    print("╚═══════════════════════════════════════════════════════════════╝")
    print(f"Execution Mode: {mode.upper()} | Target Sandbox: {BASE_DIR.name}\n")

    if not check_ollama_health():
        print("[FATAL] Ollama server is offline on http://localhost:11434.")
        print("Run 'ollama serve' in another terminal and re-launch.")
        return

    initial_bench = execute_isolated_benchmark()
    if not initial_bench["success"]:
        print(f"[FATAL] Benchmark baseline failed:\n{get_clean_tail_error(initial_bench['error'])}")
        return

    baseline_mae = initial_bench["telemetry"]["metrics"]["mae_usd"]
    baseline_asym = initial_bench["telemetry"]["metrics"]["asymmetric_mae_usd"]
    baseline_dir_acc = initial_bench["telemetry"]["metrics"]["directional_accuracy_pct"]
    baseline_composite = compute_composite_score(baseline_mae, baseline_asym, baseline_dir_acc)

    with open(ALLOWED_MUTABLE_FILE, "r", encoding="utf-8") as f:
        champion_code = f.read()

    print(f"ACTIVE CHAMPION: {initial_bench['telemetry']['model_type']}")
    print(f"├── MAE:         ${baseline_mae:.4f} / gal")
    print(f"├── Asym Loss:   ${baseline_asym:.4f}")
    print(f"├── Dir Acc:     {baseline_dir_acc:.1f}%")
    print(f"└── Comp Score:  {baseline_composite:.4f}\n")

    # Ensure today's GitHub dashboard is already updated with the active champion
    check_and_sync_daily_dashboard(champion_code)

    initial_state: AgentCouncilState = {
        "mode": mode,
        "iteration": 0,
        "max_iterations": iterations,
        "retry_count": 0,
        "max_retries": 2,
        "promotions_total": 0,
        "champion_mae": baseline_mae,
        "champion_asym_mae": baseline_asym,
        "champion_composite_score": baseline_composite,
        "champion_code": champion_code,
        "feature_proposal": "",
        "web_research_context": "",
        "candidate_code": "",
        "last_error": None,
        "candidate_mae": None,
        "candidate_asym_mae": None,
        "candidate_dir_acc": None,
        "candidate_decision_acc": None,
        "candidate_composite_score": None,
        "candidate_model_type": None,
        "candidate_hyperparams": None,
        "recent_trials_summary": [],
        "eval_error": None,
        "status": "INITIALIZED"
    }

    app = build_council_graph()

    try:
        app.invoke(initial_state)
    except KeyboardInterrupt:
        print("\n[COUNCIL PAUSED] Manual interruption detected (Ctrl+C). Restoring verified champion...")
        sandboxed_write_candidate(champion_code)
        save_agent_state(initial_state["iteration"], baseline_mae, initial_bench["telemetry"]["model_type"])
        print("[SHUTDOWN CLEAN] All logs flushed to disk. Champion intact.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Autonomous Fuel Pricing ML Council")
    parser.add_argument(
        "--mode",
        choices=["once", "until_improvement", "continuous"],
        default="once",
        help="Execution mode: 'once' (N iterations), 'until_improvement' (stops at first promotion), 'continuous' (loops indefinitely)."
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=3,
        help="Number of iterations for --mode once (default: 3)."
    )
    args = parser.parse_args()

    run_autonomous_council(mode=args.mode, iterations=args.iterations)