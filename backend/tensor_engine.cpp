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
    };

    class ActivationLayer {
    public:
        // Softmax with Temperature scaling
        std::vector<float> softmax(const std::vector<float>& raw_scores, float temperature) {
            std::vector<float> probabilities(raw_scores.size());
            float sum_exp = 0.0f;

            // Prevent dividing by zero if temperature is set too low
            if (temperature < 0.1f) temperature = 0.1f;

            for (size_t i = 0; i < raw_scores.size(); ++i) {
                // Scale raw vectors by temperature before running exponentials
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

        int vocab_size = 80;
        int embed_dim = 4;

        EmbeddingLayer embed(vocab_size, embed_dim);
        WeightMatrix neural_gate(vocab_size, embed_dim);
        neural_gate.initialize_weights();
        ActivationLayer activation;

        int last_token = tokens.back();

        std::vector<float> embedded_vector = embed.lookup(last_token);
        std::vector<float> matrix_weights = neural_gate.forward_layer(last_token);

        // FIXED: Expanded raw scores vector array container to scan all 80 vocabulary channels!
        std::vector<float> raw_scores(vocab_size, 0.0f);

        // Compute scores across the entire vocabulary grid
        for (int i = 0; i < vocab_size; ++i) {
            std::vector<float> word_weights = neural_gate.forward_layer(i);
            float score = 0.0f;
            for (int j = 0; j < embed_dim; ++j) {
                score += embedded_vector[j] * word_weights[j];
            }
            raw_scores[i] = score;
        }

        // Run Softmax with a default operational temperature configuration of 0.7
        std::vector<float> token_probabilities = activation.softmax(raw_scores, 0.7f);

        auto max_iter = std::max_element(token_probabilities.begin(), token_probabilities.end());
        int predicted_token_id = std::distance(token_probabilities.begin(), max_iter);

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
