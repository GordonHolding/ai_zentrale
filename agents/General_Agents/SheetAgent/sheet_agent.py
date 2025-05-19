# sheet_agent.py – Zentrale Steuerlogik für GPT-gesteuerte Tabellen

from agents.General_Agents.SheetAgent.sheet_templates import load_sheet_template
from agents.General_Agents.SheetAgent.sheet_generator import generate_sheet_data
from modules.output_infrastruktur.sheet_creator import export_to_sheet
from modules.output_infrastruktur.pdf_generator_fpdf import create_simple_pdf

def handle_sheet_request(template_key: str, variables: dict, output_format="sheet"):
    template = load_sheet_template(template_key)
    if not template:
        return f"❌ Template '{template_key}' nicht gefunden."

    table = generate_sheet_data(template, variables)

    if output_format == "pdf":
        text_version = "\n".join([" | ".join(row) for row in table])
        create_simple_pdf(text=text_version, filename="sheet_output.pdf")
        return "✅ Tabelle als PDF generiert."
    elif output_format == "sheet":
        export_to_sheet(table, sheet_name=template_key)
        return "✅ Tabelle als Google Sheet gespeichert."
    else:
        return table
