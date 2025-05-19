# sheet_summary.py

import openai
import os
from modules.input_interfaces.sheet_reader import read_sheet
from modules.ai_intelligenz.gpt_prompt_selector import load_prompt_for_project

openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize_sheet(spreadsheet_id, range_name, project_key="2.0_GORDON_HOLDING", instruction="Fasse die Inhalte der Tabelle zusammen.") -> str:
    values = read_sheet(spreadsheet_id, range_name)
    raw = "\n".join([", ".join(row) for row in values])
    prompt = load_prompt_for_project(project_key=project_key)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"{instruction}\n\n{raw}"}
            ]
        )
        return response.choices[0].message["content"]
    except Exception as e:
        return f"❌ Fehler bei GPT-Sheet-Auswertung: {e}"
