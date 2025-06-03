# main_controller.py – Zentrale Steuerinstanz der AI-ZENTRALE (Chainlit-kompatibel)

import json
import importlib
import os
import traceback

# 📄 Lade JSON-Dateien (z. B. system_modules.json)
def load_json_file(path: str) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        return {"error": f"❌ Fehler beim Laden von {path}: {e}"}

# 🔁 Lade aktivierte Module aus Konfig
def load_active_modules():
    modules = load_json_file("config/system_modules.json")
    if isinstance(modules, dict) and "error" in modules:
        return [], modules["error"]
    return [m for m in modules if m.get("active") is True], None

# 🚀 Starte alle aktivierten Module (optional: Ergebnisse zurückgeben)
async def run_full_system_check():
    modules, error = load_active_modules()
    if error:
        return {"status": "error", "message": error}

    results = []
    for module in modules:
        import_path = module.get("import_path")
        try:
            importlib.import_module(import_path)
            results.append({"module": import_path, "status": "ok"})
        except Exception as e:
            results.append({
                "module": import_path,
                "status": "error",
                "message": str(e),
                "traceback": traceback.format_exc()
            })

    return {
        "status": "done",
        "checked_modules": len(modules),
        "results": results
    }

# ▶ Optionaler CLI-Test
if __name__ == "__main__":
    import asyncio
    print("🚀 Starte MAIN CONTROLLER ...")
    result = asyncio.run(run_full_system_check())
    print(json.dumps(result, indent=2, ensure_ascii=False))
