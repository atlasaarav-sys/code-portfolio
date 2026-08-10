CXX = g++
CXXFLAGS = -Wall -Wextra -std=c++17 -O2

expr_demo: main.cpp evaluator.hpp shunting_yard.hpp tokenizer.hpp
	$(CXX) $(CXXFLAGS) -o expr_demo main.cpp

clean:
	rm -f expr_demo *.o
