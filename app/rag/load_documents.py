import os

from app.rag.document_loader import load_pdf
from app.rag.chunker import chunk_text
from app.rag.faiss_store import add_document


def load_all_documents():

    folder = "app/documents"

    for file in os.listdir(folder):

        if file.endswith(".pdf"):

            path = os.path.join(folder, file)

            print(f"Loading {file}")

            text = load_pdf(path)

            chunks = chunk_text(text)

            for chunk in chunks:

                add_document(chunk)

            print(f"{file} loaded successfully")