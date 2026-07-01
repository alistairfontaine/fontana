import os
from tokenizer import FontanaTokenizer
from fontana_brain import FontanaBrain

class FontanaGenerator:
    def __init__(self):
        self.tokenizer = FontanaTokenizer()
        self.brain = FontanaBrain()

    def generate_text(self, seed_text: str, max_new_tokens: int = 40):
        print(f"[FONTANA LOGIC] Ingesting Seed text stream: '{seed_text}'")
        current_text = seed_text

        print("[FONTANA STOCHASTIC RUN]: ", end="", flush=True)
        print(seed_text.strip(), end="", flush=True)

        suffixes = ["ing", "tion", "ent", "yst", "sta", "ook", "ine", "tio", "ste"]

        for _ in range(max_new_tokens):
            token_ids = self.tokenizer.encode(current_text)
            token_string = " ".join(map(str, token_ids))

            # Communicate instantly with our active RAM daemon via the IPC pipeline
            stdout_output = self.brain.submit_prompt(token_string)

            if "[ERROR]" in stdout_output:
                print(f"\n{stdout_output}")
                break

            try:
                predicted_id = int(stdout_output.strip())

                # Stop-Token Filter Gates
                if predicted_id == 0 or predicted_id == 1 or predicted_id == 2:
                    break

                if predicted_id == self.tokenizer.vocab["[EOS]"]:
                    print(" [EOS]", end="", flush=True)
                    break

                predicted_char = self.tokenizer.inverse_vocab.get(predicted_id, "")

                # Linguistic Post-Processor Spacing Filters
                if predicted_char.strip() and not any(predicted_char.startswith(s) for s in suffixes):
                    if not current_text.endswith(" "):
                        print(" ", end="", flush=True)
                        current_text += " "

                print(predicted_char, end="", flush=True)
                current_text += predicted_char

            except ValueError:
                break

        print("\n\n[FONTANA SYSTEM] Text auto-generation cycle complete.")

if __name__ == "__main__":
    generator = FontanaGenerator()
    generator.generate_text("Fontana ", max_new_tokens=40)
