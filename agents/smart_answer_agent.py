class SmartAnswerAgent:
    def __init__(self, llm_callable):
        self.llm = llm_callable


        self.templates = {
    'simple': """You are a concise and helpful assistant. Answer clearly using only the information below.

{context}

Q: {question}
A:""",

    'complex': """You are a George Brown College assistant. Provide a detailed answer using the relevant information below.

{context}

Question: {question}
Answer (include steps if applicable):""",

    'policy': """You are a George Brown College assistant. Respond with a clear summary of the policy, including any exceptions.

{context}

Policy question: {question}
Answer:""",

    'general': """You are a helpful assistant at George Brown College. Respond naturally and informatively using the information below.

{context}

Question: {question}
Answer:"""
}

    def _get_query_type(self, question: str) -> str:
        q = question.lower()

        if any(phrase in q for phrase in [
            "what is", "define", "meaning of", "explain", "give me a definition"
        ]):
            return "simple"

        elif any(phrase in q for phrase in [
            "how do", "how to", "steps", "process", "procedure", "guide", "requirement", "instructions"
        ]):
            return "complex"

        elif any(phrase in q for phrase in [
            "policy", "rule", "allowed", "not allowed", "can i", "permitted", "regulation", "compliance"
        ]):
            return "policy"

        elif any(phrase in q for phrase in [
            "who are you", "what can you do", "your purpose", "what is this", "introduce yourself"
        ]):
            return "general"  # general personality/system question

        else:
            return "general"


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
