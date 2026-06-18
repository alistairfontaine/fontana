import subprocess
import os
import random
from tokenizer import FontanaTokenizer

class FontanaGenerator:
    def __init__(self):
        self.tokenizer = FontanaTokenizer()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.backend_path = os.path.join(os.path.dirname(script_dir), "backend", "tensor_engine_binary")

    def generate_text(self, seed_text: str, max_new_tokens: int = 25):
        print(f"[FONTANA LOGIC] Ingesting Seed text stream: '{seed_text}'")
        current_text = seed_text

        print("[FONTANA SYNTHESIS RUN]: ", end="", flush=True)
        print(seed_text, end="", flush=True)

        last_predicted_id = None

        for _ in range(max_new_tokens):
            token_ids = self.tokenizer.encode(current_text)
            token_string = " ".join(map(str, token_ids))

            process = subprocess.Popen(
                [self.backend_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            stdout_output, _ = process.communicate(input=token_string)

            try:
                predicted_id = int(stdout_output.strip())

                # FIXED: True Loop-Breaker. If the model gets stuck repeating the exact same token block,
                # we force a temporary random exploration drift to shift the context matrix windows.
                if predicted_id == last_predicted_id:
                    vocab_pool = list(self.tokenizer.vocab.values())
                    # Select from our multi-letter subwords pool to inject syllable diversity
                    predicted_id = random.choice(vocab_pool[76:])

                last_predicted_id = predicted_id

                if predicted_id == self.tokenizer.vocab["[EOS]"]:
                    break

                predicted_char = self.tokenizer.inverse_vocab.get(predicted_id, "")
                print(predicted_char, end="", flush=True)

                current_text += predicted_char

            except ValueError:
                break

        print("\n\n[FONTANA SYSTEM] Text auto-generation cycle complete.")

if __name__ == "__main__":
    generator = FontanaGenerator()
    generator.generate_text("Fontana", max_new_tokens=25)
