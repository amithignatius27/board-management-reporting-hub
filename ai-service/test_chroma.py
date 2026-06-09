from services.chroma_service import collection

results = collection.query(
    query_texts=["supply chain issues"],
    n_results=3
)

print(results)