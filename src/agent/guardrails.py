import ast
import json
import os
import signal
import subprocess
import sys
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(r"C:\Users\david\code\autonomous\autonomous-driver").resolve()
ALLOWED_MUTABLE_FILE = (BASE_DIR / "src" / "models" / "model_candidate.py").resolve()
STATE_CHECKPOINT_FILE = (BASE_DIR / "data" / "agent_state.json").resolve()
BENCHMARK_SCRIPT = (BASE_DIR / "src" / "models" / "evaluate_benchmark.py").resolve()
EXPERIMENT_LOG_PATH = (BASE_DIR / "data" / "model_experiments.jsonl").resolve()

SHUTDOWN_REQUESTED = False

def handle_exit_signal(signum, frame):
    global SHUTDOWN_REQUESTED
    print(f"\n[SYSTEM] Intercepted signal ({signum}). Gracefully stopping agent...")
    SHUTDOWN_REQUESTED = True

signal.signal(signal.SIGINT, handle_exit_signal)
signal.signal(signal.SIGTERM, handle_exit_signal)
if hasattr(signal, "SIGBREAK"):
    signal.signal(signal.SIGBREAK, handle_exit_signal)

# -----------------------------------------------------------------------------
# Layer 1: Deterministic AST Static Security Inspection
# -----------------------------------------------------------------------------
BLOCKED_MODULES = {
    "os", "sys", "subprocess", "shutil", "socket", "urllib", "requests",
    "pathlib", "ctypes", "winreg", "builtins", "importlib", "pickle",
    "shelve", "multiprocessing", "threading", "pty", "platform"
}

# Whitelist of allowed data science, ML, and optimization modules
ALLOWED_TOP_LEVEL_MODULES = {
    "numpy", "pandas", "sklearn", "lightgbm", "xgboost", "catboost", "scipy",
    "optuna", "torch", "statsmodels", "polars", "math", "typing", "collections", "itertools"
}

SAFE_PIP_PACKAGE_MAP = {
    "lightgbm": "lightgbm",
    "xgboost": "xgboost",
    "catboost": "catboost",
    "optuna": "optuna",
    "scipy": "scipy",
    "statsmodels": "statsmodels",
    "polars": "polars"
}

BLOCKED_CALLS = {
    "eval", "exec", "compile", "__import__", "open", "input",
    "breakpoint", "memoryview", "globals", "locals"
}

def auto_install_package_if_allowed(module_name: str) -> bool:
    """Installs missing ML packages on-demand if present in the safe whitelist."""
    pkg = SAFE_PIP_PACKAGE_MAP.get(module_name.lower())
    if not pkg:
        return False
    print(f"[AGENT PIP] Detected missing package '{pkg}'. Auto-installing into local environment...")
    res = subprocess.run([sys.executable, "-m", "pip", "install", pkg], capture_output=True, text=True)
    if res.returncode == 0:
        print(f"[AGENT PIP SUCCESS] Successfully installed '{pkg}'.")
        return True
    print(f"[AGENT PIP FAILED] Could not install '{pkg}': {res.stderr.strip()[:200]}")
    return False

def verify_ast_safety(code_str: str) -> tuple[bool, str]:
    try:
        tree = ast.parse(code_str)
    except SyntaxError as e:
        return False, f"Syntax Error: {e}"

    base_dir_str = str(BASE_DIR).lower()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root_module = alias.name.split('.')[0]
                if root_module in BLOCKED_MODULES or root_module not in ALLOWED_TOP_LEVEL_MODULES:
                    return False, f"Security Violation: Import of '{alias.name}' is strictly forbidden."
        
        elif isinstance(node, ast.ImportFrom):
            root_module = node.module.split('.')[0] if node.module else ""
            if root_module in BLOCKED_MODULES or root_module not in ALLOWED_TOP_LEVEL_MODULES:
                return False, f"Security Violation: Import from '{node.module}' is strictly forbidden."

        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in BLOCKED_CALLS:
                return False, f"Security Violation: Dangerous function call '{node.func.id}()' blocked."

        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            val = node.value.lower()
            if ".." in val or ":\\" in val or ":/" in val:
                if not val.startswith(base_dir_str):
                    return False, f"Security Violation: External path literal detected: '{node.value}'."

    return True, "AST static verification passed."

