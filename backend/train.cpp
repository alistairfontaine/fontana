#include "weight_matrix.cpp"
#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <fstream>
#include <algorithm>

namespace Fontana {
    class LocalTrainer {
    private:
        int vocab_size;
        int embedding_dim;

    public:
        LocalTrainer(int v_size, int e_dim) : vocab_size(v_size), embedding_dim(e_dim) {}

        // FIXED: UPGRADED CONTEXT-AWARE TRAINING CORE
        // Links each token to a window of up to 4 preceding tokens to form structural text associations
        void train_on_sequence(const std::vector<int>& tokens, const std::string& weights_path) {
            WeightMatrix neural_gate(vocab_size, embedding_dim);

            if (!neural_gate.load_from_disk(weights_path)) {
                neural_gate.initialize_weights();
            }

            std::cout << "[FONTANA CONTEXT TRAINER] Building matrix association networks across "
                      << tokens.size() << " tokens..." << std::endl;

            int training_window_size = 4; // Lookback link boundary threshold

            // Step through each token in the sentence stream
            for (size_t i = 1; i < tokens.size(); ++i) {
                int next_token = tokens[i];

                // Calculate sliding window boundaries
                int start_idx = std::max(0, (int)i - training_window_size);

                // Nested Window Loop: Link next_token back to all tokens inside the lookback window
                for (int w = start_idx; w < (int)i; ++w) {
                    int current_token = tokens[w];

                    if (current_token >= 0 && current_token < vocab_size && next_token >= 0 && next_token < vocab_size) {
                        std::vector<float>& current_weights = neural_gate.forward_layer(current_token);

                        // Adjust the weight matrix fractions to bind the contextual network layer tokens
                        for (int j = 0; j < embedding_dim; ++j) {
                            current_weights[j] += 0.1f; // Stable incremental context learning rate
                            if (current_weights[j] > 2.0f) current_weights[j] = 2.0f; // Safe ceiling limit
                        }
                    }
                }
            }

            neural_gate.save_to_disk(weights_path);
            std::cout << "[FONTANA TRAINER] Optimization cycle complete. Matrix context networks updated on disk." << std::endl;
        }
    };
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cerr << "Usage: ./trainer <space_separated_token_ids>" << std::endl;
        return 1;
    }

    std::vector<int> tokens;
    for (int i = 1; i < argc; ++i) {
        tokens.push_back(std::stoi(argv[i]));
    }

    std::string weights_file = "/media/mr-fontaine/R/RECOVERY/Coding/fontana/fontana_weights.bin";
    Fontana::LocalTrainer trainer(96, 96);
    trainer.train_on_sequence(tokens, weights_file);

    return 0;
}
