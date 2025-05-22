from agents.optimized_retriever_agent import OptimizedRetrieverAgent
from agents.smart_answer_agent import SmartAnswerAgent
from llm.ollama_wrapper import ollama_chat
import time

def main():
    print("🚀 Loading optimized AskGeorge+ system...")
    start_time = time.time()

    retriever = OptimizedRetrieverAgent(
        index_path="logs/chunk_faiss.index",
        metadata_path="logs/chunk_metadata.pkl"
    )
    answer_agent = SmartAnswerAgent(llm_callable=ollama_chat)

    load_time = time.time() - start_time
    print(f"✅ System loaded in {load_time:.2f} seconds\n")

    while True:
        question = input("❓ Enter your question (or 'exit'): ").strip()
        if question.lower() in ["exit", "quit"]:
            break

        start_time = time.time()

        # Step 1: Smart Retrieval
        retrieved = retriever.retrieve(question)
        retrieval_time = time.time() - start_time

        print(f"\n🔍 Found {len(retrieved)} relevant chunks in {retrieval_time:.2f}s\n")

        # Show top 2 chunks
        for i, chunk in enumerate(retrieved[:2]):
            print(f"[{i+1}] 📄 {chunk['source_file']} | 📁 {chunk['category']} | Score: {chunk['distance']:.3f}")
            print(chunk['text'][:200].replace("\n", " ") + "...\n")

        # Step 2: Generate answer
        print("💬 Generating answer...")
        gen_start = time.time()
        answer = answer_agent.generate_answer(question, retrieved)
        gen_time = time.time() - gen_start

        total_time = time.time() - start_time

        print(f"\n✅ Answer (generated in {gen_time:.2f}s, total: {total_time:.2f}s):\n")
        print(answer)
        print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    main()
