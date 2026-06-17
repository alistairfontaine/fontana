#ifndef TENSOR_ENGINE_HPP
#define TENSOR_ENGINE_HPP

#include <vector>
#include <string>

namespace Fontana {
    class TensorEngine {
    public:
        TensorEngine();
        ~TensorEngine();

        // High-speed processing signature for your text token integers
        void process_tokens(const std::vector<int>& tokens);
    };
}

#endif // TENSOR_ENGINE_HPP
