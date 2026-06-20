import re

class FontanaTokenizer:
    def __init__(self):
        # Base control symbols
        self.vocab = {
            "[PAD]": 0,
            "[UNK]": 1,
            "[BOS]": 2,
            "[EOS]": 3,
        }

        # Step 1: Add individual base characters cleanly
        base_chars = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,!?_@#:-/"
        for i, char in enumerate(base_chars):
            self.vocab[char] = i + 4

        # Step 2: NEW - Inject structural multi-character subwords and syllables directly into the index pool
        # This allows our model engine to predict entire blocks of text chunks at zero storage cost!
        subwords = [
            'the',
            'and',
            'ing',
            'ion',
            'ent',
            'pro',
            'con',
            'sta',
            'font',
            'brain',
            'logic',
            'tech',
            'music',
            'code',
            'system',
            'auto',
            'fontana',
            'istair',
            's',
            'i',
            'a',
            't',
            'y',
            'ste',
            'ine',
            'ana',
            'tio',
            'sys',
            'yst',
            'ook',
            'loo',
            'oks',
            'ell',
            'lli',
            'ith'
        ]

        start_index = len(base_chars) + 4
        for i, syllable in enumerate(subwords):
            self.vocab[syllable] = start_index + i

        # Establish inverse vocabulary dimensions for fast decoding loops
        self.inverse_vocab = {v: k for k, v in self.vocab.items()}

        # Build an internal compilation regex sorting longest subwords first to prevent character splitting
        sorted_patterns = sorted(list(self.vocab.keys()), key=len, reverse=True)
        # Escape punctuation safely to prevent runtime system crash patterns
        escaped_patterns = [re.escape(p) for p in sorted_patterns if p not in ["[PAD]", "[UNK]", "[BOS]", "[EOS]"]]
        self.tokenizer_regex = re.compile("|".join(escaped_patterns))

    def encode(self, text: str) -> list[int]:
        """Parses human sentences into optimized structural subword integer strings."""
        tokens = [self.vocab["[BOS]"]]

        # Scan text streams and isolate matching subwords or fallback base characters
        matches = self.tokenizer_regex.findall(text)

        for segment in matches:
            if segment in self.vocab:
                tokens.append(self.vocab[segment])
            else:
                # Handle stray unmapped characters securely
                for char in segment:
                    tokens.append(self.vocab.get(char, self.vocab["[UNK]"]))

        tokens.append(self.vocab["[EOS]"])
        return tokens

    def decode(self, token_ids: list[int]) -> str:
        """Decodes integer sequences back into fluid text phrases."""
        segments = []
        for token_id in token_ids:
            if token_id in [self.vocab["[BOS]"], self.vocab["[EOS]"], self.vocab["[PAD]"]]:
                continue
            segments.append(self.inverse_vocab.get(token_id, ""))
        return "".join(segments)

if __name__ == "__main__":
    tokenizer = FontanaTokenizer()
    # Test text containing raw structural subwords
    test_phrase = "the fontana system code is loading logic"

    encoded = tokenizer.encode(test_phrase)
    print(f"[SUBWORD TEST] Raw Sentence: '{test_phrase}'")
    print(f"[SUBWORD TEST] Encoded Array IDs: {encoded}")
    print(f"[SUBWORD TEST] Decoded Verification: '{tokenizer.decode(encoded)}'")
    print(f"[SUBWORD TEST] Total Vocabulary Dimensions: {len(tokenizer.vocab)} paths.")
