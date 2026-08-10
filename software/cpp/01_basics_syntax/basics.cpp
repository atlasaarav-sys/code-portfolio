#include <iostream>
#include <string>
#include <vector>

int add(int a, int b) {
    return a + b;
}

double add(double a, double b) {
    return a + b;
}

std::string greet(const std::string &name, const std::string &greeting = "Hello") {
    return greeting + ", " + name + "!";
}

int main() {
    // Variables & auto
    int age = 21;
    auto pi = 3.14159;
    std::cout << "age=" << age << " pi=" << pi << "\n";

    // References
    int x = 10;
    int &ref = x;
    ref += 5;
    std::cout << "x after modifying ref: " << x << "\n";

    // Control flow
    for (int i = 1; i <= 5; i++) {
        std::cout << (i % 2 == 0 ? "even" : "odd") << " ";
    }
    std::cout << "\n";

    // vector + range-based for
    std::vector<int> numbers = {1, 2, 3, 4, 5};
    int sum = 0;
    for (const auto &n : numbers) {
        sum += n;
    }
    std::cout << "sum = " << sum << "\n";

    // function overloading
    std::cout << "add(2, 3) = " << add(2, 3) << "\n";
    std::cout << "add(2.5, 3.5) = " << add(2.5, 3.5) << "\n";

    // default args
    std::cout << greet("Sam") << "\n";
    std::cout << greet("Sam", "Hi") << "\n";

    return 0;
}
