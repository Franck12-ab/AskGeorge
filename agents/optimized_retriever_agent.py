import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Optional
import logging
from functools import lru_cache

class OptimizedRetrieverAgent:
    def __init__(self, index_path, metadata_path, model_name="all-MiniLM-L6-v2"):
        self.index = faiss.read_index(index_path)
        with open(metadata_path, "rb") as f:
            self.meta = pickle.load(f)
        self.model = SentenceTransformer(model_name)
        self.chunk_cache = self._load_all_chunks()

        self.query_patterns = {
            'simple': ['what is', 'define', 'explain'],
            'complex': ['how to', 'process', 'steps', 'requirements'],
            'comparison': ['vs', 'versus', 'difference', 'compare'],
            'policy': ['policy', 'rule', 'regulation', 'allowed']
        }

    def _load_all_chunks(self) -> Dict[int, str]:
        cache = {}
        for i, meta_item in enumerate(self.meta):
            chunk_file = meta_item['source_file'].replace('.pdf', f"_chunk_{meta_item['chunk_id']}.txt")
            try:
                with open(f"chunks/{chunk_file}", "r") as f:
                    cache[i] = f.read().strip()
            except Exception as e:
                logging.warning(f"❌ Failed to load chunk {i}: {e}")
                cache[i] = ""
        return cache

    def _classify_query(self, question: str) -> str:
        q = question.lower()
        for qtype, patterns in self.query_patterns.items():
            if any(p in q for p in patterns):
                return qtype
        return 'general'

    def _get_dynamic_k(self, query_type: str, question: str) -> int:
        if query_type == 'simple':
            return 2
        elif query_type == 'complex':
            return 7
        elif len(question.split()) > 15:
            return 6
        return 4

    @lru_cache(maxsize=128)
    def _cached_embedding(self, question: str):
        return self.model.encode([question])

    def retrieve(self, question: str, top_k: Optional[int] = None, rerank: bool = False, llm_callable=None) -> List[Dict]:

        query_type = self._classify_query(question)
        k = top_k or self._get_dynamic_k(query_type, question)

        q_embedding = self._cached_embedding(question)
        distances, indices = self.index.search(np.array(q_embedding), k)

        results = []
        for idx, dist in zip(indices[0], distances[0]):
            if idx < len(self.meta):
                results.append({
                    "source_file": self.meta[idx]['source_file'],
                    "category": self.meta[idx]['category'],
                    "chunk_id": self.meta[idx]['chunk_id'],
                    "text": self.chunk_cache.get(idx, ""),
                    "distance": float(dist)
                })

        if rerank and llm_callable:
            results = self._rerank_with_llm(question, results, llm_callable)

        return results

    def _rerank_with_llm(self, question: str, results: List[Dict], llm_callable, top_n: int = 5) -> List[Dict]:
        prompts = [
            f"Rate the relevance of the following text to the question:\n\nQuestion: {question}\nText: {item['text']}\n\nScore (0-10):"
            for item in results
        ]
        scores = []
        for prompt in prompts:
            try:
                score = int(llm_callable(prompt))
            except Exception:
                score = 0
            scores.append(score)

        reranked = sorted(zip(scores, results), key=lambda x: -x[0])
        return [r[1] for r in reranked[:top_n]]

