CXX = g++
CXXFLAGS = -Wall -Wextra -std=c++17 -O2

smart_ptr_demo: main.cpp my_unique_ptr.hpp my_shared_ptr.hpp
	$(CXX) $(CXXFLAGS) -o smart_ptr_demo main.cpp

clean:
	rm -f smart_ptr_demo *.o
