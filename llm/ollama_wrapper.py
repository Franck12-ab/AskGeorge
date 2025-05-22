import requests

def ollama_chat(prompt, model="phi3:mini"):  # ⬅️ use faster model
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()["response"].strip()
