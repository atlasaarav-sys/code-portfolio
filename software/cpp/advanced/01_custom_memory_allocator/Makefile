CXX = g++
CXXFLAGS = -Wall -Wextra -std=c++17 -O2

allocator_demo: main.cpp pool_allocator.hpp
	$(CXX) $(CXXFLAGS) -o allocator_demo main.cpp

clean:
	rm -f allocator_demo *.o
