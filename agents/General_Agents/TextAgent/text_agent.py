# text_agent.py – zentrale GPT-Logik für Textgenerierung

import openai
import os
from agents.General_Agents.TextAgent.text_templates import load_text_template
from modules.output_infrastruktur.format_optimizer import format_text_ci_style

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_text_from_template(template_key, variables: dict, model="gpt-4o"):
    template = load_text_template(template_key)
    if not template:
        return f"❌ Template '{template_key}' nicht gefunden."

    prompt = template["prompt"]
    for key, value in variables.items():
        prompt = prompt.replace(f"[{key.upper()}]", value)

    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": template.get("system_prompt", "Du bist ein professioneller Textagent.")},
            {"role": "user", "content": prompt}
        ]
    )
    result = response.choices[0].message["content"]
    return format_text_ci_style(result)
