from fastapi import FastAPI
from app.api.chat import router as chat_router
from app.api.summary import router as summary_router

from app.rag.faiss_store import load_index
from app.rag.load_documents import load_all_documents
from app.api.meta_webhook import router as meta_router

load_index()
load_all_documents()

import app.documents.company_knowledge

app = FastAPI()

app.include_router(chat_router)
app.include_router(summary_router)
app.include_router(meta_router)

@app.get("/")
def home():
    return {
        "status": "running",
        "message": "AI Chatbot Backend"
    }