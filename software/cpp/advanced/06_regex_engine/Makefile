CXX = g++
CXXFLAGS = -Wall -Wextra -std=c++17 -O2

regex_demo: main.cpp nfa.hpp regex_parser.hpp regex_ast.hpp
	$(CXX) $(CXXFLAGS) -o regex_demo main.cpp

clean:
	rm -f regex_demo *.o