# -----------------------------------------------------------------------------
# Layer 2: Atomic Sandboxed File Operations
# -----------------------------------------------------------------------------
def sandboxed_write_candidate(code_content: str) -> tuple[bool, str]:
    is_safe, reason = verify_ast_safety(code_content)
    if not is_safe:
        return False, reason

    target_path = ALLOWED_MUTABLE_FILE.resolve()

    try:
        target_path.relative_to(BASE_DIR)
    except ValueError:
        raise PermissionError(f"[SANDBOX SECURITY BREACH] Attempted write outside {BASE_DIR}")

    if target_path != ALLOWED_MUTABLE_FILE:
        raise PermissionError(f"[SANDBOX VIOLATION] Only {ALLOWED_MUTABLE_FILE.name} can be modified.")

    temp_file = target_path.with_suffix(".tmp")
    try:
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(code_content)
        temp_file.replace(target_path)
        return True, "File atomically written."
    except Exception as e:
        if temp_file.exists():
            temp_file.unlink()
        return False, f"Write failure: {e}"

# -----------------------------------------------------------------------------
# Layer 3: Isolated Subprocess Execution
# -----------------------------------------------------------------------------
def execute_isolated_benchmark(timeout_sec: int = 60) -> dict:
    try:
        proc = subprocess.run(
            [sys.executable, str(BENCHMARK_SCRIPT)],
            cwd=str(BASE_DIR),
            capture_output=True,
            text=True,
            timeout=timeout_sec
        )
        if proc.returncode != 0:
            return {"success": False, "error": proc.stderr.strip() or proc.stdout.strip()}

        telemetry_path = BASE_DIR / "data" / "telemetry.json"
        with open(telemetry_path, "r", encoding="utf-8") as f:
            return {"success": True, "telemetry": json.load(f)}

    except subprocess.TimeoutExpired:
        return {"success": False, "error": f"Evaluation timed out after {timeout_sec}s (infinite loop guard)."}
    except Exception as e:
        return {"success": False, "error": str(e)}

def save_agent_state(iteration: int, champion_mae: float, best_model_type: str):
    payload = {
        "iteration": iteration,
        "champion_mae": champion_mae,
        "best_model_type": best_model_type,
        "shutdown_requested": SHUTDOWN_REQUESTED
    }
    with open(STATE_CHECKPOINT_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

def log_experiment_attempt(
    iteration: int,
    model_type: str,
    status: str,
    mae: float = None,
    rmse: float = None,
    directional_acc: float = None,
    champion_mae: float = None,
    hyperparameters: dict = None,
    feature_proposal: str = None,
    error_trace: str = None
):
    record = {
        "timestamp": datetime.now().isoformat(),
        "iteration": iteration,
        "model_type": model_type or "Unknown",
        "status": status,
        "mae_usd": round(mae, 4) if mae is not None else None,
        "rmse_usd": round(rmse, 4) if rmse is not None else None,
        "directional_accuracy_pct": round(directional_acc, 2) if directional_acc is not None else None,
        "champion_mae_usd": round(champion_mae, 4) if champion_mae is not None else None,
        "mae_delta_usd": round(champion_mae - mae, 4) if (mae is not None and champion_mae is not None) else None,
        "hyperparameters": hyperparameters or {},
        "feature_proposal": (feature_proposal[:160] + "...") if feature_proposal else None,
        "error_trace": error_trace[:300] if error_trace else None
    }

    try:
        with open(EXPERIMENT_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
    except Exception as e:
        print(f"[LOGGER WARNING] Failed to record experiment log: {e}")