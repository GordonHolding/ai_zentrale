# sheet_agent.py

import os
from .sheet_creator import create_sheet
from .sheet_generator import generate_sheet
from .sheet_reader import read_sheet
from .sheet_summary import summarize_sheet
from .sheet_templates import get_sheet_template
from .sheet_router import resolve_sheet_action

from modules.reasoning_intelligenz.memory_log import log_sheet_action
from modules.reasoning_intelligenz.qa_checker import validate_sheet_output
from modules.ai_intelligenz.gpt_response_parser import parse_gpt_response

SHEET_AGENT_BASE_PATH = os.path.dirname(__file__)
PROMPT_PATH = os.path.join(SHEET_AGENT_BASE_PATH, "SheetAgent_Kontexte_Promptweitergaben", "sheet_agent_prompt.json")
LOG_DIR = os.path.join(SHEET_AGENT_BASE_PATH, "SheetAgent_Memory")

def load_sheet_prompt():
    with open(PROMPT_PATH) as f:
        return f.read()

def handle_sheet_command(user_input: str):
    """
    Haupteinstiegspunkt für GPT-basierte Sheet-Kommandos.
    Erwartet strukturierte GPT-Response oder freien Text.
    """
    try:
        parsed = parse_gpt_response(user_input)
        action = resolve_sheet_action(parsed)

        if action == "create":
            title = parsed.get("title", "Neue Tabelle")
            sheet_id = create_sheet(title)
            log_sheet_action("sheet_generation_log.json", {"title": title, "sheet_id": sheet_id})
            return f"📄 Neues Sheet erstellt: {title}"

        elif action == "generate":
            title = parsed.get("title", "GPT-Tabelle")
            headers = parsed.get("headers", [["Spalte A", "Spalte B"]])
            sheet_id = generate_sheet(title, headers)
            log_sheet_action("sheet_generation_log.json", {"title": title, "sheet_id": sheet_id})
            return f"📊 Tabelle erstellt mit Headern: {headers}"

        elif action == "read":
            sheet_id = parsed.get("sheet_id")
            range_name = parsed.get("range", "Tabelle1!A1:D20")
            values = read_sheet(sheet_id, range_name)
            log_sheet_action("sheet_read_log.json", {"sheet_id": sheet_id, "range": range_name})
            return f"📥 Gelesene Daten:\n{values}"

        elif action == "summarize":
            sheet_id = parsed.get("sheet_id")
            range_name = parsed.get("range", "Tabelle1!A1:D20")
            summary = summarize_sheet(sheet_id, range_name)
            log_sheet_action("sheet_summary_log.json", {"sheet_id": sheet_id, "range": range_name, "summary": summary})
            return summary

        elif action == "template":
            template_key = parsed.get("template_key")
            data = parsed.get("data", [])
            sheet_id = get_sheet_template(template_key, data)
            return f"📎 Sheet mit Template erstellt: {sheet_id}"

        else:
            return "❌ Keine gültige Aktion erkannt."

    except Exception as e:
        log_sheet_action("sheet_error_log.json", {"error": str(e)})
        return f"❌ Fehler im SheetAgent: {e}"
