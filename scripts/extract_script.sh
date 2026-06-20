#!/bin/bash

# --- FONTANA MULTI-SOURCE DATASET HARVESTER PIPELINE ---
# Extracts and flattens PDF screenplays and raw TXT novels into our local sandbox partition

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE}")/.." && pwd)"
cd "$PROJECT_ROOT" || exit

echo "=================================================="
echo "🧭 [FONTANA INGEST] Initializing Multi-Source Parser..."
echo "=================================================="

# Process Screenplay 1
if [ -f "screenplay.pdf" ]; then
    echo "[1/5] [PARSING] Processing Primary Screenplay..."
    pdftotext screenplay.pdf raw_script1.txt
    cat raw_script1.txt | tr '[:upper:]' '[:lower:]' | tr -d '#*`\-\[\]\(\)\{\}\=\_\:\;\/\n' | tr -s ' ' >> dataset.txt
    rm raw_script1.txt
fi

# Process Screenplay 2
if [ -f "screenplay2.pdf" ]; then
    echo "[2/5] [PARSING] Processing Secondary Screenplay..."
    pdftotext screenplay2.pdf raw_script2.txt
    cat raw_script2.txt | tr '[:upper:]' '[:lower:]' | tr -d '#*`\-\[\]\(\)\{\}\=\_\:\;\/\n' | tr -s ' ' >> dataset.txt
    rm raw_script2.txt
fi

# Process Classic Novel 1 (Frankenstein)
if [ -f "novel1.txt" ]; then
    echo "[3/5] [PARSING] Processing Classic Novel 1 (Frankenstein)..."
    cat novel1.txt | tr '[:upper:]' '[:lower:]' | tr -d '#*`\-\[\]\(\)\{\}\=\_\:\;\/\n' | tr -s ' ' >> dataset.txt
fi

# Process Classic Novel 2 (Dracula)
if [ -f "novel2.txt" ]; then
    echo "[4/5] [PARSING] Processing Classic Novel 2 (Dracula)..."
    cat novel2.txt | tr '[:upper:]' '[:lower:]' | tr -d '#*`\-\[\]\(\)\{\}\=\_\:\;\/\n' | tr -s ' ' >> dataset.txt
    echo " . " >> dataset.txt
fi

echo "=================================================="
echo "🚀 [5/5] [VOCAB EXPANSION] Regenerating Self-Evolving Vocabulary Map..."
python3 core/expand_vocab.py

echo "=================================================="
echo "🌟 [SUCCESS] All Screenplays and Novels Unified."
echo "=================================================="
