CXX = g++
CXXFLAGS = -Wall -Wextra -std=c++17 -O2 -pthread

work_stealing_demo: main.cpp work_stealing_pool.hpp
	$(CXX) $(CXXFLAGS) -o work_stealing_demo main.cpp

clean:
	rm -f work_stealing_demo *.o
