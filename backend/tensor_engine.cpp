#include "tensor_engine.hpp"
#include "weight_matrix.cpp"
#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <cmath>
#include <numeric>
#include <algorithm> // Needed for std::max_element

namespace Fontana {
    TensorEngine::TensorEngine() {}
    TensorEngine::~TensorEngine() {}

    class ActivationLayer {
    public:
        std::vector<float> softmax(const std::vector<float>& raw_scores) {
            std::vector<float> probabilities(raw_scores.size());
            float sum_exp = 0.0f;

            for (size_t i = 0; i < raw_scores.size(); ++i) {
                probabilities[i] = std::exp(raw_scores[i]);
                sum_exp += probabilities[i];
            }

            for (size_t i = 0; i < probabilities.size(); ++i) {
                probabilities[i] /= sum_exp;
            }

            return probabilities;
        }
    };

    // This function now returns the single best next token ID predicted by the matrix
    int TensorEngine::predict_next_token(const std::vector<int>& tokens) {
        if (tokens.empty()) return 3; // Default to [EOS] if empty

        WeightMatrix neural_gate(80, 4);
        neural_gate.initialize_weights();
        ActivationLayer activation;

        // Fetch the raw weights for the absolute LAST token in the current sentence
        int last_token = tokens.back();
        std::vector<float> raw_weights = neural_gate.forward_layer(last_token);

        // Pass it through Softmax to get percentages
        std::vector<float> token_probabilities = activation.softmax(raw_weights);

        // Find the index of the highest probability value (ArgMax)
        auto max_iter = std::max_element(token_probabilities.begin(), token_probabilities.end());
        int predicted_token_id = std::distance(token_probabilities.begin(), max_iter);

        return predicted_token_id;
    }

    // Keep our older process method alive for backward logging compatibility
    void TensorEngine::process_tokens(const std::vector<int>& tokens) {
        // Log display code managed by engine script
    }
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
        // Calculate the next token math
        int next_token = engine.predict_next_token(received_tokens);

        // CRUCIAL: Print ONLY the raw numerical integer ID back to the Linux stream for Python
        std::cout << next_token << std::endl;
    }
    return 0;
}
