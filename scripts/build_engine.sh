#!/bin/bash

echo "=================================================="
echo "🧭 [FONTANA BUILD] Initializing Engine Assembler..."
echo "=================================================="

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT" || exit

if [ -f "backend/tensor_engine_binary" ]; then
    echo "[1/4] [CLEANUP] Removing outdated binary executable..."
    rm backend/tensor_engine_binary
fi

echo "[2/4] [COMPILING] Baking raw C++ code into machine binaries..."
# Compile the execution brain, standard trainer, and our new stride loader
g++ -std=c++17 backend/tensor_engine.cpp -o backend/tensor_engine_binary
g++ -std=c++17 backend/train.cpp -o backend/trainer_binary
g++ -std=c++17 backend/train_optimized.cpp -o backend/trainer_optimized_binary

if [ $? -eq 0 ]; then
    echo "[3/4] [SUCCESS] C++ backend compiled cleanly with zero errors."
    echo "=================================================="
    echo "🚀 [4/4] [EXECUTION] Launching Fontana Background Daemon..."
    echo "=================================================="

    # FIXED: MILESTONE 1 DAEMON ENGINE LAUNCHER
    # Spawn the C++ process directly into your RAM background tracks using the Linux ampersand operator.
    # This prevents the terminal prompt line from freezing!
    ./backend/tensor_engine_binary &
else
    echo "❌ [ERROR] C++ compilation failed. Inspect compiler logs above."
    exit 1
fi
