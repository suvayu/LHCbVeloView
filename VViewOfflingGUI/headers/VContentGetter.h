#ifndef __VCONFIGSGETTER_H_INCLUDED__
#define __VCONFIGSGETTER_H_INCLUDED__

#include <vector>
#include "VTabContent.h"
#include "VPlot.h"
#include "VPlottable.h"
#include "VTable.h"

#include <stdio.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>

// Author: Daniel Saunders


class VContentGetter {
public:

  // Methods __________________________________________________________________
  VContentGetter(){}
  static VTabContent * veloShortConfigs(VPlotOps*);
  static VTabContent * veloFileConfigs(VPlotOps*, std::string);
  static void findChildren(VTabContent * parentTab,
    std::vector<VTabContent*> * allTabs,
    std::vector< std::vector< std::string > > * ops);
  static void findPlots(std::vector<VTabContent*> * allTabs,
    std::vector< std::vector< std::string > > * ops, VPlotOps * plotOps);
};

#endif
