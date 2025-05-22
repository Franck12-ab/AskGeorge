class SmartAnswerAgent:
    def __init__(self, llm_callable):
        self.llm = llm_callable

        self.templates = {
            'simple': """Answer this question briefly and directly using the context.

Context: {context}
Question: {question}

Answer (1-2 sentences):""",

            'complex': """You are a George Brown College assistant. Provide a comprehensive answer with steps/requirements.

Context: {context}
Question: {question}

Answer (include specific steps/requirements):""",

            'policy': """Answer this policy question with specific rules and any exceptions.

Context: {context}
Question: {question}

Answer (be specific about policies):""",

            'general': """You are a helpful George Brown College assistant. Answer based on the context provided.

Context: {context}
Question: {question}

Answer:"""
        }

    def _get_query_type(self, question: str) -> str:
        q = question.lower()
        if any(w in q for w in ['what is', 'define', 'explain briefly']):
            return 'simple'
        elif any(w in q for w in ['how to', 'process', 'steps', 'requirements']):
            return 'complex'
        elif any(w in q for w in ['policy', 'rule', 'allowed', 'can i']):
            return 'policy'
        return 'general'

    def _smart_context_selection(self, retrieved_chunks, max_tokens=2000):
        sorted_chunks = sorted(retrieved_chunks, key=lambda x: x.get('distance', 0))
        context_parts = []
        total_tokens = 0

        for chunk in sorted_chunks:
            text = chunk["text"]
            tokens = len(text) // 4  # estimate: 4 chars = 1 token
            if total_tokens + tokens > max_tokens:
                break
            context_parts.append(f"[{chunk['category']}] {text}")
            total_tokens += tokens

        return "\n\n".join(context_parts)

    def generate_answer(self, question: str, retrieved_chunks):
        if not retrieved_chunks:
            return "❌ I couldn't find relevant information to answer your question."

        context = self._smart_context_selection(retrieved_chunks)
        query_type = self._get_query_type(question)
        template = self.templates.get(query_type, self.templates['general'])
        prompt = template.format(context=context, question=question)

        return self.llm(prompt)
