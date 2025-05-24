from agents.optimized_retriever_agent import OptimizedRetrieverAgent
from agents.smart_answer_agent import SmartAnswerAgent
from llm.llm import choose_llm, get_response
import time

def main():
    print("🚀 Loading optimized AskGeorge+ system...")
    start_time = time.time()

    # Load Chroma-based retriever
    retriever = OptimizedRetrieverAgent(
        persist_path="chroma_index",       # ✅ Adjusted to match actual location
        collection_name="askgeorge"        # ✅ Same name used during embedding
    )

    # Ask user which LLM to use
    llm_mode = choose_llm()

    load_time = time.time() - start_time
    print(f"✅ System loaded in {load_time:.2f} seconds\n")

    while True:
        question = input("❓ Enter your question (or 'exit'): ").strip()
        if question.lower() in ["exit", "quit"]:
            break
        if not question:
            print("⚠️ Please enter a valid question.\n")
            continue

        start_time = time.time()

        # Step 1: Retrieve relevant chunks
        retrieved = retriever.retrieve(
            question,
            rerank=False,
            llm_callable=lambda prompt: get_response(question, prompt, mode=llm_mode)
        )

        retrieval_time = time.time() - start_time
        print(f"\n🔍 Found {len(retrieved)} relevant chunks in {retrieval_time:.2f}s\n")

        for i, chunk in enumerate(retrieved[:2]):
            print(f"[{i+1}] 📄 {chunk['source_file']} | 📁 {chunk['category']} | Score: {chunk['distance']:.3f}")
            print(chunk['text'][:200].replace("\n", " ") + "...\n")

        # Step 2: Generate answer using chosen LLM
        print("💬 Generating answer...")

        answer_agent = SmartAnswerAgent(
            llm_callable=lambda prompt: get_response(question, prompt, mode=llm_mode)
        )

        gen_start = time.time()
        answer = answer_agent.generate_answer(question, retrieved)
        gen_time = time.time() - gen_start
        total_time = time.time() - start_time

        print(f"\n✅ Answer (generated in {gen_time:.2f}s, total: {total_time:.2f}s):\n")
        print(answer)
        print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    main()
