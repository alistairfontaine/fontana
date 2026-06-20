#include "weight_matrix.cpp"
#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <fstream>
#include <algorithm>
#include <cmath>

namespace Fontana {
    class OptimizedTrainer {
    private:
        int vocab_size;
        int embedding_dim;

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
                probs[i] = std::exp(score / 0.3f);
                sum_exp += probs[i];
            }

            for (int i = 0; i < vocab_size; ++i) {
                probs[i] /= sum_exp;
            }
            return probs;
        }

    public:
        OptimizedTrainer(int v_size, int e_dim) : vocab_size(v_size), embedding_dim(e_dim) {}

        void train_on_sequence(const std::vector<int>& tokens, const std::string& weights_path) {
            WeightMatrix neural_gate(vocab_size, embedding_dim);

            if (!neural_gate.load_from_disk(weights_path)) {
                neural_gate.initialize_weights();
            }

            std::cout << "[FONTANA BALANCED STRIDE TRAINER] Executing 50% data-stride optimizations..." << std::endl;

            int training_window_size = 4;
            float total_loss = 0.0f;
            int loss_count = 0;

            int stride_step = 2;
            float learning_rate = 1.0f / sqrt(static_cast<float>(tokens.size()));
            float weight_decay = 0.995f;

            std::vector<float> mock_embed(embedding_dim, 0.1f);

            for (size_t i = 1; i < tokens.size(); i += stride_step) {
                int next_token = tokens[i];
                int start_idx = std::max(0, (int)i - training_window_size);

                if (i % 2000 == 0) {
                    std::vector<float> probs = compute_scores_and_softmax(mock_embed, neural_gate);
                    if (next_token >= 0 && next_token < vocab_size) {
                        float token_prob = std::max(probs[next_token], 1e-5f);
                        total_loss += -std::log(token_prob);
                        loss_count++;
                    }
                }

                if (i % 1000 == 0) {
                    for (int v = 0; v < vocab_size; ++v) {
                        std::vector<float>& weights = neural_gate.forward_layer(v);
                        for (int d = 0; d < embedding_dim; ++d) {
                            weights[d] *= weight_decay;
                        }
                    }
                }

                for (int w = start_idx; w < (int)i; ++w) {
                    int current_token = tokens[w];

                    if (current_token >= 0 && current_token < vocab_size && next_token >= 0 && next_token < vocab_size) {
                        std::vector<float>& current_weights = neural_gate.forward_layer(current_token);

                        for (int j = 0; j < embedding_dim; ++j) {
                            current_weights[j] += learning_rate;
                            if (current_weights[j] > 3.0f) current_weights[j] = 3.0f;
                        }
                    }
                }
            }

            if (loss_count > 0) {
                std::cout << "🌟 [BALANCED ACCURACY] Current Loss Estimate: " << (total_loss / (float)loss_count) << std::endl;
            }

            neural_gate.save_to_disk(weights_path);
            std::cout << "[FONTANA STRIDE TRAINER] Balanced context optimization matrix locked to disk." << std::endl;
        }
    };
}

int main() {
    int parsed_vocab_size = 95;
    std::string meta_path = "/media/mr-fontaine/R/RECOVERY/Coding/fontana/core/vocab_meta.json";
    std::ifstream meta_file(meta_path);

    if (meta_file.is_open()) {
        std::string line;
        if (std::getline(meta_file, line)) {
            size_t pos = line.find("vocab_size\":");
            if (pos != std::string::npos) {
                std::string size_str = line.substr(pos + 12);
                size_str = size_str.substr(0, size_str.find("}"));
                parsed_vocab_size = std::stoi(size_str);
            }
        }
        meta_file.close();
    }

    std::vector<int> tokens;
    std::string token_file_path = "/media/mr-fontaine/R/RECOVERY/Coding/fontana/core/training_tokens.txt";
    std::ifstream token_file(token_file_path);

    if (token_file.is_open()) {
        int token_id;
        while (token_file >> token_id) {
            tokens.push_back(token_id);
        }
        token_file.close();
    } else {
        std::cerr << "[CRITICAL ERROR] Failed to locate core/training_tokens.txt stream!" << std::endl;
        return 1;
    }

    std::string weights_file = "/media/mr-fontaine/R/RECOVERY/Coding/fontana/fontana_weights.bin";
    // FIXED: STEP 1 UPGRADE - Cranking internal parameter limits from 96 directly to 256 embedding dimensions
    Fontana::OptimizedTrainer trainer(parsed_vocab_size, 256);
    trainer.train_on_sequence(tokens, weights_file);

    return 0;
}
