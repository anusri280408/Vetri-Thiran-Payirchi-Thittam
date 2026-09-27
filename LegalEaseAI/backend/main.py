from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router

app = FastAPI(title="LegalEase API", version="1.0.0", description="AI-powered legal document generator")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=False, allow_methods=["*"], allow_headers=["*"])
app.include_router(router)

@app.get("/")
def root():
    return {"service": "LegalEase", "status": "running"}

@app.get("/health")
def health():
    return {"status": "ok"}
