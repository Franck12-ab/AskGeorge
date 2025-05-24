from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import time
import os

# 🔁 Updated Chroma-compatible agent
from agents.optimized_retriever_agent import OptimizedRetrieverAgent
from agents.smart_answer_agent import SmartAnswerAgent
from llm.llm import get_response

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # ⚠️ Use a secure random key in production

# 📦 Default port for local use or Heroku-style deployment
port = int(os.environ.get("PORT", 10000))

# 🔁 Instantiate Chroma-based retriever
retriever = OptimizedRetrieverAgent(
    persist_path="chroma_index",
    collection_name="askgeorge"
)


@app.route('/', methods=['GET', 'POST'])
def select_model():
    if request.method == 'POST':
        selected_llm = request.form.get('llm', 'ollama')
        session['selected_llm'] = selected_llm
        session['chat_history'] = []
        return redirect(url_for('chat'))
    return render_template('select_model.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'selected_llm' not in session:
        return redirect(url_for('select_model'))

    if 'chat_history' not in session:
        session['chat_history'] = []

    selected_llm = session['selected_llm']

    if request.method == 'POST':
        question = request.form.get('question', '').strip()
        answer_content = "Sorry, I couldn't process that."

        if question:
            start_time = time.time()

            # 🔍 Retrieve chunks using ChromaDB
            retrieved = retriever.retrieve(question)

            # 🧠 Use LLM to generate answer from retrieved context
            answer_agent = SmartAnswerAgent(
                llm_callable=lambda prompt: get_response(question, prompt, mode=selected_llm)
            )

            gen_start = time.time()
            answer_content = answer_agent.generate_answer(question, retrieved)
            gen_time = time.time() - gen_start
            total_time = time.time() - start_time

            # 💾 Store in session history
            entry = {
                "question": question,
                "answer": answer_content,
                "timing": {
                    "retrieval": round(gen_time, 2),
                    "generation": round(gen_time, 2),
                    "total": round(total_time, 2)
                },
                "llm": selected_llm
            }
            session['chat_history'].append(entry)
            session.modified = True

            # ✅ AJAX-compatible JSON response
            return jsonify({"answer": answer_content, "question": question})

        else:
            return jsonify({"answer": "Please ask a question.", "question": ""}), 400

    return render_template(
        'chat.html',
        chat_history=session.get('chat_history', []),
        selected_llm=selected_llm
    )

@app.route('/clear')
def clear():
    session.pop('chat_history', None)
    session.modified = True
    return redirect(url_for('chat'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
