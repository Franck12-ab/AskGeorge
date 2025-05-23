# AskGeorge+ 🧠📚  
*A Multi-Agent AI Support Assistant for George Brown College*

AskGeorge+ is a Retrieval-Augmented Generation (RAG) system built with modular agents to help George Brown College students get quick, accurate answers to academic and administrative questions. It combines document scraping, semantic search with FAISS, and natural language answers powered by local LLMs.

---

## 🔧 Features

- 📄 Web scraper for George Brown College PDFs  
- 📚 Semantic chunking + embedding with FAISS  
- 🔍 OptimizedRetrieverAgent: filters and ranks chunks  
- 💬 SmartAnswerAgent: context-aware LLM prompt engine  
- 🧠 LLM via Ollama (supports `phi3:mini`, `mistral`)  
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
├── main.py                 # CLI app interface
├── requirements.txt        # Python dependencies
```

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/askgeorge.git
cd askgeorge
```

### 2. Set Up Environment
```bash
python -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. (Optional) Install Ollama + Model
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

```bash
python main.py
```

Then type:
```
What GPA is required for co-op?
```

The system will:
- Retrieve top-matching document chunks  
- Generate a context-aware answer using your LLM  
- Show response time and source info  

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
| LLM                | Ollama (`phi3:mini`) or Hugging Face |
| Embedding Model    | `all-MiniLM-L6-v2` via sentence-transformers |
| Vector Search      | FAISS                                |
| PDF Parsing        | pdfplumber                           |
| Web Scraping       | requests + BeautifulSoup             |
| Prompt Templates   | Manually written by question type    |

---

## 📊 Logs & Metadata

| File                     | Description                          |
|--------------------------|--------------------------------------|
| `logs/metadata.csv`      | Source PDFs and download info        |
| `logs/text_metadata.csv` | Word/char count of cleaned files     |
| `chunk_faiss.index`      | FAISS index for vector search        |
| `chunk_metadata.pkl`     | Metadata for each chunk              |

---

## 📝 License

This project is licensed under the MIT License.

---

## 🙌 Acknowledgements

Built for George Brown College’s project by G9.