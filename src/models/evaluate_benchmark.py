import json
import os
import sys
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import TimeSeriesSplit

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FEATURE_STORE = os.path.join(BASE_DIR, "data", "feature_matrix.csv")
TELEMETRY_PATH = os.path.join(BASE_DIR, "data", "telemetry.json")

sys.path.insert(0, BASE_DIR)
from src.models.model_candidate import train_and_forecast

def to_scalar_float(val) -> float:
    """Flattens any torch.Tensor, np.ndarray, list, or scalar to a float."""
    if hasattr(val, "detach"):
        val = val.detach().cpu().numpy()
    arr = np.asarray(val).ravel()
    if len(arr) > 0:
        return float(arr[0])
    return 0.0

def generate_user_action_insight(current_price: float, predicted_tomorrow: float, rbob_momentum: float) -> dict:
    delta = predicted_tomorrow - current_price
    
    if delta >= 0.025 or rbob_momentum > 0.04:
        recommendation = "FILL UP TODAY"
        reason = f"Imminent upward price pressure of +${delta:.2f}/gal detected from wholesale rack momentum."
    elif delta <= -0.025:
        recommendation = "WAIT TO FILL"
        reason = f"Pump prices expected to ease by -${abs(delta):.2f}/gal over the next 24-48 hours."
    else:
        recommendation = "STEADY / NEUTRAL"
        reason = "Local Lincoln Road margins are in equilibrium. Buy fuel as needed."

    return {
        "current_retail_avg": round(current_price, 3),
        "predicted_tomorrow_retail": round(predicted_tomorrow, 3),
        "expected_delta_usd": round(delta, 3),
        "recommendation": recommendation,
        "reasoning": reason
    }

def run_benchmark():
    if not os.path.exists(FEATURE_STORE):
        raise FileNotFoundError(f"Feature matrix missing at {FEATURE_STORE}")

    df = pd.read_csv(FEATURE_STORE).dropna(
        subset=["wti_usd_bbl", "rbob_wholesale_usd_gal", "target_escanaba_retail_price"]
    )
    df = df[df["target_escanaba_retail_price"] > 1.80].reset_index(drop=True)

    if len(df) < 18:
        raise ValueError(f"Insufficient valid rows ({len(df)}) to run historical backtest.")

    # Guarantee temporal features exist so candidates never hit KeyError: 'month'
    if "timestamp" in df.columns:
        ts = pd.to_datetime(df["timestamp"])
        df["month"] = ts.dt.month
        df["day_of_week"] = ts.dt.dayofweek
        df["day"] = ts.dt.day
    else:
        df["month"] = 9
        df["day_of_week"] = 4
        df["day"] = 11

    tscv = TimeSeriesSplit(n_splits=4)
    fold_maes = []
    fold_asym_maes = []
    all_actuals = []
    all_preds = []

    latest_output = None
    latest_row = df.iloc[-1].to_dict()
    rbob_momentum = float(df["rbob_wholesale_usd_gal"].diff(periods=2).iloc[-1])
    if np.isnan(rbob_momentum):
        rbob_momentum = 0.0
    latest_row["rbob_wholesale_usd_gal"] += (rbob_momentum * 0.5)

    for fold, (train_idx, test_idx) in enumerate(tscv.split(df)):
        train_fold = df.iloc[train_idx].copy()
        test_fold = df.iloc[test_idx].copy()

        output = train_and_forecast(train_fold, test_fold, latest_row)
        latest_output = output

        actuals = test_fold["target_escanaba_retail_price"].values
        raw_preds = output.get("test_predictions")
        if hasattr(raw_preds, "detach"):
            raw_preds = raw_preds.detach().cpu().numpy()
        preds = np.asarray(raw_preds, dtype=float).flatten()

        if len(preds) != len(actuals):
            raise ValueError(f"Fold {fold+1} Mismatch: Got {len(preds)} predictions, expected {len(actuals)}.")

        # Safety Fallback: If model predicted raw margin (< $2.00), reconstruct retail price
        if np.nanmean(preds) < 2.0:
            preds = (
                test_fold["rbob_wholesale_usd_gal"].values
                + test_fold["tax_floor_usd"].values
                + preds
            )

        fold_maes.append(mean_absolute_error(actuals, preds))
        
        errors = actuals - preds
        weights = np.where(errors > 0, 2.0, 1.0)
        asym_mae = np.mean(weights * np.abs(errors))
        fold_asym_maes.append(asym_mae)

        all_actuals.extend(actuals)
        all_preds.extend(preds)

    backtest_mae = float(np.mean(fold_maes))
    backtest_asym_mae = float(np.mean(fold_asym_maes))

    diff_actuals = np.diff(all_actuals)
    diff_preds = np.diff(all_preds)
    directional_acc = float(np.mean((diff_actuals * diff_preds) >= 0) * 100.0) if len(diff_actuals) > 0 else 0.0

    correct_actions = []
    for actual_d, pred_d in zip(diff_actuals, diff_preds):
        if pred_d >= 0.02:
            correct_actions.append(actual_d > 0.0)
        elif pred_d <= -0.02:
            correct_actions.append(actual_d <= 0.0)
        else:
            correct_actions.append(abs(actual_d) < 0.03)

    decision_success_pct = float(np.mean(correct_actions) * 100.0) if correct_actions else 0.0

    current_retail = float(df["target_escanaba_retail_price"].iloc[-1])
    tomorrow_forecast = to_scalar_float(latest_output["predicted_tomorrow_retail"])

    if tomorrow_forecast < 2.0:
        tomorrow_forecast = float(
            latest_row["rbob_wholesale_usd_gal"]
            + latest_row["tax_floor_usd"]
            + tomorrow_forecast
        )

    insight = generate_user_action_insight(current_retail, tomorrow_forecast, rbob_momentum)
    hyperparams = latest_output.get("hyperparameters", {})

    benchmark_results = {
        "timestamp": df["timestamp"].iloc[-1],
        "total_valid_samples": len(df),
        "backtest_type": "WalkForward_TimeSeriesSplit_4Folds",
        "model_type": str(latest_output.get("model_type", "UnknownModel")),
        "hyperparameters": hyperparams,
        "metrics": {
            "mae_usd": round(backtest_mae, 4),
            "asymmetric_mae_usd": round(backtest_asym_mae, 4),
            "directional_accuracy_pct": round(directional_acc, 2),
            "decision_success_pct": round(decision_success_pct, 2)
        },
        "forecast_tomorrow": insight
    }

    with open(TELEMETRY_PATH, "w", encoding="utf-8") as f:
        json.dump(benchmark_results, f, indent=2)

    return benchmark_results

if __name__ == "__main__":
    results = run_benchmark()
    print(json.dumps(results, indent=2))