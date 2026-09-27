from backend.utils.exporters import format_docx, format_pdf, format_txt

def test_exports():
    text = "LEGAL AGREEMENT\n\n1. Payment: Within 30 days.\n\nImportant Notice: Review before use."
    assert format_txt(text).startswith(b"LEGAL")
    assert format_docx(text, "Agreement").startswith(b"PK")
    assert format_pdf(text, "Agreement").startswith(b"%PDF")
