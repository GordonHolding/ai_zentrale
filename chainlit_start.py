# chainlit_start.py – Startet NUR die Chainlit-Oberfläche

import argparse
import os
import subprocess
import sys

def main():
    parser = argparse.ArgumentParser(description="Starte Chainlit GUI.")
    parser.add_argument("--port", type=int, default=int(os.environ.get("CHAINLIT_PORT", 8000)))
    args = parser.parse_args()

    print(f"🚀 Starte Chainlit auf Port {args.port} mit chainlitapp.py ...")
    try:
        subprocess.run([
            sys.executable, "-m", "chainlit", "run", "chainlitapp.py",
            "--host", "0.0.0.0", "--port", str(args.port)
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Fehler beim Start von Chainlit: {e}")

if __name__ == "__main__":
    main()
