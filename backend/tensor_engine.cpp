#include "tensor_engine.hpp"
#include "weight_matrix.cpp"
#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <cmath>
#include <numeric>
#include <algorithm>
#include <random>
#include <fstream>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

namespace Fontana {

    class EmbeddingLayer {
    private:
        int vocab_size;
        int embedding_dim;
        std::vector<std::vector<float>> embedding_table;

    public:
        EmbeddingLayer(int v_size, int e_dim) : vocab_size(v_size), embedding_dim(e_dim) {
            embedding_table.resize(vocab_size, std::vector<float>(embedding_dim, 0.0f));
        }

        void initialize_random_embeddings() {
            std::random_device rd;
            std::mt19937 gen(rd());
            std::uniform_real_distribution<float> dis(-0.5f, 0.5f);

            for (int i = 0; i < vocab_size; ++i) {
                for (int j = 0; j < embedding_dim; ++j) {
                    embedding_table[i][j] = dis(gen);
                }
            }
        }

        std::vector<float> lookup(int token_id) {
            if (token_id < 0 || token_id >= vocab_size) {
                return std::vector<float>(embedding_dim, 0.0f);
            }
            return embedding_table[token_id];
        }

        bool save_to_disk(const std::string& filename) {
            std::ofstream out_file(filename, std::ios::binary);
            if (!out_file) return false;
            for (int i = 0; i < vocab_size; ++i) {
                out_file.write(reinterpret_cast<const char*>(embedding_table[i].data()), embedding_dim * sizeof(float));
            }
            out_file.close();
            return true;
        }

        bool load_from_disk(const std::string& filename) {
            std::ifstream in_file(filename, std::ios::binary);
            if (!in_file) return false;
            for (int i = 0; i < vocab_size; ++i) {
                in_file.read(reinterpret_cast<char*>(embedding_table[i].data()), embedding_dim * sizeof(float));
            }
            in_file.close();
            return true;
        }
    };

    class ActivationLayer {
    public:
        std::vector<float> softmax(const std::vector<float>& raw_scores, float temperature) {
            std::vector<float> probabilities(raw_scores.size());
            float sum_exp = 0.0f;

            if (temperature < 0.04f) temperature = 0.04f;

            for (size_t i = 0; i < raw_scores.size(); ++i) {
                probabilities[i] = std::exp(raw_scores[i] / temperature);
                sum_exp += probabilities[i];
            }

            for (size_t i = 0; i < probabilities.size(); ++i) {
                probabilities[i] /= sum_exp;
            }

            return probabilities;
        }
    };

