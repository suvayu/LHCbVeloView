#ifndef __VTABCONTENT_H_INCLUDED__
#define __VTABCONTENT_H_INCLUDED__

#include <vector>
#include "VPlot.h"
#include <qwidget.h>
#include <QGridLayout>
#include "VTable.h"

// VTabContent - an object containing one tabs worth of content (be it plots or 
// tabs). Note that tabs and plots is not currently supported.
// Author: Daniel Saunders


class VPlot;
class VTable;

class VTabContent : public QWidget {
public:
  // Set of configurations of sub-tabs that are displayed in this tab.
  std::vector<VTabContent*> m_subContents;
  std::vector<VPlot*> m_plots; // Plots to be shown in this tab - up to 9.
  std::vector<VTable*> m_tables; // Tables to be shown in this tab.
  std::string m_title; // This tabs name.
  int m_plotFillDirection; // 0 for filling rows first, 1 for columns. TODO
  int m_subTabViewMethod; // 0 to draw as tabs, 1 for drop down list. TODO
  QWidget * m_widget; // Pointer to its own widget in the GUI.
  QGridLayout * m_plotLayout;
  VTabContent * m_parentTab;
  int m_ID;
  int m_parentID;
  

  // Methods __________________________________________________________________
  VTabContent() : m_subContents(),
                  m_plots(),
                  m_title("Default Tab Name"),
                  m_plotFillDirection(0),
                  m_subTabViewMethod(0),
                  m_widget(NULL),
                  m_plotLayout(NULL),
                  m_parentTab(NULL),
                  m_ID(0){} // Top tab constructor.

  VTabContent(std::string title) :
                  m_subContents(),
                  m_plots(),
                  m_plotFillDirection(0),
                  m_subTabViewMethod(0),
                  m_widget(NULL),
                  m_plotLayout(NULL),
                  m_parentTab(NULL),
                  m_ID(0){
                    m_title = title;
                  } // Top tab constructor.


  VTabContent(std::string title,
              VTabContent * parentTab) :
                m_subContents(),
                m_plots(),
                m_plotFillDirection(0),
                m_subTabViewMethod(0),
                m_widget(NULL),
                m_plotLayout(NULL){
                  m_title = title;
                  m_parentTab = parentTab;
                  m_parentTab->m_subContents.push_back(this);
                }

  VTabContent(std::string title,
              VTabContent * parentTab, int ID) :
                m_subContents(),
                m_plots(),
                m_plotFillDirection(0),
                m_subTabViewMethod(0),
                m_widget(NULL),
                m_plotLayout(NULL){
                  m_title = title;
                  m_parentTab = parentTab;
                  m_parentTab->m_subContents.push_back(this);
                  m_ID = ID;
                } // Other tabs.



  //___________________________________________________________________________

  void showEvent(QShowEvent *) {
    if (m_plots.size() > 0) drawPlots();
    if (m_tables.size() > 0) drawTables();
  } // Re-implemented from QWidget.

  void drawPlots();
  void drawTables();


  //___________________________________________________________________________
};

#endif
