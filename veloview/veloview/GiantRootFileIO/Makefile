TARGETS = VeloGUIUtilsRflx.cxx libVeloGUIUtils.so runList
alldicts += VeloGUIUtilsRflx.cxx

include Rules.mk

VeloGUIUtilsRflx.cxx: VeloGUIUtilsRflx.h VeloGUIUtilsRflx.xml

libVeloGUIUtils.so: VeloGUIUtilsRflx.os $(patsubst %.cc,%.os,$(filter-out runList.cc,$(allsrc)))

# runList standalone executable; link with C++ compiler, use C++11
runList: runList.o DotLock.o
runList: CC=$(CXX)
runList.o: CXXFLAGS+=-std=c++11
.deps/runList.dd: CPPFLAGS+=-std=c++11
