import os
import sys
import subprocess
from generation import FontanaGenerator
from train_link import FontanaTrainerLink
from load_profile import FontanaProfileLoader
from tokenizer import FontanaTokenizer

class FontanaConsoleApp:
    def __init__(self):
        self.generator = FontanaGenerator()
        self.trainer = FontanaTrainerLink()
        self.loader = FontanaProfileLoader()
        self.tokenizer = FontanaTokenizer()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.project_root = os.path.dirname(script_dir)
        self.trainer_path = os.path.join(self.project_root, "backend", "trainer_optimized_binary")
        self.token_file_path = os.path.join(script_dir, "training_tokens.txt")
        self.dataset_path = os.path.join(self.project_root, "dataset.txt")
        self.max_tokens = 25
        # FIXED: CREATIVE ROADMAP STEP 2 - INTERACTIVE PROMPT HISTORY CACHE LAYER
        self.history_cache = []

    def print_help_menu(self):
        print("\n==================================================")
        print("🧭 FONTANA CORE CONSOLE COMMAND MANUAL")
        print("==================================================")
        print("  /generate <seed>  -> Run stochastic text generation")
        print("  /history          -> Review stashed prompt memory tracking traces")
        print("  /length <num>     -> Scale dynamic token output bounds live")
        print("  /train            -> Enter MULTILINE dialogue training stream mode")
        print("  /load <suffix>    -> Hot-swap active memory profiles instantly")
        print("  /help             -> Print this operational dashboard manual")
        print("  /exit             -> Terminate session safely and freeze files")
        print("==================================================")

    def launch_shell(self):
        print("==================================================")
        print("🧭 THE FONTANA ENGINE CORE INTERACTIVE SHELL v2.5")
        print("    AuDHD Multi-Prompt Live Hot-Swap Command Shell")
        print("==================================================")
        self.print_help_menu()

        backup_dir = os.path.join(self.project_root, "weights_backup")
        if os.path.exists(backup_dir):
            files = os.listdir(backup_dir)
            suffixes = sorted(list(set([
                f.replace("fontana_weights_", "").replace(".bin", "").replace("fontana_embeddings_", "")
                for f in files if f.endswith(".bin")
            ])))
            print(f"Active Stored Profiles on Disk: {suffixes}")
        print("==================================================\n")

        while True:
            try:
                user_input = input(f"fontana-[len:{self.max_tokens}]> ").strip()

                if not user_input:
                    continue

                if user_input.lower() == "/exit":
                    print("\n[SHUTDOWN] Saving system state... Terminating Fontana shell.")
                    break

                elif user_input.lower() == "/help":
                    self.print_help_menu()
                    print("\n")
                    continue

                # FIXED: HISTORY MEMORY COGNITIVE LOOKUP ENDPOINT
                elif user_input.lower() == "/history":
                    print("\n🧭 [PROMPT MEMORY CACHE LOOKUP TRACKS]:")
                    if not self.history_cache:
                        print("  [STATUS] No prompts stashed in this tracking block yet.\n")
                    else:
                        for idx, item in enumerate(self.history_cache, 1):
                            print(f"  [{idx}] '{item}'")
                        print("\n")
                    continue

                elif user_input.startswith("/length"):
                    len_str = user_input[7:].strip()
                    if not len_str:
                        print("[SHELL ERROR] Parameter missing. Usage: /length <integer_value>\n")
                        continue
                    try:
                        new_len = int(len_str)
                        if 5 <= new_len <= 150:
                            self.max_tokens = new_len
                            print(f"[SHELL STATUS] Dynamic output generation bounds scaled to: {self.max_tokens} tokens.\n")
                        else:
                            print("[SHELL ERROR] Length bounds must fall strictly between 5 and 150 tokens.\n")
                    except ValueError:
                        print("[SHELL ERROR] Invalid format type. Usage: /length <integer_value>\n")
                    continue

                elif user_input.startswith("/generate"):
                    seed_phrase = user_input[9:].strip()
                    if not seed_phrase:
                        print("[SHELL ERROR] Seed phrase missing. Usage: /generate <seed_phrase>\n")
                        continue

                    # Cache the active generation run into our memory tracking pool
                    if seed_phrase not in self.history_cache:
                        self.history_cache.append(seed_phrase)

                    seed_phrase_padded = seed_phrase + " "
                    self.generator.generate_text(seed_phrase_padded, max_new_tokens=self.max_tokens)
                    print("\n")

                elif user_input.lower() == "/train":
                    print("\n[MULTILINE MODE] Paste script blocks below. Press ENTER on an empty line to compile training:")
                    print("--------------------------------------------------------------------------------")
                    lines = []
                    while True:
                        line = sys.stdin.readline()
                        if line == "\n" or not line:
                            break
                        lines.append(line.strip())

                    training_data = " ".join(lines).strip().lower()
                    if not training_data:
                        print("[SHELL ERROR] Empty payload. Training aborted.\n")
                        continue

                    word_count = len(training_data.split())
                    if word_count < 4:
                        print(f"[SHELL ERROR] Trajectory too small ({word_count} words). Need at least 4 words.\n")
                        continue

                    if os.path.exists(self.dataset_path):
                        with open(self.dataset_path, "a", encoding="utf-8") as dataset_f:
                            dataset_f.write("\n" + training_data)

                    print(f"[LIVE TRAINING] Encapsulating persistent text stream...")
                    token_ids = self.tokenizer.encode(training_data)

                    with open(self.token_file_path, "w", encoding="utf-8") as token_f:
                        token_f.write(" ".join(map(str, token_ids)))

                    print(f"[LIVE OPTIMIZATION] Invoking C++ matrix pipeline execution...")
                    try:
                        subprocess.run([self.trainer_path], capture_output=True, text=True, check=True)
                        print("[SHELL STATUS] Matrix weight fields adjusted permanently across multiline text block.\n")
                    except subprocess.CalledProcessError as e:
                        print(f"❌ [LIVE PIPELINE BREAK] C++ trainer rejected sequence. Details: {e}\n")

                    if os.path.exists(self.token_file_path):
                        os.remove(self.token_file_path)
                    continue

                elif user_input.startswith("/load"):
                    profile_suffix = user_input[5:].strip()
                    if not profile_suffix:
                        print("[SHELL ERROR] Profile name missing. Usage: /load <profile_suffix>\n")
                        continue

                    success = self.loader.swap_active_profile(profile_suffix)
                    if success:
                        print(f"[SHELL STATUS] Fontana memory matrix hot-swapped onto profile: {profile_suffix.upper()}\n")
                    else:
                        print("[SHELL ERROR] Target profile swap failed. Verify label name.\n")

                elif not user_input.startswith("/") or user_input.split() in ["load", "generate", "train", "length", "exit", "help"]:
                    print(f"[SHELL ERROR] Invalid command format syntax. Did you forget a leading '/'?")
                    self.print_help_menu()
                    print("\n")

                else:
                    print(f"[SHELL ERROR] Unknown command context. Use /generate, /length, /load, or /exit.\n")

            except (KeyboardInterrupt, EOFError):
                print("\n\n[SHUTDOWN] Interruption detected. Terminating shell safely.")
                break

if __name__ == "__main__":
    app = FontanaConsoleApp()
    app.launch_shell()
