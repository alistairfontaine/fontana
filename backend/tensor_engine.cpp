#include "tensor_engine.hpp"
#include "weight_matrix.cpp"
#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <cmath>
#include <numeric>
#include <algorithm>
#include <random>

namespace Fontana {

    class EmbeddingLayer {
    private:
        int vocab_size;
        int embedding_dim;
        std::vector<std::vector<float>> embedding_table;

    public:
        EmbeddingLayer(int v_size, int e_dim) : vocab_size(v_size), embedding_dim(e_dim) {
            embedding_table.resize(vocab_size, std::vector<float>(embedding_dim, 0.0f));
        }

        void initialize_random_embeddings() {
            std::random_device rd;
            std::mt19937 gen(rd());
            std::uniform_real_distribution<float> dis(-0.5f, 0.5f);

            for (int i = 0; i < vocab_size; ++i) {
                for (int j = 0; j < embedding_dim; ++j) {
                    embedding_table[i][j] = dis(gen);
                }
            }
        }

        std::vector<float> lookup(int token_id) {
            if (token_id < 0 || token_id >= vocab_size) {
                return std::vector<float>(embedding_dim, 0.0f);
            }
            return embedding_table[token_id];
        }

        bool save_to_disk(const std::string& filename) {
            std::ofstream out_file(filename, std::ios::binary);
            if (!out_file) return false;
            for (int i = 0; i < vocab_size; ++i) {
                out_file.write(reinterpret_cast<const char*>(embedding_table[i].data()), embedding_dim * sizeof(float));
            }
            out_file.close();
            return true;
        }

        bool load_from_disk(const std::string& filename) {
            std::ifstream in_file(filename, std::ios::binary);
            if (!in_file) return false;
            for (int i = 0; i < vocab_size; ++i) {
                in_file.read(reinterpret_cast<char*>(embedding_table[i].data()), embedding_dim * sizeof(float));
            }
            in_file.close();
            return true;
        }
    };

    class ActivationLayer {
    public:
        std::vector<float> softmax(const std::vector<float>& raw_scores, float temperature) {
            std::vector<float> probabilities(raw_scores.size());
            float sum_exp = 0.0f;

            if (temperature < 0.1f) temperature = 0.1f;

            for (size_t i = 0; i < raw_scores.size(); ++i) {
                probabilities[i] = std::exp(raw_scores[i] / temperature);
                sum_exp += probabilities[i];
            }

            for (size_t i = 0; i < probabilities.size(); ++i) {
                probabilities[i] /= sum_exp;
            }

            return probabilities;
        }
    };

    int TensorEngine::predict_next_token(const std::vector<int>& tokens) {
        if (tokens.empty()) return 3; // Default to [EOS]

        int vocab_size = 96;
        int embed_dim = 96;
        int context_window_size = 8; // Lookback window limit

        std::string weights_file = "/media/mr-fontaine/R/RECOVERY/Coding/fontana/fontana_weights.bin";
        std::string embed_file = "/media/mr-fontaine/R/RECOVERY/Coding/fontana/fontana_embeddings.bin";

        EmbeddingLayer embed(vocab_size, embed_dim);
        WeightMatrix neural_gate(vocab_size, embed_dim);
        ActivationLayer activation;

        if (!embed.load_from_disk(embed_file)) {
            embed.initialize_random_embeddings();
            embed.save_to_disk(embed_file);
        }

        if (!neural_gate.load_from_disk(weights_file)) {
            neural_gate.initialize_weights();
            neural_gate.save_to_disk(weights_file);
        }

        // FIXED: FIXED CONTEXT MEMORY LAYER.
        // We aggregate up to 8 tokens from our history to build a mean-pooled context token coordinate vector.
        std::vector<float> context_vector(embed_dim, 0.0f);
        int tokens_to_scan = std::min(context_window_size, (int)tokens.size());
        int start_idx = tokens.size() - tokens_to_scan;

        for (int i = start_idx; i < (int)tokens.size(); ++i) {
            std::vector<float> single_embed = embed.lookup(tokens[i]);
            for (int j = 0; j < embed_dim; ++j) {
                context_vector[j] += single_embed[j];
            }
        }
        // Divide by total token count to complete the mean pool average allocation
        for (int j = 0; j < embed_dim; ++j) {
            context_vector[j] /= (float)tokens_to_scan;
        }

        std::vector<float> raw_scores(vocab_size, 0.0f);

        for (int i = 0; i < vocab_size; ++i) {
            std::vector<float>& word_weights = neural_gate.forward_layer(i);
            float score = 0.0f;
            for (int j = 0; j < embed_dim; ++j) {
                score += context_vector[j] * word_weights[j]; // Evaluate matrix against whole sentence context
            }
            raw_scores[i] = score;
        }

        std::vector<float> token_probabilities = activation.softmax(raw_scores, 0.8f);

        std::random_device rd;
        std::mt19937 gen(rd());
        std::discrete_distribution<int> dice_roller(token_probabilities.begin(), token_probabilities.end());

        int predicted_token_id = dice_roller(gen);

        return predicted_token_id;
    }

    void TensorEngine::process_tokens(const std::vector<int>& tokens) {}

    TensorEngine::TensorEngine() {}
    TensorEngine::~TensorEngine() {}
}

int main() {
    std::string input_line;
    if (std::getline(std::cin, input_line)) {
        std::vector<int> received_tokens;
        std::stringstream ss(input_line);
        int token_id;

        while (ss >> token_id) {
            received_tokens.push_back(token_id);
        }

        Fontana::TensorEngine engine;
        int next_token = engine.predict_next_token(received_tokens);
        std::cout << next_token << std::endl;
    }
    return 0;
}
