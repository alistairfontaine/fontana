#ifndef WEIGHT_MATRIX_HPP
#define WEIGHT_MATRIX_HPP

#include <vector>

namespace Fontana {
    class WeightMatrix {
    private:
        int vocab_size;
        int embedding_dim;
        // Two-dimensional grid representing our neural connection weights
        std::vector<std::vector<float>> matrix;

    public:
        WeightMatrix(int v_size, int e_dim);
        ~WeightMatrix();

        // Initializes the matrix weights with a controlled mathematical pattern
        void initialize_weights();

        // Performs vector dot-product multiplication against an incoming token ID
        std::vector<float> forward_layer(int token_id);
    };
}

#endif // WEIGHT_MATRIX_HPP
