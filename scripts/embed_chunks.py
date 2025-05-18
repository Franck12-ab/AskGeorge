import os
import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

# Load chunk metadata
chunk_df = pd.read_csv("logs/chunk_metadata.csv")
chunk_texts = []
meta_info = []

# Load all chunk texts
for _, row in chunk_df.iterrows():
    try:
        with open(f"chunks/{row['source_file'].replace('.pdf', f'_chunk_{row['chunk_id']}.txt')}", "r") as f:
            text = f.read().strip()
            chunk_texts.append(text)
            meta_info.append({
                "chunk_id": row["chunk_id"],
                "source_file": row["source_file"],
                "category": row["category"]
            })
    except Exception as e:
        print(f"❌ Failed loading chunk {row['chunk_id']} | {e}")

# Generate embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(chunk_texts, show_progress_bar=True)

# Build FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

# Save index and metadata
faiss.write_index(index, "logs/chunk_faiss.index")
with open("logs/chunk_metadata.pkl", "wb") as f:
    pickle.dump(meta_info, f)

print("✅ Embeddings saved and indexed.")
