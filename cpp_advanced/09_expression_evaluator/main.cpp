#include <cmath>
#include <cstdio>
#include <unordered_map>
#include <vector>

#include "evaluator.hpp"

struct TestCase {
    std::string expr;
    std::unordered_map<std::string, double> vars;
    double expected;
};

int main() {
    std::vector<TestCase> tests = {
        {"2 + 3 * 4", {}, 14.0},
        {"(2 + 3) * 4", {}, 20.0},
        {"2 ^ 3 ^ 2", {}, 512.0}, // right-associative: 2^(3^2) = 2^9
        {"-5 + 3", {}, -2.0},
        {"10 - -3", {}, 13.0},
        {"3 * -2 + 1", {}, -5.0},
        {"x * x + y", {{"x", 3.0}, {"y", 4.0}}, 13.0},
        {"(a + b) / 2", {{"a", 10.0}, {"b", 20.0}}, 15.0},
        {"2 * (3 + (4 - 1))", {}, 12.0},
    };

    int passed = 0;
    for (const auto &tc : tests) {
        double result = evaluate(tc.expr, tc.vars);
        bool ok = std::fabs(result - tc.expected) < 1e-9;
        passed += ok;
        std::printf("%-4s \"%s\" = %.4f (expected %.4f)\n",
                    ok ? "OK" : "FAIL", tc.expr.c_str(), result, tc.expected);
    }

    std::printf("\n%d/%zu tests passed.\n", passed, tests.size());
    return (passed == static_cast<int>(tests.size())) ? 0 : 1;
}
