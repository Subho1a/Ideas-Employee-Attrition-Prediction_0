import sys
import os
import subprocess
import argparse

# Get absolute paths
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
VENV_PYTHON = os.path.join(PROJECT_ROOT, "ideas", "Scripts", "python.exe")
VENV_UVICORN = os.path.join(PROJECT_ROOT, "ideas", "Scripts", "uvicorn.exe")
VENV_STREAMLIT = os.path.join(PROJECT_ROOT, "ideas", "Scripts", "streamlit.exe")

# Fallbacks if venv path is different
if not os.path.exists(VENV_PYTHON):
    VENV_PYTHON = "python"
if not os.path.exists(VENV_UVICORN):
    VENV_UVICORN = "uvicorn"
if not os.path.exists(VENV_STREAMLIT):
    VENV_STREAMLIT = "streamlit"

def run_train():
    """Runs the model training pipeline."""
    print(f"Starting model training pipeline via {VENV_PYTHON} -m src.train...")
    cmd = [VENV_PYTHON, "-m", "src.train"]
    return subprocess.call(cmd, cwd=PROJECT_ROOT)

def run_backend(host="127.0.0.1", port=8000):
    """Launches the FastAPI backend server using uvicorn."""
    print(f"Starting FastAPI backend server on http://{host}:{port}...")
    cmd = [VENV_UVICORN, "backend.main:app", "--host", host, "--port", str(port), "--reload"]
    return subprocess.call(cmd, cwd=PROJECT_ROOT)

def run_frontend(port=8501):
    """Launches the Streamlit frontend dashboard."""
    print(f"Starting Streamlit frontend server on port {port}...")
    app_path = os.path.join(PROJECT_ROOT, "frontend", "app.py")
    cmd = [VENV_STREAMLIT, "run", app_path, "--server.port", str(port)]
    return subprocess.call(cmd, cwd=PROJECT_ROOT)

def main():
    parser = argparse.ArgumentParser(description="Employee Attrition Prediction Project Runner")
    parser.add_argument(
        "command",
        choices=["train", "backend", "frontend"],
        help="Command to run: 'train' (model training), 'backend' (FastAPI REST service), 'frontend' (Streamlit dashboard)"
    )
    parser.add_argument("--host", default="127.0.0.1", help="Host for server commands")
    parser.add_argument("--port", type=int, help="Port for server commands")
    
    args = parser.parse_args()
    
    try:
        if args.command == "train":
            sys.exit(run_train())
        elif args.command == "backend":
            port = args.port or 8000
            sys.exit(run_backend(host=args.host, port=port))
        elif args.command == "frontend":
            port = args.port or 8501
            sys.exit(run_frontend(port=port))
    except KeyboardInterrupt:
        print("\nShutting down service...")
        sys.exit(0)

if __name__ == "__main__":
    main()
