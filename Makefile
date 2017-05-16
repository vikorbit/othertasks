CC      = gcc
CXX 	= g++
AS      = as
LD      = g++
AR      = ar
RANLIB  = ranlib
OBJCOPY = objcopy


CXXFLAGS += -c -std=c++0x  -Wall -O6 -Wextra -pedantic -g
INCDIRS = -I.


all: task_4

task_4: task_4.o
	$(LD) -o $@ $^

task_4.o: task_4.cpp
	$(CXX) $(INCDIRS) task_4.cpp -o $@ $(CXXFLAGS)

clean:
	rm -rf task_4 task_4.o