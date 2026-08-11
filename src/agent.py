import json
import os
import subprocess
import urllib.request
from datetime import datetime

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma4:12b"

def query_ollama(prompt: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }
    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        return result.get('response', '')

def generate_dashboard(ingest_data: dict, telemetry_data: dict) -> str:
    prompt = (
        f"You are an MLOps & Energy Market Analyst bot tracking Escanaba, MI fuel prices.\n"
        f"Analyze this daily ingestion and telemetry JSON payload:\n\n"
        f"INGEST: {json.dumps(ingest_data, indent=2)}\n\n"
        f"TELEMETRY: {json.dumps(telemetry_data, indent=2)}\n\n"
        f"Generate a clean executive Markdown dashboard with these sections:\n"
        f"1. ## Daily Market Summary (Escanaba ZIP 49829)\n"
        f"2. ## Key Macro & Regional Indicators\n"
        f"3. ## Model Performance & Margin Telemetry\n"
        f"Keep it concise, professional, and directly actionable. Output ONLY Markdown."
    )
    return query_ollama(prompt)

def generate_commit_message(telemetry_data: dict) -> str:
    mae = telemetry_data.get("metrics", {}).get("mae_usd", 0.0)
    drift = telemetry_data.get("drift_telemetry", {}).get("margin_drift_usd", 0.0)
    
    prompt = (
        f"Write a simple, concise git commit message under 50 characters describing a daily MLOps pipeline run.\n"
        f"Current MAE: ${mae:.4f}/gal, Margin Drift: ${drift:.4f}/gal.\n"
        f"Do NOT use conventional prefixes (no 'feat:', 'fix:'). No quotes, no markdown. Keep it plain text."
    )
    msg = query_ollama(prompt).strip().replace('"', '').replace("'", "")
    return msg if len(msg) > 5 else "update daily gas forecast telemetry"

def run_agent_pipeline():
    print("==================================================")
    print("  Executing Autonomous MLOps Pipeline")
    print("==================================================\n")

    # 1. Run Data Ingestion
    print("[Step 1/5] Ingesting 9-Factor Data Payload...")
    subprocess.run(["python", "src/ingest/fetch_all.py"], check=True)

    # 2. Run Feature Engineering
    print("\n[Step 2/5] Updating Feature Matrix...")
    subprocess.run(["python", "src/features/engineer.py"], check=True)

    # 3. Run Model Training & Evaluation
    print("\n[Step 3/5] Training Model & Computing Telemetry...")
    subprocess.run(["python", "src/models/train_eval.py"], check=True)

    # 4. Read Artifacts
    with open("data/raw/latest_ingest.json", "r", encoding="utf-8") as f:
        ingest_data = json.load(f)
    with open("data/telemetry.json", "r", encoding="utf-8") as f:
        telemetry_data = json.load(f)

    # 5. Generate Reports via Gemma 4 12B
    print("\n[Step 4/5] Generating Markdown Dashboard with Gemma 4 12B...")
    dashboard_md = generate_dashboard(ingest_data, telemetry_data)
    
    os.makedirs("dashboards", exist_ok=True)
    today_str = datetime.now().strftime("%Y-%m-%d")
    dashboard_path = os.path.join("dashboards", f"{today_str}_escanaba_telemetry.md")
    latest_dashboard_path = os.path.join("dashboards", "latest_telemetry.md")

    with open(dashboard_path, "w", encoding="utf-8") as f:
        f.write(dashboard_md)
    with open(latest_dashboard_path, "w", encoding="utf-8") as f:
        f.write(dashboard_md)

    print(f"[SUCCESS] Dashboard written to {dashboard_path}")

    # 6. Generate Simple Commit Message
    print("\n[Step 5/5] Generating Dynamic Commit Message...")
    commit_msg = generate_commit_message(telemetry_data)
    
    with open(".commit_msg.tmp", "w", encoding="utf-8") as f:
        f.write(commit_msg)
        
    print(f"Generated Commit Message: '{commit_msg}'")

if __name__ == "__main__":
    run_agent_pipeline()