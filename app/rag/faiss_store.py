import faiss
import numpy as np
from app.embeddings.embedding_service import get_embedding
import pickle

dimension = 384

index = faiss.IndexFlatL2(dimension)

PRICE_KEYWORDS = [
    "price", "cost", "₹", "rs", "budget", "offer"
]

documents = []
document_set = set()

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

    

def search(query, k=5):

    q = query.lower().strip()

    if any(kword in q for kword in PRICE_KEYWORDS):
        return []

    vector = get_embedding(query)

    distances, indices = index.search(
        np.array([vector]).astype("float32"),
        k
    )

    results = []

    for idx in indices[0]:

        if idx < len(documents):

            results.append(
                documents[idx]
            )

    return results

def save_index():

    faiss.write_index(
        index,
        "faiss_index.bin"
    )

    with open(
        "documents.pkl",
        "wb"
    ) as f:

        pickle.dump(
            documents,
            f
        )

def load_index():

    global index
    global documents
    global document_set

    try:

        index = faiss.read_index(
            "faiss_index.bin"
        )

        with open(
            "documents.pkl",
            "rb"
        ) as f:

            documents = pickle.load(
                f
            )
            document_set = set(documents)
            


        print("FAISS loaded.")

    except:

        print("No existing FAISS index.")


def retrieve_context(query):

    q = query.lower()

    if any(k in q for k in PRICE_KEYWORDS):
        return {
            "type": "product",
            "data": []
        }

    return {
        "type": "rag",
        "data": search(query)
    }