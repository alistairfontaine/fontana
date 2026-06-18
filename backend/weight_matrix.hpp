#ifndef WEIGHT_MATRIX_HPP
#define WEIGHT_MATRIX_HPP

#include <vector>
#include <string>

namespace Fontana {
    class WeightMatrix {
    private:
        int vocab_size;
        int embedding_dim;
        std::vector<std::vector<float>> matrix;

    public:
        WeightMatrix(int v_size, int e_dim);
        ~WeightMatrix();

        void initialize_weights();
        std::vector<float> forward_layer(int token_id);

        // NEW: Direct file-system serialization protocols
        bool save_to_disk(const std::string& filename);
        bool load_from_disk(const std::string& filename);
    };
}

#endif // WEIGHT_MATRIX_HPP
