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

        # Step 2: Inject structural multi-character subwords and syllables directly into the index pool
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

        # Skip subwords that already exist in the vocab (e.g. the single characters
        # 's', 'i', 'a', 't', 'y' above). Re-assigning them would overwrite their
        # original single-character IDs, leaving those IDs orphaned (encodable by the
        # engine but undecodable -> silently dropped as ""), and would push the last
        # subwords past the engine's fixed vocab_size of 107, where they can never be
        # predicted and look up a zero embedding. Deduplicated, the vocab is exactly
        # 107 entries (IDs 0-106), matching the tensor engine.
        next_index = len(base_chars) + 4
        for syllable in subwords:
            if syllable not in self.vocab:
                self.vocab[syllable] = next_index
                next_index += 1

        # Establish inverse vocabulary dimensions for fast decoding loops
        self.inverse_vocab = {v: k for k, v in self.vocab.items()}

        # Build an internal compilation regex sorting longest subwords first to prevent character splitting
        sorted_patterns = sorted(list(self.vocab.keys()), key=len, reverse=True)
        escaped_patterns = [re.escape(p) for p in sorted_patterns if p not in ["[PAD]", "[UNK]", "[BOS]", "[EOS]"]]
        self.tokenizer_regex = re.compile("|".join(escaped_patterns))

    def encode(self, text: str) -> list[int]:
        """Parses human sentences into optimized structural subword integer strings."""
        tokens = [self.vocab["[BOS]"]]

        matches = self.tokenizer_regex.findall(text)

        for segment in matches:
            if segment in self.vocab:
                tokens.append(self.vocab[segment])
            else:
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
    test_phrase = "the fontana system code is loading logic"

    encoded = tokenizer.encode(test_phrase)
    print(f"[SUBWORD TEST] Raw Sentence: '{test_phrase}'")
    print(f"[SUBWORD TEST] Encoded Array IDs: {encoded}")
    print(f"[SUBWORD TEST] Decoded Verification: '{tokenizer.decode(encoded)}'")
    print(f"[SUBWORD TEST] Total Vocabulary Dimensions: {len(tokenizer.vocab)} paths.")
