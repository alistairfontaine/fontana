#!/bin/bash

# --- FONTANA PROFILE OPTIMIZATION & WEIGHT MANAGEMENT TOOL ---
# Enforces clean file operations across our local 30GB partition sandbox

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT" || exit

echo "=================================================="
echo "🧭 [FONTANA OPTIMIZE] Initializing File Management Pipeline..."
echo "=================================================="

# 1. Ask the developer for a profile backup name
echo -n "Enter backup profile suffix (e.g., screenplay, tech, baseline): "
read -r PROFILE_NAME

if [ -z "$PROFILE_NAME" ]; then
    PROFILE_NAME="default_backup"
fi

# 2. Check if current model weights exist and create an optimized local backup folder
if [ -f "fontana_weights.bin" ]; then
    echo "[1/4] [BACKUP] Stash-saving current weights matrix configuration..."
    mkdir -p weights_backup
    cp fontana_weights.bin "weights_backup/fontana_weights_${PROFILE_NAME}.bin"
    cp fontana_embeddings.bin "weights_backup/fontana_embeddings_${PROFILE_NAME}.bin"
    echo "      ✓ Saved to: weights_backup/fontana_weights_${PROFILE_NAME}.bin"
else
    echo "[1/4] [STATUS] No active weights binary detected. Skipping backup."
fi

# 3. Clean and purge active binary cache memory frames to open up partition space
echo "[2/4] [PURGE] Clearing active memory runtime files..."
rm -f fontana_weights.bin fontana_embeddings.bin

# 4. Re-run bulk dataset instruction paths to bake a fresh clean matrix
echo "[3/4] [TRAINING] Triggering fresh dataset ingestion pipeline..."
python3 core/train_dataset.py

if [ $? -eq 0 ]; then
    echo "=================================================="
    echo "🌟 [4/4] [SUCCESS] System optimized. Fontana is fresh."
    echo "=================================================="
else
    echo "❌ [ERROR] Dataset retraining failed. Inspect pipeline logs."
    exit 1
fi
