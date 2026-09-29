import os
import sys
import json
import time
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

BASE_DIR = Path(r"C:\Users\david\code\autonomous\autonomous-driver").resolve()
DOSSIER_PATH = BASE_DIR / "data" / "deep_research_dossier.json"
QUERY_LOG_PATH = BASE_DIR / "data" / "deep_research_query_log.json"

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5-coder:7b-instruct-q8_0"

try:
    from src.agent.web_search import search_web_knowledge
except (ModuleNotFoundError, ImportError):
    from web_search import search_web_knowledge

CLR_RESET  = "\033[0m"
CLR_BOLD   = "\033[1m"
CLR_CYAN   = "\033[96m"
CLR_GRAY   = "\033[90m"

RESEARCH_TRACKS = [
    {
        "name": "Standardized Regularization & Information Criteria",
        "queries": [
            "scikit learn Pipeline StandardScaler ElasticNetCV small sample time series",
            "LassoLarsIC AIC BIC model selection small sample time series scikit learn",
            "RidgeCV alphas tuning retail gasoline margin forecasting"
        ]
    },
    {
        "name": "Asymmetric Rack Momentum & Second Derivatives",
        "queries": [
            "wholesale gasoline price acceleration second derivative time series forecasting",
            "asymmetric price transmission rockets feathers empirical econometrics python",
            "crack spread acceleration ratio retail gasoline price pass through"
        ]
    },
    {
        "name": "Robust Loss Function Tuning & Outlier Bounds",
        "queries": [
            "HuberRegressor epsilon alpha tuning retail gasoline margin outliers",
            "QuantileRegressor pinball loss retail gasoline price forecasting scikit learn",
            "scikit learn robust linear regression small sample time series cross validation"
        ]
    },
    {
        "name": "Moving Window Volatility & Interaction Dynamics",
        "queries": [
            "exponential moving average rack to retail gasoline price spread",
            "rolling z score retail gasoline price spread anomaly detection",
            "time weighted moving average fuel margin forecasting python"
        ]
    },
    {
        "name": "Spatial Terminal Logistics & Bottleneck Spreads",
        "queries": [
            "Upper Peninsula Michigan fuel supply logistics Green Bay terminal pricing",
            "refinery outage crack spread price spike regional gasoline econometrics",
            "terminal rack to retail price lag distributed lag model python"
        ]
    }
]

def load_query_log() -> List[str]:
    if QUERY_LOG_PATH.exists():
        try:
            with open(QUERY_LOG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_query_log(queries: List[str]):
    existing = load_query_log()
    existing.extend(queries)
    existing = list(dict.fromkeys(existing))[-60:]
    with open(QUERY_LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2)

def call_ollama(prompt: str, temperature: float = 0.35, timeout_sec: int = 90) -> str:
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_predict": 1024,
            "top_p": 0.90
        }
    }
    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
        return json.loads(resp.read().decode("utf-8")).get("response", "")

