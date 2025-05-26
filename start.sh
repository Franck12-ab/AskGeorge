#!/bin/bash

CHROMA_DIR="chroma_index"

echo "📦 Checking for Chroma index in ./$CHROMA_DIR..."
if [ -d "$CHROMA_DIR" ]; then
    echo "✅ Chroma index already exists. Skipping download."
else
    echo "📥 Downloading prebuilt Chroma index ZIP..."
    curl -L "https://www.dropbox.com/scl/fi/twth9kyz7qpdxwh3qxplc/chroma_index.zip?rlkey=22ndkbo7aoslblwqakhp4avkb&st=h66c0pqd&dl=1" -o chroma_index.zip

    echo "🗜️ Extracting ZIP..."
    unzip chroma_index.zip

    echo "🧹 Cleaning up ZIP file..."
    rm chroma_index.zip

    echo "✅ Chroma index ready in $CHROMA_DIR"
fi

echo "🚀 Launching Flask app..."
python app.py
