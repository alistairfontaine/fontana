#include "tensor_engine.hpp"
#include "weight_matrix.cpp"
#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <cmath>
#include <numeric>

namespace Fontana {
    // FIXED: Added missing constructor and destructor implementations back for the linker
    TensorEngine::TensorEngine() {}
    TensorEngine::~TensorEngine() {}

    class ActivationLayer {
    public:
        // Softmax converts raw fractional vectors into clean probability distributions (0.0 to 1.0)
        std::vector<float> softmax(const std::vector<float>& raw_scores) {
            std::vector<float> probabilities(raw_scores.size());
            float sum_exp = 0.0f;

            // 1. Calculate the exponential of each score to eliminate negative numbers
            for (size_t i = 0; i < raw_scores.size(); ++i) {
                probabilities[i] = std::exp(raw_scores[i]);
                sum_exp += probabilities[i];
            }

            // 2. Normalize by dividing each element by the total sum
            for (size_t i = 0; i < probabilities.size(); ++i) {
                probabilities[i] /= sum_exp;
            }

            return probabilities;
        }
    };

    void TensorEngine::process_tokens(const std::vector<int>& tokens) {
        std::cout << "[FONTANA C++ ENGINE] Processing continuous stream of " << tokens.size() << " tokens." << std::endl;

        WeightMatrix neural_gate(80, 4);
        neural_gate.initialize_weights();
        ActivationLayer activation;

        std::cout << "\n[FONTANA NEURAL NET PROBABILITIES (SOFTMAX)]:" << std::endl;

        // Loop through our live tokens, fetch their weights, and pass them through Softmax
        for (size_t i = 0; i < tokens.size(); ++i) {
            int current_token = tokens[i];
            std::vector<float> raw_weights = neural_gate.forward_layer(current_token);

            // Fire the vector down the Softmax activation pipeline
            std::vector<float> token_probabilities = activation.softmax(raw_weights);

            std::cout << "  Token Index [" << i << "] ID: " << current_token << " -> Probability Matrix: [";
            for (float prob : token_probabilities) {
                // Format output to show clean percentage arrays
                std::cout << " " << std::round(prob * 100.0f) << "%";
            }
            std::cout << " ]" << std::endl;
        }
        std::cout << "\n[FONTANA O³ PATH] Activation layer processing matrix complete." << std::endl;
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
        engine.process_tokens(received_tokens);
    }
    return 0;
}
