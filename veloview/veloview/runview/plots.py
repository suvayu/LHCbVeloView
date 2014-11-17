"""Methods dealing with run view plots."""
import glob

import ROOT

from veloview.runview import utils


def get_run_plot(plot, run, reference=False):
    """Return the object at the plot path in the run file.

    Keyword arguments:
    plot -- Path within the run file to the plot object.
            A KeyError is raised if plot is not found in the run file
    run -- Run number
    reference -- If True, fetch the reference plot for the given plot and run
    """
    if reference:
        run = utils.reference_run(plot, run)

    # Get the latest run file in the run's directory
    base = utils.run_file_path(run)
    files = sorted(glob.glob("{0}/*.root".format(base)))
    try:
        path = files[-1]
    except IndexError:
        raise IOError("Run file not found for run {0}".format(run))

    # Try to open the file
    f = ROOT.TFile(path)
    if f.IsZombie():
        raise IOError("Run file not found for run {0}".format(run))

    # Retrieve the object
    obj = f.Get(plot)
    if not obj:
        raise KeyError("Plot {0} not found in run file {1}".format(plot, run))
    # The file will be closed when the function returns, so we need to clone
    # the fetched object outside the file's scope
    ROOT.gROOT.cd()
    clone = obj.Clone(obj.GetName())
    f.Close()

    return clone
