#pragma once

#include <cmath>
#include <stdexcept>
#include <unordered_map>
#include <vector>

#include "shunting_yard.hpp"

inline double evaluate_rpn(const std::vector<Token> &rpn, const std::unordered_map<std::string, double> &vars = {}) {
    std::vector<double> stack;

    for (const Token &tok : rpn) {
        if (tok.type == TokenType::Number) {
            stack.push_back(tok.number);
        } else if (tok.type == TokenType::Identifier) {
            auto it = vars.find(tok.text);
            if (it == vars.end()) throw std::runtime_error("undefined variable: " + tok.text);
            stack.push_back(it->second);
        } else if (tok.type == TokenType::Operator) {
            if (tok.text == "u-") {
                if (stack.empty()) throw std::runtime_error("malformed expression");
                double a = stack.back();
                stack.back() = -a;
                continue;
            }
            if (stack.size() < 2) throw std::runtime_error("malformed expression");
            double b = stack.back(); stack.pop_back();
            double a = stack.back(); stack.pop_back();

            double result;
            if (tok.text == "+") result = a + b;
            else if (tok.text == "-") result = a - b;
            else if (tok.text == "*") result = a * b;
            else if (tok.text == "/") result = a / b;
            else if (tok.text == "^") result = std::pow(a, b);
            else throw std::runtime_error("unknown operator: " + tok.text);

            stack.push_back(result);
        }
    }

    if (stack.size() != 1) throw std::runtime_error("malformed expression");
    return stack[0];
}

inline double evaluate(const std::string &expr, const std::unordered_map<std::string, double> &vars = {}) {
    return evaluate_rpn(to_rpn(tokenize(expr)), vars);
}
