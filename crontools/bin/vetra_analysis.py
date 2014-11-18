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
    runs = range(last_run + 1, last_run + 1000) # NOTE: use 10 for testing

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
    jobopts = '/calib/velo/dqm/DQS/cron/FilterBeamBeam_Heartbeat.py'


## trim list of runs by run duration from run database.
from crontools.rundbquery import RunDBQuery
debug('Run list before trimming: %s' % runs)
# query the database and get validated list of runs
query = RunDBQuery(runs)
query.parse()
runs = query.get_valid_runs(_cliopts.threshold)
debug('Run list after trimming: %s' % runs)


from crontools.utils import add_runs, make_dir_tree
from crontools.runlock import RunLock
from crontools.vetraopts import (get_runinfo, get_gaudi_opts, get_runinfo,
                                 get_optfile, get_datacard)

## acquire lock and run job
for run in runs:
    info('Processing run: %s, stream: %s' % (run, stream))
    # job directory
    jobdir_t = make_dir_tree(run, prefix=_cliopts.jobdir)
    try:
        try:
            os.makedirs(jobdir_t)
        except OSError as err:
            if err.errno != errno.EEXIST: raise
        os.chdir(jobdir_t)
        debug('Job directory: %s', jobdir_t)
    except OSError as err:
        error('Run %d, stream %s: Oops! Problem with job directory.',
              run, stream, exc_info=True)
        continue
    try:
        # start the job
        with RunLock(jobdir_t, run, stream):
            from subprocess import call
            # Default Gaudi option files
            gaudi_w_opts = get_gaudi_opts(stream)

            # option files and datacards
            year = query.get_time(run)[0].tm_year       # info from run DB query
            runinfo = get_runinfo(run, year, stream) # info for option files
            prefix = 'VELODQM_{}_{}_{}'.format(run, runinfo['timestamp'], stream)
            optfiles = {
                # '{}.useropts.py'.format(prefix): get_optfile(), # same as FilterBeamBeam_HeartBeat
                '{}.data.py'.format(prefix): get_datacard(runinfo, query.get_files(run),
                                                          maxevts = _cliopts.nevents)
            }
            # create them
            try:
                for optfile, contents in optfiles.items():
                    optfile = file(optfile, 'w')
                    optfile.write(contents)
                    optfile.close()
            except OSError:
                error('Exception while writing option files', exc_info=True)
                continue

            # complete command
            cmd_w_args = gaudi_w_opts + optfiles.keys() + jobopts.split(' ')
            debug('Job command: %s', ' '.join(cmd_w_args))

            info('Starting Vetra')
            logfile = open('{}.log'.format(prefix), 'w')
            retcode = call(cmd_w_args, stdout=logfile)
            if retcode != 0:
                warning('Oops! It seems Vetra failed!')
            else:
                retcode = add_runs(run, runlist, prefix=os.path.dirname(__file__))
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
