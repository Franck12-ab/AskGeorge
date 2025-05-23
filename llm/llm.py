import os
import requests
import json
from dotenv import load_dotenv
import anthropic
from openai import OpenAI
import datetime

# Load environment variables
load_dotenv()

# Initialize clients
openai_client = OpenAI()  # Uses OPENAI_API_KEY
anthropic_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# === 1. Ollama (Local LLM) ===
def ollama_chat(prompt, model="phi3:mini"):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=15
        )
        data = response.json()
        return data.get("response", "⚠️ Ollama error or invalid response").strip()
    except requests.exceptions.Timeout:
        return "⚠️ Ollama timed out. Try again after the model is ready."
    except requests.exceptions.ConnectionError:
        return "⚠️ Ollama not running. Start it with: `ollama run phi3:mini`"
    except Exception as e:
        return f"⚠️ Ollama error: {e}"

# === 2. OpenAI (Cloud LLM) ===
def openai_chat(prompt, model="gpt-3.5-turbo"):
    try:
        response = openai_client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ OpenAI error: {e}"

# === 3. Claude (Anthropic LLM) ===
def claude_chat(prompt, model="claude-3-haiku-20240307"):
    try:
        response = anthropic_client.messages.create(
            model=model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text.strip()
    except anthropic.APIStatusError as e:
        if e.status_code == 400 and "credit balance" in str(e):
            return "⚠️ Claude is unavailable due to insufficient credits."
        return f"⚠️ Claude API error: {e}"
    except Exception as e:
        return f"⚠️ Claude error: {e}"

# === 4. Hugging Face (Free Cloud LLM) ===
def huggingface_chat(prompt):
    api_key = os.getenv("HUGGINGFACE_API_KEY")
    model = os.getenv("HUGGINGFACE_MODEL", "tiiuae/falcon-7b-instruct")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 256},
        "options": {"wait_for_model": True}
    }

    try:
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{model}",
            headers=headers,
            data=json.dumps(payload),
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        if isinstance(result, list) and "generated_text" in result[0]:
            return result[0]["generated_text"].strip()
        else:
            return f"⚠️ Unexpected Hugging Face response: {result}"
    except Exception as e:
        return f"⚠️ Hugging Face error: {e}"

# === 5. Google Gemini (Free via AI Studio) ===


def gemini_chat(prompt):
    api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
    model = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    log_path = "logs/gemini_chat_log.jsonl"

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    log_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "model": model,
        "prompt": prompt,
        "url": url,
        "request_payload": data,
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=20)
        response.raise_for_status()
        result = response.json()
        reply = result["candidates"][0]["content"]["parts"][0]["text"].strip()

        log_entry["response"] = reply
        log_entry["status"] = "success"

    except Exception as e:
        log_entry["status"] = "error"
        log_entry["error"] = str(e)
        reply = f"⚠️ Gemini API error: {e}"

    # Write log entry to file (line-delimited JSON for easy parsing)
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    return reply

# === User Prompt for Model Selection ===
def choose_llm():
    print("🤖 Choose LLM engine:")
    print("1. Local (Ollama)")
    print("2. Cloud (OpenAI)")
    print("3. Cloud (Claude)")
    print("4. Cloud (Hugging Face)")
    print("5. Cloud (Gemini)")
    choice = input("Enter 1, 2, 3, 4, or 5: ").strip()
    return {
        "1": "ollama",
        "2": "openai",
        "3": "claude",
        "4": "huggingface",
        "5": "gemini"
    }.get(choice, "ollama")

# === Unified Chat Handler ===
def get_response(prompt, mode="ollama"):
    if mode == "ollama":
        return ollama_chat(prompt)
    elif mode == "openai":
        return openai_chat(prompt)
    elif mode == "claude":
        return claude_chat(prompt)
    elif mode == "huggingface":
        return huggingface_chat(prompt)
    elif mode == "gemini":
        return gemini_chat(prompt)
    else:
        return "⚠️ Invalid LLM mode."
