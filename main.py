from agents.conversational_agent import ConversationalAgent
import time
from dotenv import load_dotenv

load_dotenv()

def main():
    print("🚀 Launching AskGeorge+ (CLI with memory + Gemini)...")


    # Initialize the conversational agent with memory + Gemini + LangChain-compatible Chroma
    agent = ConversationalAgent(persist_path="chroma_index")

    while True:
        question = input("❓ Enter your question (or type 'exit'): ").strip()
        if question.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break
        if not question:
            print("⚠️ Please enter a valid question.\n")
            continue

        start_time = time.time()

        # Run the agent
        result = agent.run(question)
        answer = result["answer"]

        # Show retrieved document info if needed
        print("🔍 Inspecting retrieved sources (first 5):\n")
        for i, doc in enumerate(result.get("sources", [])[:5]):
            print(f"[{i+1}] 🔎 Type: {type(doc)}")
            print(f"     🧾 Content: {repr(doc)}\n")

        print(f"\n✅ Answer:\n{answer}")
        print(f"\n⏱️ Total time: {round(time.time() - start_time, 2)}s")
        print("=" * 80 + "\n")

if __name__ == "__main__":
    main()
