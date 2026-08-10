#pragma once

#include <cctype>
#include <stdexcept>
#include <string>
#include <vector>

enum class TokenType { Number, Identifier, Operator, LParen, RParen };

struct Token {
    TokenType type;
    std::string text;
    double number = 0.0;
};

inline std::vector<Token> tokenize(const std::string &expr) {
    std::vector<Token> tokens;
    size_t i = 0;

    while (i < expr.size()) {
        char c = expr[i];

        if (std::isspace(static_cast<unsigned char>(c))) {
            i++;
        } else if (std::isdigit(static_cast<unsigned char>(c)) || c == '.') {
            size_t start = i;
            while (i < expr.size() && (std::isdigit(static_cast<unsigned char>(expr[i])) || expr[i] == '.')) i++;
            std::string text = expr.substr(start, i - start);
            tokens.push_back({TokenType::Number, text, std::stod(text)});
        } else if (std::isalpha(static_cast<unsigned char>(c)) || c == '_') {
            size_t start = i;
            while (i < expr.size() && (std::isalnum(static_cast<unsigned char>(expr[i])) || expr[i] == '_')) i++;
            tokens.push_back({TokenType::Identifier, expr.substr(start, i - start)});
        } else if (c == '(') {
            tokens.push_back({TokenType::LParen, "("});
            i++;
        } else if (c == ')') {
            tokens.push_back({TokenType::RParen, ")"});
            i++;
        } else if (std::string("+-*/^").find(c) != std::string::npos) {
            tokens.push_back({TokenType::Operator, std::string(1, c)});
            i++;
        } else {
            throw std::runtime_error(std::string("unexpected character '") + c + "' in expression");
        }
    }

    return tokens;
}
