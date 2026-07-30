from app.rag.faiss_store import search


def retrieve_context(query: str):

    results = search(
        query,
        k=2
    )

    print("\nRetrieved documents:")
    print(results)

    context = "\n\n".join(
        results
    )

    context = context[:3000]

    print("\nContext:")
    print(context)

    return context