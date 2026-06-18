#include "weight_matrix.cpp"
#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <fstream>
#include <algorithm>
#include <cmath> // Required for log calculations

namespace Fontana {
    class LocalTrainer {
    private:
        int vocab_size;
        int embedding_dim;

        // Lightweight Softmax emulator for loss score mapping inside our trainer
        std::vector<float> compute_scores_and_softmax(const std::vector<float>& embed, WeightMatrix& gate) {
            std::vector<float> scores(vocab_size, 0.0f);
            std::vector<float> probs(vocab_size, 0.0f);
            float sum_exp = 0.0f;

            for (int i = 0; i < vocab_size; ++i) {
                std::vector<float>& weights = gate.forward_layer(i);
                float score = 0.0f;
                for (int j = 0; j < embedding_dim; ++j) {
                    score += embed[j] * weights[j];
                }
                scores[i] = score;
                probs[i] = std::exp(score / 0.3f); // Match generation temperature scale
                sum_exp += probs[i];
            }

            for (int i = 0; i < vocab_size; ++i) {
                probs[i] /= sum_exp;
            }
            return probs;
        }

    public:
        LocalTrainer(int v_size, int e_dim) : vocab_size(v_size), embedding_dim(e_dim) {}

        void train_on_sequence(const std::vector<int>& tokens, const std::string& weights_path) {
            WeightMatrix neural_gate(vocab_size, embedding_dim);

            if (!neural_gate.load_from_disk(weights_path)) {
                neural_gate.initialize_weights();
            }

            std::cout << "[FONTANA CONTEXT TRAINER] Building matrix association networks across "
                      << tokens.size() << " tokens..." << std::endl;

            int training_window_size = 4;
            float total_loss = 0.0f;
            int loss_count = 0;

            // Initialize a temporary flat embedding matrix to emulate text lookup contexts inside training
            std::vector<float> mock_embed(embedding_dim, 0.1f);

            for (size_t i = 1; i < tokens.size(); ++i) {
                int next_token = tokens[i];
                int start_idx = std::max(0, (int)i - training_window_size);

                // --- NEW: SPREAD MATRIX PERFORMANCE LOSS ASSESSMENT ---
                std::vector<float> probs = compute_scores_and_softmax(mock_embed, neural_gate);
                if (next_token >= 0 && next_token < vocab_size) {
                    // Cross-Entropy Loss: negative natural log of the correct token's probability
                    float token_prob = std::max(probs[next_token], 1e-5f); // Prevent log(0) crashes
                    total_loss += -std::log(token_prob);
                    loss_count++;
                }

                for (int w = start_idx; w < (int)i; ++w) {
                    int current_token = tokens[w];

                    if (current_token >= 0 && current_token < vocab_size && next_token >= 0 && next_token < vocab_size) {
                        std::vector<float>& current_weights = neural_gate.forward_layer(current_token);

                        for (int j = 0; j < embedding_dim; ++j) {
                            current_weights[j] += 0.05f;
                            if (current_weights[j] > 2.0f) current_weights[j] = 2.0f;
                        }
                    }
                }
            }

            // Print out the structural evaluation score directly
            if (loss_count > 0) {
                std::cout << "🌟 [MATRIX ACCURACY] Current Training Loss Estimate: " << (total_loss / (float)loss_count) << std::endl;
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
