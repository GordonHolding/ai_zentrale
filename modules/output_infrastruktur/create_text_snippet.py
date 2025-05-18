# create_text_snippet.py

import os
import openai
from modules.ai_intelligenz.gpt_prompt_selector import load_prompt_for_project

openai.api_key = os.getenv("OPENAI_API_KEY")

def create_text_snippet(project_key="2.0_GORDON_HOLDING", context="statusbericht", instruction=None):
    prompt = load_prompt_for_project(project_key)
    system_instruction = instruction or f"Erstelle einen kompakten, GPT-basierten Text zum Kontext '{context}'. Ziel: sofort nutzbarer AI-Textoutput."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": system_instruction}
            ]
        )
        return response.choices[0].message["content"]
    except Exception as e:
        return f"❌ Fehler bei GPT-Generierung: {e}"
