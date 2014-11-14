include Rules.mk

# runList standalone executable; link with C++ compiler, use C++11
runList: runList.o DotLock.o
runList: CC=$(CXX)
runList.o: CXXFLAGS+=-std=c++11
.deps/runList.dd: CPPFLAGS+=-std=c++11
