import os
import subprocess
from tokenizer import FontanaTokenizer

class FontanaTrainerLink:
    def __init__(self):
        self.tokenizer = FontanaTokenizer()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.project_root = os.path.dirname(script_dir)
        # Target your optimized C++ training binary cleanly on your partition paths
        self.trainer_path = os.path.join(self.project_root, "backend", "trainer_optimized_binary")
        self.token_file_path = os.path.join(script_dir, "training_tokens.txt")

    def train_on_text(self, training_text: str):
        print(f"[FONTANA O³] Ingesting training text: '{training_text}'")

        if not os.path.exists(self.trainer_path):
            return "[ERROR] C++ trainer matrix binary executable file missing!"

        # 1. Transform raw text into optimized subword ID arrays via your 108-line regex tokenizer
        token_ids = self.tokenizer.encode(training_text)
        token_string = " ".join(map(str, token_ids))

        print(f"[DEBUG] Feeding token sequences to C++ trainer: {token_ids}")

        try:
            # 2. FIXED: Write the scratchpad file to disk to satisfy the hardcoded C++ ifstream bounds
            with open(self.token_file_path, "w", encoding="utf-8") as token_f:
                token_f.write(token_string)

            # 3. Invoke the C++ trainer binary as an isolated execution pass (no parameters passed in argv)
            result = subprocess.run(
                [self.trainer_path],
                capture_output=True,
                text=True,
                check=True
            )

            if result.stdout:
                print(f"[C++ TRAINER OUTPUT]: {result.stdout.strip()}")
            if result.stderr:
                print(f"[C++ TRAINER WARNING]: {result.stderr.strip()}")

            # 4. Clean up the scratchpad file instantly to keep your folder paths unpolluted
            if os.path.exists(self.token_file_path):
                os.remove(self.token_file_path)

            return f"[SUCCESS] Matrix weight fields adjusted permanently."

        except subprocess.CalledProcessError as e:
            if os.path.exists(self.token_file_path):
                os.remove(self.token_file_path)
            print(f"[PIPELINE ERROR]: C++ trainer process execution failed. Details: {e}")
            return f"[ERROR] C++ Trainer failure: {str(e)}"
        except Exception as e:
            if os.path.exists(self.token_file_path):
                os.remove(self.token_file_path)
            return f"[ERROR] Pipeline Break: {str(e)}"

if __name__ == "__main__":
    link = FontanaTrainerLink()
    link.train_on_text("the fontana system code is loading logic tech")