def execute_deep_research(
    topic: Optional[str] = None,
    trial_history: Optional[List[str]] = None,
    current_champion_mae: float = 0.0877,
    current_champion_code: str = "",
    cycle_count: int = 0
) -> Dict:
    start_time = time.time()
    MAX_BUDGET_SEC = 115

    past_queries = load_query_log()

    print(f"\n  {CLR_BOLD}{CLR_CYAN}+-----------------------------------------------------------------------------+{CLR_RESET}")
    if topic:
        print(f"  {CLR_BOLD}{CLR_CYAN}| DEEP RESEARCH ENGINE : ERROR DIAGNOSTIC INVESTIGATION                       |{CLR_RESET}")
    else:
        print(f"  {CLR_BOLD}{CLR_CYAN}| DEEP RESEARCH ENGINE : MULTI-STAGE COGNITIVE INVESTIGATION                  |{CLR_RESET}")
    print(f"  {CLR_BOLD}{CLR_CYAN}+-----------------------------------------------------------------------------+{CLR_RESET}")

    if topic:
        print(f"  | [STAGE 1/4] Diagnosing runtime error: {CLR_GRAY}{topic[:55]}...{CLR_RESET}")
        clean_err = topic.splitlines()[-1] if topic else "error"
        queries = [
            f"python scikit learn {clean_err[:45]}",
            f"pandas {clean_err[:45]} solution",
            "scikit learn handle inf nan float64 replace"
        ]
        track_name = "Runtime Error Resolution"
    else:
        track_idx = cycle_count % len(RESEARCH_TRACKS)
        selected_track = RESEARCH_TRACKS[track_idx]
        track_name = selected_track["name"]
        print(f"  | [STAGE 1/4] Research Track: {track_name}")
        print(f"  |             Targeting baseline improvement (${current_champion_mae:.4f} MAE)...")
        queries = [q for q in selected_track["queries"] if q not in past_queries]
        if not queries:
            queries = selected_track["queries"]

    save_query_log(queries)

    print(f"  | [STAGE 2/4] Harvesting literature across {len(queries)} search vectors...")
    evidence = []
    for idx, q in enumerate(queries, 1):
        if (time.time() - start_time) > (MAX_BUDGET_SEC - 35):
            break
        print(f"  |  -> Query {idx}: {CLR_GRAY}\"{q[:60]}...\"{CLR_RESET}")
        web_res = search_web_knowledge(q, max_results=2)
        evidence.append({"query": q, "content": web_res})
        time.sleep(1.2)

    elapsed_so_far = round(time.time() - start_time, 1)
    print(f"  | [STAGE 3/4] Deliberating solutions for N=35 dataset (Elapsed: {elapsed_so_far}s)...")

    if topic:
        stage3_prompt = (
            f"You are the Senior Machine Learning Engineer.\n"
            f"A candidate crashed with this exact error:\n```\n{topic}\n```\n\n"
            f"SEARCH EVIDENCE GATHERED:\n{json.dumps(evidence, indent=2)}\n\n"
            "TASK:\n"
            "Provide the exact Python code fix to prevent this error.\n"
            "NOTE: DO NOT use statsmodels seasonal_decompose or STL! The folds only have 12-25 rows.\n"
            "Do not use VotingRegressor. Include proper replacement of inf/nan."
        )
    else:
        clean_champ_snippet = current_champion_code[:900] if current_champion_code else "ElasticNetCV baseline"
        stage3_prompt = (
            f"You are the Principal Quantitative Econometrician.\n"
            f"CURRENT CHAMPION CODE (MAE ${current_champion_mae:.4f}/gal):\n```python\n{clean_champ_snippet}\n```\n\n"
            f"LITERATURE EVIDENCE ON {track_name.upper()}:\n{json.dumps(evidence, indent=2)}\n\n"
            "Analyze how to beat ElasticNetCV ($0.0877 MAE):\n"
            "1. DO NOT manually prune features. ElasticNetCV handles feature selection automatically.\n"
            "2. DO NOT use VotingRegressor (unweighted voting degrades small-sample performance).\n"
            "3. DO NOT force internal cross-validation with cv=3 inside ElasticNetCV (causes severe shrinkage on small folds).\n"
            "4. Recommend fine-tuning the ElasticNetCV regularization path (using default cv or RidgeCV) and adding 1 high-signal acceleration feature."
        )

    analysis = call_ollama(stage3_prompt, temperature=0.3, timeout_sec=30)

    elapsed_stage3 = round(time.time() - start_time, 1)
    print(f"  | [STAGE 4/4] Writing executable blueprint (Elapsed: {elapsed_stage3}s)...")
    remaining_sec = max(20, int(MAX_BUDGET_SEC - (time.time() - start_time)))

    stage4_prompt = (
        f"You are the Chief Quantitative Architect.\n"
        f"SYNTHESIS:\n{analysis}\n\n"
        "TASK:\n"
        "Produce an authoritative engineering dossier for the Model Architect:\n"
        "1. Recommend keeping the champion's core model architecture.\n"
        "2. Exact mathematical formula for 1 high-signal feature (e.g. wholesale momentum acceleration `diff(1) - diff(2)`).\n"
        "3. Explicitly state: `d[numeric_cols].replace([np.inf, -np.inf], np.nan).bfill().ffill().fillna(0.0)`.\n"
        "4. DO NOT prune columns manually. DO NOT recommend VotingRegressor or statsmodels seasonal_decompose.\n"
        "Keep output dense, technical, and directly executable."
    )

    try:
        dossier_text = call_ollama(stage4_prompt, temperature=0.35, timeout_sec=remaining_sec)
    except Exception:
        dossier_text = (
            "1. Architecture: Pipeline([('scaler', StandardScaler()), ('model', ElasticNetCV(l1_ratio=[0.01, 0.05, 0.1, 0.2, 0.5, 0.8]))])\n"
            "2. Feature: `d['rbob_accel'] = d['rbob_wholesale_usd_gal'].diff(1) - d['rbob_wholesale_usd_gal'].diff(2)`\n"
            "3. DO NOT prune columns manually; ElasticNet handles sparsity.\n"
            "4. NEVER use statsmodels seasonal_decompose or VotingRegressor.\n"
            "5. Always call `.replace([np.inf, -np.inf], np.nan).bfill().ffill().fillna(0.0)`."
        )

    total_duration = round(time.time() - start_time, 1)

    dossier = {
        "timestamp": datetime.now().isoformat(),
        "elapsed_seconds": total_duration,
        "track": track_name,
        "synthesis": dossier_text.strip()
    }

    os.makedirs(BASE_DIR / "data", exist_ok=True)
    with open(DOSSIER_PATH, "w", encoding="utf-8") as f:
        json.dump(dossier, f, indent=2)

    print(f"  {CLR_BOLD}{CLR_CYAN}+-----------------------------------------------------------------------------+{CLR_RESET}")
    print(f"  | Deep Research completed in {total_duration:<5}s | Dossier compiled and active             |")
    print(f"  {CLR_BOLD}{CLR_CYAN}+-----------------------------------------------------------------------------+{CLR_RESET}\n")

    return dossier

def get_latest_dossier() -> Optional[str]:
    if DOSSIER_PATH.exists():
        try:
            with open(DOSSIER_PATH, "r", encoding="utf-8") as f:
                return json.load(f).get("synthesis")
        except Exception:
            return None
    return None

if __name__ == "__main__":
    execute_deep_research()