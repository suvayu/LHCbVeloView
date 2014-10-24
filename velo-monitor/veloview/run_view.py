from collections import OrderedDict

import ROOT

from veloview.jsonifier import data_for_object


ROOT.gRandom.SetSeed(0)


pages_dict = OrderedDict([
    ('dqs', {
        'title': 'DQS'
    }),
    ('pedestals', {
        'title': 'Pedestals',
        'plots': [
            {
                'title': 'Pedestal bank',
                'name': 'Vetra/VeloPedestalSubtractorMoni/TELL1_{0:03d}/Pedestal_Bank',
                'sensor_dependent': True
            },
            {
                'title': 'Subtracted ADC profile',
                'name': 'Vetra/VeloPedestalSubtractorMoni/TELL1_{0:03d}/Ped_Sub_ADCs_Profile',
                'sensor_dependent': True
            },
            {
                'title': 'Subtracted ADC 2D',
                'name': 'Vetra/VeloPedestalSubtractorMoni/TELL1_{0:03d}/Ped_Sub_ADCs_2D',
                'sensor_dependent': True
            }
        ]
    }),
    ('common_mode', {
        'title': 'Common mode'
    }),
    ('noise', {
        'title': 'Noise',
        'plots': [
            {
                'title': 'RMS noise vs. chip channel',
                'name': 'Vetra/NoiseMon/DecodedADC/TELL1_{0:03d}/RMSNoise_vs_ChipChannel',
                'sensor_dependent': True
            },
            {
                'title': 'RMS noise vs. strip',
                'name': 'Vetra/NoiseMon/DecodedADC/TELL1_{0:03d}/RMSNoise_vs_Strip',
                'sensor_dependent': True
            },
        ]
    }),
    ('clusters', {
        'title': 'Clusters',
        'plots': [
            {
                'title': 'Number of VELO clusters per event (Default)',
                'short': 'Clusters per event',
                'name': 'Velo/VeloClusterMonitor/# VELO clusters'
            },
            {
                'title': 'Number of strips per cluster',
                'short': 'Strips per cluster',
                'name': 'Velo/VeloClusterMonitor/Cluster size',
                'options': {
                    'showUncertainties': True
                }
            },
            {
                'title': 'Active chip links versus sensor',
                'short': 'Active links per sensor',
                'name': 'Velo/VeloClusterMonitor/Active chip links vs sensor'
            },
            {
                'title': 'Number of strips per cluster versus sensor',
                'short': 'Strips per cluster vs. sensor',
                'name': 'Velo/VeloClusterMonitor/Cluster size vs sensor'
            }
        ]
    }),
    ('occupancy', {
        'title': 'Occupancy',
        'plots': [
            {
                'title': 'Channel occupancy',
                'name': 'Velo/VeloOccupancyMonitor/OccPerChannelSens{0}',
                'sensor_dependent': True
            },
            {
                'title': 'Average sensor occupancy',
                'name': 'Velo/VeloOccupancyMonitor/OccAvrgSens'
            },
            {
                'title': 'Occupancy spectrum (zoom)',
                'short': 'Occupancy spectrum',
                'name': 'Velo/VeloOccupancyMonitor/OccSpectMaxLow'
            },
            {
                'title': '% VELO occupancy vs. LHC bunch ID (A side)',
                'short': 'Occupancy vs. BCID (A side)',
                'name': 'Velo/VeloOccupancyMonitor/h_veloOccVsBunchId_ASide'
            },
            {
                'title': '% VELO occupancy vs. LHC bunch ID (C side)',
                'short': 'Occupancy vs. BCID (C side)',
                'name': 'Velo/VeloOccupancyMonitor/h_veloOccVsBunchId_CSide'
            }
        ]
    }),
    ('tracks', {
        'title': 'Tracks'
    }),
    ('vertices', {
        'title': 'Vertices'
    }),
    ('errors', {
        'title': 'Errors'
    }),
    ('sensor_overview', {
        'title': 'Sensor overview'
    })
])


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


def get_plot(name, run):
    plot = run_plot(name, run)
    # Don't return a reference for 2D plots
    if '2' in plot['data']['key_class']:
        return plot
    else:
        return [plot, reference_plot(name, run)]
