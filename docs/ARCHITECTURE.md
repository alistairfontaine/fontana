# 📂 TECHNICAL SPECIFICATIONS // ARCHITECTURE VIEW [v4.7 AUDITED]

## 1. Low-Level Core Foundations (The Skeletal Layer)
The Fontana AI Engine's native engine block is constructed in pure modern C++17 (`backend/tensor_engine.cpp`), establishing a zero-overhead execution environment compiled directly to native x86 machine code. By utilizing standard template library arrays (`std::vector`) and non-blocking streaming channels, the backend acts as a highly optimized matrix math processor.

### Data Storage & Initialization Layers
- **Embedding Matrix Representation:** Accommodates high-dimensional vector representations (`512-HD Spatial Tensors`) across an allocated discrete index space of unique subword symbols. Parameters are stored in un-throttled binary streams (`fontana_weights.bin` and `fontana_embeddings.bin`) and loaded into RAM arrays via low-level binary input streams (`std::ifstream::read`).
- **Numerically Stable Activation Mechanics [PR #2 Patched]:** Leverages an industry-standard Max-Logit Subtraction Softmax layer to transform unnormalized prediction scores (`raw_scores`) into discrete probability spaces. By isolating the maximum logit value and subtracting it from every element prior to computing the exponent, the exponents are mathematically guaranteed to stay ≤ 0.0f, keeping values locked between `0.0f` and `1.0f` and completely eliminating floating-point register overflows to positive infinity (`+inf`) or `NaN` deadlocks:

\[P(x_i) = \frac{e^{\frac{S_i - S_{max}}{T}}}{\sum_{j} e^{\frac{S_j - S_{max}}{T}}}\]

---

## 2. The Interprocess Communication Loop (The Nervous Bridge)
Rather than spawning short-lived, high-overhead command executions that stall the CPU, Fontana relies on a long-lived, persistent background subprocess daemon model.

### The Stdin/Stdout Non-Blocking Stream Pipe
- **Python Bridge Initialization:** The orchestration wrapper (`core/fontana_brain.py`) utilizes asynchronous pipe allocations (`subprocess.Popen`) to permanently grab input and output handles of the hot C++ executable.
- **Multi-Parametric Pipe Line Delimitation [PR #4 Patched]:** Data strings pass across system buffers using specialized pipe characters as string bounds delimiters, passing raw tokens alongside user slider metrics dynamically:
  ```text
  [TOKEN_IDS_ARRAY_STRING] | [TEMPERATURE_FLOAT] | [TOP_K_INT] | [TOP_P_FLOAT]
  ```
- **C++ Multi-Parametric Parser [Phase O Conquered]:** The compiled binary utilizes high-integrity string stream segment extraction tools (`std::stringstream` and `std::getline`) with separate, independent string variables (`temp_part`, `topk_part`, `topp_part`) to isolate values natively without stalling the read thread or triggering input type mismatch deadlocks.

---

## 3. High-Density Tokenization & Memory Sandboxing (The Soft Tissue)
Linguistic matching is decoupled from standard word boundaries to prevent vocabulary fragmentation.

### The Syllable-Aware Extraction Utility [PR #1 & PR #3 Patched]
- **De-duplicated Vocabulary Index Mapping:** Strict dictionary building constraints inside `core/tokenizer.py` that filter out duplicate subwords, preventing index collisions with base characters and ensuring the final token indices do not spill over the C++ engine threshold.
- **Catch-All Data-Integrity Regex node:** Appends a single-character catch-all symbol (`.`) at the absolute tail end of the sorted patterns array and enforces `re.DOTALL` compilation masks, ensuring unknown punctuation or characters are safely routed into `[UNK]` slots instead of being silently dropped.
- **RAM-Isolated Multi-Tenant Architecture:** Converts global lookback list structures into a highly organized multi-user mapping dictionary (`SESSION_HISTORY_MAPS`). Individual channels are tracked via a unique user parameter (`session_id`). This completely isolates the context windows, allowing multiple characters to generate separate screenplay tracks simultaneously within the same system thread with absolute zero data pollution.
