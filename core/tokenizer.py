import re

class FontanaTokenizer:
    def __init__(self):
        # A lightweight vocabulary mapping characters and common tokens to unique integer IDs
        # We start with basic ASCII mapping + specialized model control tokens
        self.vocab = {
            "[PAD]": 0,   # Padding token
            "[UNK]": 1,   # Unknown characters
            "[BOS]": 2,   # Beginning of sentence
            "[EOS]": 3,   # End of sentence
        }

        # Build out a simple vocabulary pool dynamically using common characters
        # This keeps our storage footprint tiny (a few kilobytes)
        for i, char in enumerate(" abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,!?_@#:-/"):
            self.vocab[char] = i + 4 # Shift by 4 to preserve our control tokens

        # Reverse vocabulary lookup to decode numbers back into human characters
        self.inverse_vocab = {v: k for k, v in self.vocab.items()}

    def encode(self, text: str) -> list[int]:
        """Converts human text into a structured list of token integer IDs."""
        tokens = [self.vocab["[BOS]"]] # Always begin with our Beginning of Sentence token

        for char in text:
            if char in self.vocab:
                tokens.append(self.vocab[char])
            else:
                tokens.append(self.vocab["[UNK]"]) # Handle characters outside our vocabulary

        tokens.append(self.vocab["[EOS]"]) # Cap with our End of Sentence token
        return tokens

    def decode(self, token_ids: list[int]) -> str:
        """Converts a sequence of token IDs back into human readable text."""
        chars = []
        for token_id in token_ids:
            if token_id in [self.vocab["[BOS]"], self.vocab["[EOS]"], self.vocab["[PAD]"]]:
                continue # Skip formatting tokens during playback
            chars.append(self.inverse_vocab.get(token_id, ""))
        return "".join(chars)

# Standalone test block to verify your Python logic works immediately
if __name__ == "__main__":
    tokenizer = FontanaTokenizer()
    sample_text = "Project Fontana v1.0 initialized."

    # Run encoder
    encoded_ids = tokenizer.encode(sample_text)
    print(f"[FONTANA TOKENIZER] Original Text: '{sample_text}'")
    print(f"[FONTANA TOKENIZER] Encoded Token IDs: {encoded_ids}")

    # Run decoder to ensure data integrity
    decoded_text = tokenizer.decode(encoded_ids)
    print(f"[FONTANA TOKENIZER] Decoded Verification: '{decoded_text}'")
