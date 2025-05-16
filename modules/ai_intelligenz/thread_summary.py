# thread_summary.py – Automatische Zusammenfassung von E-Mail-Threads per GPT

import openai

def summarize_thread_messages(thread_messages: list) -> str:
    """
    GPT-gestützte Zusammenfassung eines gesamten Mail-Threads (Snippets).
    """
    snippets = [msg.get("snippet", "") for msg in thread_messages if msg.get("snippet")]
    if not snippets:
        return "Kein Thread-Inhalt vorhanden."

    joined = "\n---\n".join(snippets)
    prompt = f"Fasse die bisherige Kommunikation in diesem E-Mail-Verlauf kurz und präzise zusammen:\n\n{joined}"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message["content"].strip()

    except Exception as e:
        return f"❌ Fehler bei Thread-Zusammenfassung: {e}"
