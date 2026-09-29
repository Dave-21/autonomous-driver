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
from typing import TypedDict, Optional, List, Any

if os.name == "nt":
    os.system("")

BASE_DIR = Path(r"C:\Users\david\code\autonomous\autonomous-driver").resolve()
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

try:
    from src.agent.guardrails import (
        sandboxed_write_candidate,
        execute_isolated_benchmark,
        save_agent_state,
        ALLOWED_MUTABLE_FILE,
        log_experiment_attempt,
        auto_install_package_if_allowed
    )
    from src.agent.web_search import search_web_knowledge
    from src.agent.deep_research import execute_deep_research, get_latest_dossier
except (ModuleNotFoundError, ImportError):
    from guardrails import (
        sandboxed_write_candidate,
        execute_isolated_benchmark,
        save_agent_state,
        ALLOWED_MUTABLE_FILE,
        log_experiment_attempt,
        auto_install_package_if_allowed
    )
    from web_search import search_web_knowledge
    from deep_research import execute_deep_research, get_latest_dossier

from langgraph.graph import StateGraph, END

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5-coder:7b-instruct-q8_0"
TRIPLE_BACKTICKS = chr(96) * 3

CLR_RESET   = "\033[0m"
CLR_BOLD    = "\033[1m"
CLR_DIM     = "\033[2m"
CLR_CYAN    = "\033[96m"
CLR_GREEN   = "\033[92m"
CLR_YELLOW  = "\033[93m"
CLR_RED     = "\033[91m"
CLR_GRAY    = "\033[90m"
CLR_WHITE   = "\033[97m"

ACTIVE_CHAMPION_CODE: str = ""
SHUTDOWN_TRIGGERED = False

def immediate_shutdown_handler(signum, frame):
    global SHUTDOWN_TRIGGERED
    if SHUTDOWN_TRIGGERED:
        sys.exit(1)
    SHUTDOWN_TRIGGERED = True
    print(f"\n\n  {CLR_YELLOW}[INTERRUPT]{CLR_RESET} Signal {signum} received. Restoring champion and exiting...")
    if ACTIVE_CHAMPION_CODE:
        sandboxed_write_candidate(ACTIVE_CHAMPION_CODE)
    print(f"  {CLR_GREEN}[SAFE EXIT]{CLR_RESET} Verified champion model preserved on disk.")
    sys.exit(0)

signal.signal(signal.SIGINT, immediate_shutdown_handler)
signal.signal(signal.SIGTERM, immediate_shutdown_handler)
if hasattr(signal, "SIGBREAK"):
    signal.signal(signal.SIGBREAK, immediate_shutdown_handler)

def fetch_live_market_futures() -> dict:
    """Retrieves current settlement futures for WTI, Brent, and NYMEX RBOB."""
    defaults = {"wti": 71.50, "brent": 75.20, "rbob": 2.0850}
    try:
        import yfinance as yf
        tickers = yf.Tickers("CL=F BZ=F RB=F")
        wti = tickers.tickers["CL=F"].fast_info.last_price or defaults["wti"]
        brent = tickers.tickers["BZ=F"].fast_info.last_price or defaults["brent"]
        rbob = tickers.tickers["RB=F"].fast_info.last_price or defaults["rbob"]
        return {"wti": float(wti), "brent": float(brent), "rbob": float(rbob)}
    except Exception:
        return defaults

