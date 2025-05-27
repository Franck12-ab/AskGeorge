from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import time
import os
from dotenv import load_dotenv
from langchain_core.documents import Document
load_dotenv()

from agents.conversational_agent import ConversationalAgent

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # ⚠️ Use a secure random key in production
port = int(os.environ.get("PORT", 10000))

# 🌐 Initialize LangChain-based agent with memory + Gemini + ChromaDB
agent = ConversationalAgent(persist_path="chroma_index")


@app.route('/', methods=['GET', 'POST'])
def select_model():
    if request.method == 'POST':
        # No model selection needed anymore; only Gemini for now
        session['chat_history'] = []
        return redirect(url_for('chat'))
    return render_template('select_model.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'chat_history' not in session:
        session['chat_history'] = []

    if request.method == 'POST':
        question = request.form.get('question', '').strip()

        if not question:
            return jsonify({"answer": "Please ask a question.", "question": ""}), 400

        start_time = time.time()
        result = agent.run(question)
        answer = result["answer"]
        chat_history = result["chat_history"]
        source_files = [
            doc.metadata.get("source_file", "unknown")
            if isinstance(doc, Document) else "unknown"
            for doc in result["sources"]
        ]

        entry = {
            "question": question,
            "answer": answer,
            "sources": source_files,
            "llm": "gemini",
            "timing": {
                "total": round(time.time() - start_time, 2)
            },
            "history_len": len(chat_history)
        }

        session['chat_history'].append(entry)
        session.modified = True

        return jsonify({"answer": answer, "question": question})

    return render_template(
        'chat.html',
        chat_history=session.get('chat_history', []),
        selected_llm="gemini"
    )

@app.route('/clear')
def clear():
    session.pop('chat_history', None)
    session.modified = True
    return redirect(url_for('chat'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
