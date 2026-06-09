from services.chroma_service import collection
from data.knowledge_base import documents

for i, doc in enumerate(documents):
    collection.add(
        documents=[doc],
        ids=[f"doc_{i}"]
    )

print("10 documents inserted successfully")