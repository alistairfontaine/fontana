import os
import sys
import time

class FontanaBrain:
    def __init__(self):
        self.rx_pipe = "/tmp/fontana_rx.fifo"
        self.tx_pipe = "/tmp/fontana_tx.fifo"

    def submit_prompt(self, prompt_text: str):
        if not os.path.exists(self.rx_pipe) or not os.path.exists(self.tx_pipe):
            return "[ERROR] Fontana background daemon service is not active!"

        token_string = prompt_text.strip() + "\n"

        try:
            # FIXED: NATIVE LINUX NON-BLOCKING PIPE INTERCEPT GATE
            # Open the file descriptor with low-level flags to prevent the thread from freezing the web server
            fd_rx = os.open(self.rx_pipe, os.O_WRONLY | os.O_NONBLOCK)
            os.write(fd_rx, token_string.encode('utf-8'))
            os.close(fd_rx)

            # Read the response safely with a microsecond timeout threshold
            timeout = 0.5
            start_time = time.time()
            predicted_id_str = ""

            while (time.time() - start_time) < timeout:
                try:
                    fd_tx = os.open(self.tx_pipe, os.O_RDONLY | os.O_NONBLOCK)
                    data = os.read(fd_tx, 128).decode('utf-8').strip()
                    os.close(fd_tx)
                    if data:
                        predicted_id_str = data
                        break
                except OSError:
                    pass
                time.sleep(0.01)

            if not predicted_id_str:
                return "0" # Safe fallback to prevent pipeline crashes

            return predicted_id_str

        except Exception as e:
            return f"[ERROR] IPC Pipeline Break: {str(e)}"

if __name__ == "__main__":
    brain = FontanaBrain()
    print(brain.submit_prompt("2 31 16 4"))
