from sentence_transformers import SentenceTransformer

print("Loading embedding model...")

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

print("Embedding model loaded")

sample_embedding = embedding_model.encode("Revenue dropped")

print("Embedding Length:", len(sample_embedding))