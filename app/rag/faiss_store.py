import faiss
import numpy as np
import pickle
import json
import os

from app.embeddings.embedding_service import get_embedding

# ---------------- CONFIG ----------------
dimension = 384
index = faiss.IndexFlatL2(dimension)

documents = []
document_set = set()

# ---------------- PRICE KEYWORDS ----------------
PRICE_KEYWORDS = [
    "price", "cost", "₹", "rs", "budget", "offer", "pricing"
]


# ---------------- ADD DOCUMENT ----------------
def add_document(text):

    global document_set

    if text in document_set:
        return

    vector = get_embedding(text)

    index.add(
        np.array([vector]).astype("float32")
    )

    documents.append(text)
    document_set.add(text)


# ---------------- FAISS SEARCH ----------------
def search(query, k=5):

    q = query.lower()

    # 🚨 BLOCK PRODUCT QUERIES COMPLETELY
    if any(word in q for word in PRICE_KEYWORDS):
        return []

    vector = get_embedding(query)

    distances, indices = index.search(
        np.array([vector]).astype("float32"),
        k
    )

    results = []

    for idx in indices[0]:
        if idx < len(documents):
            results.append(documents[idx])

    return results


# ---------------- SAVE INDEX ----------------
def save_index():

    faiss.write_index(
        index,
        "faiss_index.bin"
    )

    with open("documents.pkl", "wb") as f:
        pickle.dump(documents, f)


# ---------------- LOAD INDEX ----------------
def load_index():

    global index, documents, document_set

    try:
        index = faiss.read_index("faiss_index.bin")

        with open("documents.pkl", "rb") as f:
            documents = pickle.load(f)
            document_set = set(documents)

        print("✅ FAISS loaded successfully")

    except Exception as e:
        print("⚠️ No existing FAISS index:", e)


# ---------------- LOAD PRODUCTS ----------------
def load_products():

    path = os.path.join(os.getcwd(), "products.json")

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print("❌ Products load error:", e)
        return []


# ---------------- MAIN ROUTER (IMPORTANT FIX) ----------------
def retrieve_context(query):

    q = query.lower()

    price_keywords = ["price", "cost", "₹", "budget", "offer", "pricing"]

    # 🚨 FORCE PRODUCT MODE
    if any(k in q for k in price_keywords):
        return {
            "type": "product",
            "data": []
        }

    # ONLY RAG FOR NON-PRICE
    return {
        "type": "rag",
        "data": search(query)
    }