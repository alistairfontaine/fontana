import subprocess
import os
import sys
from tokenizer import FontanaTokenizer

class FontanaGenerator:
    def __init__(self):
        self.tokenizer = FontanaTokenizer()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.backend_path = os.path.join(os.path.dirname(script_dir), "backend", "tensor_engine_binary")

    def generate_text(self, seed_text: str, max_new_tokens: int = 10):
        print(f"[FONTANA LOGIC] Ingesting Seed: '{seed_text}'")
        current_text = seed_text

        print("[FONTANA GENERATION START]: ", end="", flush=True)
        print(seed_text, end="", flush=True)

        # The Autoregressive Loop: runs repeatedly to generate characters one-by-one
        for _ in range(max_new_tokens):
            # 1. Encode the current working text into integer lists
            token_ids = self.tokenizer.encode(current_text)
            token_string = " ".join(map(str, token_ids))

            # 2. Spin up the C++ sub-process
            process = subprocess.Popen(
                [self.backend_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # 3. Shoot current tokens into C++ and capture the single predicted response integer
            stdout_output, _ = process.communicate(input=token_string)

            try:
                # Parse the raw C++ output line into a clean integer token ID
                predicted_id = int(stdout_output.strip())

                # If the engine predicts [EOS] (End of Sentence, ID 3), break the loop cleanly
                if predicted_id == 3:
                    break

                # 4. Decode the number back into a single text character
                predicted_char = self.tokenizer.inverse_vocab.get(predicted_id, "")

                # 5. Print the character to your screen immediately with zero delay
                print(predicted_char, end="", flush=True)

                # Append the new character to our text so the loop can send it back to C++
                current_text += predicted_char

            except ValueError:
                print("\n[PROCESS ERROR] Received unstructured string data from C++ pipe.")
                break

        print("\n\n[FONTANA SYSTEM] Text auto-generation cycle complete.")

if __name__ == "__main__":
    generator = FontanaGenerator()
    # Test a live autoregressive run
    generator.generate_text("Fontana", max_new_tokens=8)
