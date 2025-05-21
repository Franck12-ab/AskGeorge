import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

# Load index + metadata
index = faiss.read_index("logs/chunk_faiss.index")
with open("logs/chunk_metadata.pkl", "rb") as f:
    meta = pickle.load(f)

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

def query(question, top_k=5):
    q_embedding = model.encode([question])
    distances, indices = index.search(np.array(q_embedding), top_k)

    print(f"\n🔍 Top {top_k} results for: \"{question}\"\n")
    for rank, idx in enumerate(indices[0]):
        result = meta[idx]
        print(f"[{rank+1}] 📄 {result['source_file']} | 📁 {result['category']}")
        chunk_path = f"chunks/{result['source_file'].replace('.pdf', f'_chunk_{result['chunk_id']}.txt')}"
        with open(chunk_path, "r") as f:
            text = f.read().strip()
            print(text[:500].replace("\n", " ") + "...\n")


# Example
if __name__ == "__main__":
    while True:
        q = input("❓ Enter your question (or 'exit'): ")
        if q.lower() in ["exit", "quit"]:
            break
        query(q)
