import os
import sys
from generation import FontanaGenerator
from train_link import FontanaTrainerLink
from load_profile import FontanaProfileLoader

class FontanaConsoleApp:
    def __init__(self):
        self.generator = FontanaGenerator()
        self.trainer = FontanaTrainerLink()
        self.loader = FontanaProfileLoader()
        self.max_tokens = 25 # Dynamic length tracking state variable

    def print_help_menu(self):
        print("\n==================================================")
        print("🧭 FONTANA CORE CONSOLE COMMAND MANUAL")
        print("==================================================")
        print("  /generate <seed>  -> Run stochastic text generation")
        print("  /length <num>     -> Scale dynamic token output bounds live")
        print("  /train <text>     -> Train weights instantly on live context")
        print("  /load <suffix>    -> Hot-swap active memory profiles instantly")
        print("  /help             -> Print this operational dashboard manual")
        print("  /exit             -> Terminate session safely and freeze files")
        print("==================================================")

    def launch_shell(self):
        print("==================================================")
        print("🧭 THE FONTANA ENGINE CORE INTERACTIVE SHELL v1.8")
        print("    AuDHD Multi-Prompt Live Hot-Swap Command Shell")
        print("==================================================")
        self.print_help_menu()

        script_dir = os.path.dirname(os.path.abspath(__file__))
        backup_dir = os.path.join(os.path.dirname(script_dir), "weights_backup")

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

                # LIVE INFERENCE LENGTH MODIFIER GATE
                elif user_input.startswith("/length "):
                    len_str = user_input[8:].strip()
                    try:
                        new_len = int(len_str)
                        if 5 <= new_len <= 150:
                            self.max_tokens = new_len
                            print(f"[SHELL STATUS] Dynamic output generation bounds scaled to: {self.max_tokens} tokens.\n")
                        else:
                            print("[SHELL ERROR] Length bounds must fall strictly between 5 and 150 tokens.\n")
                    except ValueError:
                        print("[SHELL ERROR] Usage: /length <integer_value>\n")
                    continue

                elif user_input.startswith("/generate "):
                    seed_phrase = user_input[10:].strip() + " "
                    if not seed_phrase.strip():
                        print("[SHELL ERROR] Usage: /generate <seed>\n")
                        continue
                    # Passes the dynamically tracking length state variable cleanly
                    self.generator.generate_text(seed_phrase, max_new_tokens=self.max_tokens)
                    print("\n")

                elif user_input.startswith("/train "):
                    training_data = user_input[7:].strip()
                    if not training_data:
                        print("[SHELL ERROR] Usage: /train <text>\n")
                        continue
                    self.trainer.train_on_text(training_data)
                    print("[SHELL STATUS] Matrix weights scaled dynamically on disk.\n")

                elif user_input.startswith("/load "):
                    profile_suffix = user_input[6:].strip()
                    if not profile_suffix:
                        print("[SHELL ERROR] Usage: /load <profile_suffix>\n")
                        continue

                    success = self.loader.swap_active_profile(profile_suffix)
                    if success:
                        print(f"[SHELL STATUS] Fontana memory matrix hot-swapped onto profile: {profile_suffix.upper()}\n")
                    else:
                        print("[SHELL ERROR] Target profile swap failed.\n")

                # FIXED: VALIDATION GUARDRAIL
                # Catch raw inputs missing leading slashes and block them from breaking RAM generation loops
                elif not user_input.startswith("/"):
                    print(f"[SHELL ERROR] Invalid command syntax context. Did you forget a '/'?")
                    print(f"              Type /help to view valid control structures.\n")

                else:
                    print(f"[SHELL ERROR] Unknown command context. Use /generate, /length, /load, or /exit.\n")

            except (KeyboardInterrupt, EOFError):
                print("\n\n[SHUTDOWN] Interruption detected. Terminating shell safely.")
                break

if __name__ == "__main__":
    app = FontanaConsoleApp()
    app.launch_shell()
