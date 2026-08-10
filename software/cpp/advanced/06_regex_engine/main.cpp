#include <cstdio>
#include <vector>

#include "nfa.hpp"

struct TestCase {
    std::string pattern;
    std::string input;
    bool expected;
};

int main() {
    std::vector<TestCase> tests = {
        {"abc", "abc", true},
        {"abc", "abd", false},
        {"a*", "", true},
        {"a*", "aaaa", true},
        {"a+", "", false},
        {"a+", "aaa", true},
        {"a?b", "b", true},
        {"a?b", "ab", true},
        {"a?b", "aab", false},
        {"cat|dog", "cat", true},
        {"cat|dog", "dog", true},
        {"cat|dog", "bird", false},
        {"(ab)+", "ababab", true},
        {"(ab)+", "aba", false},
        {"a.c", "abc", true},
        {"a.c", "axc", true},
        {"a.c", "ac", false},
        {"(a|b)*c", "aabbabc", true},
        {"(a|b)*c", "aabbab", false},
    };

    int passed = 0;
    for (const auto &tc : tests) {
        bool result = regex_match(tc.pattern, tc.input);
        bool ok = (result == tc.expected);
        passed += ok;
        std::printf("%-4s /%s/ matches \"%s\": got=%s expected=%s\n",
                    ok ? "OK" : "FAIL", tc.pattern.c_str(), tc.input.c_str(),
                    result ? "true" : "false", tc.expected ? "true" : "false");
    }

    std::printf("\n%d/%zu tests passed.\n", passed, tests.size());
    return (passed == static_cast<int>(tests.size())) ? 0 : 1;
}
