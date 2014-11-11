#!/usr/bin/env python
# coding=utf-8

"""This script runs Vetra analysis to produce monitoring histograms.

@author:  Suvayu Ali
@date:    2013-06-11

"""


## option parsing
import argparse
parser = argparse.ArgumentParser(description=__doc__)
parser.formatter_class = argparse.RawDescriptionHelpFormatter

parser.add_argument('runs', nargs='*', type=int, help='List of runs to process.')
parser.add_argument('-r', '--run-range', nargs=2, type=int,
                    metavar=('START', 'END'), help='Run range to process.')
parser.add_argument('-v', '--vetra-version', dest='vetra', default='v14r0',
                    help='Vetra version to use (default: v14r0).')
parser.add_argument('-s', '--stream', dest='stream', default='NZS',
                    choices=['NZS', 'ZS'], help='Which stream to process '
                    '(default: NZS).')
parser.add_argument('-n', '--nevents', dest='nevents', type=int, default=70000,
                    help='Number of events to process (default: 70000).')
parser.add_argument('-t', '--time-threshold', dest='threshold', default=1800,
                    type=int, help='Minimum run duration in seconds (default: 1800).')
parser.add_argument('-jd', '--job-dir', dest='jobdir',
                    default='/calib/velo/dqm/VeloView/VetraOutput', help='Job '
                    'directory (default: /calib/velo/dqm/VeloView/VetraOutput).')
parser.add_argument('-o', '--job-options', dest='jobopts',
                    help='Override default Vetra job options (quoted).')
parser.add_argument('-c', '--cron', action='store_true',
                    help='Run from a cron job.')
parser.add_argument('-d', '--debug', dest='debug', action='store_true',
                    help='Turn debug on messages.')

_cliopts = parser.parse_args()


## logging
from logging import getLogger, debug, info, warning, error, basicConfig
logger = getLogger(__name__)
if _cliopts.debug:
    from logging import DEBUG as lvl
else:
    from logging import INFO as lvl
basicConfig(level=lvl, datefmt='%d-%m-%Y %H:%M:%S',
            format='%(levelname)s:%(module)s:%(asctime)s: %(message)s')


## option setup
debug('Script options: %s' % _cliopts)

# import python modules
import os, errno, sys, re
from glob import glob

# stream to process
pattern = re.compile('NZS|ZS')
if pattern.match(_cliopts.stream):
    stream = _cliopts.stream
else:
    sys.exit('Unknown stream: %s. Exiting.' % _cliopts.stream)

jobdir = _cliopts.jobdir
runlist = '/calib/velo/dqm/VeloView/VetraOutput/RunList.txt'
from crontools.utils import get_last_run

# run range to process (old: 1k runs from last processed run in DQS
# directory).
if _cliopts.runs:
    runs = _cliopts.runs
elif _cliopts.run_range:
    runs = range(int(_cliopts.run_range[0]),
                 int(_cliopts.run_range[1])+1)
else:
    debug('No run range or list was provided. ' \
          'List of runs will be determined automagically!')

    ## old: last processed + 1k
    last_run = get_last_run(runlist)
    # We only process runs longer than time threshold (~30 min), many
    # runs are likely to be skipped b/c of this condition.  Assign an
    # arbitrary run range (1k is long enough to cover a technical
    # stop) such that we always find one significant run.
    runs = range(last_run + 1, last_run + 11) # range 10 for testing

    ## new: TODO
    # 1. get run fill from (1)
    #
    # 2. get latest fill (is getting latest physics fill sufficient?
    #    probably not)
    #
    # 3. generate list of runs from fill id (2), last processed run (1)
    #    and latest fill (3).

# job options
if _cliopts.jobopts:
    jobopts = _cliopts.jobopts
else:
    jobopts = '-a -t {} -d /castorfs/cern.ch/grid/lhcb/data/2011/' \
              'RAW/FULL/LHCb/COLLISION11 -u /calib/velo/dqm/DQS/cron' \
              '/FilterBeamBeam_Heartbeat.py'.format(stream)


## trim list of runs by run duration from run database.
from crontools.rundbquery import RunDBQuery
debug('Run list before trimming: %s' % runs)
# query the database and get validated list of runs
query = RunDBQuery(runs)
query.parse()
runs = query.get_valid_runs(_cliopts.threshold)
debug('Run list after trimming: %s' % runs)


## acquire lock and run job
from crontools.utils import add_runs, make_dir_tree
from crontools.runlock import (RunLock)
for run in runs:
    info('Processing run: %s, stream: %s' % (run, stream))
    from subprocess import call
    # FIXME: temporarily hard coded vetra script name
    vetraOffline = '/cvmfs/lhcb.cern.ch/lib/lhcb/VETRA/VETRA_{}' \
                   '/Velo/VetraScripts/scripts/vetraOffline'.format(_cliopts.vetra)
    cmd_w_args = ([vetraOffline] + jobopts.split(' ') +
                  [str(run), str(_cliopts.nevents)])
    debug('Job command: %s', ' '.join(cmd_w_args))

    # job directory
    jobdir_t = _cliopts.jobdir + '/{}'.format(make_dir_tree(run))
    try:
        try:
            os.makedirs(jobdir_t)
        except OSError as err:
            if err.errno != errno.EEXIST: raise
        os.chdir(jobdir_t)
    except OSError as err:
        error('Run %d, stream %s: Oops! Problem with job directory.',
              run, stream, exc_info=True)
        continue
    try:
        # start the job
        with RunLock(jobdir_t, run, stream):
            info('Starting Vetra')
            retcode = call(cmd_w_args)
            if retcode != 0:
                warning('Oops! It seems Vetra failed!')
            else:
                retcode = add_runs(run, runlist)
                if retcode: error('Run %d couldn\'t be added to the list.')
            info('Vetra returned with: %d', retcode)
    except:
        error('Oops! Unexpected exception, crashing disgracefully.',
              exc_info=True)
        raise
    if _cliopts.cron:   # quit after 1 job when run by cron
        debug('Running from cron, quitting after 1 job.')
        break

sys.exit('Bye bye ...')
