import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

class RetrieverAgent:
    def __init__(self, index_path, metadata_path, model_name="all-MiniLM-L6-v2"):
        self.index = faiss.read_index(index_path)
        with open(metadata_path, "rb") as f:
            self.meta = pickle.load(f)
        self.model = SentenceTransformer(model_name)

        # 🔍 Keywords we care about (broad coverage)
        self.allowed_keywords = [
            "policy", "accessibility", "accommodation", "aoda", 
            "learning", "student", "co-op", "coop", "faq", 
            "disability", "services", "inclusion"
        ]

    def is_relevant(self, meta):
        category = meta.get("category", "").lower()
        filename = meta.get("source_file", "").lower()

        return any(kw in category or kw in filename for kw in self.allowed_keywords)

    def retrieve(self, question, top_k=3):
        q_embedding = self.model.encode([question])
        distances, indices = self.index.search(np.array(q_embedding), 20)

        results = []
        for idx in indices[0]:
            result = self.meta[idx]

            if not self.is_relevant(result):
                print(f"⚠️ Skipped {result['source_file']} | {result['category']}")
                continue

            chunk_file = result['source_file'].replace('.pdf', f"_chunk_{result['chunk_id']}.txt")
            with open(f"chunks/{chunk_file}", "r") as f:
                text = f.read().strip()

            results.append({
                "source_file": result['source_file'],
                "category": result['category'],
                "chunk_id": result['chunk_id'],
                "text": text
            })

            if len(results) == top_k:
                break

        return results
