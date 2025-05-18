import os
import csv
import pandas as pd
from pathlib import Path

clean_folder = "clean_text"
chunk_folder = "chunks"
log_file = "logs/text_metadata.csv"
chunk_log_file = "logs/chunk_metadata.csv"

os.makedirs(chunk_folder, exist_ok=True)

df = pd.read_csv(log_file)

chunk_size = 512
overlap = 128
chunk_id = 0

with open(chunk_log_file, mode="w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["chunk_id", "source_file", "category", "word_count", "chunk_text"])

    for _, row in df.iterrows():
        file_path = row["text_file"]
        category = row["category"]
        filename = row["filename"]

        try:
            with open(file_path, "r", encoding="utf-8") as f_txt:
                words = f_txt.read().split()

            for i in range(0, len(words), chunk_size - overlap):
                chunk_words = words[i:i + chunk_size]
                if len(chunk_words) < 100:  # Skip very small chunks
                    continue

                chunk_text = " ".join(chunk_words)
                chunk_filename = f"{Path(filename).stem}_chunk_{chunk_id}.txt"
                chunk_path = os.path.join(chunk_folder, chunk_filename)

                with open(chunk_path, "w", encoding="utf-8") as cf:
                    cf.write(chunk_text)

                writer.writerow([
                    chunk_id,
                    filename,
                    category,
                    len(chunk_words),
                    chunk_text[:100].replace("\n", " ") + "..."  # preview only
                ])

                print(f"✅ Chunked {filename} → {chunk_filename}")
                chunk_id += 1

        except Exception as e:
            print(f"❌ Failed to chunk {filename} | {e}")
