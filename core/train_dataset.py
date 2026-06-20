import subprocess
import os
import sys
from tokenizer import FontanaTokenizer

class FontanaDatasetTrainer:
    def __init__(self):
        self.tokenizer = FontanaTokenizer()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.project_root = os.path.dirname(script_dir)
        self.trainer_path = os.path.join(self.project_root, "backend", "trainer_optimized_binary")
        self.dataset_path = os.path.join(self.project_root, "dataset.txt")
        # FIXED: Zero-cost file stream scratchpad link channel
        self.token_file_path = os.path.join(script_dir, "training_tokens.txt")

    def run_file_ingestion(self, epochs: int = 5):
        print("==================================================")
        print(f"🧭 [FONTANA TRAINING] Ingesting File: '{self.dataset_path}'")
        print("==================================================")

        if not os.path.exists(self.dataset_path):
            return

        with open(self.dataset_path, "r", encoding="utf-8") as f:
            raw_data = f.read().strip()

        if not raw_data:
            return

        print(f"[PROCESS] Compressing corpus into subword tokens...")
        token_ids = self.tokenizer.encode(raw_data)

        print(f"[STATUS] Corpus compiled into {len(token_ids)} active tokens.")

        # FIXED: Stream token IDs down onto the drive partition file to bypass Linux ARG_MAX buffer limits permanently
        with open(self.token_file_path, "w", encoding="utf-8") as token_f:
            token_f.write(" ".join(map(str, token_ids)))
        print(f"[SUCCESS] Streaming index links written to scratchpad.")

        for epoch in range(1, epochs + 1):
            print(f"\n🚀 [EPOCH {epoch}/{epochs}] Launching High-Speed File-Stream Matrix Pass...")

            try:
                # Subprocess call remains simple and empty of heavy shell string inputs
                result = subprocess.run(
                    [self.trainer_path],
                    capture_output=True,
                    text=True,
                    check=True
                )
                print(result.stdout.strip())

            except subprocess.CalledProcessError as e:
                print(f"❌ [PIPELINE FAILURE] Epoch {epoch} crashed. Details: {e}")
                if e.output:
                    print(f"C++ Logs: {e.output}")
                break

        # Clean up the local data scratchpad file securely after training complete
        if os.path.exists(self.token_file_path):
            os.remove(self.token_file_path)

        print("\n==================================================")
        print("🌟 [FONTANA SYSTEM] Bulk Dataset Training Complete.")
        print("==================================================")

if __name__ == "__main__":
    trainer = FontanaDatasetTrainer()
    trainer.run_file_ingestion(epochs=5)
