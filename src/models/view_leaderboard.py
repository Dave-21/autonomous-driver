import os
import json
import pandas as pd
from pathlib import Path

BASE_DIR = Path(r"C:\Users\david\code\autonomous\autonomous-driver").resolve()
EXPERIMENT_LOG_PATH = BASE_DIR / "data" / "model_experiments.jsonl"

def display_leaderboard():
    if not os.path.exists(EXPERIMENT_LOG_PATH):
        print("[INFO] No experiments recorded yet. Run autonomous_loop.py first.")
        return

    records = []
    with open(EXPERIMENT_LOG_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))

    if not records:
        print("[INFO] Experiment log is empty.")
        return

    df = pd.DataFrame(records)

    print("\n" + "=" * 95)
    print("                    ESCANABA GAS PRICE MODEL EXPERIMENT LEADERBOARD")
    print("=" * 95)

    valid_df = df[df["mae_usd"].notnull()]
    if not valid_df.empty:
        summary = valid_df.groupby("model_type").agg(
            trials=("status", "count"),
            promotions=("status", lambda x: (x == "PROMOTED").sum()),
            best_mae=("mae_usd", "min"),
            best_dir_acc=("directional_accuracy_pct", "max"),
            best_surge_recall=("surge_recall_pct", "max"),
            best_f1=("surge_f1_score", "max")
        ).reset_index().sort_values("best_mae")

        print("\n--- Model Family Benchmarks ---")
        print(summary.to_string(index=False))

    print("\n--- Recent Experiment Trials ---")
    display_cols = [
        "iteration", "model_type", "status", "mae_usd",
        "mae_delta_usd", "directional_accuracy_pct", "surge_recall_pct", "surge_f1_score"
    ]
    present_cols = [c for c in display_cols if c in df.columns]
    print(df[present_cols].tail(10).to_string(index=False))
    print("=" * 95 + "\n")

if __name__ == "__main__":
    display_leaderboard()