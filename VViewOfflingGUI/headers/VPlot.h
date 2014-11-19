#ifndef __VPLOT_H_INCLUDED__
#define __VPLOT_H_INCLUDED__

#include <vector>
#include "VPlottable.h"
#include <qwidget.h>
#include "VCustomPlot.h"
#include <QGridLayout>
#include "VTabContent.h"
#include "VPlotOps.h"
#include <QComboBox>
#include <QSpinBox>
#include <QLabel>


// Author: Daniel Saunders

class VTabContent;
class VPlottable;
class VCustomPlot;
class VPlotOps;


class VPlot : public QFrame{
  Q_OBJECT
public:
  std::vector<VPlottable*> m_plottables;
  std::string m_title;
  std::string m_xAxisTitle;
  std::string m_yAxisTitle;
  std::string m_zAxisTitle;
  bool m_drawn;
  VCustomPlot * m_vcp;
  QGridLayout * m_layout;
  VTabContent * m_tab;
  bool m_multipleModules;
  QComboBox * m_selector1;
  QComboBox * m_selector2;
  VPlotOps * m_plotOps;
  QWidget * m_statsBox;


  // Methods __________________________________________________________________
  VPlot();
  VPlot(std::string, VTabContent*, bool, VPlotOps*);
  void draw();
  VCustomPlot * setupPlot(bool);
  void setupLayout();
  void setupPlottables(VCustomPlot*);
  void add1dPlot(VCustomPlot*, VPlottable*);
  void addColzPlot(VCustomPlot*, VPlottable*);
  void getData();
  void addStatsBox(VCustomPlot*, bool);
  QWidget * exportStatsBox();

private slots:
  void makePopUp();
  void refresh();
  void moduleChanged();


  //___________________________________________________________________________
};

#endif
