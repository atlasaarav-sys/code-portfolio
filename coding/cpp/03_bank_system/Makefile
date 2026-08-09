CXX = g++
CXXFLAGS = -Wall -Wextra -std=c++17
SRCS = main.cpp account.cpp bank.cpp
TARGET = bank_demo

$(TARGET): $(SRCS) account.hpp bank.hpp
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(SRCS)

clean:
	rm -f $(TARGET) *.o accounts.txt
