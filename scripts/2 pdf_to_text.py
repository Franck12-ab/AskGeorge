import os
import pdfplumber
import csv
import pandas as pd

raw_folder = "raw_data"
clean_folder = "clean_text"
metadata_path = "logs/metadata.csv"
output_csv = "logs/text_metadata.csv"

# Ensure clean_text folder exists
os.makedirs(clean_folder, exist_ok=True)

# Load PDF metadata
metadata = pd.read_csv(metadata_path)

# Open the output log CSV
with open(output_csv, mode="w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["filename", "text_file", "word_count", "char_count", "category"])

    # Iterate over all PDF files
    for filename in os.listdir(raw_folder):
        if not filename.endswith(".pdf"):
            continue

        pdf_path = os.path.join(raw_folder, filename)
        txt_path = os.path.join(clean_folder, filename.replace(".pdf", ".txt"))

        try:
            with pdfplumber.open(pdf_path) as pdf:
                full_text = "\n".join(page.extract_text() or "" for page in pdf.pages)

            with open(txt_path, "w", encoding="utf-8") as f_txt:
                f_txt.write(full_text)

            # Match category from metadata
            match = metadata[metadata['filename'] == filename]
            category = match.iloc[0]['category'] if not match.empty else "Unknown"

            word_count = len(full_text.split())
            char_count = len(full_text)

            writer.writerow([filename, txt_path, word_count, char_count, category])
            print(f"✅ Processed: {filename} → {word_count} words")

        except Exception as e:
            print(f"❌ Failed to process {filename} | {e}")
