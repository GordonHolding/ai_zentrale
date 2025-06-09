# chainlit_start.py – Render-kompatibler Chainlit-Starter mit Fallback-Logik

import argparse
import os
import subprocess
import sys

def main():
    # Nutze PORT von Render oder CLI (z. B. --port 8080)
    parser = argparse.ArgumentParser(description=""Starte Chainlit GUI."")
    parser.add_argument(""--port"", type=int, default=int(os.environ.get(""PORT"", 8000)))
    args = parser.parse_args()

    print(f""🚀 Starte Chainlit auf Port {args.port} mit chainlit_app.py ..."")
    try:
        subprocess.run([
            sys.executable, ""-m"", ""chainlit"", ""run"", ""chainlit_app.py"",
            ""--host"", ""0.0.0.0"", ""--port"", str(args.port)
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f""❌ Fehler beim Start von Chainlit: {e}"")

if __name__ == ""__main__"":
    main()
