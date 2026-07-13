from sentence_transformers import SentenceTransformer


model = SentenceTransformer("BAAI/bge-small-en-v1.5")
#model = SentenceTransformer("nomic-ai/nomic-embed-text-v1.5")
#model = SentenceTransformer("BAAI/bge-base-en-v1.5")

def embed_documents(documents):
    texts = [doc.page_content for doc in documents]
    return model.encode(texts,
                        normalize_embeddings=True,
                        convert_to_numpy=True,
                        show_progress_bar=True,
                        batch_size=32)

def embed_query(query):
    return model.encode([query],
                        normalize_embeddings=True,
                        convert_to_numpy=True)