import os
import requests
import json
from dotenv import load_dotenv
import anthropic
from openai import OpenAI
from .log import log_llm_interaction

# Load environment variables
load_dotenv()

# Global logging toggle
log = False

# Initialize clients
openai_client = OpenAI()  # Uses OPENAI_API_KEY
anthropic_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# === 1. Ollama ===
def ollama_chat(question, prompt, model="phi3:mini"):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=15
        )
        data = response.json()
        reply = data.get("response", "⚠️ Ollama error or invalid response").strip()
        if log:
            log_llm_interaction("ollama", model, question, prompt, response=reply)
        return reply
    except Exception as e:
        if log:
            log_llm_interaction("ollama", model, prompt, error=e)
        return f"⚠️ Ollama error: {e}"

# === 2. OpenAI ===
def openai_chat(question, prompt, model="gpt-3.5-turbo"):
    try:
        response = openai_client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        reply = response.choices[0].message.content.strip()
        if log:
            log_llm_interaction("openai", model, question, prompt, response=reply)
        return reply
    except Exception as e:
        if log:
            log_llm_interaction("openai", model, question, prompt, error=e)
        return f"⚠️ OpenAI error: {e}"

# === 3. Claude ===
def claude_chat(question, prompt, model="claude-3-haiku-20240307"):
    try:
        response = anthropic_client.messages.create(
            model=model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        reply = response.content[0].text.strip()
        if log:
            log_llm_interaction("claude", model, question, prompt, response=reply)
        return reply
    except Exception as e:
        if log:
            log_llm_interaction("claude", model, question, prompt, error=e)
        return f"⚠️ Claude API error: {e}"

# === 4. Hugging Face ===
def huggingface_chat(question, prompt):
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
        reply = result[0]["generated_text"].strip() if isinstance(result, list) else "⚠️ Unexpected response"
        if log:
            log_llm_interaction("huggingface", model, question, prompt, response=reply)
        return reply
    except Exception as e:
        if log:
            log_llm_interaction("huggingface", model, question, prompt, error=e)
        return f"⚠️ Hugging Face error: {e}"

# === 5. Google Gemini ===
def gemini_chat(question, prompt):
    api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
    model = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=20)
        response.raise_for_status()
        result = response.json()
        reply = result["candidates"][0]["content"]["parts"][0]["text"].strip()
        if log:
            log_llm_interaction("gemini", model, question, prompt, response=reply)
        return reply
    except Exception as e:
        if log:
            log_llm_interaction("gemini", model, question, prompt, error=e)
        return f"⚠️ Gemini API error: {e}"

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
def get_response(question, prompt, mode="ollama"):
    if mode == "ollama":
        return ollama_chat(question, prompt)
    elif mode == "openai":
        return openai_chat(question, prompt)
    elif mode == "claude":
        return claude_chat(question, prompt)
    elif mode == "huggingface":
        return huggingface_chat(question, prompt)
    elif mode == "gemini":
        return gemini_chat(question, prompt)
    else:
        return "⚠️ Invalid LLM mode."