def ensure_autonomous_data_freshness():
    """
    Autonomously checks if feature_matrix.csv is missing records for today.
    If stale, executes scrapers and appends current prices directly to feature_matrix.csv.
    """
    feature_store = BASE_DIR / "data" / "feature_matrix.csv"
    today_str = datetime.now().strftime("%Y-%m-%d")

    needs_update = True
    if feature_store.exists():
        try:
            with open(feature_store, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]
                if len(lines) > 1:
                    last_line = lines[-1]
                    last_ts = last_line.split(",")[0]
                    if today_str in last_ts:
                        needs_update = False
        except Exception:
            needs_update = True

    if needs_update:
        print(f"  {CLR_YELLOW}[AUTO-INGEST]{CLR_RESET} Data matrix missing records for {today_str}.")
        print(f"  {CLR_YELLOW}[AUTO-INGEST]{CLR_RESET} Initiating live GasBuddy & futures collection pipeline...")

        # 1. Run local scraper
        scraper_path = BASE_DIR / "src" / "ingest" / "scrape_escanaba.py"
        latest_retail = 4.770
        price_spread = 0.200

        if scraper_path.exists():
            print(f"  {CLR_GRAY}├── Executing: {scraper_path.relative_to(BASE_DIR)}...{CLR_RESET}")
            subprocess.run([sys.executable, str(scraper_path)], cwd=str(BASE_DIR), capture_output=True, text=True)

        # Inspect any newly generated price caches
        cache_candidates = [
            BASE_DIR / "data" / "escanaba_prices.json",
            BASE_DIR / "data" / "gasbuddy_raw.json",
            BASE_DIR / "data" / "station_prices.csv"
        ]
        for c in cache_candidates:
            if c.exists():
                try:
                    if c.suffix == ".json":
                        with open(c, "r", encoding="utf-8") as f:
                            data = json.load(f)
                            if isinstance(data, list) and len(data) > 0:
                                prices = [float(x.get("price", 0)) for x in data if float(x.get("price", 0)) > 2.0]
                                if prices:
                                    latest_retail = round(sum(prices) / len(prices), 3)
                                    price_spread = round(max(prices) - min(prices), 3)
                except Exception:
                    pass

        # 2. Fetch live futures
        print(f"  {CLR_GRAY}├── Fetching live NYMEX RBOB & crude futures...{CLR_RESET}")
        futures = fetch_live_market_futures()
        wti = futures["wti"]
        brent = futures["brent"]
        rbob = futures["rbob"]
        crack_spread = round((rbob * 42.0) - wti, 3)

        # 3. Append to feature_matrix.csv
        now_ts = datetime.now().isoformat()
        now_dt = datetime.now()
        month = now_dt.month
        day_of_week = now_dt.weekday()
        tax_floor = 0.5156
        traffic = 1.15
        whiting_risk = 0.20
        gb_risk = 0.25
        nat_risk = 0.10
        is_summer = 0

        new_row = (
            f"{now_ts},{month},{tax_floor},{traffic},{whiting_risk},{gb_risk},"
            f"{nat_risk},{day_of_week},{is_summer},{latest_retail},{price_spread},"
            f"{today_str},{wti},{rbob},{brent},{crack_spread}\n"
        )

        try:
            with open(feature_store, "a", encoding="utf-8") as f:
                f.write(new_row)
            print(f"  {CLR_GREEN}[AUTO-INGEST]{CLR_RESET} Appended new observation: Lincoln Rd Retail=${latest_retail}/gal | RBOB=${rbob:.3f} | Crack=${crack_spread:.2f}\n")
        except Exception as e:
            print(f"  {CLR_RED}[AUTO-INGEST ERROR]{CLR_RESET} Could not append to feature matrix: {e}\n")
    else:
        print(f"  {CLR_GREEN}[AUTO-INGEST]{CLR_RESET} Data matrix verified current for {today_str}.\n")

DATA_SCHEMA_MANIFEST = """
============================== STRICT DATA SCHEMA ==============================
RAW COLUMNS AVAILABLE IN df_train & df_test:
| Column Name                     | Dtype   | Description                                              |
| :------------------------------ | :------ | :------------------------------------------------------- |
| `timestamp`                     | object  | ISO Datetime string. NEVER pass to model.fit()!          |
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
| `target_escanaba_retail_price`  | float64 | TARGET VARIABLE. Exists ONLY in df_train!                |

CRITICAL CONTRACT RULES:
1. NEVER reference `target_escanaba_retail_price` inside `extract_features(df)`!
2. DO NOT manually prune base columns. ElasticNet handles selection.
3. DO NOT use statsmodels seasonal_decompose or STL (fails on small samples).
4. DO NOT use VotingRegressor.
5. MANDATORY NUMERIC CLEANING:
   `return d[numeric_cols].replace([np.inf, -np.inf], np.nan).bfill().ffill().fillna(0.0)`.
================================================================================
"""

class AgentCouncilState(TypedDict):
    mode: str
    iteration: int
    max_iterations: int
    retry_count: int
    max_retries: int
    consecutive_rejections: int
    last_deep_research_iter: int
    deep_research_cycle: int
    promotions_total: int
    champion_mae: float
    champion_asym_mae: float
    champion_dir_acc: float
    champion_turn_acc: float
    champion_decision_acc: float
    champion_composite_score: float
    champion_model_type: str
    champion_code: str
    feature_proposal: str
    web_research_context: str
    deep_research_dossier: str
    candidate_code: str
    last_error: Optional[str]
    candidate_mae: Optional[float]
    candidate_asym_mae: Optional[float]
    candidate_dir_acc: Optional[float]
    candidate_turn_acc: Optional[float]
    candidate_decision_acc: Optional[float]
    candidate_composite_score: Optional[float]
    candidate_model_type: Optional[str]
    candidate_hyperparams: Optional[dict]
    recent_trials_summary: List[str]
    eval_error: Optional[str]
    status: str

def compute_composite_score(mae: float, asym_mae: float, dir_acc: float, turning_point_acc: float) -> float:
    dir_acc_norm = max(0.0, min(1.0, dir_acc / 100.0))
    turn_acc_norm = max(0.0, min(1.0, turning_point_acc / 100.0))
    accuracy_penalty = 1.0 + (0.20 * (1.0 - dir_acc_norm)) + (0.15 * (1.0 - turn_acc_norm))
    score = (0.45 * mae + 0.45 * asym_mae) * accuracy_penalty
    return round(score, 4)

