import collections
import os

class FontanaMemoryMap:
    def __init__(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.project_root = os.path.dirname(script_dir)
        self.dataset_path = os.path.join(self.project_root, "dataset.txt")

    def extract_dynamic_subwords(self, top_n: int = 10) -> list[str]:
        print("==================================================")
        print("🧭 [FONTANA MEMORY MAP] Analyzing Corpus Patterns...")
        print("==================================================")

        if not os.path.exists(self.dataset_path):
            print(f"[ERROR] Target dataset file not found at: {self.dataset_path}")
            return []

        with open(self.dataset_path, "r", encoding="utf-8") as f:
            text = f.read().strip().lower()

        # Isolate individual alpha words cleanly
        words = [w for w in text.split() if w.isalpha() and len(w) > 3]

        # Track 3-character syllable fragments across your dataset text corpus
        fragments = []
        for word in words:
            for i in range(len(word) - 2):
                fragments.append(word[i:i+3])

        # Extract the highest frequency multi-character syllables automatically
        frequency_counter = collections.Counter(fragments)
        top_syllables = [item[0] for item in frequency_counter.most_common(top_n)]

        print(f"[SUCCESS] Discovered top {len(top_syllables)} high-density syllable roots:")
        for rank, item in enumerate(frequency_counter.most_common(top_n), 1):
            print(f"  Rank [{rank}] Syllable: '{item[0]}' | Frequency Count: {item[1]}")

        print("==================================================")
        return top_syllables

if __name__ == "__main__":
    mapper = FontanaMemoryMap()
    mapper.extract_dynamic_subwords(top_n=8)
