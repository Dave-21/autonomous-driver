import os
import json
import pandas as pd

def test_feature_store_exists_and_valid():
    csv_path = os.path.join("data", "feature_matrix.csv")
    assert os.path.exists(csv_path), "Feature store CSV missing."
    df = pd.read_csv(csv_path)
    assert len(df) > 0, "Feature matrix is empty."
    assert "gross_rack_to_retail_margin" in df.columns, "Missing calculated margin column."

def test_telemetry_metrics_valid():
    telemetry_path = os.path.join("data", "telemetry.json")
    assert os.path.exists(telemetry_path), "Telemetry JSON missing."
    with open(telemetry_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert "metrics" in data, "Telemetry missing metrics object."
        assert "mae_usd" in data["metrics"], "Missing MAE metric."

def test_dashboard_report_generated():
    dashboard_path = os.path.join("dashboards", "latest_telemetry.md")
    assert os.path.exists(dashboard_path), "Latest telemetry dashboard missing."
    with open(dashboard_path, "r", encoding="utf-8") as f:
        content = f.read().strip()
        assert len(content) > 100, "Dashboard report is too short."