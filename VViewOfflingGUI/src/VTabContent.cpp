#include "../headers/VTabContent.h"

//_____________________________________________________________________________
void VTabContent::drawPlots() {
  // Drawn in real time when requested to be viewed, including layout.

  QLayoutItem *child;
  while ((child = layout()->takeAt(0)) != 0) {
    delete child;
  }

  // Set the layout.
  if (layout()!=NULL) delete layout();
  m_plotLayout = new QGridLayout(this);
  m_plotLayout->setContentsMargins(2,2,2,2);
  m_plotLayout->setHorizontalSpacing(2);
  m_plotLayout->setVerticalSpacing(2);
  setLayout(m_plotLayout);

  // Decide on the number of plots.
  unsigned int nx, ny;
  if (m_plots.size() < 5) {
    nx = 2;
    ny = 2;
  }

  else {
    nx = 3;
    ny = 3;
  }

//  if (m_plots.size() == 8) {
//    nx = 4;
//    ny = 2;
//  }

  // Add the plots.
  for (unsigned int i = 0; i<m_plots.size(); i++) {
    unsigned int row, column;
    if (m_plotFillDirection == 0) {row = i / nx; column = i % nx;}
    else {row = i % ny; column = i / ny;}
    m_plotLayout->addWidget(m_plots[i], row, column, 1, 1);
    m_plots[i]->draw();
  }
}


//_____________________________________________________________________________

void VTabContent::drawTables() {
  if (layout()!=NULL) delete layout();
  m_plotLayout = new QGridLayout(this);
  m_plotLayout->setContentsMargins(2,2,2,2);
  m_plotLayout->setHorizontalSpacing(2);
  m_plotLayout->setVerticalSpacing(2);
  setLayout(m_plotLayout);

  int nside = 4;
  // Add the tables.
  for (unsigned int i = 0; i<m_tables.size(); i++) {
    unsigned int row, column;
    if (m_plotFillDirection == 0) {row = i / nside; column = i % nside;}
    else {row = i % nside; column = i / nside;}
    m_plotLayout->addWidget(m_tables[i], row, column, 1, 1);
    m_tables[i]->draw();
  }
}


//_____________________________________________________________________________
