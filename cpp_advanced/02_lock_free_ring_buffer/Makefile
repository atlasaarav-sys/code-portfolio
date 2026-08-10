CXX = g++
CXXFLAGS = -Wall -Wextra -std=c++17 -O2 -pthread

ring_buffer_demo: main.cpp spsc_ring_buffer.hpp
	$(CXX) $(CXXFLAGS) -o ring_buffer_demo main.cpp

clean:
	rm -f ring_buffer_demo *.o
