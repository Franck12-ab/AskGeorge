class AnswerAgent:
    def __init__(self, llm_callable):
        self.llm = llm_callable

    def generate_answer(self, question, retrieved_chunks):
        context = "\n\n".join(chunk["text"] for chunk in retrieved_chunks)
        prompt = f"""You are a helpful assistant for George Brown College students.

Answer the following question based only on the context provided.

Context:
{context}

Question: {question}

Answer:"""

        return self.llm(prompt)