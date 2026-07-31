# 📕 UNIVERSAL USER CONTROL PANEL MANUAL // OPERATIONAL BLUEPRINT

## 1. Local Environment Deployment Sequence
To initialize the uncompromised hybrid cross-language architecture natively on your Linux partition storage drive, open your shell terminal console environment and execute these commands inside separate tab windows:

### Terminal Tab 1: Recompile the Native Inference Core
```bash
cd /media/mr-fontaine/R/RECOVERY/Coding/fontana
g++ -std=c++17 backend/tensor_engine.cpp -o backend/tensor_engine_binary
```

### Terminal Tab 2: Deploy the FastAPI Gateway
```bash
cd /media/mr-fontaine/R/RECOVERY/Coding/fontana
export PYTHONPATH=PYTHONPATH:(pwd)/core && python3 -m uvicorn core.app:app --host 127.0.0.1 --port 8000 --reload
```

### Terminal Tab 3: Launch the Front-End Control Panel
```bash
cd /media/mr-fontaine/R/RECOVERY/Coding/fontana/core
python3 -m http.server 8080
```

---

## 2. Managing the Multi-Parametric Input Sliders

The Stochastic Synthesis panel provides real-time mathematical authority straight over the compiled C++ activation layers. Adjust these parameters to change the linguistic trajectory of the model:

### A. Softmax Probability Temperature Slider
- **Range Bounds:** `0.05` to `1.00`
- **Behavior Mapping:** Dropping the slider value near zero (`0.05` - `0.15`) strips away entropy, forcing the C++ engine to compute with near-perfect deterministic certainty, selecting only the highest-frequency baseline training tokens. Scaling the slider upward (`0.60` - `0.95`) introduces structural entropy, fracturing the sentences into highly creative, unpredictable long-range screenplays.

### B. Top-K Probability Pool Filter Slider
- **Range Bounds:** `1` to `25` active token selection choices.
- **Behavior Mapping:** Constrains the selection horizon to the top $N$ most probable tokens. Lowering this limits choice paths, while raising it lets the model pull from a broader pool of vocabulary vectors.

### C. Nucleus Sampling Top-P Boundary Slider
- **Range Bounds:** `0.10` to `1.00` percentage gates.
- **Behavior Mapping:** Truncates the cumulative probability distribution matrix. The model dynamically tracks sorting structures and cuts off all candidate tokens the exact millisecond their combined weight crosses your specified threshold, slicing away low-probability noise patterns.
