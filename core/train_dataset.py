import subprocess
import os
import sys
from tokenizer import FontanaTokenizer

class FontanaDatasetTrainer:
    def __init__(self):
        self.tokenizer = FontanaTokenizer()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.project_root = os.path.dirname(script_dir)
        self.trainer_path = os.path.join(self.project_root, "backend", "trainer_binary")
        self.dataset_path = os.path.join(self.project_root, "dataset.txt")

    def run_file_ingestion(self, epochs: int = 5):
        print("==================================================")
        print(f"🧭 [FONTANA TRAINING] Ingesting File: '{self.dataset_path}'")
        print("==================================================")

        if not os.path.exists(self.dataset_path):
            print(f"[CRITICAL ERROR] dataset.txt not found at: {self.dataset_path}")
            return

        # 1. Read the raw text data from your storage drive partition
        with open(self.dataset_path, "r", encoding="utf-8") as f:
            raw_data = f.read().strip()

        if not raw_data:
            print("[WARNING] Dataset file is completely empty.")
            return

        # 2. Tokenize the entire raw text corpus into structural subword array IDs
        print(f"[PROCESS] Compressing corpus into subword tokens...")
        token_ids = self.tokenizer.encode(raw_data)
        string_args = list(map(str, token_ids))

        print(f"[STATUS] Corpus compiled into {len(token_ids)} active tokens.")

        # 3. Training Loop Epochs: Feed the tokens repeatedly to sharpen the weight associations
        for epoch in range(1, epochs + 1):
            print(f"\n🚀 [EPOCH {epoch}/{epochs}] Launching C++ Matrix Optimization Pass...")

            try:
                # Trigger the compiled C++ binary, passing the full token token arguments list
                result = subprocess.run(
                    [self.trainer_path] + string_args,
                    capture_output=True,
                    text=True,
                    check=True
                )
                # Output the C++ console logs directly
                print(result.stdout.strip())

            except subprocess.CalledProcessError as e:
                print(f"❌ [PIPELINE FAILURE] Epoch {epoch} crashed. Details: {e}")
                if e.output:
                    print(f"C++ Logs: {e.output}")
                break

        print("\n==================================================")
        print("🌟 [FONTANA SYSTEM] Bulk Dataset Training Complete.")
        print("==================================================")

if __name__ == "__main__":
    trainer = FontanaDatasetTrainer()
    # Run a fast 5-epoch training optimization loop
    trainer.run_file_ingestion(epochs=5)
