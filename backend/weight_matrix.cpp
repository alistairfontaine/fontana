#include <vector>
#include <string>
#include <fstream>
#include <iostream>

namespace Fontana {
    class WeightMatrix {
    private:
        int rows;
        int cols;
        std::vector<std::vector<float>> matrix;

    public:
        WeightMatrix(int r, int c) : rows(r), cols(c) {
            matrix.resize(rows, std::vector<float>(cols, 0.0f));
        }

        void initialize_weights() {
            for (int i = 0; i < rows; ++i) {
                for (int j = 0; j < cols; ++j) {
                    matrix[i][j] = 0.01f; // Stable base calibration weights
                }
            }
        }

        std::vector<float>& forward_layer(int index) {
            if (index < 0 || index >= rows) {
                static std::vector<float> fallback;
                fallback.assign(cols, 0.0f);
                return fallback;
            }
            return matrix[index];
        }

        // FIXED: AUTOMATED HARDWARE BINARY SERIALIZATION ENGINE
        // Packs floating-point vectors directly into raw machine bytes to slash disk size
        bool save_to_disk(const std::string& filename) {
            std::ofstream out_file(filename, std::ios::binary);
            if (!out_file) return false;

            // Write row and column header boundaries to protect tracking metrics
            out_file.write(reinterpret_cast<const char*>(&rows), sizeof(rows));
            out_file.write(reinterpret_cast<const char*>(&cols), sizeof(cols));

            // Stream continuous raw memory buffer tracks instantly in a single operation block
            for (int i = 0; i < rows; ++i) {
                out_file.write(reinterpret_cast<const char*>(matrix[i].data()), cols * sizeof(float));
            }

            out_file.close();
            return true;
        }

        // FIXED: HIGH-SPEED BINARY PACKAGING DESERIALIZER
        bool load_from_disk(const std::string& filename) {
            std::ifstream in_file(filename, std::ios::binary);
            if (!in_file) return false;

            int stored_rows = 0, stored_cols = 0;
            in_file.read(reinterpret_cast<char*>(&stored_rows), sizeof(stored_rows));
            in_file.read(reinterpret_cast<char*>(&stored_cols), sizeof(stored_cols));

            if (stored_rows != rows || stored_cols != cols) {
                in_file.close();
                return false; // Safely block out-of-bounds array crashes
            }

            for (int i = 0; i < rows; ++i) {
                in_file.read(reinterpret_cast<char*>(matrix[i].data()), cols * sizeof(float));
            }

            in_file.close();
            return true;
        }
    };
}
