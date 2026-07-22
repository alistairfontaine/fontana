 <img src="assets/logo.png" alt="THE FONTANA AI ENGINE CORE" width="100%">

# 🧭 The Fontana Engine Core (v4.6)
### An AuDHD-Optimized Hybrid C++/FastAPI Real-Time Neural Text Synthesis & Screenplay Architecture

Built by **Alistair Fontaine** in Bulawayo, Zimbabwe [context].

The Fontana Engine Core is a high-performance, hybrid-language neural text synthesis platform engineered specifically to eliminate corporate abstraction, maximize information density, and enforce an absolute, step-by-step **Order of Operations (O³)**. Built with a strict focus on memory safety, defensive coding protocols, and persistent background process isolation, this framework contains no massive commercial engine wrappers or black-box APIs—every weight matrix forward pass, subword syllable matching lookup, and stateful lookback context array stream is manually written, mapped, and compiled natively.

---

## 🛠️ The Ultimate Rescue Compilation Chain
If the runtime ever scrambles, cross-origin network queries deadlock, or unexpected subprocess errors try to freeze your workspace, execute this exact unbroken production pipeline string directly inside your Linux shell terminal to force a clean cache swap, re-allocate the socket lines, and deploy the safe engine baseline:

```bash
pkill -f tensor_engine_binary && pkill -f uvicorn && fuser -k 8000/tcp && fuser -k 8080/tcp && g++ -std=c++17 backend/tensor_engine.cpp -o backend/tensor_engine_binary && export PYTHONPATH=PYTHONPATH:(pwd)/core && python3 -m uvicorn core.app:app --host 127.0.0.1 :8000 --reload
```

---

## 🚀 Completed Milestones & Architectural Core

### 1. Hybrid Cross-Language Ingestion Architecture
- **Persistent Subprocess Background Daemon:** Boots your ultra-fast compiled C++ engine core once into volatile RAM cache storage tracks via long-lived asynchronous `subprocess.Popen` pipelines, keeping the neural parameters hot and responsive for sub-millisecond thread execution.
- **Asynchronous REST API Gateway:** Full FastAPI network abstraction layer utilizing non-blocking asynchronous event loops to pipe JSON telemetry tokens cleanly back and forth over local loopback ports.

### 2. High-Density Subword Syllable Tokenization
- **108-Line Regex BPE Pattern Matcher:** Independent implementation of a syllable-aware subword extraction utility. Uses optimized sorting regular expressions to look for custom structural screenplay blocks (like `fontana`, `istair`, `brain`, `logic`, `code`, `system`) and fuse them natively on startup to prevent character-splitting stutter noise loops.

### 3. Stateful Long-Range Sequence Calibration
- **Softmax Matrix Probability Scaling:** Fine-tuned activation layers inside `backend/tensor_engine.cpp` with a fluid long-range temperature floor scaling between `0.05f` and `1.00f` to provide natural creative entropy breathing space and crush transitional character static.
- **Broadened Selection Pool Truncation:** Expands token lookahead pathways via customized `Top-K` and `Top-P` selection filter gates, normalizing the discrete probability distribution pools directly inside standard template vector maps.

### 4. Stateful Session Memory & Brutalist Command Workspace
- **Rolling Context Lookback History Buffer:** Stateful array caches running inside `core/app.py` that intercept your prompt streams, bundle the last 3 generated sentences dynamically, and feed them back down the pipe to enable deep, continuous, multi-page screenplay scene construction.
- **Multi-Tenant Memory Sandboxing:** Full dictionary isolation mapping rows keyed to unique, incoming session payload tokens (`session_id`), allowing completely separate characters or screenplay threads to execute in parallel inside system memory without state pollution or data cross-talk [context].
- **Brutalist Antagonist vs. Opium Web UI Vault:** High-contrast minimalist frontend interface featuring a non-blocking class-based hot-swapper to flip between **Antagonist Green (`#00ff66`)** and **Opium Crimson Red (`#ff0055`)** inside Firefox with a single mouse click.
- **One-Click Markdown Scenario Exporter:** Integrated JavaScript file pipeline handler that captures your live generation logs, packages them into structured screenplay markdown files (`.md`), and automatically triggers local browser downloads on impact lock.

### 5. Live Hardware Vector & Performance Telemetry Trackers
- **Real-Time ASCII Status Dashboard:** Parses dynamic neural parameter returns and pipes them into a dedicated container panel layout inside Firefox, tracking active token paths and hidden unit layer configurations on every pass.
- **Dynamic Vector Magnitude Graph Bars:** Converts live raw token ID matrices into responsive visual CSS flex indicator blocks that paint heights dynamically to visually chart data magnitude changes inside system memory.
- **Monotonic Hardware Clock Tracker:** Captures microsecond execution latency deltas (`time.perf_counter()`) across the C++ IPC pipe line to display live computational velocity benchmarks on your dashboard in real-time.

---

## 📂 Core Documentation Map

- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — The technical nitty-gritty specifications detailing how Fontana was constructed from absolute flat zero variables.
- [`docs/ROADMAP.md`](docs/ROADMAP.md) — Chronological history tracking where our architecture came from, where we are sitting, and our unpolluted future parameters.
- [`docs/VISION.md`](docs/VISION.md) — The fundamental philosophy, target purpose, and systemic Tao of Fontana.

## 🔧 Build Requirements & Infrastructure

### Core Stack
- **Languages:** Modern C++17 & Python 3.12+
- **Network Application Server:** FastAPI & Uvicorn (StatReload Profile Enabled)
- **Local Interface Gateway:** Firefox Web Browser Module
- **Operating Environment:** Linux Storage Partition Environment (Debian/Ubuntu Core)

### System Package Setup (Debian/Ubuntu Linux Partition)
```bash
sudo apt-get update
sudo apt-get install build-essential python3-pip python3-fastapi uvicorn curl
```
