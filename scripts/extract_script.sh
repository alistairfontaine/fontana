#!/bin/bash

# --- FONTANA MULTI-SCREENPLAY DATASET EXPANSION PIPELINE ---
# Extracts and flattens multiple PDF scripts safely into our 30GB partition sandbox

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE}")/.." && pwd)"
cd "$PROJECT_ROOT" || exit

echo "=================================================="
echo "🧭 [FONTANA INGEST] Initializing Multi-Script Parser..."
echo "=================================================="

# Process Screenplay 1
if [ -f "screenplay.pdf" ]; then
    echo "[1/4] [PARSING] Processing Primary Screenplay..."
    pdftotext screenplay.pdf raw_script1.txt
    cat raw_script1.txt | tr '[:upper:]' '[:lower:]' | tr -d '#*`\-\[\]\(\)\{\}\=\_\:\;\/\n' | tr -s ' ' >> dataset.txt
    rm raw_script1.txt
else
    echo "[WARNING] Primary screenplay.pdf not found. Skipping."
fi

# Process Screenplay 2
if [ -f "screenplay2.pdf" ]; then
    echo "[2/4] [PARSING] Processing Secondary Trelby Screenplay..."
    pdftotext screenplay2.pdf raw_script2.txt
    cat raw_script2.txt | tr '[:upper:]' '[:lower:]' | tr -d '#*`\-\[\]\(\)\{\}\=\_\:\;\/\n' | tr -s ' ' >> dataset.txt
    rm raw_script2.txt
    echo " . " >> dataset.txt
    echo "🌟 [SUCCESS] Secondary script integrated successfully."
else
    echo "❌ [ERROR] screenplay2.pdf not found in root folder!"
    exit 1
fi

echo "=================================================="
echo "🚀 [3/4] [VOCAB EXPANSION] Regenerating Self-Evolving Vocabulary Map..."
python3 core/expand_vocab.py

echo "=================================================="
echo "🌟 [4/4] [SUCCESS] All Screenplays Ingested and Unified."
echo "             Ready for accelerated matrix training loops!"
echo "=================================================="
