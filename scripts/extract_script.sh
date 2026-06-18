#!/bin/bash

# --- FONTANA SCREENPLAY INGESTION PREPARATION PIPELINE ---
# Extracts and cleans raw text from local PDF screenplays for dataset expansion

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE}")/.." && pwd)"
cd "$PROJECT_ROOT" || exit

echo "=================================================="
echo "🧭 [FONTANA INGEST] Initializing Screenplay Parser..."
echo "=================================================="

if [ ! -f "screenplay.pdf" ]; then
    echo "❌ [ERROR] screenplay.pdf not found in root folder!"
    exit 1
fi

echo "[1/3] [PARSING] Converting screenplay.pdf to raw text layout..."
# Convert PDF to text, preserving structural spacing layout parameters
pdftotext screenplay.pdf raw_script.txt

echo "[2/3] [CLEANING] Polishing text streams and formatting structure chunks..."
# Clean text: convert to lowercase, strip formatting noise, and normalize spaces
cat raw_script.txt | tr '[:upper:]' '[:lower:]' | tr -d '#*`\-\[\]\(\)\{\}\=\_\:\;\/\n' | tr -s ' ' > cleaned_script.txt

echo "[3/3] [APPENDING] Merging screenplay grammar blocks into active dataset.txt..."
# Append the polished script corpus text directly to your primary training file
cat cleaned_script.txt >> dataset.txt
echo " . " >> dataset.txt

# Clean up transient temporary scratchpad files to preserve your 30GB partition footprint
rm raw_script.txt cleaned_script.txt

echo "=================================================="
echo "🌟 [SUCCESS] Screenplay fully integrated into dataset.txt."
echo "             Ready for multi-epoch training passes!"
echo "=================================================="
