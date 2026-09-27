# LegalEase: AI-Powered Legal Document Generator

LegalEase is a local full-stack project based on the supplied project documentation. It uses **Streamlit** for the frontend, **FastAPI** for the backend, **Gemini** for AI generation, and `python-docx`/`fpdf2` for exports. The supplied document specifies Gemini 1.5 Pro, but model availability changes; the project therefore uses the `GEMINI_MODEL` environment variable and defaults to `gemini-2.5-flash`.

## Project structure

```text
LegalEase/
├── backend/
│   ├── ai_core/gemini_generator.py
│   ├── utils/exporters.py
│   ├── utils/sanitize.py
│   ├── models.py
│   ├── routes.py
│   └── main.py
├── frontend/app.py
├── assets/logo.png
├── tests/test_api.py
├── .env.example
├── requirements.txt
└── README.md
```

## 1. Open in VS Code

Open the `LegalEase` folder in VS Code. Use **Terminal > New Terminal**.

## 2. Create a virtual environment

Windows PowerShell:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Windows CMD:

```cmd
py -3 -m venv .venv
.venv\Scripts\activate
```

## 3. Install packages

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Configure Gemini

Copy `.env.example` to `.env` and put your Google Gemini API key in `GEMINI_API_KEY`.

Example:

```env
GEMINI_API_KEY=your_real_key
GEMINI_MODEL=gemini-2.5-flash
BACKEND_URL=http://127.0.0.1:8000
```

Never upload `.env` to GitHub.

## 5. Start the backend

Terminal 1:

```bash
uvicorn backend.main:app --reload --port 8000
```

Test in a browser:

- http://127.0.0.1:8000/
- http://127.0.0.1:8000/health
- http://127.0.0.1:8000/docs

## 6. Start the frontend

Terminal 2:

```bash
streamlit run frontend/app.py
```

Open the URL Streamlit prints, normally:

`http://localhost:8501`

## 7. Test the complete flow

1. Select a document type.
2. Enter parties.
3. Enter the effective date.
4. Enter terms separated by semicolons, as described in the source documentation.
5. Click **Generate Document**.
6. Edit the generated content if required.
7. Download TXT, DOCX, and PDF.

## 8. Run automated tests

```bash
pytest -q
```

## Troubleshooting

### `Could not connect to FastAPI`
Make sure Terminal 1 is running:

```bash
uvicorn backend.main:app --reload --port 8000
```

### `GEMINI_API_KEY is not configured`
Create `.env` in the project root and add your API key.

### Gemini model error
Change `GEMINI_MODEL` in `.env` to a model available to your Google AI account. No source-code change is required.

### Import errors
Make sure the VS Code terminal is opened in the `LegalEase` project root and the virtual environment is activated.

## Architecture

```text
Streamlit UI
    │ POST /generate
    ▼
FastAPI
    │
    ▼
GeminiDocumentGenerator
    │
    ▼
Google Gemini API
    │
    ▼
Generated legal draft
    │
    ├── Editable preview
    ├── TXT exporter
    ├── DOCX exporter
    └── PDF exporter
```

## Important scope note

This application generates legal-document drafts from user-provided information. It does not establish that a document is legally valid for a particular jurisdiction. Users should review generated documents with a qualified legal professional before relying on them.
