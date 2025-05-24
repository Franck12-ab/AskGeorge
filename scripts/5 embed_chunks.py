import os
import pandas as pd
from pathlib import Path
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

# === Paths ===
chunk_log_path = "logs/chunk_metadata.csv"
chunk_folder = "chunks"
persist_directory = "chroma_index"
batch_size = 500  # ✅ Safe batch size for Chroma

# === Load Chroma Client ===
chroma_client = chromadb.PersistentClient(path=persist_directory)
collection = chroma_client.get_or_create_collection("askgeorge")

# === Load metadata ===
chunk_df = pd.read_csv(chunk_log_path)
texts, metadatas, ids = [], [], []

# === Read chunk files ===
for _, row in chunk_df.iterrows():
    try:
        chunk_id = str(row["chunk_id"])
        filename = row["source_file"]
        category = row["category"]
        chunk_filename = f"{Path(filename).stem}_chunk_{chunk_id}.txt"
        chunk_path = os.path.join(chunk_folder, chunk_filename)

        with open(chunk_path, "r", encoding="utf-8") as f:
            text = f.read().strip()

        texts.append(text)
        metadatas.append({
            "chunk_id": chunk_id,
            "source_file": filename,
            "category": category
        })
        ids.append(chunk_id)

    except Exception as e:
        print(f"❌ Failed loading chunk {row['chunk_id']} | {e}")

# === Embed ===
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(texts, show_progress_bar=True).tolist()

# === Add to Chroma in batches ===
print(f"\n📦 Inserting {len(texts)} chunks into ChromaDB in batches...")
for i in range(0, len(texts), batch_size):
    collection.add(
        documents=texts[i:i + batch_size],
        metadatas=metadatas[i:i + batch_size],
        ids=ids[i:i + batch_size],
        embeddings=embeddings[i:i + batch_size]
    )
    print(f"✅ Added batch {i // batch_size + 1}")

print(f"\n✅ All {len(texts)} chunks embedded and saved to ChromaDB at: {persist_directory}")
