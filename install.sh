#!/bin/bash

set -e

echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "📥 Setting up Chroma index..."

mkdir -p chroma_index

if [ ! -f "chroma_index/chroma.sqlite3" ]; then
    echo "📥 Downloading prebuilt Chroma index ZIP..."
    curl -L "https://www.dropbox.com/scl/fi/twth9kyz7qpdxwh3qxplc/chroma_index.zip?rlkey=22ndkbo7aoslblwqakhp4avkb&dl=1" -o chroma_index.zip
    unzip -q chroma_index.zip -d .
    rm chroma_index.zip
    echo "✅ Chroma index ready."
else
    echo "✅ Chroma index already exists. Skipping download."
fi
