# gpt_pdf_summary.py

import os
import openai
import fitz  # PyMuPDF
from modules.ai_intelligenz.gpt_prompt_selector import load_prompt_for_project
from modules.reasoning_intelligenz.memory_log import log_interaction
from datetime import datetime

openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_text_from_pdf(pdf_path: str) -> str:
    try:
        doc = fitz.open(pdf_path)
        text = "\n".join(page.get_text() for page in doc)
        return text[:5000]
    except Exception as e:
        return f"❌ Fehler beim PDF-Parsing: {e}"

def summarize_pdf(pdf_path: str, project_key="2.0_GORDON_HOLDING", instruction="Fasse den Inhalt dieses PDFs zusammen.") -> str:
    text = extract_text_from_pdf(pdf_path)
    prompt = load_prompt_for_project(project_key=project_key)
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"{instruction}\n\n{text}"}
            ]
        )
        summary = response.choices[0].message["content"]

        log_interaction("System", {
            "type": "PDFSummary",
            "file": os.path.basename(pdf_path),
            "summary": summary[:300],
            "timestamp": datetime.now().isoformat()
        })

        return summary
    except Exception as e:
        return f"❌ Fehler bei GPT-Zusammenfassung: {e}"
