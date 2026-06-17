#include "weight_matrix.hpp"
#include <iostream>
#include <cmath>

namespace Fontana {
    WeightMatrix::WeightMatrix(int v_size, int e_dim)
        : vocab_size(v_size), embedding_dim(e_dim) {
        matrix.resize(vocab_size, std::vector<float>(embedding_dim, 0.0f));
    }

    WeightMatrix::~WeightMatrix() {}

    void WeightMatrix::initialize_weights() {
        // COMMENTED OUT: Staging text removed to protect Python data stream
        // std::cout << "[FONTANA MATRIX] Generating native..." << std::endl;

        for (int i = 0; i < vocab_size; ++i) {
            for (int j = 0; j < embedding_dim; ++j) {
                matrix[i][j] = std::sin(i + j) * 0.1f;
            }
        }
        // std::cout << "[FONTANA O³ PATH] Verified..." << std::endl;
    }

    std::vector<float> WeightMatrix::forward_layer(int token_id) {
        if (token_id < 0 || token_id >= vocab_size) {
            return std::vector<float>(embedding_dim, 0.0f);
        }
        return matrix[token_id];
    }
}
