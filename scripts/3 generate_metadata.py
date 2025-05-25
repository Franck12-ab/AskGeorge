import os
import csv
from pathlib import Path

output_csv = "logs/all_text_metadata.csv"
folders = {
    "clean_text": "PDF",
    "pages": "All Page",
}

os.makedirs("logs", exist_ok=True)

with open(output_csv, mode="w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["filename", "text_file", "word_count", "char_count", "category"])

    for folder, category in folders.items():
        for file in os.listdir(folder):
            if file.endswith(".txt"):
                path = os.path.join(folder, file)
                with open(path, "r", encoding="utf-8") as txt_file:
                    content = txt_file.read()
                word_count = len(content.split())
                char_count = len(content)
                writer.writerow([file, path, word_count, char_count, category])
                print(f"✅ Logged: {path}")
