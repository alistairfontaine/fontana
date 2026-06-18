import os
import re
from memory_map import FontanaMemoryMap

class FontanaVocabExpander:
    def __init__(self):
        self.mapper = FontanaMemoryMap()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.tokenizer_path = os.path.join(script_dir, "tokenizer.py")

    def optimize_system_vocabulary(self):
        # 1. Harvest the top 8 high-density syllables discovered by our pattern parser
        discovered_pairs = self.mapper.extract_dynamic_subwords(top_n=8)
        new_syllables = [item[0] for item in discovered_pairs]

        if not os.path.exists(self.tokenizer_path):
            print(f"[ERROR] Target tokenizer module not found at: {self.tokenizer_path}")
            return

        with open(self.tokenizer_path, "r", encoding="utf-8") as f:
            tokenizer_code = f.read()

        # 2. Extract the current hardcoded subwords list from your tokenizer code using regex
        match = re.search(r'subwords\s*=\s*\[(.*?)\]', tokenizer_code, re.DOTALL)
        if not match:
            print("[CRITICAL] Could not locate the subwords list block inside tokenizer.py!")
            return

        raw_list_content = match.group(1)
        # Parse into a clean python list of string names
        current_subwords = [w.strip().strip('"').strip("'") for w in raw_list_content.split(',') if w.strip()]

        # 3. Check for duplicates and filter only completely new unique subwords
        added_count = 0
        for syllable in new_syllables:
            if syllable not in current_subwords:
                current_subwords.append(syllable)
                added_count += 1

        if added_count == 0:
            print("\n[STATUS] Vocabulary is already fully optimized. No new paths required.")
            return

        # 4. Reconstruct the string array layout content cleanly
        new_list_string = ",\n            ".join([f"'{w}'" for w in current_subwords])
        updated_code = re.sub(r'subwords\s*=\s*\[.*?\]', f'subwords = [\n            {new_list_string}\n        ]', tokenizer_code, flags=re.DOTALL)

        # 5. Inject the newly expanded python code straight back onto your disk partition
        with open(self.tokenizer_path, "w", encoding="utf-8") as f:
            f.write(updated_code)

        print(f"\n🌟 [SUCCESS] Successfully injected {added_count} new structural subwords into tokenizer.py!")
        print(f"   [TOTAL CHANNELS]: Expanded to {len(current_subwords)} distinct subword segments.")
        print("==================================================")

if __name__ == "__main__":
    expander = FontanaVocabExpander()
    expander.optimize_system_vocabulary()
