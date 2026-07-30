from fastapi import FastAPI

from app.api.chat import router as chat_router
from app.api.summary import router as summary_router
from app.api.meta_webhook import router as meta_router

from app.rag.faiss_store import load_index
from app.rag.load_documents import load_all_documents

from app.database.connection import Base, engine

app = FastAPI()


# ---------------- ROUTES ----------------
app.include_router(chat_router)
app.include_router(summary_router)
app.include_router(meta_router)


# ---------------- STARTUP EVENT ----------------
@app.on_event("startup")
def startup():

    print("🚀 Starting application...")

    # 1. Create DB tables automatically (ONE TIME SAFE)
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables ensured")

    # 2. Load FAISS index
    load_index()
    print("✅ FAISS loaded")

    # 3. Load documents
    load_all_documents()
    print("✅ Documents loaded")


# ---------------- ROOT ----------------
@app.get("/")
def home():
    return {
        "status": "running",
        "message": "AI Chatbot Backend"
    }