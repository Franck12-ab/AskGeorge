import requests

def ollama_chat(prompt, model="phi3:mini"):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            }
        )
        data = response.json()

        if "response" in data:
            return data["response"].strip()
        elif "error" in data:
            return f"⚠️ Ollama error: {data['error']}"
        else:
            return f"⚠️ Unexpected response: {data}"

    except requests.exceptions.ConnectionError:
        return "⚠️ Could not connect to Ollama. Is it running at http://localhost:11434?"

    except Exception as e:
        return f"⚠️ Unexpected error: {str(e)}"
