# AskGeorge+ 🧠📚  
*A Multi-Agent AI Support Assistant for George Brown College*

AskGeorge+ is a Retrieval-Augmented Generation (RAG) system built with LangChain to help George Brown College students get quick, accurate answers to academic and administrative questions. It combines document scraping, semantic search with ChromaDB through LangChain, and natural language answers powered by Google's Gemini model, with a modern Flask web interface.

🌐 **Live Demo**: [askgeorge.onrender.com](https://askgeorge.onrender.com) - Unstable (Free Tier)

---

## 🔧 Features

- 📄 Web scraper for George Brown College Website with automated processing pipeline  
- 📚 LangChain-powered semantic search with ChromaDB integration
- 🧠 Conversational AI powered by Google Gemini
- 💬 Smart conversation memory for context-aware responses
- 🔍 Natural language formatting for human-like interactions
- 🌐 Modern Flask web interface with real-time chat
- 🧪 Built-in conversation history and source tracking
- 🗃️ Automated document processing and embedding pipeline

---

## 📁 Project Structure

```
├── agents/                     # LangChain agent implementation
│   └── conversational_agent.py # Main conversation handler with LangChain
├── chroma_index/              # [Downloaded] ChromaDB vector store
├── scripts/                   # Numbered scripts (1-5) for processing pipeline
├── templates/                 # Flask HTML templates
│   ├── chat.html             # Main chat interface
│   └── select_model.html     # Model selection page
├── app.py                    # Flask web application
├── main.py                   # CLI interface application
├── start.sh                  # Startup script for downloading and setup
├── install.sh                # Installation script
└── requirements.txt          # Python dependencies
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
```

### 3. Configure Google Cloud Credentials
Create a `.env` file in the root directory with the following:
```bash
# Path to your Google Cloud service account JSON key file
GOOGLE_APPLICATION_CREDENTIALS=keys/your-key-file.json

# Port for the Flask application (optional)
PORT=10000
```

---

## 💬 Run the Assistant

### First Time Setup
```bash
# Run the installation script - this will:
# 1. Set up the environment
# 2. Install dependencies
# 3. Download the ChromaDB index
./install.sh
```

### Running the Application
You can start the application in two ways:

1. Using start script (Recommended):
```bash
# This will verify ChromaDB index exists and start the application
./start.sh
```

2. Direct Python execution:
```bash
# Make sure ChromaDB index is downloaded first
python app.py
```

Then open http://localhost:10000 in your browser.

### CLI Interface (Alternative)
```bash
python main.py
```

---

## 🧠 Tech Stack

| Component          | Tool/Library                         |
|--------------------|--------------------------------------|
| Framework          | LangChain                           |
| Web Framework      | Flask 3.1.0                         |
| LLM               | Google Gemini                        |
| Embedding Model    | `all-MiniLM-L6-v2` via HuggingFace |
| Vector Store      | ChromaDB via LangChain              |
| Memory System     | ConversationBufferMemory            |
| PDF Processing    | pdfplumber                           |
| Web Scraping      | requests + BeautifulSoup             |
| API Key Management | python-dotenv                        |

---

## 📊 Logs & Metadata

| File                     | Description                          |
|--------------------------|--------------------------------------|
| `chroma_index/`          | ChromaDB vector store                |
| `chat_logs`              | Chat logs - toggle on llm.py         |

---

## 📝 License

This project is licensed under the MIT License.

---

## 🙌 Acknowledgements

Built for George Brown College's project by G9.
