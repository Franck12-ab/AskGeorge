# main.py

from agents.retriever_agent import RetrieverAgent
from agents.answer_agent import AnswerAgent
from llm.ollama_wrapper import ollama_chat

def main():
    retriever = RetrieverAgent(
        index_path="logs/chunk_faiss.index",
        metadata_path="logs/chunk_metadata.pkl"
    )
    answer_agent = AnswerAgent(llm_callable=ollama_chat)

    while True:
        question = input("❓ Enter your question (or 'exit'): ").strip()
        if question.lower() in ["exit", "quit"]:
            break

        # Step 1: Retrieve chunks
        retrieved = retriever.retrieve(question)
        print(f"\n🔍 Found {len(retrieved)} relevant chunks.\n")

        for i, chunk in enumerate(retrieved):
            print(f"[{i+1}] 📄 {chunk['source_file']} | 📁 {chunk['category']}")
            print(chunk['text'][:300].replace("\n", " ") + "...\n")

        # Step 2: Generate answer
        print("💬 Generating answer...\n")
        answer = answer_agent.generate_answer(question, retrieved)
        print("✅ Answer:\n")
        print(answer)
        print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    main()
