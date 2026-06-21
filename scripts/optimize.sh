#!/bin/bash

# --- FONTANA ARCHITECTURE WORKSPACE OPTIMIZER & PERMANENT PROFILE STASHER ---
# Automates matrix generation, structural weight alignment, and dynamic profile stashing

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT" || exit

echo "=================================================="
echo "🧭 [FONTANA OPTIMIZE] Initializing Safe File Management Pipeline..."
echo "=================================================="

# 1. Capture target backup label assignment metrics
read -p "Enter backup profile suffix (e.g., screenplay, tech, baseline): " PROFILE_NAME

if [ -z "$PROFILE_NAME" ]; then
    echo "❌ [ERROR] Profile name suffix cannot be blank! Aborting pipeline."
    exit 1
fi

BACKUP_DIR="weights_backup"
mkdir -p "$BACKUP_DIR"

# 2. Clear un-stashed transient matrix caches from root folder safely
echo "[1/4] [PURGE] Clearing active memory runtime files..."
rm -f fontana_weights.bin fontana_embeddings.bin

# 3. Launch python tokenization compression and training matrix layers pass
echo "[2/4] [TRAINING] Triggering fresh dataset ingestion pipeline..."
python3 core/train_dataset.py

if [ $? -ne 0 ]; then
    echo "❌ [ERROR] Dataset retraining failed! Aborting stasher pass."
    exit 1
fi

# 4. FIXED: Force-Initialize Aligned High-HD Embeddings File Automatically
echo "[3/4] [ALIGNMENT] Forcing 512-dimensional embedding map initialization..."
if [ ! -f "fontana_embeddings.bin" ]; then
    # Stream a dummy baseline context string to the execution brain binary to drop a clean file onto disk
    echo "2 3 4" | ./backend/tensor_engine_binary > /dev/null 2>&1
fi

# 5. FIXED: Automated Stashing. Duplicate both files cleanly to the backup storage partition pools
echo "[4/4] [STASHING] Freezing parameters to weights_backup/..."
if [ -f "fontana_weights.bin" ] && [ -f "fontana_embeddings.bin" ]; then
    cp fontana_weights.bin "${BACKUP_DIR}/fontana_weights_${PROFILE_NAME}.bin"
    cp fontana_embeddings.bin "${BACKUP_DIR}/fontana_embeddings_${PROFILE_NAME}.bin"

    echo "=================================================="
    echo "🌟 [SUCCESS] System fully optimized and stashed!"
    echo "             Profile Layer: '${PROFILE_NAME^^}' is live on disk."
    echo "=================================================="
else
    echo "❌ [CRITICAL ERROR] Failed to capture output files in root directory!"
    exit 1
fi
