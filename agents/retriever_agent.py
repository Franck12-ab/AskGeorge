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

    def retrieve(self, question, top_k=5):
        q_embedding = self.model.encode([question])
        distances, indices = self.index.search(np.array(q_embedding), top_k)

        results = []
        for idx in indices[0]:
            result = self.meta[idx]
            chunk_file = result['source_file'].replace('.pdf', f"_chunk_{result['chunk_id']}.txt")
            with open(f"chunks/{chunk_file}", "r") as f:
                text = f.read().strip()
            results.append({
                "source_file": result['source_file'],
                "category": result['category'],
                "chunk_id": result['chunk_id'],
                "text": text
            })
        return results
