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

parser.add_argument('runs', nargs='*', type=int,
                    help='List of runs to process.')
parser.add_argument('-r', '--run-range', nargs=2, type=int,
                    metavar=('START', 'END'),
                    help='Run range to process.')
parser.add_argument('-s', '--stream', dest='stream', default='NZS',
                    help='Which stream to process, ZS/NZS (default).')
parser.add_argument('-n', '--nevents', dest='nevents', type=int, default=70000,
                    help='Number of events to process (default 70000).')
parser.add_argument('-t', '--time-threshold', dest='threshold',
                    type=int, help='Minimum run duration in seconds.')
parser.add_argument('-jd', '--job-dir', dest='job_dir',
                    default='/calib/velo/dqm', help='Job directory '
                    '(default: /calib/velo/dqm).')
parser.add_argument('-o', '--job-options', dest='jobopts',
                    help='Override default Vetra job options (quoted).')
parser.add_argument('-c', '--cron', action='store_true',
                    help='Run from a cron job.')
parser.add_argument('-d', '--debug', dest='debug', action='store_true',
                    help='Turn debug options on.')

_cliopts = parser.parse_args()


## option setup
debug = _cliopts.debug
if debug:
    print 'Script options: %s' % _cliopts

# import python modules
import os, sys, re
from glob import glob
if debug:
    from traceback import print_exc

# stream to process
pattern = re.compile('NZS|ZS')
if pattern.match(_cliopts.stream):
    stream = _cliopts.stream
else:
    sys.exit('Unknown stream: %s. Exiting.' % _cliopts.stream)

# run range to process (old: 1k runs from last processed run in DQS
# directory).
if _cliopts.runs:
    runs = _cliopts.runs
elif _cliopts.run_range:
    runs = range(int(_cliopts.run_range[0]),
                 int(_cliopts.run_range[1])+1)
else:
    if debug:
        print 'No run range or list was provided. ' \
            'List of runs will be determined automagically!'

    ## old: last processed + 1k
    # get last processed run
    files = glob('/calib/velo/dqm/??????/VELODQM_*_'+stream+'.root') # 6 digit run numbers
    # # following line is used only for debugging
    # files = glob('data/??????/VELODQM_*_'+stream+'.root') # 6 digit run numbers

    # lexically sort file list
    files.sort()

    # extract run number from last entry
    last_run = int(files[-1].split('_')[1])
    # assign arbitrary run range (1k is long enough to cover a technical stop)
    runs = range(last_run + 1, last_run + 11) # range 10 for testing

    ## new: TODO
    # 1. get run fill from (1)
    #
    # 2. get latest fill (is getting latest physics fill sufficient?
    #    probably not)
    #
    # 3. generate list of runs from fill id (2), last processed run (1)
    #    and latest fill (3).


## trim list of runs by run duration from run database.
from VeloCronPyTools.rundbquery import RunDBQuery, RunInfo

if debug:
    print 'Run list before trimming: %s' % runs

# query the database and get validated list of runs
query = RunDBQuery(runs)
runs = query.get_valid_runs(_cliopts.threshold)

if debug:
    print 'Run list after trimming: %s' % runs


## acquire lock and run job
from VeloCronPyTools.runlock import (RunLock, UndefinedRunLock,
                                     RunLockExists)

if _cliopts.jobopts:
    jobopts = _cliopts.jobopts
else:
    jobopts = '-a -t NZS -d /castorfs/cern.ch/grid/lhcb/data/2011/' \
              'RAW/FULL/LHCb/COLLISION11 -u /calib/velo/dqm/DQS/cron' \
              '/FilterBeamBeam_Heartbeat.py'

for run in runs:
    with RunLock(run, stream):
        print 'Processing run: %s, stream: %s' % (run, stream)
        from subprocess import call, check_call
        # FIXME: temporarily hard coded vetra script name
        vetraOffline = '/cvmfs/lhcb.cern.ch/lib/lhcb/VETRA/VETRA_v13r2' \
                       '/Velo/VetraScripts/scripts/vetraOffline'
        cmd_w_args = ([vetraOffline] + jobopts.split(' ') +
                      [str(run), str(_cliopts.nevents)])
        print 'Job command with options: %s' % cmd_w_args

        # start the job
        log_hdrs = '='*5 + '{0:^{width}}' + '='*5
        print log_hdrs.format('Starting Vetra', width=40)
        try:
            os.chdir(_cliopts.job_dir)
            retcode = call(cmd_w_args)
            if retcode != 0:
                print 'Oops! It seems Vetra failed!'
            print log_hdrs.format('Vetra returned: %d' % retcode, width=40)

            if _cliopts.cron:   # quit after 1 job when run by cron
                print 'Bye bye'
                break
        except:
            exc = sys.exc_info()
            print 'Oops! Unexpected exception, may crash disgracefully. ' \
                '(%s: %s)' % (exc[0].__name__, exc[1])
            raise
