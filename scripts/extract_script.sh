#!/bin/bash

# --- FONTANA PURE LIT-STREAM DATASET HARVESTER PIPELINE ---
# Extracts and flattens PDF screenplays and unpolluted EPUB novels into our local sandbox

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE}")/.." && pwd)"
cd "$PROJECT_ROOT" || exit

echo "=================================================="
echo "🧭 [FONTANA INGEST] Initializing Pure Ingestion Parser..."
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

# Process Classic Novel 1 (Frankenstein EPUB)
if [ -f "novel1.epub" ]; then
    echo "[3/5] [PARSING] Processing Frankenstein EPUB (Stripping Content Clutter)..."
    python3 -c "
import zipfile, re
with zipfile.ZipFile('novel1.epub') as z:
    for f in z.namelist():
        if f.endswith(('html', 'xhtml')):
            text = z.read(f).decode('utf-8', errors='ignore')
            clean = re.sub(r'<[^>]+>', ' ', text) # Strip HTML tags completely
            print(clean)
" | tr '[:upper:]' '[:lower:]' | tr -d '#*`\-\[\]\(\)\{\}\=\_\:\;\/\n' | tr -s ' ' >> dataset.txt
fi

# Process Classic Novel 2 (Dracula EPUB)
if [ -f "novel2.epub" ]; then
    echo "[4/5] [PARSING] Processing Dracula EPUB (Stripping Content Clutter)..."
    python3 -c "
import zipfile, re
with zipfile.ZipFile('novel2.epub') as z:
    for f in z.namelist():
        if f.endswith(('html', 'xhtml')):
            text = z.read(f).decode('utf-8', errors='ignore')
            clean = re.sub(r'<[^>]+>', ' ', text) # Strip HTML tags completely
            print(clean)
" | tr '[:upper:]' '[:lower:]' | tr -d '#*`\-\[\]\(\)\{\}\=\_\:\;\/\n' | tr -s ' ' >> dataset.txt
    echo " . " >> dataset.txt
fi

echo "=================================================="
echo "🚀 [5/5] [VOCAB EXPANSION] Regenerating Self-Evolving Vocabulary Map..."
python3 core/expand_vocab.py

echo "=================================================="
echo "🌟 [SUCCESS] Screenplays and Unpolluted Novels Completely Unified."
echo "=================================================="
