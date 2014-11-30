#!/usr/bin/env python
# coding=utf-8

"""This script runs Vetra analysis to produce monitoring histograms.

@author:  Suvayu Ali
@date:    2013-06-11

"""


## option parsing
import argparse
parser = argparse.ArgumentParser(description=__doc__)
class RawArgDefaultFormatter(argparse.ArgumentDefaultsHelpFormatter,
                             argparse.RawDescriptionHelpFormatter):
    pass
parser.formatter_class = RawArgDefaultFormatter

parser.add_argument('run', type=int, help='Run to process.')
parser.add_argument('-r', '--run-range', nargs=2, type=int,
                    metavar=('START', 'END'), help='Run range to process.')
parser.add_argument('-s', '--stream', dest='stream', default='NZS',
                    choices=['NZS', 'ZS', 'NZS+ZS', 'TED14', 'NOISE', 'RR',
                             'ADCDELAYSCAN', 'GAIN', 'TAE', 'EXCM', 'ERROR',
                             'ALLZS', 'DEBUG', 'COLLISION', 'BADSTRIPS',
                             'HVOff', 'HVOn'], help='Which stream to process.')
parser.add_argument('-n', '--nevents', dest='nevents', type=int, default=20000,
                    help='Number of events to process.')
parser.add_argument('-t', '--time-threshold', dest='threshold', default=1800,
                    type=int, help='Minimum run duration in seconds.')
parser.add_argument('-jd', '--job-dir', dest='jobdir', help='Job directory.',
                    default='/calib/velo/dqm/VeloView/VetraOutput')
parser.add_argument('-o', '--job-options', dest='jobopts', default='',
                    help='Override default Vetra job options (quoted).')
parser.add_argument('-c', '--cron', action='store_true',
                    help='Run from a cron job.')
parser.add_argument('-d', '--debug', dest='debug', action='store_true',
                    help='Turn debug on messages.')
parser.add_argument('-l', '--local', action='store_true', default=False,
                    help='Try to find files locally.')
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
import os, errno, sys

debug('Script options: %s' % _cliopts)
# stream to process
stream = _cliopts.stream
jobdir = _cliopts.jobdir
jobopts = _cliopts.jobopts
# old jobopts: '/calib/velo/dqm/DQS/cron/FilterBeamBeam_Heartbeat.py'

from crontools.utils import get_last_run
runlist = '/calib/velo/dqm/VeloView/VetraOutput/RunList.txt'
graveyardrunlist = '/calib/velo/dqm/VeloView/VetraOutput/GraveyardRunList.txt'
# run range to process (1k runs from last processed run)
if _cliopts.run:
    runs = _cliopts.run
elif _cliopts.run_range:
    runs = _cliopts.run_range
else:
    debug('No run range or list was provided. ' \
          'List of runs will be determined automagically!')
    # NOTE: We only process runs longer than time threshold (~30 min
    # default), many runs are likely to be skipped b/c of this
    # condition.  Assign an arbitrary run range (1k is long enough to
    # cover a technical stop) such that we always find at least one
    # significant run.
    last_run = max(get_last_run(runlist),get_last_run(graveyardrunlist))
    runs = [last_run + 1, last_run + 1000]


## trim list of runs by run duration from run database.
from crontools.rundbquery import RunDBQuery
debug('Run list before trimming: %s' % runs)
# query the database and get validated list of runs
query = RunDBQuery(runs)
query.parse()
runs = query.get_valid_runs(_cliopts.threshold)
# NOTE: If there is a need to further filter the run list according to
# other criteria, one can use something like this:
# def _my_filter(run):
#     rinfo = query.get_run_info(run)
#     if test(rinfo): return True
#     return False
# runs = filter(_my_filter, runs)
debug('Run list after trimming: %s' % runs)


## acquire lock and run job
from crontools.utils import add_runs, make_dir_tree
from crontools.runlock import RunLock
from crontools.vetraopts import (get_runinfo, get_gaudi_opts, get_runinfo,
                                 get_optfile, get_datacard)

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
        retcode = add_runs(run, graveyardrunlist, prefix=os.path.dirname(__file__))
        if retcode: error('Run %d couldn\'t be added to the graveyard list.')
        continue
    try:
        # start the job
        with RunLock(jobdir_t, run, stream):
            from subprocess import call
            # Default Gaudi option files
            gaudi_w_opts = get_gaudi_opts(stream)

            # option files and datacards
            year = query.get_time(run)[0].tm_year       # info from run DB query
            partition = query.get_run_info(run)['partitionName']
            # info for option files, time stamp is also created here
            runinfo = get_runinfo(run, year, partition, stream)
            if _cliopts.local: runinfo['protocol'] = 'file'
            prefix = 'VELODQM_{}_{}_{}'.format(run, runinfo['timestamp'], stream)
            optfiles = {
                '{}.useropts.py'.format(prefix): get_optfile(), # same as FilterBeamBeam_HeartBeat
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
                warning('Oops! It seems Vetra failed: %d', retcode)
                retcode = add_runs(run, graveyardrunlist, prefix=os.path.dirname(__file__))
                if retcode: error('Run %d couldn\'t be added to the graveyard list.')
            else:
                info('Vetra returned with: %d', retcode)
                size = os.stat('{}.root'.format(prefix)).st_size
                if size < 3000000:
                    warning('Output root file is too small: %d bytes.', size)
                retcode = add_runs(run, runlist, prefix=os.path.dirname(__file__))
                if retcode: error('Run %d couldn\'t be added to the list.')
    except:
        error('Oops! Unexpected exception, crashing disgracefully.',
              exc_info=True)
        raise
    if _cliopts.cron:   # quit after 1 job when run by cron
        debug('Running from cron, quitting after 1 job.')
        break

sys.exit('Bye bye ...')
