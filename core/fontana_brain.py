import subprocess
import os
import sys
from tokenizer import FontanaTokenizer

class FontanaBrain:
    def __init__(self):
        self.tokenizer = FontanaTokenizer()
        # Explicitly lock onto the binary file position relative to this script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.backend_path = os.path.join(os.path.dirname(script_dir), "backend", "tensor_engine_binary")

        print(f"[DEBUG] Looking for C++ binary at: {self.backend_path}")
        if not os.path.exists(self.backend_path):
            print("[CRITICAL] Error: The C++ binary does not exist at that path! Recompile it.")

    def execute_prompt(self, prompt_text: str):
        print(f"[FONTANA BRAIN] Submitting prompt: '{prompt_text}'")

        token_ids = self.tokenizer.encode(prompt_text)
        token_string = " ".join(map(str, token_ids))
        print(f"[DEBUG] Sending token string to C++: {token_string}")

        try:
            process = subprocess.Popen(
                [self.backend_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            stdout_output, stderr_output = process.communicate(input=token_string, timeout=5)

            print("[DEBUG] --- C++ Output Begins ---")
            if stdout_output:
                print(stdout_output)
            else:
                print("[WARNING] C++ returned absolutely no stdout data.")

            if stderr_output:
                print(f"[C++ INTERNAL ERROR]: {stderr_output}")
            print("[DEBUG] --- C++ Output Ends ---")

        except Exception as e:
            print(f"[PYTHON EXCEPTION]: Failed to run subprocess. Details: {e}")

if __name__ == "__main__":
    brain = FontanaBrain()
    brain.execute_prompt("Alistair Fontaine is mapping out logic structures.")
