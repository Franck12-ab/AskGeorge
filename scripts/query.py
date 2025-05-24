import chromadb
from sentence_transformers import SentenceTransformer
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

# === Load ChromaDB index ===
client = chromadb.PersistentClient(path="chroma_index")
collection = client.get_collection("askgeorge")

# === Use same embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

def query(question, top_k=5):
    q_embedding = model.encode([question]).tolist()

    results = collection.query(
        query_embeddings=q_embedding,
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    print(f"\n🔍 Top {top_k} results for: \"{question}\"\n")

    for rank, (doc, meta) in enumerate(zip(results["documents"][0], results["metadatas"][0])):
        print(f"[{rank+1}] 📄 {meta['source_file']} | 📁 {meta['category']}")
        print(doc[:500].replace("\n", " ") + "...\n")

# === CLI Loop ===
if __name__ == "__main__":
    while True:
        q = input("❓ Enter your question (or 'exit'): ")
        if q.lower() in ["exit", "quit"]:
            break
        query(q)
