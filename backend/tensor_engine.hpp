#ifndef TENSOR_ENGINE_HPP
#define TENSOR_ENGINE_HPP

#include <vector>

namespace Fontana {
    class TensorEngine {
    public:
        TensorEngine();
        ~TensorEngine();
        int predict_next_token(const std::vector<int>& tokens, float custom_temp, int custom_k, float custom_p);

        void process_tokens(const std::vector<int>& tokens);
    };
}

#endif // TENSOR_ENGINE_HPP
