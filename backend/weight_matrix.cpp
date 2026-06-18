#include "weight_matrix.hpp"
#include <iostream>
#include <vector>
#include <cmath>
#include <random>
#include <fstream> // Required for direct file stream operations

namespace Fontana {
    WeightMatrix::WeightMatrix(int v_size, int e_dim)
        : vocab_size(v_size), embedding_dim(e_dim) {
        matrix.resize(vocab_size, std::vector<float>(embedding_dim, 0.0f));
    }

    WeightMatrix::~WeightMatrix() {}

    void WeightMatrix::initialize_weights() {
        std::random_device rd;
        std::mt19937 gen(rd());
        std::uniform_real_distribution<float> dis(-0.5f, 0.5f);

        for (int i = 0; i < vocab_size; ++i) {
            for (int j = 0; j < embedding_dim; ++j) {
                matrix[i][j] = dis(gen);
            }
        }
    }

    std::vector<float> WeightMatrix::forward_layer(int token_id) {
        if (token_id < 0 || token_id >= vocab_size) {
            return std::vector<float>(embedding_dim, 0.0f);
        }
        return matrix[token_id];
    }

    // NEW: Save the neural weight tensors to a local binary storage file
    bool WeightMatrix::save_to_disk(const std::string& filename) {
        std::ofstream out_file(filename, std::ios::binary);
        if (!out_file) return false;

        // Iterate and write the raw float blocks to disk with zero overhead
        for (int i = 0; i < vocab_size; ++i) {
            out_file.write(reinterpret_cast<const char*>(matrix[i].data()), embedding_dim * sizeof(float));
        }
        out_file.close();
        return true;
    }

    // NEW: Load the pre-saved neural weights directly back into the working RAM memory
    bool WeightMatrix::load_from_disk(const std::string& filename) {
        std::ifstream in_file(filename, std::ios::binary);
        if (!in_file) return false;

        for (int i = 0; i < vocab_size; ++i) {
            in_file.read(reinterpret_cast<char*>(matrix[i].data()), embedding_dim * sizeof(float));
        }
        in_file.close();
        return true;
    }
}
