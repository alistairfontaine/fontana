import subprocess
import os
import sys
from tokenizer import FontanaTokenizer

class FontanaBrain:
    def __init__(self):
        self.tokenizer = FontanaTokenizer()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.project_root = os.path.dirname(script_dir)
        self.backend_path = os.path.join(self.project_root, "backend", "tensor_engine_binary")

    def submit_prompt(self, prompt_text: str):
        if not os.path.exists(self.backend_path):
            print(f"[CRITICAL] Error: The C++ binary does not exist at: {self.backend_path}")
            return

        token_ids = self.tokenizer.encode(prompt_text)
        token_string = " ".join(map(str, token_ids))

        # Invoke the C++ tensor engine binary via standard subprocess pipelines safely
        process = subprocess.Popen(
            [self.backend_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        stdout_output, stderr_output = process.communicate(input=token_string)

        if process.returncode == 0:
            try:
                predicted_id = int(stdout_output.strip())
                predicted_char = self.tokenizer.inverse_vocab.get(predicted_id, "[UNK]")
                return predicted_char
            except ValueError:
                return "[ERROR] Invalid numeric output from C++ backend."
        else:
            return f"[ERROR] Subprocess crash. Details: {stderr_output.strip()}"

if __name__ == "__main__":
    print("[DEBUG] Looking for C++ binary at:", os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend", "tensor_engine_binary"))
    brain = FontanaBrain()
    # High-context alignment validation signature prompt
    prompt = "Alistair Fontaine is mapping out logic structures."
    print(f"[FONTANA BRAIN] Submitting prompt: '{prompt}'")

    # Generate token string for debugging metrics visualization
    tokenizer = FontanaTokenizer()
    t_ids = tokenizer.encode(prompt)
    print(f"[DEBUG] Sending token string to C++: {' '.join(map(str, t_ids))}")

    print("[DEBUG] --- C++ Output Begins ---")
    next_char = brain.submit_prompt(prompt)
    print(next_char)
    print("[DEBUG] --- C++ Output Ends ---")
