import os, html
import requests
import streamlit as st
from dotenv import load_dotenv
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
from backend.utils.exporters import format_docx, format_pdf, format_txt

load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")

st.set_page_config(page_title="LegalEase", page_icon="⚖️", layout="wide")
st.markdown("<style>body{background:#0e1117}.hero{text-align:center;padding:12px}.card{background:#171b24;border-radius:14px;padding:22px;border:1px solid #303642}.preview{background:#11151c;color:#eee;border-radius:12px;padding:24px;max-height:620px;overflow:auto;white-space:pre-wrap;font-family:Georgia,serif;line-height:1.6}</style>", unsafe_allow_html=True)

st.markdown("<div class='hero'><h1>⚖️ LegalEase</h1><p>AI-Powered Legal Document Generator</p></div>", unsafe_allow_html=True)
st.caption("Generate an editable draft, preview it, and export it as TXT, DOCX, or PDF.")

with st.form("document_form"):
    c1, c2 = st.columns(2)
    with c1:
        document_type = st.selectbox("Document Type", ["Employment Contract", "NDA (Non-Disclosure Agreement)", "Lease Agreement", "Freelance Work Contract", "Service Agreement", "General Agreement", "Custom"])
        if document_type == "Custom": document_type = st.text_input("Custom document type")
        parties = st.text_area("Parties Involved", placeholder="Jane Doe (Service Provider), TechNova Inc. (Client)", height=120)
    with c2:
        dates = st.text_input("Effective Date", placeholder="April 10, 2026")
        terms = st.text_area("Terms & Conditions", placeholder="Payment within 30 days; Confidentiality must be maintained; Either party may terminate with 15 days notice", height=120)
    submitted = st.form_submit_button("✨ Generate Document", type="primary", use_container_width=True)

if submitted:
    if not all([document_type.strip(), parties.strip(), terms.strip(), dates.strip()]):
        st.error("Please fill in document type, parties, terms, and effective date.")
    else:
        with st.spinner("Generating your document with Gemini..."):
            try:
                r = requests.post(f"{BACKEND_URL}/generate", json={"document_type":document_type,"parties":parties,"terms":terms,"dates":dates}, timeout=90)
                if r.ok:
                    data = r.json(); st.session_state["content"] = data["content"]; st.session_state["model"] = data["model"]
                else: st.error(r.json().get("detail", r.text))
            except requests.RequestException as e: st.error(f"Could not connect to FastAPI: {e}")

if "content" in st.session_state:
    st.divider(); st.subheader("Document Preview")
    st.caption(f"Generated using: {st.session_state.get('model','Gemini')}")
    edited = st.text_area("Click to Edit Document", value=st.session_state["content"], height=500, key="editor")
    st.session_state["content"] = edited
    st.markdown("**Preview**")
    safe = html.escape(edited).replace("\n", "<br>")
    st.markdown(f"<div class='preview'>{safe}</div>", unsafe_allow_html=True)
    b1,b2,b3 = st.columns(3)
    with b1: st.download_button("⬇️ Download TXT", format_txt(edited), "legalease_document.txt", "text/plain", use_container_width=True)
    with b2: st.download_button("⬇️ Download DOCX", format_docx(edited, document_type), "legalease_document.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True)
    with b3: st.download_button("⬇️ Download PDF", format_pdf(edited, document_type), "legalease_document.pdf", "application/pdf", use_container_width=True)

st.divider(); st.caption("LegalEase drafts are AI-generated information and should be reviewed by a qualified legal professional before use.")
