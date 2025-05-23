import json
import datetime
import os
import re

LOG_DIR = "chat_logs"
os.makedirs(LOG_DIR, exist_ok=True)

def extract_keyword(text, limit=20):
    if not text:
        return "prompt"
    keyword = re.sub(r'[^\w\s-]', '', text).strip().lower()
    keyword = re.sub(r'\s+', '-', keyword)
    return keyword[:limit] or "prompt"

def log_llm_interaction(model, sub_model, question, prompt, response=None, error=None):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    keyword = extract_keyword(question)

    filename = f"{keyword}_{model}_{timestamp}.jsonl"
    log_path = os.path.join(LOG_DIR, filename)

    log_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "model": model,
        "sub_model": sub_model,
        "question": question,
        "prompt": prompt,
        "response": response if error is None else None,
        "error": str(error) if error else None,
        "status": "success" if error is None else "error"
    }

    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
