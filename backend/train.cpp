#include "weight_matrix.cpp"
#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <fstream>

namespace Fontana {
    class LocalTrainer {
    private:
        int vocab_size;
        int embedding_dim;

    public:
        LocalTrainer(int v_size, int e_dim) : vocab_size(v_size), embedding_dim(e_dim) {}

        void train_on_sequence(const std::vector<int>& tokens, const std::string& weights_path) {
            WeightMatrix neural_gate(vocab_size, embedding_dim);

            if (!neural_gate.load_from_disk(weights_path)) {
                neural_gate.initialize_weights();
            }

            std::cout << "[FONTANA TRAINER] Adjusting tensor connections across " << tokens.size() << " tokens..." << std::endl;

            for (size_t i = 0; i < tokens.size() - 1; ++i) {
                int current_token = tokens[i];
                int next_token = tokens[i + 1];

                if (current_token >= 0 && current_token < vocab_size && next_token >= 0 && next_token < vocab_size) {
                    // FIXED: Captures the reference explicitly using '&'
                    std::vector<float>& current_weights = neural_gate.forward_layer(current_token);

                    for (int j = 0; j < embedding_dim; ++j) {
                        current_weights[j] += 0.8f;
                        if (current_weights[j] > 5.0f) current_weights[j] = 5.0f;
                    }
                }
            }

            neural_gate.save_to_disk(weights_path);
            std::cout << "[FONTANA TRAINER] Optimization cycle complete. Memory updated on disk." << std::endl;
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
    // FIXED: Upgraded training tensor dimension matrix space from 4 to 96
    Fontana::LocalTrainer trainer(96, 96);
    trainer.train_on_sequence(tokens, weights_file);

    return 0;
}
