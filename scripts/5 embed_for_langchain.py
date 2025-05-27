import os
from pathlib import Path
import pandas as pd
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# === Paths ===
chunk_folder = "chunks"
chunk_log_file = "logs/chunk_metadata.csv"
persist_dir = "chroma_index"  # LangChain-compatible output

# === Load metadata ===
df = pd.read_csv(chunk_log_file)

# === Build LangChain Document objects ===
documents = []
for _, row in df.iterrows():
    chunk_id = str(row["chunk_id"])
    source_file = row["source_file"]
    category = row["category"]
    chunk_filename = f"{Path(source_file).stem}_chunk_{chunk_id}.txt"
    chunk_path = os.path.join(chunk_folder, chunk_filename)

    if not os.path.exists(chunk_path):
        continue

    with open(chunk_path, "r", encoding="utf-8") as f:
        content = f.read()

    documents.append(Document(
        page_content=content,
        metadata={
            "chunk_id": chunk_id,
            "source_file": source_file,
            "category": category
        }
    ))

print(f"📚 Loaded {len(documents)} documents for embedding.")

# === Embed and build vector store ===
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
print("⚙️  Building Chroma vector store for LangChain...")
db = Chroma.from_documents(
    documents=documents,
    embedding=embedding,
    persist_directory=persist_dir
)
db.persist()
print(f"✅ LangChain-compatible Chroma index saved to: {persist_dir}")
