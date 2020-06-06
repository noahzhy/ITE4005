# Compiler and Compile options.
CC = g++
CXXFLAGS = -g -Wall -std=c++11
MAKEFLAGS += -j

# Print Rating Matrix
# CXXFLAGS += -DPRINT

# Content Based recommendation
# CXXFLAGS += -DCONTENT_BASED

# Macros specifying path for compile.
SRCS := $(wildcard src/*.cc) 
OBJS := $(SRCS:.cpp=.o)
BIN = ./bin/
INC = ./include/
LIB = ./lib/ -lpthread

# Pre-Processor.
CPPFLAGS += -I$(INC)

# Compile command.
TARGET = recommender
$(TARGET):$(OBJS)
	$(CC) $(CXXFLAGS) $(CPPFLAGS) -o $(BIN)$(TARGET) $(SRCS) -L$(LIB)

# Delete binary & object files.
clean:
	rm ./bin/*
	rm ./data/*prediction.txt
