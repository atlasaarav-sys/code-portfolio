#pragma once

#include <stdexcept>
#include <string>

#include "regex_ast.hpp"

// Grammar (lowest to highest precedence):
//   alternation := concat ('|' concat)*
//   concat      := repeat*
//   repeat      := atom ('*' | '+' | '?')?
//   atom        := literal | '.' | '(' alternation ')'
class RegexParser {
public:
    explicit RegexParser(const std::string &pattern) : pattern_(pattern), pos_(0) {}

    RegexNodePtr parse() {
        RegexNodePtr node = parse_alternation();
        if (pos_ != pattern_.size()) {
            throw std::runtime_error("unexpected character at position " + std::to_string(pos_));
        }
        return node;
    }

private:
    const std::string &pattern_;
    size_t pos_;

    bool at_end() const { return pos_ >= pattern_.size(); }
    char peek() const { return pattern_[pos_]; }
    char advance() { return pattern_[pos_++]; }

    RegexNodePtr parse_alternation() {
        RegexNodePtr left = parse_concat();
        while (!at_end() && peek() == '|') {
            advance();
            RegexNodePtr right = parse_concat();
            auto alt = std::make_unique<RegexNode>(NodeType::Alternation);
            alt->children.push_back(std::move(left));
            alt->children.push_back(std::move(right));
            left = std::move(alt);
        }
        return left;
    }

    RegexNodePtr parse_concat() {
        auto concat = std::make_unique<RegexNode>(NodeType::Concat);
        while (!at_end() && peek() != '|' && peek() != ')') {
            concat->children.push_back(parse_repeat());
        }
        if (concat->children.size() == 1) {
            return std::move(concat->children[0]);
        }
        return concat;
    }

    RegexNodePtr parse_repeat() {
        RegexNodePtr node = parse_atom();
        while (!at_end() && (peek() == '*' || peek() == '+' || peek() == '?')) {
            char op = advance();
            NodeType type = (op == '*') ? NodeType::Star : (op == '+') ? NodeType::Plus : NodeType::Optional;
            auto wrapped = std::make_unique<RegexNode>(type);
            wrapped->children.push_back(std::move(node));
            node = std::move(wrapped);
        }
        return node;
    }

    RegexNodePtr parse_atom() {
        if (at_end()) throw std::runtime_error("unexpected end of pattern");

        char c = advance();
        if (c == '(') {
            RegexNodePtr inner = parse_alternation();
            if (at_end() || advance() != ')') throw std::runtime_error("unmatched '('");
            return inner;
        }
        if (c == '.') {
            return std::make_unique<RegexNode>(NodeType::AnyChar);
        }
        if (c == '\\' && !at_end()) {
            c = advance(); // escaped literal, e.g. \* or \.
        }
        auto lit = std::make_unique<RegexNode>(NodeType::Literal);
        lit->literal = c;
        return lit;
    }
};

inline RegexNodePtr parse_regex(const std::string &pattern) {
    return RegexParser(pattern).parse();
}
