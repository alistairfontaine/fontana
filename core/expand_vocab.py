import os
import re
import json
from memory_map import FontanaMemoryMap

class FontanaVocabExpander:
    def __init__(self):
        self.mapper = FontanaMemoryMap()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.tokenizer_path = os.path.join(script_dir, "tokenizer.py")
        self.meta_path = os.path.join(script_dir, "vocab_meta.json")
        self.dataset_path = os.path.join(os.path.dirname(script_dir), "dataset.txt")

    def optimize_system_vocabulary(self):
        # Dynamic Scale-Factor Injector
        target_top_n = 8
        if os.path.exists(self.dataset_path):
            file_size = os.path.getsize(self.dataset_path)
            if file_size > 100000:
                target_top_n = 100

        print(f"[FONTANA O³] Dynamic Vocab Sweep: Adjusting harvesting threshold to top_{target_top_n} patterns.")

        # FIXED: PR #4 BY TAPIWAMAKANDIGONA
        new_syllables = self.mapper.extract_dynamic_subwords(top_n=target_top_n)

        if not os.path.exists(self.tokenizer_path):
            return

        with open(self.tokenizer_path, "r", encoding="utf-8") as f:
            tokenizer_code = f.read()

        match = re.search(r'subwords\s*=\s*\[(.*?)\]', tokenizer_code, re.DOTALL)
        if not match:
            return

        raw_list_content = match.group(1)
        current_subwords = [w.strip().strip('"').strip("'") for w in raw_list_content.split(',') if w.strip()]

        added_count = 0
        for syllable in new_syllables:
            if syllable not in current_subwords:
                current_subwords.append(syllable)
                added_count += 1

        new_list_string = ",\n            ".join([f"'{w}'" for w in current_subwords])
        updated_code = re.sub(r'subwords\s*=\s*\[.*?\]', f'subwords = [\n            {new_list_string}\n        ]', tokenizer_code, flags=re.DOTALL)

        with open(self.tokenizer_path, "w", encoding="utf-8") as f:
            f.write(updated_code)

        from tokenizer import FontanaTokenizer
        t = FontanaTokenizer()
        total_vocab_size = len(t.vocab)

        meta_data = {"vocab_size": total_vocab_size}
        with open(self.meta_path, "w", encoding="utf-8") as f:
            json.dump(meta_data, f)

        print(f"\n🌟 [SUCCESS] Injected {added_count} new subwords into tokenizer.py!")
        print(f"   [SYNC LOCK]: Written dynamic vocabulary size ({total_vocab_size}) to vocab_meta.json")
        print("==================================================")

if __name__ == "__main__":
    expander = FontanaVocabExpander()
    expander.optimize_system_vocabulary()
