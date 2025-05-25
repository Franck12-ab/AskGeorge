import os
import pdfplumber
import csv

# Paths
script_dir = os.path.dirname(__file__)              # scripts/
base_dir = os.path.abspath(os.path.join(script_dir, ".."))  # your root folder

raw_folder = os.path.join(base_dir, "pdfs")         # ../pdfs
clean_folder = os.path.join(base_dir, "clean_text") # ../clean_text
output_csv = os.path.join(base_dir, "logs", "text_metadata.csv")

# Ensure folders exist
os.makedirs(clean_folder, exist_ok=True)
os.makedirs(os.path.join(base_dir, "logs"), exist_ok=True)

# Write metadata CSV
with open(output_csv, mode="w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["filename", "text_file", "word_count", "char_count", "category"])

    for filename in os.listdir(raw_folder):
        if not filename.endswith(".pdf"):
            continue

        pdf_path = os.path.join(raw_folder, filename)
        txt_filename = filename.replace(".pdf", ".txt")
        txt_path = os.path.join(clean_folder, txt_filename)

        try:
            with pdfplumber.open(pdf_path) as pdf:
                full_text = "\n".join(page.extract_text() or "" for page in pdf.pages)

            with open(txt_path, "w", encoding="utf-8") as f_txt:
                f_txt.write(full_text)

            word_count = len(full_text.split())
            char_count = len(full_text)
            category = "Unknown"  # or hardcoded if needed

            writer.writerow([filename, txt_path, word_count, char_count, category])
            print(f"✅ Processed: {filename} → {word_count} words")

        except Exception as e:
            print(f"❌ Failed to process {filename} | {e}")
