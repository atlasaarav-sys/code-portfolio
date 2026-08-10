CXX = g++
CXXFLAGS = -Wall -Wextra -std=c++17 -O2

json_demo: main.cpp json_parser.hpp json_value.hpp
	$(CXX) $(CXXFLAGS) -o json_demo main.cpp

clean:
	rm -f json_demo *.o
