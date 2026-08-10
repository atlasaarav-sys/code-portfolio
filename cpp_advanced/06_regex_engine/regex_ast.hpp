#pragma once

#include <memory>
#include <vector>

enum class NodeType { Literal, AnyChar, Concat, Alternation, Star, Plus, Optional };

struct RegexNode {
    NodeType type;
    char literal = '\0';                          // for Literal
    std::vector<std::unique_ptr<RegexNode>> children; // Concat: all parts; Alternation: 2 branches; Star/Plus/Optional: 1 child

    explicit RegexNode(NodeType t) : type(t) {}
};

using RegexNodePtr = std::unique_ptr<RegexNode>;
