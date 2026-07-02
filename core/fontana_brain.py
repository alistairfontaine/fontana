import os
import subprocess

class FontanaBrain:
    def __init__(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.backend_path = os.path.join(os.path.dirname(script_dir), "backend", "tensor_engine_binary")
        self.process = None
        self._init_daemon()

    def _init_daemon(self):
        """Boots the C++ binary once into memory as a persistent daemon process."""
        if os.path.exists(self.backend_path):
            self.process = subprocess.Popen(
                [self.backend_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1 # Line-buffered for instant streaming response
            )

    def submit_prompt(self, prompt_text: str):
        if not self.process or self.process.poll() is not None:
            self._init_daemon()
            if not self.process:
                return "[ERROR] Fontana background daemon failed to initialize!"

        token_string = prompt_text.strip() + "\n"

        try:
            # Stream the token string directly into the active C++ RAM memory process
            self.process.stdin.write(token_string)
            self.process.stdin.flush()

            # Instantly read the predicted response token ID back from stdout
            predicted_id_str = self.process.stdout.readline().strip()

            if not predicted_id_str:
                return "0"

            return predicted_id_str

        except Exception as e:
            return f"[ERROR] IPC Pipeline Break: {str(e)}"

if __name__ == "__main__":
    brain = FontanaBrain()
    print("🧭 [FONTANA GATEWAY] Verifying background RAM matrix connection...")
    print(brain.submit_prompt("2 31 16 4"))
