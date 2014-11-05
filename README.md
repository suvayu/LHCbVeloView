LHCb VELO View
==============

This is the repository for the VELO monitoring project.

The overarching goal is to have a data quality analysis framework to monitor
the VELO using per-run Vetra output files.
This framework, `veloview`, is used by separate web-based and desktop GUIs.

Packages
--------

The project has several packages in the top-level directory.

* `GiantRootFileIO` is a C++ library that provides versioned ROOT
  objects.  This will be used for trending information and history
  browsing.
* `veloview` is the data quality analysis framework used to monitor
  the LHCb Vertex Locator.
* `web-monitor` Flask-based web application for monitoring the VELO

Each package contains a README detailing its purpose and usage.
