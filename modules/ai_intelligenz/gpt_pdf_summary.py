# gpt_pdf_summary.py – PDF-Analyse & Zusammenfassung durch GPT

import os
import openai
import fitz  # PyMuPDF

openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extrahiert reinen Text aus einem PDF-Dokument.
    """
    try:
        doc = fitz.open(pdf_path)
        text = "\n".join(page.get_text() for page in doc)
        return text[:5000]  # Begrenzung für GPT-Eingabe (anpassbar)
    except Exception as e:
        return f"❌ Fehler beim PDF-Parsing: {e}"

def summarize_pdf(pdf_path: str, instruction: str = "Fasse den Inhalt dieses PDFs zusammen.") -> str:
    """
    GPT erstellt eine Zusammenfassung des extrahierten PDF-Textes.
    """
    text = extract_text_from_pdf(pdf_path)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": f"{instruction}\n\n{text}"}
            ]
        )
        return response.choices[0].message["content"]

    except Exception as e:
        return f"❌ Fehler bei GPT-Zusammenfassung: {e}"
