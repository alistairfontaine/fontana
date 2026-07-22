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

    int TensorEngine::predict_next_token(const std::vector<int>& tokens, float custom_temp, int custom_k) {

        if (tokens.empty()) return 3;

        const std::vector<int>& active_tokens = tokens;
        int vocab_size = 107;
        int embed_dim = 512;
        int context_window_size = 12;

        std::string weights_file = "/media/mr-fontaine/R/RECOVERY/Coding/fontana/fontana_weights.bin";
        std::string embed_file = "/media/mr-fontaine/R/RECOVERY/Coding/fontana/fontana_embeddings.bin";

        EmbeddingLayer embed(vocab_size, embed_dim);
        WeightMatrix neural_gate(vocab_size, embed_dim);
        ActivationLayer activation;

        embed.load_from_disk(embed_file);
        neural_gate.load_from_disk(weights_file);

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

            // Stable Linear Decay Loop
            if (active_tokens.size() > 3) {
                for (size_t t = 3; t < active_tokens.size(); ++t) {
                    if (active_tokens[t] == i) {
                        float distance = static_cast<float>(active_tokens.size() - 1 - t);
                        raw_scores[i] -= (2.5f / (1.0f + 0.15f * distance));
                    }
                }
            }
        }

        // FIXED: PHASE O - INTERPROCESS PARAMETRIC FLOORS
        // Dynamically applies user-adjustable slider values passed natively over IPC pipelines
        // to grant front-end sliders total control over neural matrix distributions in real-time.
        float dynamic_temperature = custom_temp;
        std::vector<float> token_probabilities = activation.softmax(raw_scores, dynamic_temperature);

        int K = std::max(1, std::min(vocab_size, custom_k));

        std::vector<size_t> indices(vocab_size);
        std::iota(indices.begin(), indices.end(), 0);

        std::sort(indices.begin(), indices.end(), [&](size_t a, size_t b) {
            return token_probabilities[a] > token_probabilities[b];
        });

        for (int i = K; i < vocab_size; ++i) {
            token_probabilities[indices[i]] = 0.0f;
        }

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
    std::string input_line;
    while (std::getline(std::cin, input_line)) {
        if (input_line.empty()) continue;

        // FIXED: PHASE O - STREAM UNBUNDLING AND PIPELINE DELIMITER PARSER
        // Safely extracts the token strings, parsing the pipe delimiter without throwing a stream panic.
        std::stringstream ss(input_line);
        std::string tokens_part, delimiter, temp_part, topk_part;

        std::getline(ss, tokens_part, '|');

        std::vector<int> received_tokens;
        std::stringstream tokens_stream(tokens_part);
        int token_id;
        while (tokens_stream >> token_id) {
            received_tokens.push_back(token_id);
        }

        float slider_temperature = 0.32f; // High-integrity production default fallbacks
        int slider_top_k = 6;

        if (std::getline(ss, temp_part, '|')) {
            std::stringstream(temp_part) >> slider_temperature;
        }
        if (std::getline(ss, topk_part)) {
            std::stringstream(topk_part) >> slider_top_k;
        }

        Fontana::TensorEngine engine;
        int next_token = engine.predict_next_token(received_tokens, slider_temperature, slider_top_k);
        std::cout << next_token << std::endl;

    }
    return 0;
}

