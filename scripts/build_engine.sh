#!/bin/bash

# --- FONTANA AUTOMATED COMPILER & PIPELINE EXECUTION TOOL ---
# Ensures absolute Order of Operations (O³) when updating our hybrid system

echo "=================================================="
echo "🧭 [FONTANA BUILD] Initializing Engine Assembler..."
echo "=================================================="

# 1. Navigate to the project root directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT" || exit

# 2. Clean out old binary builds to prevent cached data clutter
if [ -f "backend/tensor_engine_binary" ]; then
    echo "[1/4] [CLEANUP] Removing outdated binary executable..."
    rm backend/tensor_engine_binary
fi

# 3. Trigger the C++ compiler manually with strict architecture flags
echo "[2/4] [COMPILING] Baking raw C++ code into machine binaries..."
g++ -std=c++17 backend/tensor_engine.cpp -o backend/tensor_engine_binary

# 4. Check if the compilation was successful
if [ $? -eq 0 ]; then
    echo "[3/4] [SUCCESS] C++ backend compiled cleanly with zero errors."
    echo "=================================================="
    echo "🚀 [4/4] [EXECUTION] Launching Fontana Master Brain..."
    echo "=================================================="
    # Fire up the Python wrapper pipeline directly
    python3 core/fontana_brain.py
else
    echo "❌ [ERROR] C++ compilation failed. Inspect compiler logs above."
    exit 1
fi
