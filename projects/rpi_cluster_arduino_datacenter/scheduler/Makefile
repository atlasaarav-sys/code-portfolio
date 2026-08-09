CXX = g++
CXXFLAGS = -Wall -Wextra -std=c++17 -O2 -pthread

cluster_benchmark: main.cpp task_scheduler.hpp
	$(CXX) $(CXXFLAGS) -o cluster_benchmark main.cpp

clean:
	rm -f cluster_benchmark *.o
