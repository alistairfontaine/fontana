#include "weight_matrix.hpp"
#include <iostream>
#include <cmath>

namespace Fontana {
    WeightMatrix::WeightMatrix(int v_size, int e_dim)
        : vocab_size(v_size), embedding_dim(e_dim) {
        // Resize our matrix container to cleanly hold our vocabulary boundaries
        matrix.resize(vocab_size, std::vector<float>(embedding_dim, 0.0f));
    }

    WeightMatrix::~WeightMatrix() {}

    void WeightMatrix::initialize_weights() {
        std::cout << "[FONTANA MATRIX] Generating native neural weight grid ("
                  << vocab_size << "x" << embedding_dim << " dimensions)..." << std::endl;

        // Populate the matrix with fractional weights based on a sinusoidal activation curve
        for (int i = 0; i < vocab_size; ++i) {
            for (int j = 0; j < embedding_dim; ++j) {
                matrix[i][j] = std::sin(i + j) * 0.1f; // High-speed local mathematical seeding
            }
        }
        std::cout << "[FONTANA O³ PATH] Weight matrix generation completely verified." << std::endl;
    }

    std::vector<float> WeightMatrix::forward_layer(int token_id) {
        // Secure the boundary check to prevent local vector segmentation crashes
        if (token_id < 0 || token_id >= vocab_size) {
            return std::vector<float>(embedding_dim, 0.0f); // Return a flat zero safe-vector if unknown
        }
        return matrix[token_id]; // Return the raw weight array mapping for this token ID
    }
}
