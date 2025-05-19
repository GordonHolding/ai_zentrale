# pdf_export_engine.py

from fpdf import FPDF

def create_simple_pdf(text: str, filename="output.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, text)
    pdf.output(filename)
