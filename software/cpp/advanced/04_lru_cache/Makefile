CXX = g++
CXXFLAGS = -Wall -Wextra -std=c++17 -O2

lru_demo: main.cpp lru_cache.hpp
	$(CXX) $(CXXFLAGS) -o lru_demo main.cpp

clean:
	rm -f lru_demo *.o
