#pragma once

#include <set>
#include <stdexcept>
#include <vector>

#include "regex_ast.hpp"
#include "regex_parser.hpp"

struct NFAState {
    bool has_char = false;
    bool is_any = false;
    char c = '\0';
    int char_target = -1;
    std::vector<int> epsilons;
};

class NFA {
public:
    // Builds the NFA via Thompson's construction and returns a matcher-ready NFA.
    static NFA compile(const RegexNode &root) {
        NFA nfa;
        auto [start, end] = nfa.build(root);
        nfa.start_ = start;
        nfa.accept_ = end;
        return nfa;
    }

    bool matches(const std::string &input) const {
        std::set<int> current = epsilon_closure({start_});

        for (char c : input) {
            std::set<int> next;
            for (int s : current) {
                const NFAState &state = states_[s];
                if (state.has_char && (state.is_any || state.c == c)) {
                    next.insert(state.char_target);
                }
            }
            if (next.empty()) return false;
            current = epsilon_closure(next);
        }

        return current.count(accept_) > 0;
    }

private:
    std::vector<NFAState> states_;
    int start_ = -1;
    int accept_ = -1;

    int new_state() {
        states_.emplace_back();
        return static_cast<int>(states_.size()) - 1;
    }

    std::set<int> epsilon_closure(const std::set<int> &seed) const {
        std::set<int> closure = seed;
        std::vector<int> stack(seed.begin(), seed.end());
        while (!stack.empty()) {
            int s = stack.back();
            stack.pop_back();
            for (int next : states_[s].epsilons) {
                if (closure.insert(next).second) {
                    stack.push_back(next);
                }
            }
        }
        return closure;
    }

    // Returns (start, end) for the fragment; `end` is left dangling (no
    // outgoing transitions) for the caller to wire up.
    std::pair<int, int> build(const RegexNode &node) {
        switch (node.type) {
            case NodeType::Literal: {
                int a = new_state();
                int b = new_state();
                states_[a].has_char = true;
                states_[a].c = node.literal;
                states_[a].char_target = b;
                return {a, b};
            }
            case NodeType::AnyChar: {
                int a = new_state();
                int b = new_state();
                states_[a].has_char = true;
                states_[a].is_any = true;
                states_[a].char_target = b;
                return {a, b};
            }
            case NodeType::Concat: {
                if (node.children.empty()) {
                    int a = new_state();
                    return {a, a}; // empty pattern matches empty string
                }
                auto [start, end] = build(*node.children[0]);
                for (size_t i = 1; i < node.children.size(); i++) {
                    auto [next_start, next_end] = build(*node.children[i]);
                    states_[end].epsilons.push_back(next_start);
                    end = next_end;
                }
                return {start, end};
            }
            case NodeType::Alternation: {
                auto [a_start, a_end] = build(*node.children[0]);
                auto [b_start, b_end] = build(*node.children[1]);
                int start = new_state();
                int end = new_state();
                states_[start].epsilons = {a_start, b_start};
                states_[a_end].epsilons.push_back(end);
                states_[b_end].epsilons.push_back(end);
                return {start, end};
            }
            case NodeType::Star: {
                auto [inner_start, inner_end] = build(*node.children[0]);
                int start = new_state();
                int end = new_state();
                states_[start].epsilons = {inner_start, end};
                states_[inner_end].epsilons = {inner_start, end};
                return {start, end};
            }
            case NodeType::Plus: {
                auto [inner_start, inner_end] = build(*node.children[0]);
                int end = new_state();
                states_[inner_end].epsilons = {inner_start, end};
                return {inner_start, end};
            }
            case NodeType::Optional: {
                auto [inner_start, inner_end] = build(*node.children[0]);
                int start = new_state();
                int end = new_state();
                states_[start].epsilons = {inner_start, end};
                states_[inner_end].epsilons.push_back(end);
                return {start, end};
            }
        }
        throw std::runtime_error("unhandled node type");
    }
};

inline bool regex_match(const std::string &pattern, const std::string &input) {
    RegexNodePtr ast = parse_regex(pattern);
    NFA nfa = NFA::compile(*ast);
    return nfa.matches(input);
}
