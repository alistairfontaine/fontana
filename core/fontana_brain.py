import os
import sys
import time

class FontanaBrain:
    def __init__(self):
        self.rx_pipe = "/tmp/fontana_rx.fifo"
        self.tx_pipe = "/tmp/fontana_tx.fifo"

    def submit_prompt(self, prompt_text: str):
        # Safety Gate: If the C++ service daemon isn't running in the background, issue a warning
        if not os.path.exists(self.rx_pipe) or not os.path.exists(self.tx_pipe):
            return "[ERROR] Fontana background daemon service is not active! Run ./backend/tensor_engine_binary first."

        # Convert token IDs or text strings to direct hardware pipe characters
        token_string = prompt_text.strip() + "\n"

        try:
            # Write token parameters directly into the receiving communication bus channel
            with open(self.rx_pipe, "w") as rx_f:
                rx_f.write(token_string)

            # Read the predicted response scalar integer straight back out of the transmission pipe
            with open(self.tx_pipe, "r") as tx_f:
                predicted_id_str = tx_f.read().strip()

            return predicted_id_str

        except Exception as e:
            return f"[ERROR] IPC Pipeline Break: {str(e)}"

if __name__ == "__main__":
    print("🧭 [FONTANA GATEWAY] Verifying hardware pipe connections...")
    brain = FontanaBrain()
    # Simple check verification prompt string
    print(brain.submit_prompt("2 31 16 4"))