    int TensorEngine::predict_next_token(const std::vector<int>& tokens) {
        if (tokens.empty()) return 3;

        const std::vector<int>& active_tokens = tokens;

        int vocab_size = 107;
        std::string meta_path = "/media/mr-fontaine/R/RECOVERY/Coding/fontana/core/vocab_meta.json";
        std::ifstream meta_file(meta_path);

        if (meta_file.is_open()) {
            std::string line;
            if (std::getline(meta_file, line)) {
                size_t pos = line.find("vocab_size\":");
                if (pos != std::string::npos) {
                    std::string size_str = line.substr(pos + 12);
                    size_str = size_str.substr(0, size_str.find("}"));
                    vocab_size = std::stoi(size_str);
                }
            }
            meta_file.close();
        }

        int embed_dim = 512;
        int context_window_size = 12;

        std::string weights_file = "/media/mr-fontaine/R/RECOVERY/Coding/fontana/fontana_weights.bin";
        std::string embed_file = "/media/mr-fontaine/R/RECOVERY/Coding/fontana/fontana_embeddings.bin";

        EmbeddingLayer embed(vocab_size, embed_dim);
        WeightMatrix neural_gate(vocab_size, embed_dim);
        ActivationLayer activation;

        if (!embed.load_from_disk(embed_file)) {
            embed.initialize_random_embeddings();
            embed.save_to_disk(embed_file);
        }

        if (!neural_gate.load_from_disk(weights_file)) {
            neural_gate.initialize_weights();
            neural_gate.save_to_disk(weights_file);
        }

        std::vector<float> context_vector(embed_dim, 0.0f);
        int tokens_to_scan = std::min(context_window_size, (int)active_tokens.size());
        int start_idx = active_tokens.size() - tokens_to_scan;

        for (int i = start_idx; i < (int)active_tokens.size(); ++i) {
            std::vector<float> single_embed = embed.lookup(active_tokens[i]);
            for (int j = 0; j < embed_dim; ++j) {
                context_vector[j] += single_embed[j];
            }
        }
        for (int j = 0; j < embed_dim; ++j) {
            context_vector[j] /= (float)tokens_to_scan;
        }

        std::vector<float> raw_scores(vocab_size, 0.0f);

        for (int i = 0; i < vocab_size; ++i) {
            std::vector<float>& word_weights = neural_gate.forward_layer(i);
            float score = 0.0f;
            for (int j = 0; j < embed_dim; ++j) {
                score += context_vector[j] * word_weights[j];
            }
            raw_scores[i] = score;

            // Harmonic Linear Reciprocal Repetition Decay Gate
            if (active_tokens.size() > 3) {
                for (size_t t = 3; t < active_tokens.size(); ++t) {
                    if (active_tokens[t] == i) {
                        float distance = static_cast<float>(active_tokens.size() - 1 - t);
                        raw_scores[i] -= (2.5f / (1.0f + 0.15f * distance));
                    }
                }
            } else {
                for (int t : active_tokens) {
                    if (t == i) {
                        raw_scores[i] -= 0.5f;
                    }
                }
            }

            // Tightened character suppression mask
            if (i >= 5 && i <= 76) {
                if (i != 44 && i != 46 && i != 63) {
                    raw_scores[i] -= 4.5f;
                }
            }

            if (i == 0 || i == 1 || i == 2) {
                raw_scores[i] -= 10.0f;
            }
        }

        float dynamic_temperature = 0.12f;
        if (active_tokens.size() <= 4) {
            dynamic_temperature = 0.075f;
        } else {
            float sequence_decay_factor = 0.002f * static_cast<float>(active_tokens.size());
            dynamic_temperature = std::max(0.095f, 0.12f - sequence_decay_factor);
        }

        std::vector<float> token_probabilities = activation.softmax(raw_scores, dynamic_temperature);

        int K = 2;
        std::vector<size_t> indices(vocab_size);
        std::iota(indices.begin(), indices.end(), 0);

        std::sort(indices.begin(), indices.end(), [&](size_t a, size_t b) {
            return token_probabilities[a] > token_probabilities[b];
        });

        for (int i = K; i < vocab_size; ++i) {
            token_probabilities[indices[i]] = 0.0f;
        }

        // FIXED: CREATIVE ROADMAP STEP 1 - NATIVE C++ ADAPTIVE TOP-P DECAY SCHEDULER
        // Dynamically widen our nucleus selection pool ceiling as the sentence sequence stretches
        // to completely eliminate word starvation and maximize vocabulary creative variety.
        float base_top_p = 0.90f;
        float context_expansion_factor = 0.001f * static_cast<float>(active_tokens.size());
        float target_top_p = std::min(0.95f, base_top_p + context_expansion_factor);

        float cumulative_p = 0.0f;
        for (int i = 0; i < K; ++i) {
            cumulative_p += token_probabilities[indices[i]];
            if (cumulative_p > target_top_p) {
                for (int j = i + 1; j < K; ++j) {
                    token_probabilities[indices[j]] = 0.0f;
                }
                break;
            }
        }

        float prob_sum = 0.0f;
        for (int i = 0; i < K; ++i) prob_sum += token_probabilities[indices[i]];
        for (int i = 0; i < K; ++i) token_probabilities[indices[i]] /= prob_sum;

        std::random_device rd;
        std::mt19937 gen(rd());
        std::discrete_distribution<int> dice_roller(token_probabilities.begin(), token_probabilities.end());

        int predicted_token_id = dice_roller(gen);

        return predicted_token_id;
    }

    void TensorEngine::process_tokens(const std::vector<int>& tokens) {}

    TensorEngine::TensorEngine() {}
    TensorEngine::~TensorEngine() {}
}

int main() {
    std::string rx_pipe = "/tmp/fontana_rx.fifo";
    std::string tx_pipe = "/tmp/fontana_tx.fifo";

    unlink(rx_pipe.c_str());
    unlink(tx_pipe.c_str());

    mkfifo(rx_pipe.c_str(), 0666);
    mkfifo(tx_pipe.c_str(), 0666);

    std::cout << "🧭 [FONTANA DAEMON] Service loop initialized. Listening on IPC channels..." << std::endl;

    Fontana::TensorEngine engine;

    while (true) {
        int rx_fd = open(rx_pipe.c_str(), O_RDONLY);
        if (rx_fd < 0) continue;

        char buffer[1024]; // Explicit safe message track buffer
        ssize_t bytes_read = read(rx_fd, buffer, sizeof(buffer) - 1);
        close(rx_fd);

        if (bytes_read <= 0) continue;
        buffer[bytes_read] = '\0';

        std::string input_line(buffer);
        std::vector<int> received_tokens;
        std::stringstream ss(input_line);
        int token_id;

        while (ss >> token_id) {
            received_tokens.push_back(token_id);
        }

        int next_token = engine.predict_next_token(received_tokens);

        int tx_fd = open(tx_pipe.c_str(), O_WRONLY);
        if (tx_fd >= 0) {
            std::string out_str = std::to_string(next_token) + "\n";
            write(tx_fd, out_str.c_str(), out_str.size());
            close(tx_fd);
        }
    }
    return 0;
}
