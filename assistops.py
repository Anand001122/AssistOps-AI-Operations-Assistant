import subprocess
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor

def run_backend():
    print("[AssistOps] Starting Backend (FastAPI) on http://localhost:8000...")
    subprocess.run([sys.executable, "server.py"])

def run_frontend():
    print("[AssistOps] Starting Frontend (Vite)...")
    # Change directory to frontend and run npm run dev
    frontend_dir = os.path.join(os.getcwd(), "frontend")
    if os.name == 'nt':  # Windows
        subprocess.run("npm run dev", shell=True, cwd=frontend_dir)
    else:  # Linux/Mac
        subprocess.run(["npm", "run", "dev"], cwd=frontend_dir)

def main():
    print("\n" + "="*50)
    print("      AssistOps: AI Operations Assistant")
    print("="*50 + "\n")
    
    if not os.path.exists(".env"):
        print("CRITICAL: .env file not found! Please create it from .env.example.")
        sys.exit(1)

    print("Checking ports...")
    print("NOTE: By default, the frontend runs on http://localhost:5173.")
    print("If port 5173 is already in use, Vite will automatically use 5174, 5175, etc.")
    print("Please check the terminal output below for the local URL.\n")

    with ThreadPoolExecutor(max_workers=2) as executor:
        try:
            executor.submit(run_backend)
            # Small delay to let backend start first
            time.sleep(2)
            executor.submit(run_frontend)
        except KeyboardInterrupt:
            print("\n[AssistOps] Shutting down...")
            sys.exit(0)

if __name__ == "__main__":
    main()
