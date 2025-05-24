# AskGeorge+ 🧠📚  
*A Multi-Agent AI Support Assistant for George Brown College*

AskGeorge+ is a Retrieval-Augmented Generation (RAG) system built with modular agents to help George Brown College students get quick, accurate answers to academic and administrative questions. It combines document scraping, semantic search with FAISS, and natural language answers powered by both local and cloud LLMs, with a modern Flask web interface.

---

## 🔧 Features

- 📄 Web scraper for George Brown College PDFs  
- 📚 Semantic chunking + embedding with FAISS  
- 🔍 OptimizedRetrieverAgent: filters and ranks chunks  
- 💬 SmartAnswerAgent: context-aware LLM prompt engine  
- 🧠 Multiple LLM Support:
  - Local: Ollama (phi3:mini, mistral)
  - Cloud: OpenAI GPT-3.5/4, Claude, Gemini, Hugging Face
- 🔐 Secure API key management via environment variables
- 🌐 Modern Flask web interface with real-time chat
- 🧪 CLI assistant with chunk preview + response timing  
- 🗃️ Logs, metadata, and word/token EDA support  

---

## 📁 Project Structure

```
├── agents/                 # Custom agent logic (retriever, answer)
├── chunks/                 # Chunked .txt files from documents
├── clean_text/             # Raw .txt extracted from PDFs
├── llm/                    # LLM wrappers (Ollama or others)
├── logs/                   # Embedding metadata, index, logs
├── raw_data/               # Scraped PDF files
├── scripts/                # PDF scraper, text processor, embedder
├── templates/              # Flask HTML templates
├── app.py                  # Flask web application
├── requirements.txt        # Python dependencies
```

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/birajgtm/askgeorge-.git
cd askgeorge
```

### 2. Set Up Environment
```bash
python -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file for API keys
cp .env.example .env
```

### 3. Configure API Keys
Create a `.env` file in the root directory with your API keys:
```bash
# Required for OpenAI models
OPENAI_API_KEY=your_key_here

# Required for Claude models
ANTHROPIC_API_KEY=your_key_here

# Required for Hugging Face models
HUGGINGFACE_API_KEY=your_key_here
HUGGINGFACE_MODEL=tiiuae/falcon-7b-instruct  # Optional, this is default

# Required for Google Gemini
GOOGLE_GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-1.5-flash  # Optional, this is default
```

### 4. (Optional) Install Ollama for Local LLM
```bash
# Download and run a local LLM like Phi-3 or Mistral
ollama run phi3:mini
```

---

## 🔄 Build the Knowledge Base

### A. Scrape PDFs from GBC Website
```bash
python scripts/full_gbc_scraper.py
```

### B. Convert PDFs to Text
```bash
python scripts/pdf_to_text.py
```

### C. Chunk and Embed Documents
```bash
python scripts/chunk_texts.py
python scripts/embed_chunks.py
```

---

## 💬 Run the Assistant

### Web Interface (Recommended)
```bash
python app.py
```
Then open http://localhost:10000 in your browser.

You'll be prompted to choose your preferred LLM:
1. Local (Ollama)
2. Cloud (OpenAI)
3. Cloud (Claude)
4. Cloud (Hugging Face)
5. Cloud (Gemini)

### CLI Interface (Alternative)
```bash
python main.py
```

---

## 🔍 Optional: Query Tester
```bash
python scripts/query.py
```
Standalone CLI to test FAISS retrieval and chunk quality.

---

## 🧠 Tech Stack

| Component          | Tool/Library                         |
|--------------------|--------------------------------------|
| Web Framework      | Flask 3.0.3                         |
| Local LLM          | Ollama (`phi3:mini`)                |
| Cloud LLMs         | OpenAI, Claude, Gemini, Hugging Face |
| Embedding Model    | `all-MiniLM-L6-v2` via sentence-transformers |
| Vector Search      | FAISS                                |
| PDF Parsing        | pdfplumber                           |
| Web Scraping       | requests + BeautifulSoup             |
| Prompt Templates   | Manually written by question type    |
| API Key Management | python-dotenv                        |

---

## 📊 Logs & Metadata

| File                     | Description                          |
|--------------------------|--------------------------------------|
| `logs/metadata.csv`      | Source PDFs and download info        |
| `logs/text_metadata.csv` | Word/char count of cleaned files     |
| `chunk_faiss.index`      | FAISS index for vector search        |
| `chunk_metadata.pkl`     | Metadata for each chunk              |
| `chat_logs`              | Chat logs - toggle on llm.py         |

---

## 📝 License

This project is licensed under the MIT License.

---

## 🙌 Acknowledgements

Built for George Brown College's project by G9.