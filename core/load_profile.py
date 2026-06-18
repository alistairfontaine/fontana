import os
import shutil
import sys

class FontanaProfileLoader:
    def __init__(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.project_root = os.path.dirname(script_dir)
        self.backup_dir = os.path.join(self.project_root, "weights_backup")

        self.active_weights = os.path.join(self.project_root, "fontana_weights.bin")
        self.active_embeds = os.path.join(self.project_root, "fontana_embeddings.bin")

    def swap_active_profile(self, profile_suffix: str):
        print("==================================================")
        print(f"🧭 [FONTANA LOAD] Locating Profile: '{profile_suffix}'")
        print("==================================================")

        target_weights = os.path.join(self.backup_dir, f"fontana_weights_{profile_suffix}.bin")
        target_embeds = os.path.join(self.backup_dir, f"fontana_embeddings_{profile_suffix}.bin")

        if not os.path.exists(target_weights) or not os.path.exists(target_embeds):
            print(f"❌ [FILE NOT FOUND] Profile '{profile_suffix}' does not exist in backup directory!")
            print("==================================================")
            return False

        try:
            # Safely clone the backup profile weights directly into active runtime positions
            shutil.copyfile(target_weights, self.active_weights)
            shutil.copyfile(target_embeds, self.active_embeds)

            print(f"🌟 [SUCCESS] Profile swapped successfully!")
            print(f"   Active Mind State: {profile_suffix.upper()}")
            print("==================================================")
            return True

        except Exception as e:
            print(f"❌ [FILESYSTEM FAILURE] File swap operation failed. Details: {e}")
            return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 core/load_profile.py <profile_suffix>")
        sys.exit(1)

    loader = FontanaProfileLoader()
    loader.swap_active_profile(sys.argv[1])
