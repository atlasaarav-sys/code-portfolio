CXX = g++
CXXFLAGS = -Wall -Wextra -std=c++17
TARGETS = basics shapes

all: $(TARGETS)

basics: basics.cpp
	$(CXX) $(CXXFLAGS) -o $@ $<

shapes: shapes.cpp
	$(CXX) $(CXXFLAGS) -o $@ $<

clean:
	rm -f $(TARGETS) *.o
