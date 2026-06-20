import os
import sys
from generation import FontanaGenerator
from train_link import FontanaTrainerLink
from load_profile import FontanaProfileLoader

def launch_fontana_shell():
    generator = FontanaGenerator()
    trainer = FontanaTrainerLink()
    loader = FontanaProfileLoader()

    print("==================================================")
    print("🧭 THE FONTANA ENGINE CORE INTERACTIVE SHELL v1.7")
    print("    AuDHD Multi-Prompt Live Hot-Swap Command Shell")
    print("==================================================")
    print("Commands:")
    print("  /generate <seed>  -> Run stochastic text generation")
    print("  /train <text>     -> Train weights instantly on live data")
    print("  /load <suffix>    -> Hot-swap active memory profiles instantly")
    print("  /exit             -> Terminate session safely")
    print("==================================================")

    # FIXED: AUTOMATED HARD DRIVE SCANNER PIPELINE
    # Scans the local partition backup directory to display fresh stashed profiles on-the-fly
    script_dir = os.path.dirname(os.path.abspath(__file__))
    backup_dir = os.path.join(os.path.dirname(script_dir), "weights_backup")

    if os.path.exists(backup_dir):
        files = os.listdir(backup_dir)
        # Extract unique suffix names by filtering string prefixes and file extensions cleanly
        suffixes = sorted(list(set([
            f.replace("fontana_weights_", "").replace(".bin", "").replace("fontana_embeddings_", "")
            for f in files if f.endswith(".bin")
        ])))
        print(f"Active Stored Profiles on Disk: {suffixes}")
    else:
        print("Active Stored Profiles on Disk: []")
    print("==================================================\n")

    while True:
        try:
            user_input = input("fontana-shell> ").strip()

            if not user_input:
                continue

            if user_input.lower() == "/exit":
                print("\n[SHUTDOWN] Saving system state... Terminating Fontana shell.")
                break
            elif user_input.startswith("/generate "):
                # Extract seed and forcefully append a trailing word-boundary space context
                seed_phrase = user_input[10:].strip() + " "
                if not seed_phrase.strip():
                    print("[SHELL ERROR] Usage: /generate <seed>")
                    continue
                generator.generate_text(seed_phrase, max_new_tokens=25)
                print("\n")


            elif user_input.startswith("/train "):
                training_data = user_input[7:].strip()
                if not training_data:
                    print("[SHELL ERROR] Usage: /train <text>")
                    continue
                trainer.train_on_text(training_data)
                print("[SHELL STATUS] Matrix weights scaled dynamically on disk.\n")

            elif user_input.startswith("/load "):
                profile_suffix = user_input[6:].strip()
                if not profile_suffix:
                    print("[SHELL ERROR] Usage: /load <profile_suffix>")
                    continue

                success = loader.swap_active_profile(profile_suffix)
                if success:
                    print(f"[SHELL STATUS] Fontana memory matrix hot-swapped onto profile: {profile_suffix.upper()}\n")
                else:
                    print("[SHELL ERROR] Target profile swap failed.\n")

            else:
                print(f"[SHELL ERROR] Unknown command context. Use /generate, /train, /load, or /exit.")

        except (KeyboardInterrupt, EOFError):
            print("\n\n[SHUTDOWN] Interruption detected. Terminating shell safely.")
            break

if __name__ == "__main__":
    launch_fontana_shell()
