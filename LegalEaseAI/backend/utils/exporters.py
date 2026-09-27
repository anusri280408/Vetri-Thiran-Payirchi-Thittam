from io import BytesIO
from pathlib import Path
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt
from fpdf import FPDF
from PIL import Image

ASSET_DIR = Path(__file__).resolve().parents[2] / "assets"
LOGO = ASSET_DIR / "logo.png"

def _lines(text):
    return [x.strip() for x in text.splitlines() if x.strip()]

def format_docx(text: str, doc_type: str) -> bytes:
    doc = Document()
    section = doc.sections[0]
    section.top_margin = Inches(0.75); section.bottom_margin = Inches(0.75)
    section.left_margin = Inches(0.85); section.right_margin = Inches(0.85)
    if LOGO.exists():
        p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run().add_picture(str(LOGO), width=Inches(1.2))
    title = doc.add_paragraph(); title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = title.add_run(doc_type.upper()); r.bold = True; r.font.name = "Times New Roman"; r.font.size = Pt(16)
    for line in _lines(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(6)
        r = p.add_run(line)
        r.font.name = "Times New Roman"; r.font.size = Pt(11)
    footer = section.footer.paragraphs[0]; footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    footer.add_run("LegalEase - AI-generated draft | Review before use").font.size = Pt(8)
    out = BytesIO(); doc.save(out); return out.getvalue()

def format_pdf(text: str, doc_type: str) -> bytes:
    pdf = FPDF(format="A4")
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_page()
    def header():
        if LOGO.exists():
            try: pdf.image(str(LOGO), x=92, y=10, w=25)
            except Exception: pass
        pdf.set_y(38); pdf.set_font("Times", "B", 15); pdf.cell(0, 8, doc_type.upper(), align="C"); pdf.ln(12)
    def footer():
        pdf.set_y(-14); pdf.set_font("Times", "I", 8); pdf.cell(0, 8, "LegalEase - AI-generated draft | Review before use", align="C")
    for page_hook in (header, footer):
        pass
    header()
    for line in _lines(text):
        clean = line.replace("•", "-")
        is_heading = bool(clean[:3].rstrip(".").isdigit()) or clean.isupper() or clean.endswith(":")
        pdf.set_font("Times", "B" if is_heading else "", 11)
        pdf.multi_cell(0, 6, clean)
        pdf.ln(1)
        if pdf.get_y() > 270:
            footer(); pdf.add_page(); header()
    footer()
    return bytes(pdf.output())

def format_txt(text: str) -> bytes:
    return text.encode("utf-8")
