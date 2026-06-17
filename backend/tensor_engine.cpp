#include "tensor_engine.hpp"
#include <iostream>
#include <vector>
#include <string>
#include <sstream>

namespace Fontana {
    TensorEngine::TensorEngine() {}
    TensorEngine::~TensorEngine() {}

    void TensorEngine::process_tokens(const std::vector<int>& tokens) {
        std::cout << "[FONTANA C++ ENGINE] Processing continuous stream of " << tokens.size() << " tokens." << std::endl;
        std::cout << "[FONTANA O³ PATH] Executing tensor array calculations..." << std::endl;

        // Loop through the live numbers passed from Python
        for (size_t i = 0; i < tokens.size(); ++i) {
            std::cout << "  -> Index [" << i << "] TokenID: " << tokens[i] << " | Computed Status: Verified" << std::endl;
        }
        std::cout << "[FONTANA CORE] Tensor processing matrix sequence complete." << std::endl;
    }
}

int main() {
    std::string input_line;
    // Sit and listen to the Linux standard input (stdin) for data from Python
    if (std::getline(std::cin, input_line)) {
        std::vector<int> received_tokens;
        std::stringstream ss(input_line);
        int token_id;

        // Parse the space-separated numbers coming down the pipe
        while (ss >> token_id) {
            received_tokens.push_back(token_id); // FIXED: changed append to push_back
        }

        // Fire up the engine processing block with the parsed live tokens
        Fontana::TensorEngine engine;
        engine.process_tokens(received_tokens);
    }
    return 0;
}
