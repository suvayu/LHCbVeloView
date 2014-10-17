import ROOT

from veloview.jsonifier import data_for_object


ROOT.gRandom.SetSeed(0)

# Dictionary of per-page paths within run files
directory_map = {
    'pedestals': 'Vetra/VeloPedestalSubtractorMoni',
    'noise': 'Vetra/NoiseMon/DecodedADC',
    'clusters': 'Velo/VeloClusterMonitor',
    'occupancy': 'Velo/VeloOccupancyMonitor'
}


def default_run():
    """Retrieve the default run rumber from veloview.

    Used when no run number is specified by the user, or if the given run is
    invalid (as judged by valid_run`).
    """
    return 123988


def valid_run(run):
    """Returns True if run is a valid run number."""
    return run in run_list()


def run_list():
    """Return the list of available runs from veloview."""
    return range(123995, 123984, -1)


def nearby_runs(run, runs, distance=3):
    """Return the runs +/- distance either side of run in runs."""
    idx = runs.index(run)
    lower = idx - distance if idx >= distance else 0
    upper = idx + distance + 1
    return runs[lower:upper]


def key_dict(name, tfile):
    """Return information on the key within the TFile as a dictionary.

    Keyword arguments:
    name -- Name of the plot, i.e. the path to it in a run file
    tfile -- Run file as an open TFile instance
    """
    key = tfile.Get(name)
    d = dict(
        success=True,
        data=dict(
            key_name=key.GetName(),
            key_title=key.GetTitle(),
            key_class=key.ClassName(),
            key_data=data_for_object(key)
        )
    )
    return d


def run_file(run):
    """Return TFile object for the given run.

    If not appropriate file can be found, None is returned.
    Keyword arguments:
    run -- LHC run ID
    """
    f = ROOT.TFile.Open('/afs/cern.ch/user/s/sali/public/veloview/data/VELODQM_130560_2012-10-18_04.45.10_NZS_ZS.root')
    if f.IsZombie():
        return None
    return f


def reference_file(run):
    """Return corresponding reference TFile object for the run.

    If not appropriate file can be found, None is returned.
    Keyword arguments:
    run -- LHC run ID
    """
    f = ROOT.TFile.Open('/afs/cern.ch/user/s/sali/public/veloview/data/VELODQM_127193_2012-09-05_02.00.09_NZS_ZS.root')
    if f.IsZombie():
        return None
    return f


def run_plot(name, run):
    """Return named plot for the specified run.

    Keyword arguments:
    name -- Name of the plot, i.e. the path to it in a run file
    run -- LHC run ID
    """
    f = run_file(run)
    d = key_dict(name, f)
    f.Close()
    return d


def reference_plot(name, run):
    """Return corresponding reference plot for the specified run.

    Keyword arguments:
    name -- Name of the plot, i.e. the path to it in a run file
    run -- LHC run ID
    """
    f = reference_file(run)
    d = key_dict(name, f)
    d['data']['key_name'] += '_reference'
    d['data']['key_title'] += ' (reference)'
    f.Close()
    return d


def pedestals(name, run):
    path = directory_map['pedestals']
    key = '{0}/{1}'.format(path, name)
    plot = run_plot(key, run)
    # Don't return a reference for 2D plots
    if '2' in plot['data']['key_class']:
        return plot
    else:
        return [plot, reference_plot(key, run)]


def noise(name, run):
    path = directory_map['noise']
    key = '{0}/{1}'.format(path, name)
    plot = run_plot(key, run)
    # Don't return a reference for 2D plots
    if '2' in plot['data']['key_class']:
        return plot
    else:
        return [plot, reference_plot(key, run)]


def clusters(name, run):
    path = directory_map['clusters']
    key = '{0}/{1}'.format(path, name)
    plot = run_plot(key, run)
    # Don't return a reference for 2D plots
    if '2' in plot['data']['key_class']:
        return plot
    else:
        return [plot, reference_plot(key, run)]


def occupancy(name, run):
    path = directory_map['occupancy']
    key = '{0}/{1}'.format(path, name)
    plot = run_plot(key, run)
    # Don't return a reference for 2D plots
    if '2' in plot['data']['key_class']:
        return plot
    else:
        return [plot, reference_plot(key, run)]
