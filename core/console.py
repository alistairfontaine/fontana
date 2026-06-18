import os
import sys
from generation import FontanaGenerator
from train_link import FontanaTrainerLink

def launch_fontana_shell():
    # Initialize our generator and training subsystem modules
    generator = FontanaGenerator()
    trainer = FontanaTrainerLink()

    print("==================================================")
    # Fontana identity profile signature display
    print("🧭 THE FONTANA ENGINE CORE INTERACTIVE SHELL v1.5")
    print("    AuDHD Multi-Prompt Architecture Sandbox")
    print("==================================================")
    print("Commands:")
    print("  /generate <seed>  -> Run stochastic text generation")
    print("  /train <text>     -> Train weights instantly on live data")
    print("  /exit             -> Terminate session safely")
    print("==================================================\n")

    while True:
        try:
            # Capture keyboard stream input from the terminal line
            user_input = input("fontana-shell> ").strip()

            if not user_input:
                continue

            # Command Routing Gate: Check for exit signature
            if user_input.lower() == "/exit":
                print("\n[SHUTDOWN] Saving system state... Terminating Fontana shell.")
                break

            # Command Routing Gate: Trigger real-time text generation
            elif user_input.startswith("/generate "):
                seed_phrase = user_input[10:].strip()
                if not seed_phrase:
                    print("[SHELL ERROR] Please provide a seed phrase. Usage: /generate <seed>")
                    continue
                # Fire the generator using standard lookback parameters
                generator.generate_text(seed_phrase, max_new_tokens=25)
                print("\n") # Add clean spacing layout spacing

            # Command Routing Gate: Execute real-time dynamic training updates
            elif user_input.startswith("/train "):
                training_data = user_input[7:].strip()
                if not training_data:
                    print("[SHELL ERROR] No text provided. Usage: /train <text>")
                    continue
                # Inject text down the trainer pipeline binary safely
                trainer.train_on_text(training_data)
                print("[SHELL STATUS] Matrix weights scaled dynamically on disk.\n")

            else:
                print(f"[SHELL ERROR] Unknown command context: '{user_input}'. Use /generate, /train, or /exit.")

        except (KeyboardInterrupt, EOFError):
            print("\n\n[SHUTDOWN] Interruption detected. Terminating shell safely.")
            break

if __name__ == "__main__":
    launch_fontana_shell()
