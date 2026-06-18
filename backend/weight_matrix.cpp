#include "weight_matrix.hpp"
#include <iostream>
#include <vector>
#include <cmath>
#include <random>
#include <fstream>

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

    // FIXED: Returns a direct reference to the row inside the matrix container
    std::vector<float>& WeightMatrix::forward_layer(int token_id) {
        if (token_id < 0 || token_id >= vocab_size) {
            // Static fallback safe block
            static std::vector<float> fallback(embedding_dim, 0.0f);
            return fallback;
        }
        return matrix[token_id];
    }

    bool WeightMatrix::save_to_disk(const std::string& filename) {
        std::ofstream out_file(filename, std::ios::binary);
        if (!out_file) return false;

        for (int i = 0; i < vocab_size; ++i) {
            out_file.write(reinterpret_cast<const char*>(matrix[i].data()), embedding_dim * sizeof(float));
        }
        out_file.close();
        return true;
    }

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
