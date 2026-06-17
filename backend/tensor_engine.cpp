#include "tensor_engine.hpp"
#include "weight_matrix.cpp" // Direct local implementation inclusion
#include <iostream>
#include <vector>
#include <string>
#include <sstream>

namespace Fontana {
    TensorEngine::TensorEngine() {}
    TensorEngine::~TensorEngine() {}

    void TensorEngine::process_tokens(const std::vector<int>& tokens) {
        std::cout << "[FONTANA C++ ENGINE] Processing continuous stream of " << tokens.size() << " tokens." << std::endl;

        // Initialize a local 80-word vocabulary with a 4-dimension neural vector weight layout
        WeightMatrix neural_gate(80, 4);
        neural_gate.initialize_weights();

        std::cout << "\n[FONTANA NEURAL MULTIPLICATION LOGS]:" << std::endl;
        // Step through each live token and run it through our matrix network
        for (size_t i = 0; i < tokens.size(); ++i) {
            int current_token = tokens[i];
            std::vector<float> dynamic_vector = neural_gate.forward_layer(current_token);

            std::cout << "  Token index [" << i << "] ID: " << current_token << " -> Weights Vector: [";
            for (float weight : dynamic_vector) {
                std::cout << " " << weight;
            }
            std::cout << " ]" << std::endl;
        }
        std::cout << "\n[FONTANA CORE] Neural tensor array sequence processing complete." << std::endl;
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
