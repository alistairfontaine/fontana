#include "weight_matrix.hpp"
#include <iostream>
#include <vector>
#include <cmath>
#include <random> // Added for high-quality hardware random seeding

namespace Fontana {
    WeightMatrix::WeightMatrix(int v_size, int e_dim)
        : vocab_size(v_size), embedding_dim(e_dim) {
        matrix.resize(vocab_size, std::vector<float>(embedding_dim, 0.0f));
    }

    WeightMatrix::~WeightMatrix() {}

    void WeightMatrix::initialize_weights() {
        // Setup a standard hardware random device seed
        std::random_device rd;
        std::mt19937 gen(rd());
        // Distribute weights evenly between -0.5 and 0.5 (standard AI initialization)
        std::uniform_real_distribution<float> dis(-0.5f, 0.5f);

        for (int i = 0; i < vocab_size; ++i) {
            for (int j = 0; j < embedding_dim; ++j) {
                matrix[i][j] = dis(gen); // FIXED: Matrix is now seeded randomly!
            }
        }
    }

    std::vector<float> WeightMatrix::forward_layer(int token_id) {
        if (token_id < 0 || token_id >= vocab_size) {
            return std::vector<float>(embedding_dim, 0.0f);
        }
        return matrix[token_id];
    }
}
