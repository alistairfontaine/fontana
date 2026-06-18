import subprocess
import os
from tokenizer import FontanaTokenizer

class FontanaTrainerLink:
    def __init__(self):
        self.tokenizer = FontanaTokenizer()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Target our newly compiled high-speed C++ trainer binary
        self.trainer_path = os.path.join(os.path.dirname(script_dir), "backend", "trainer_binary")

    def train_on_text(self, training_text: str):
        print(f"[FONTANA O³] Ingesting training text: '{training_text}'")

        # 1. Transform raw text into compressed subword ID arrays
        token_ids = self.tokenizer.encode(training_text)

        # 2. Map everything to clean string argument lists for the Linux terminal
        string_args = list(map(str, token_ids))

        print(f"[DEBUG] Feeding token sequences to C++ trainer: {string_args}")

        # 3. Fire up the C++ trainer binary as a background subprocess, passing the token IDs
        try:
            result = subprocess.run(
                [self.trainer_path] + string_args,
                capture_output=True,
                text=True,
                check=True
            )
            print(result.stdout)
            if result.stderr:
                print(f"[C++ TRAINER WARNING]: {result.stderr}")

        except subprocess.CalledProcessError as e:
            print(f"[PIPELINE ERROR]: C++ trainer process execution failed. Details: {e}")
            if e.output:
                print(f"Trainer Output: {e.output}")

if __name__ == "__main__":
    link = FontanaTrainerLink()

    # Let's feed Fontana a training sentence to teach it to link syllables together!
    link.train_on_text("the fontana system code is loading logic tech")
