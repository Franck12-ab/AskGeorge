import chromadb
from sentence_transformers import SentenceTransformer
from functools import lru_cache
from typing import List, Dict, Optional

class OptimizedRetrieverAgent:
    def __init__(self, persist_path, collection_name="askgeorge", model_name="all-MiniLM-L6-v2"):
        self.client = chromadb.PersistentClient(path=persist_path)
        self.collection = self.client.get_or_create_collection(name=collection_name)
        self.model = SentenceTransformer(model_name)

        self.query_patterns = {
            'simple': ['what is', 'define', 'explain'],
            'complex': ['how to', 'process', 'steps', 'requirements'],
            'comparison': ['vs', 'versus', 'difference', 'compare'],
            'policy': ['policy', 'rule', 'regulation', 'allowed']
        }

    def _classify_query(self, question: str) -> str:
        q = question.lower()
        for qtype, patterns in self.query_patterns.items():
            if any(p in q for p in patterns):
                return qtype
        return 'general'

    def _get_dynamic_k(self, query_type: str, question: str) -> int:
        if query_type == 'simple':
            return 3
        elif query_type == 'complex':
            return 7
        elif len(question.split()) > 15:
            return 6
        return 4

    @lru_cache(maxsize=128)
    def _cached_embedding(self, question: str):
        # ✅ Correct: returns 1D list, not [[...]]
        return self.model.encode(question).tolist()

    def retrieve(self, question: str, top_k: Optional[int] = None, rerank: bool = False, llm_callable=None) -> List[Dict]:
        query_type = self._classify_query(question)
        k = top_k or self._get_dynamic_k(query_type, question)

        query_vec = self._cached_embedding(question)

        results = self.collection.query(
            query_embeddings=[query_vec],  # ✅ Accepts a list of 1D vectors
            n_results=k,
            include=["documents", "metadatas", "distances"]
        )

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        output = []
        for doc, meta, dist in zip(documents, metadatas, distances):
            output.append({
                "source_file": meta.get("source_file", "unknown"),
                "category": meta.get("category", "unknown"),
                "chunk_id": meta.get("chunk_id", "unknown"),
                "text": doc,
                "distance": dist
            })

        if rerank and llm_callable:
            output = self._rerank_with_llm(question, output, llm_callable)

        return output

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
