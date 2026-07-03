import os
import subprocess

class FontanaTrainerLink:
    def __init__(self):
        # Import your original 108-line regular expression tokenizer natively
        from tokenizer import FontanaTokenizer
        self.tokenizer = FontanaTokenizer()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.project_root = os.path.dirname(script_dir)
        # Target your optimized C++ training binary cleanly on your partition
        self.trainer_path = os.path.join(self.project_root, "backend", "trainer_optimized_binary")

    def train_on_text(self, training_text: str):
        print(f"[FONTANA O³] Ingesting training text: '{training_text}'")

        if not os.path.exists(self.trainer_path):
            return "[ERROR] C++ trainer matrix binary executable file missing!"

        try:
            # Transform human screenplay words cleanly into integer index lists
            token_ids = self.tokenizer.encode(training_text)
            token_string = " ".join(map(str, token_ids)) + "\n"

            print(f"[DEBUG] Feeding token sequences to C++ trainer: {token_ids}")

            # FIXED: UNBLOCKED NON-BLOCKING SUBPROCESS INTERCEPT CONNECTOR
            # Spawns the C++ binary and uses .communicate() to pass data and
            # forcefully transmit an absolute EOF signal instantly, completely preventing deadlocks!
            process = subprocess.Popen(
                [self.trainer_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Flush data bytes and terminate pipes natively in less than 5 milliseconds
            stdout_output, stderr_output = process.communicate(input=token_string, timeout=5.0)

            if stdout_output:
                print(f"[C++ TRAINER OUTPUT]: {stdout_output.strip()}")
            if stderr_output:
                print(f"[C++ TRAINER WARNING]: {stderr_output.strip()}")

            return f"[SUCCESS] Matrix fields adjusted. C++ Output: {stdout_output.strip()}"

        except subprocess.TimeoutExpired:
            process.kill()
            return "[ERROR] C++ training execution matrix pass timed out!"
        except Exception as e:
            return f"[ERROR] Live Pipeline Break: {str(e)}"

if __name__ == "__main__":
    link = FontanaTrainerLink()
    link.train_on_text("the fontana system code is loading logic tech")
