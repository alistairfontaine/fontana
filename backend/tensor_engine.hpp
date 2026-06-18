#ifndef TENSOR_ENGINE_HPP
#define TENSOR_ENGINE_HPP

#include <vector>
#include <string>

namespace Fontana {
    class TensorEngine {
    public:
        TensorEngine();
        ~TensorEngine();

        void process_tokens(const std::vector<int>& tokens);
        int predict_next_token(const std::vector<int>& tokens);
    };
}

#endif // TENSOR_ENGINE_HPP
