# chainlit.py – Eigenständiges Startskript für Chainlit

import argparse
import os

def main():
    parser = argparse.ArgumentParser(description="Starte Chainlit Server mit optionalem Port.")
    parser.add_argument("--port", type=int, default=int(os.environ.get("CHAINLIT_PORT", 8000)))
    args = parser.parse_args()

    # Starte Chainlit auf dem gegebenen Port (hier als Beispiel mit "chainlit run")
    # Voraussetzung: chainlit ist installiert und ein passendes config/script vorhanden!
    import subprocess
    import sys

    print(f"🚀 Starte Chainlit auf Port {args.port} ...")
    try:
        # Passe ggf. den Dateinamen (z.B. "app.py") an, falls du ein eigenes Script hast!
        subprocess.run([
            sys.executable, "-m", "chainlit", "run", "app.py", "--port", str(args.port)
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Fehler beim Start von Chainlit: {e}")

if __name__ == "__main__":
    main()
