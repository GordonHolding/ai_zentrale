# text_agent.py – zentrale GPT-Logik für Textgenerierung

import openai
import os
from agents.General_Agents.TextAgent.text_templates import load_text_template
from modules.output_infrastruktur.format_optimizer import format_text_ci_style

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_text(prompt: str, model="gpt-4o") -> str:
    """
    Generiert Freitext ohne Vorlage – z. B. bei spontanen Eingaben.
    """
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "Du bist ein professioneller Text-KI-Agent."},
            {"role": "user", "content": prompt}
        ]
    )
    return format_text_ci_style(response.choices[0].message["content"])

def generate_text_from_template(template_key_or_prompt, variables: dict = {}, model="gpt-4o"):
    """
    Nutzt Vorlagen – fällt automatisch auf Freitext zurück, wenn kein Template vorhanden.
    """
    template = load_text_template(template_key_or_prompt)

    if template:
        prompt = template["prompt"]
        for key, value in variables.items():
            prompt = prompt.replace(f"[{key.upper()}]", value)
        system_message = template.get("system_prompt", "Du bist ein professioneller Text-KI-Agent.")
    else:
        prompt = template_key_or_prompt
        system_message = "Du bist ein professioneller Text-KI-Agent."

    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ]
    )
    return format_text_ci_style(response.choices[0].message["content"])
