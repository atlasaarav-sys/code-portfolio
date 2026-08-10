#pragma once

#include <stdexcept>
#include <vector>

#include "tokenizer.hpp"

inline int precedence(const std::string &op) {
    if (op == "u-") return 4; // unary minus binds tighter than binary ops except ^
    if (op == "^") return 3;
    if (op == "*" || op == "/") return 2;
    if (op == "+" || op == "-") return 1;
    return -1;
}

inline bool right_associative(const std::string &op) {
    return op == "^" || op == "u-";
}

// Converts infix tokens to RPN (Reverse Polish Notation) order.
inline std::vector<Token> to_rpn(const std::vector<Token> &infix) {
    std::vector<Token> output;
    std::vector<Token> op_stack;

    for (size_t i = 0; i < infix.size(); i++) {
        const Token &tok = infix[i];

        if (tok.type == TokenType::Number || tok.type == TokenType::Identifier) {
            output.push_back(tok);
        } else if (tok.type == TokenType::Operator) {
            std::string op = tok.text;

            // Detect unary minus: a '-' is unary if it's the first token,
            // or the previous token is an operator or '('.
            bool is_unary_minus = (op == "-") &&
                (i == 0 || infix[i - 1].type == TokenType::Operator || infix[i - 1].type == TokenType::LParen);
            if (is_unary_minus) op = "u-";

            while (!op_stack.empty() && op_stack.back().type == TokenType::Operator &&
                   ((right_associative(op) && precedence(op) < precedence(op_stack.back().text)) ||
                    (!right_associative(op) && precedence(op) <= precedence(op_stack.back().text)))) {
                output.push_back(op_stack.back());
                op_stack.pop_back();
            }
            op_stack.push_back({TokenType::Operator, op});
        } else if (tok.type == TokenType::LParen) {
            op_stack.push_back(tok);
        } else if (tok.type == TokenType::RParen) {
            while (!op_stack.empty() && op_stack.back().type != TokenType::LParen) {
                output.push_back(op_stack.back());
                op_stack.pop_back();
            }
            if (op_stack.empty()) throw std::runtime_error("mismatched parentheses");
            op_stack.pop_back(); // discard the '('
        }
    }

    while (!op_stack.empty()) {
        if (op_stack.back().type == TokenType::LParen) throw std::runtime_error("mismatched parentheses");
        output.push_back(op_stack.back());
        op_stack.pop_back();
    }

    return output;
}
