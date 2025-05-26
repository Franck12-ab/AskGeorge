#!/bin/bash

CHROMA_DIR="chroma_index"

echo "📦 Checking for Chroma index in ./$CHROMA_DIR..."
if [ -d "$CHROMA_DIR" ]; then
    echo "✅ Chroma index exists."
fi

echo "🚀 Launching Flask app..."
python app.py