def sanitize_for_json(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {k: sanitize_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [sanitize_for_json(v) for v in obj]
    elif hasattr(obj, "item"):
        return obj.item()
    return str(obj)

def check_ollama_health() -> bool:
    try:
        req = urllib.request.Request("http://localhost:11434/", method="GET")
        with urllib.request.urlopen(req, timeout=3) as resp:
            return resp.status == 200
    except Exception:
        return False

def call_ollama(prompt: str, temperature: float = 0.35, max_retries: int = 3) -> str:
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
        if SHUTDOWN_TRIGGERED:
            sys.exit(0)
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
        if "must have 2 complete cycles" in line or "requires 730 observations" in line:
            return "scikit learn time series avoid seasonal_decompose small sample"
        if "contains infinity or a value too large" in line:
            return "scikit learn ValueError Input X contains infinity float64 replace nan"
        if "VotingRegressor" in line:
            return "scikit learn remove VotingRegressor use Pipeline ElasticNetCV"
        if "HuberRegressor" in line and "random_state" in line:
            return "scikit learn HuberRegressor does not accept random_state"
        if any(err in line for err in ["ValueError:", "TypeError:", "NameError:", "AttributeError:", "ModuleNotFoundError:", "ImportError:"]):
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
        analysis = (
            f"Wholesale RBOB futures and terminal rack costs indicate upward price pressure. "
            f"Lincoln Road pump prices are projected to rise by ~+${delta:.2f}/gal within 24-48 hours. "
            f"Fill up today to lock in current rates."
        )
    elif delta <= -0.025:
        analysis = (
            f"Downstream wholesale costs in Green Bay/Chicago have eased while station margins expanded. "
            f"Lincoln Road pump prices are projected to drop by -${abs(delta):.2f}/gal over the next 1-2 days. "
            f"Hold off on filling up until tomorrow to capture lower prices."
        )
    else:
        analysis = (
            f"Wholesale rack costs and local retail prices are in equilibrium. "
            f"No major price swings anticipated. Buy fuel as needed."
        )

    dashboard_content = f"""# Escanaba Retail Fuel Intelligence Dashboard
**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | **Data Timestamp:** {ts}

---

## Driver Recommendation: {recommendation}
**Current Lincoln Rd Average:** ${cur_price:.3f}/gal  
**Projected 24h Retail Price:** ${pred_price:.3f}/gal (**{'+' if delta > 0 else ''}{delta:.3f}/gal**)

### Market Analysis
{analysis}

---

## Model Benchmark Telemetry
- **Active Champion Architecture:** `{model_type}`
- **Walk-Forward Backtest MAE:** `${metrics.get('mae_usd', 0.0):.4f}/gal`
- **Asymmetric Spike Loss:** `${metrics.get('asymmetric_mae_usd', 0.0):.4f}/gal`
- **Directional Trend Accuracy:** `{metrics.get('directional_accuracy_pct', 0.0)}%`
- **Turning Point (Inflection) Accuracy:** `{metrics.get('turning_point_acc_pct', 0.0)}%`
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
    today_str = datetime.now().strftime("%Y-%m-%d")
    date_file = BASE_DIR / "dashboards" / f"{today_str}_escanaba_telemetry.md"

    if not date_file.exists():
        print(f"  {CLR_GRAY}[Daily Sync]{CLR_RESET} Compiling forecast for {today_str} using active champion...")
        bench = execute_isolated_benchmark()
        if bench["success"]:
            generate_and_save_dashboard(bench["telemetry"], champion_code)
            subprocess.run(["git", "add", "dashboards/", "data/telemetry.json"], cwd=str(BASE_DIR), capture_output=True)
            commit_msg = f"Daily Fuel Intelligence: Champion {bench['telemetry']['model_type']} update for {today_str}"
            subprocess.run(["git", "commit", "-m", commit_msg], cwd=str(BASE_DIR), capture_output=True)
            push_res = subprocess.run(["git", "push"], cwd=str(BASE_DIR), capture_output=True, text=True)
            if push_res.returncode == 0:
                print(f"  {CLR_GREEN}[Daily Sync]{CLR_RESET} Pushed latest forecast dashboard to GitHub.\n")
            else:
                print(f"  {CLR_YELLOW}[Daily Sync]{CLR_RESET} Local commit created ({push_res.stderr.strip()[:40]}).\n")
    else:
        print(f"  {CLR_GRAY}[Daily Sync]{CLR_RESET} Today's GitHub dashboard is current for {today_str}.\n")

# Mathematical Table Formatter: Exact 81-Character Aligned Boundary
INDENT = "  "
W_LABEL = 37
W_VAL1  = 17
W_VAL2  = 17
INNER_TOTAL = (W_LABEL + 2) + 1 + (W_VAL1 + 2) + 1 + (W_VAL2 + 2)  # 77 chars
BOX_DIVIDER   = f"{INDENT}+{'-' * INNER_TOTAL}+"                      # 81 chars outer
TABLE_DIVIDER = f"{INDENT}+{'-' * (W_LABEL + 2)}+{'-' * (W_VAL1 + 2)}+{'-' * (W_VAL2 + 2)}+"

def render_scorecard_row(label: str, col1_val: str, col2_val: str, col2_color: str = "") -> str:
    col1_clean = f"{col1_val:>{W_VAL1}}"
    col2_clean = f"{col2_val:>{W_VAL2}}"
    if col2_color:
        col2_formatted = f"{col2_color}{col2_clean}{CLR_RESET}"
    else:
        col2_formatted = col2_clean
    return f"{INDENT}| {label:<{W_LABEL}} | {col1_clean} | {col2_formatted} |"

# -----------------------------------------------------------------------------
# LangGraph Council Nodes
# -----------------------------------------------------------------------------
def feature_engineer_node(state: AgentCouncilState) -> dict:
    if SHUTDOWN_TRIGGERED:
        sys.exit(0)

    current_iter = state["iteration"] + 1
    dossier_text = state.get("deep_research_dossier", "")
    last_res_iter = state.get("last_deep_research_iter", 0)
    cycle = state.get("deep_research_cycle", 0)

    should_deep_research = (
        (current_iter - last_res_iter >= 6) and (state.get("consecutive_rejections", 0) >= 4)
    ) or not dossier_text

    if should_deep_research:
        cycle += 1
        print(f"\n  {CLR_BOLD}{CLR_YELLOW}[PLATEAU AUDIT]{CLR_RESET} Stagnation detected at MAE ${state['champion_mae']:.4f}/gal.")
        print(f"  {CLR_BOLD}{CLR_CYAN}[COUNCIL ACTION]{CLR_RESET} Authorizing Deep Research investigation (Track {cycle})...")
        dossier = execute_deep_research(
            trial_history=state.get("recent_trials_summary", []),
            current_champion_mae=state["champion_mae"],
            current_champion_code=state["champion_code"],
            cycle_count=cycle
        )
        dossier_text = dossier["synthesis"]
        last_res_iter = current_iter

    title_str = f"ITERATION {current_iter} | MODE: {state['mode'].upper()}"
    print(f"\n{CLR_BOLD}{CLR_CYAN}{BOX_DIVIDER}{CLR_RESET}")
    print(f"{CLR_BOLD}{CLR_CYAN}{INDENT}| {title_str:<{INNER_TOTAL - 2}} |{CLR_RESET}")
    print(f"{CLR_BOLD}{CLR_CYAN}{BOX_DIVIDER}{CLR_RESET}")
    print(f"  [FEATURE ENG]   Formulating transformations...")

    prompt = (
        f"{DATA_SCHEMA_MANIFEST}\n\n"
        f"LATEST DEEP RESEARCH BLUEPRINT:\n{dossier_text}\n\n"
        f"ACTIVE CHAMPION: {state['champion_model_type']} with MAE ${state['champion_mae']:.4f}/gal\n\n"
        "TASK:\n"
        "Propose ONE single, high-impact feature transformation to add to the existing feature set.\n"
        "Focus on: wholesale momentum acceleration `d['rbob_accel'] = d['rbob_wholesale_usd_gal'].diff(1) - d['rbob_wholesale_usd_gal'].diff(2)` "
        "or crack spread momentum ratios.\n"
        "DO NOT propose dropping columns. ElasticNet handles sparsity. Keep proposal to 2 concise sentences."
    )
    try:
        proposal = call_ollama(prompt, temperature=0.35)
    except Exception:
        proposal = "Calculate wholesale acceleration difference `diff(1) - diff(2)` and crack spread volatility ratio."

    clean_lines = [l.strip() for l in proposal.splitlines() if l.strip() and not l.startswith("```")]
    display_prop = " ".join(clean_lines)
    if len(display_prop) > 95:
        display_prop = display_prop[:92] + "..."
    print(f"                  Proposal : {CLR_DIM}{display_prop}{CLR_RESET}")

    return {
        "iteration": current_iter,
        "retry_count": 0,
        "last_error": None,
        "last_deep_research_iter": last_res_iter,
        "deep_research_cycle": cycle,
        "deep_research_dossier": dossier_text,
        "feature_proposal": proposal
    }

def model_architect_node(state: AgentCouncilState) -> dict:
    if SHUTDOWN_TRIGGERED:
        sys.exit(0)

    is_retry = state["retry_count"] > 0
    research_section = ""
    cycle = state.get("deep_research_cycle", 0)

    if is_retry and state["last_error"]:
        if state["retry_count"] >= 3:
            cycle += 1
            print(f"  {CLR_YELLOW}[SELF-REPAIR {state['retry_count']}/{state['max_retries']}]{CLR_RESET} Deep Diagnostic on crash...")
            dossier = execute_deep_research(
                topic=state["last_error"],
                trial_history=state.get("recent_trials_summary", []),
                current_champion_mae=state["champion_mae"],
                current_champion_code=state["champion_code"],
                cycle_count=cycle
            )
            rag_solution = dossier["synthesis"]
        else:
            print(f"  {CLR_YELLOW}[SELF-REPAIR {state['retry_count']}/{state['max_retries']}]{CLR_RESET} Running targeted error lookup...")
            tail_err = get_clean_tail_error(state["last_error"])
            search_query = extract_search_query_from_error(tail_err)
            rag_solution = search_web_knowledge(search_query, max_results=2)

        tail_err = get_clean_tail_error(state["last_error"])
        research_section = (
            f"CRITICAL RUNTIME ERROR IN PREVIOUS ATTEMPT:\n```\n{tail_err}\n```\n"
            f"DIAGNOSTIC GUIDANCE:\n{rag_solution}\n\n"
        )
    else:
        print(f"  [ARCHITECT]     Refining champion architecture...")
        research_section = f"RESEARCH BLUEPRINT:\n{state.get('deep_research_dossier', '')}\n\n"

    history_context = "\n".join(state["recent_trials_summary"][-4:]) if state["recent_trials_summary"] else "No previous trials."

    prompt = (
        f"{DATA_SCHEMA_MANIFEST}\n\n"
        f"{research_section}"
        f"RECENT TRIAL HISTORY:\n{history_context}\n\n"
        f"PROPOSED REFINEMENT STRATEGY: {state['feature_proposal']}\n\n"
        f"ACTIVE CHAMPION CODE (CURRENT BEST: MAE ${state['champion_mae']:.4f}/gal):\n"
        f"```python\n{state['champion_code']}\n```\n\n"
        f"YOUR OBJECTIVE (EVOLUTIONARY REFINEMENT):\n"
        f"Evolve this champion code to beat Score: {state['champion_composite_score']:.4f} (MAE ${state['champion_mae']:.4f}).\n"
        f"1. DO NOT drop base columns. Keep the champion's features intact and add the proposed feature.\n"
        f"2. DO NOT use VotingRegressor or statsmodels seasonal_decompose.\n"
        f"3. Refine the ElasticNetCV grid: e.g. `ElasticNetCV(l1_ratio=[0.01, 0.05, 0.1, 0.2, 0.5, 0.8, 0.95])` (DO NOT specify cv=3).\n"
        f"4. MANDATORY NUMERIC CLEANING:\n"
        f"   `numeric_cols = [c for c in d.columns if c not in ['timestamp', 'target_escanaba_retail_price'] and pd.api.types.is_numeric_dtype(d[c])]`\n"
        f"   `return d[numeric_cols].replace([np.inf, -np.inf], np.nan).bfill().ffill().fillna(0.0)`\n"
        f"5. `hyperparameters` dict must contain ONLY simple scalar strings or floats (no objects).\n\n"
        f"Output ONLY complete, runnable Python code inside {TRIPLE_BACKTICKS}python {TRIPLE_BACKTICKS} blocks."
    )

    code = extract_code(call_ollama(prompt, temperature=0.35))
    return {"candidate_code": code, "deep_research_cycle": cycle}

def ast_guardrail_node(state: AgentCouncilState) -> dict:
    if SHUTDOWN_TRIGGERED:
        sys.exit(0)

    success, reason = sandboxed_write_candidate(state["candidate_code"])
    if not success:
        print(f"  [AST GUARD]     BLOCKED: {reason}")
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
    print(f"  [AST GUARD]     PASSED (Static verification clean)")
    return {"eval_error": None, "last_error": None, "status": "WRITTEN"}

def benchmark_evaluator_node(state: AgentCouncilState) -> dict:
    if SHUTDOWN_TRIGGERED:
        sys.exit(0)

    print(f"  [BENCHMARK]     Running 4-fold walk-forward cross validation...")
    result = execute_isolated_benchmark(timeout_sec=60)

    if not result["success"]:
        err_msg = result["error"]
        if "ModuleNotFoundError: No module named" in err_msg:
            try:
                missing_mod = err_msg.split("No module named '")[1].split("'")[0]
                installed = auto_install_package_if_allowed(missing_mod)
                if installed:
                    print(f"  [AUTO-PIP]      Installed '{missing_mod}', re-evaluating...")
                    result = execute_isolated_benchmark(timeout_sec=60)
            except Exception:
                pass

    if not result["success"]:
        err_msg = result["error"]
        tail_err = get_clean_tail_error(err_msg)
        short_err = tail_err.splitlines()[-1] if tail_err else "Execution halted"
        print(f"  {CLR_RED}[FAIL]{CLR_RESET}          {short_err}")
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
    mae = float(telemetry["metrics"]["mae_usd"])
    asym_mae = float(telemetry["metrics"]["asymmetric_mae_usd"])
    dir_acc = float(telemetry["metrics"]["directional_accuracy_pct"])
    turn_acc = float(telemetry["metrics"].get("turning_point_acc_pct", 80.0))
    decision_acc = float(telemetry["metrics"]["decision_success_pct"])
    model_type = str(telemetry["model_type"])
    hyperparams = sanitize_for_json(telemetry.get("hyperparameters", {}))

    composite = compute_composite_score(mae, asym_mae, dir_acc, turn_acc)

    delta_mae = mae - state["champion_mae"]
    delta_score = composite - state["champion_composite_score"]
    
    col_mae_esc = CLR_GREEN if delta_mae <= 0 else CLR_RED
    col_score_esc = CLR_GREEN if delta_score <= 0 else CLR_RED

    header_title = f"CANDIDATE SCORECARD: {model_type}"[:(INNER_TOTAL - 4)]
    print(f"\n{BOX_DIVIDER}")
    print(f"{INDENT}| {header_title:<{INNER_TOTAL - 2}} |")
    print(f"{TABLE_DIVIDER}")
    print(f"{INDENT}| {'Metric':<{W_LABEL}} | {'Candidate':>{W_VAL1}} | {'vs Champion':>{W_VAL2}} |")
    print(f"{TABLE_DIVIDER}")
    print(render_scorecard_row("Mean Absolute Error (MAE)", f"${mae:.4f} / gal", f"{delta_mae:+.4f} / gal", col_mae_esc))
    print(render_scorecard_row("Asymmetric Spike Loss", f"${asym_mae:.4f} / gal", f"${state['champion_asym_mae']:.4f} / gal"))
    print(render_scorecard_row("Directional Trend Accuracy", f"{dir_acc:.1f}%", f"{state['champion_dir_acc']:.1f}%"))
    print(render_scorecard_row("Turning Point (Inflection) Accuracy", f"{turn_acc:.1f}%", f"{state['champion_turn_acc']:.1f}%"))
    print(render_scorecard_row("Profitable Action Rate", f"{decision_acc:.1f}%", f"{state['champion_decision_acc']:.1f}%"))
    print(render_scorecard_row("Council Composite Score", f"{composite:.4f}", f"{delta_score:+.4f}", col_score_esc))
    print(f"{TABLE_DIVIDER}\n")

    return {
        "candidate_mae": mae,
        "candidate_asym_mae": asym_mae,
        "candidate_dir_acc": dir_acc,
        "candidate_turn_acc": turn_acc,
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
    cand_turn_acc = state.get("candidate_turn_acc", 0.0)

    promoted = False
    promotion_reason = ""

    if cand_comp is not None and cand_mae is not None:
        # Rule 1: Direct improvement on composite score
        if cand_comp < champ_comp:
            promoted = True
            diff = champ_comp - cand_comp
            promotion_reason = f"Beat composite score by {diff:+.4f} points"
        # Rule 2: MAE strictly improved without degrading directional accuracy
        elif cand_mae < state["champion_mae"] and cand_comp <= champ_comp:
            promoted = True
            diff = champ_comp - cand_comp
            promotion_reason = f"MAE improved from ${state['champion_mae']:.4f} to${cand_mae:.4f}"
        # Rule 3: Turning Point Accuracy improved without hurting MAE
        elif cand_turn_acc > state["champion_turn_acc"] and cand_mae <= (state["champion_mae"] + 0.005) and cand_comp <= (champ_comp + 0.002):
            promoted = True
            diff = champ_comp - cand_comp
            promotion_reason = f"Turning point accuracy improved ({cand_turn_acc:.1f}% vs {state['champion_turn_acc']:.1f}%)"

    if promoted:
        diff = champ_comp - cand_comp
        print(f"  {CLR_BOLD}{CLR_GREEN}[VERDICT: PROMOTION APPROVED]{CLR_RESET}")
        print(f"  Reason: {promotion_reason}.\n")

        old_m = state['champion_model_type'][:13]
        new_m = cand_model[:13]
        mae_gain = cand_mae - state['champion_mae']
        asym_gain = cand_asym - state['champion_asym_mae']
        dir_gain = state['candidate_dir_acc'] - state['champion_dir_acc']
        turn_gain = state['candidate_turn_acc'] - state['champion_turn_acc']
        act_gain = state['candidate_decision_acc'] - state['champion_decision_acc']

        # Aligned audit table matching 81-character outer boundary
        W_A1, W_A2, W_A3, W_A4 = 27, 13, 13, 15
        DIV_AUDIT = f"{INDENT}+{'-' * (W_A1 + 2)}+{'-' * (W_A2 + 2)}+{'-' * (W_A3 + 2)}+{'-' * (W_A4 + 2)}+"

        s_mae_old = f"${state['champion_mae']:>6.4f} / gal"
        s_mae_new = f"${cand_mae:>6.4f} / gal"
        s_mae_del = f"{mae_gain:>+7.4f} / gal"

        s_asym_old = f"${state['champion_asym_mae']:>6.4f} / gal"
        s_asym_new = f"${cand_asym:>6.4f} / gal"
        s_asym_del = f"{asym_gain:>+7.4f} / gal"

        s_dir_old = f"{state['champion_dir_acc']:>12.1f}%"
        s_dir_new = f"{state['candidate_dir_acc']:>12.1f}%"
        s_dir_del = f"{dir_gain:>+14.1f}%"

        s_turn_old = f"{state['champion_turn_acc']:>12.1f}%"
        s_turn_new = f"{state['candidate_turn_acc']:>12.1f}%"
        s_turn_del = f"{turn_gain:>+14.1f}%"

        s_act_old = f"{state['champion_decision_acc']:>12.1f}%"
        s_act_new = f"{state['candidate_decision_acc']:>12.1f}%"
        s_act_del = f"{act_gain:>+14.1f}%"

        s_score_old = f"{champ_comp:>13.4f}"
        s_score_new = f"{cand_comp:>13.4f}"
        s_score_del = f"{-diff:>15.4f}"

        print(f"{CLR_BOLD}{CLR_CYAN}{DIV_AUDIT}{CLR_RESET}")
        print(f"{CLR_BOLD}{CLR_CYAN}{INDENT}| {'CHAMPION PROMOTION COMPARISON AUDIT':<{INNER_TOTAL - 2}} |{CLR_RESET}")
        print(f"{CLR_BOLD}{CLR_CYAN}{DIV_AUDIT}{CLR_RESET}")
        print(f"{INDENT}| {'Metric':<{W_A1}} | {'Old Champion':>{W_A2}} | {'New Champion':>{W_A3}} | {'Delta':>{W_A4}} |")
        print(f"{DIV_AUDIT}")
        print(f"{INDENT}| {'Architecture':<{W_A1}} | {old_m:>{W_A2}} | {new_m:>{W_A3}} | {CLR_GREEN}{'UPGRADED':>{W_A4}}{CLR_RESET} |")
        print(f"{INDENT}| {'Mean Absolute Error (MAE)':<{W_A1}} | {s_mae_old:>{W_A2}} | {s_mae_new:>{W_A3}} | {CLR_GREEN}{s_mae_del:>{W_A4}}{CLR_RESET} |")
        print(f"{INDENT}| {'Asymmetric Spike Loss':<{W_A1}} | {s_asym_old:>{W_A2}} | {s_asym_new:>{W_A3}} | {CLR_GREEN}{s_asym_del:>{W_A4}}{CLR_RESET} |")
        print(f"{INDENT}| {'Directional Trend Acc':<{W_A1}} | {s_dir_old:>{W_A2}} | {s_dir_new:>{W_A3}} | {CLR_GREEN}{s_dir_del:>{W_A4}}{CLR_RESET} |")
        print(f"{INDENT}| {'Turning Point Acc':<{W_A1}} | {s_turn_old:>{W_A2}} | {s_turn_new:>{W_A3}} | {CLR_GREEN}{s_turn_del:>{W_A4}}{CLR_RESET} |")
        print(f"{INDENT}| {'Profitable Action Rate':<{W_A1}} | {s_act_old:>{W_A2}} | {s_act_new:>{W_A3}} | {CLR_GREEN}{s_act_del:>{W_A4}}{CLR_RESET} |")
        print(f"{INDENT}| {'Council Composite Score':<{W_A1}} | {s_score_old:>{W_A2}} | {s_score_new:>{W_A3}} | {CLR_GREEN}{s_score_del:>{W_A4}}{CLR_RESET} |")
        print(f"{CLR_BOLD}{CLR_CYAN}{DIV_AUDIT}{CLR_RESET}\n")

        telemetry_file = BASE_DIR / "data" / "telemetry.json"
        with open(telemetry_file, "r", encoding="utf-8") as f:
            telemetry_data = json.load(f)

        generate_and_save_dashboard(telemetry_data, state["candidate_code"])

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
            cwd=str(BASE_DIR), capture_output=True
        )
        commit_msg = f"Council Champion: {cand_model} Score {cand_comp:.4f} | MAE ${cand_mae:.4f}"
        subprocess.run(["git", "commit", "-m", commit_msg], cwd=str(BASE_DIR), capture_output=True)
        push_res = subprocess.run(["git", "push"], cwd=str(BASE_DIR), capture_output=True, text=True)
        
        git_status = "Pushed to GitHub" if push_res.returncode == 0 else "Committed locally"
        print(f"  [DEPLOY] Model committed ({git_status}).")

        global ACTIVE_CHAMPION_CODE
        ACTIVE_CHAMPION_CODE = state["candidate_code"]

        save_agent_state(state["iteration"], cand_mae, cand_model)
        trial_note = f"Iteration {state['iteration']}: {cand_model} PROMOTED (Score: {cand_comp:.4f}, MAE: ${cand_mae:.4f})"

        return {
            "promotions_total": state["promotions_total"] + 1,
            "consecutive_rejections": 0,
            "champion_mae": cand_mae,
            "champion_asym_mae": cand_asym,
            "champion_dir_acc": state.get("candidate_dir_acc", 75.0),
            "champion_turn_acc": state.get("candidate_turn_acc", 80.0),
            "champion_decision_acc": state.get("candidate_decision_acc", 75.0),
            "champion_composite_score": cand_comp,
            "champion_model_type": cand_model,
            "champion_code": state["candidate_code"],
            "recent_trials_summary": state["recent_trials_summary"] + [trial_note],
            "status": "PROMOTED"
        }
    else:
        if cand_comp is not None:
            print(f"  {CLR_RED}[VERDICT: REJECTED]{CLR_RESET} Score {cand_comp:.4f} did not meet promotion threshold ({champ_comp:.4f}). Baseline restored.")
        else:
            print(f"  {CLR_RED}[VERDICT: REJECTED]{CLR_RESET} Candidate execution failed. Baseline restored.")
        
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
        trial_note = f"Iteration {state['iteration']}: {cand_model} REVERTED (Score: {cand_comp})"
        return {
            "consecutive_rejections": state.get("consecutive_rejections", 0) + 1,
            "recent_trials_summary": state["recent_trials_summary"] + [trial_note],
            "status": "REVERTED"
        }

# -----------------------------------------------------------------------------
# Routing Logic
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
    if SHUTDOWN_TRIGGERED:
        return END

    if state["mode"] == "until_improvement" and state["status"] == "PROMOTED":
        print(f"\n  {CLR_BOLD}{CLR_GREEN}[HALT]{CLR_RESET} Target improvement achieved under --mode until_improvement.\n")
        return END

    if state["mode"] == "once" and state["iteration"] >= state["max_iterations"]:
        print(f"\n  {CLR_GRAY}[COMPLETE]{CLR_RESET} Finished {state['max_iterations']} iterations.\n")
        return END

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
# Main Entrypoint
# -----------------------------------------------------------------------------
def run_autonomous_council(mode: str = "once", iterations: int = 3, force_deep_research: bool = False):
    print(f"\n{CLR_BOLD}{CLR_CYAN}================================================================={CLR_RESET}")
    print(f"{CLR_BOLD}{CLR_WHITE}  ESCANABA RETAIL FUEL  ::  AUTONOMOUS ML COUNCIL               {CLR_RESET}")
    print(f"{CLR_GRAY}  LangGraph Multi-Agent Committee • Deep Research RAG • AST Sandbox{CLR_RESET}")
    print(f"{CLR_BOLD}{CLR_CYAN}================================================================={CLR_RESET}")
    print(f"  Mode: {CLR_BOLD}{mode.upper()}{CLR_RESET} | Retries Allowed: {CLR_BOLD}4{CLR_RESET} | Sandbox: {BASE_DIR.name}\n")

    if not check_ollama_health():
        print(f"{CLR_RED}[FATAL] Ollama server is offline at http://localhost:11434.{CLR_RESET}")
        print("Start Ollama in another terminal via 'ollama serve' and re-launch.")
        return

    # Automatically refreshes feature matrix and appends current prices if stale
    ensure_autonomous_data_freshness()

    initial_bench = execute_isolated_benchmark()
    if not initial_bench["success"]:
        print(f"{CLR_RED}[FATAL] Initial baseline benchmark failed:\n{get_clean_tail_error(initial_bench['error'])}{CLR_RESET}")
        return

    baseline_mae = float(initial_bench["telemetry"]["metrics"]["mae_usd"])
    baseline_asym = float(initial_bench["telemetry"]["metrics"]["asymmetric_mae_usd"])
    baseline_dir_acc = float(initial_bench["telemetry"]["metrics"]["directional_accuracy_pct"])
    baseline_turn_acc = float(initial_bench["telemetry"]["metrics"].get("turning_point_acc_pct", 80.0))
    baseline_decision_acc = float(initial_bench["telemetry"]["metrics"]["decision_success_pct"])
    baseline_composite = compute_composite_score(baseline_mae, baseline_asym, baseline_dir_acc, baseline_turn_acc)
    champion_model_type = str(initial_bench["telemetry"]["model_type"])

    with open(ALLOWED_MUTABLE_FILE, "r", encoding="utf-8") as f:
        champion_code = f.read()

    global ACTIVE_CHAMPION_CODE
    ACTIVE_CHAMPION_CODE = champion_code

    print(f"  {CLR_BOLD}Active Champion Baseline:{CLR_RESET} {champion_model_type}")
    print(f"  ├── Mean Absolute Error (MAE)         : ${baseline_mae:.4f} / gal")
    print(f"  ├── Asymmetric Spike Loss             : ${baseline_asym:.4f} / gal")
    print(f"  ├── Directional Trend Accuracy        : {baseline_dir_acc:.1f}%")
    print(f"  ├── Turning Point (Inflection) Acc    : {baseline_turn_acc:.1f}%")
    print(f"  └── Council Composite Score           : {CLR_BOLD}{baseline_composite:.4f}{CLR_RESET}\n")

    check_and_sync_daily_dashboard(champion_code)

    initial_dossier = get_latest_dossier() or ""
    if force_deep_research or not initial_dossier:
        dossier_data = execute_deep_research(
            current_champion_mae=baseline_mae,
            current_champion_code=champion_code,
            cycle_count=0
        )
        initial_dossier = dossier_data["synthesis"]

    initial_state: AgentCouncilState = {
        "mode": mode,
        "iteration": 0,
        "max_iterations": iterations,
        "retry_count": 0,
        "max_retries": 4,
        "consecutive_rejections": 0,
        "last_deep_research_iter": 0,
        "deep_research_cycle": 0,
        "promotions_total": 0,
        "champion_mae": baseline_mae,
        "champion_asym_mae": baseline_asym,
        "champion_dir_acc": baseline_dir_acc,
        "champion_turn_acc": baseline_turn_acc,
        "champion_decision_acc": baseline_decision_acc,
        "champion_composite_score": baseline_composite,
        "champion_model_type": champion_model_type,
        "champion_code": champion_code,
        "feature_proposal": "",
        "web_research_context": "",
        "deep_research_dossier": initial_dossier,
        "candidate_code": "",
        "last_error": None,
        "candidate_mae": None,
        "candidate_asym_mae": None,
        "candidate_dir_acc": None,
        "candidate_turn_acc": None,
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
        immediate_shutdown_handler(signal.SIGINT, None)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Autonomous Fuel Pricing ML Council")
    parser.add_argument(
        "--mode",
        choices=["once", "until_improvement", "continuous"],
        default="once",
        help="Execution mode: 'once', 'until_improvement', or 'continuous'."
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=3,
        help="Number of iterations for --mode once (default: 3)."
    )
    parser.add_argument(
        "--deep-research",
        action="store_true",
        help="Forces an in-depth research cycle before starting trials."
    )
    args = parser.parse_args()

    run_autonomous_council(mode=args.mode, iterations=args.iterations, force_deep_research=args.deep_research)