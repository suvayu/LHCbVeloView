# coding=utf-8
"""This module provides a book run database tool (rdbt) parser.

@author:  Suvayu Ali
@date:    2013-06-10

"""


# logging
from logging import getLogger, debug, info, warning, error


class RunDBQuery(object):
    """Query the run database and determine valid runs from given list.

    The rdbt cli tool is used to perform the query.  Note that the
    tool is called once per entry in the run list.

    _regexps_ is a dictionary which holds the regular expressions
    used to parse the different fields.  It can be overridden to add
    support for additional fields.

    __cmd__ is the rdbt shell command used to talk to the run
    database.  You can override this, although it is not recommended.

    """

    def __init__(self, runs):
        """`runs` can be a single run or a list of runs."""

        try:
            self.runs = list(runs)
        except TypeError:
            self.runs = [runs]
        if len(self.runs) > 2:
            raise TypeError('More than 2 numbers in run range: %s' % len(runs))
        if len(self.runs) == 2 and self.runs[1] < self.runs[0]:
            raise ValueError('Wrong run range order: %d !> %d' %
                             (runs[1], runs[0]))

        from subprocess import (check_output, STDOUT,
                                CalledProcessError)
        try:
            cmd = ['rdbt', '-n'] + [str(run) for run in self.runs]
            self.output = check_output(cmd, stderr=STDOUT).splitlines()[1:]
        except CalledProcessError:
            error('Oops! Bad rdbt command.')
            raise

        import re
        self._regexps_ = {
            'marker' : re.compile('^=+$'),
            'run' : re.compile('^run ([0-9]+)'),
            'destination' : re.compile('destination:\s+([^\t]+)'),
            'state' : re.compile('state:\s+([^\t]+)'),
            'startTime' : re.compile('startTime:\s+([^\t]+)'),
            'endTime' : re.compile('.+endTime:\s+([^\t]+)')
        }


    def parse(self):
        """Parse rdbt output and get run information.

        Saves an empty dictionary when parsing fails.  On success,
        saves a dictionary with the fields: startTime, endTime, and
        state for each run.  Hack _regexps_ to include more fields.

        """

        self.run_info = {}
        info = {}               # for first line (needed when no output)
        for line in range(0, len(self.output)):
            # each run info block starts with marker.  The length of a
            # block can vary, can't rely on that.
            for field in self._regexps_:
                match = self._regexps_[field].match(self.output[line])
                if match:
                    if field == 'marker': # always the first to match
                        info = {}
                    else:
                        info[field] = match.groups()[0]
                if len(info) == len(self._regexps_)-1: # -1 because of marker
                    self.run_info[int(info['run'])] = info


    def get_run_info(self, run):
        """Retrive run info with necessary protections.

        Returns None when run does not exist, an empty dictionary when
        parsing failed.

        """

        try:
            info = self.run_info[run]
        except KeyError:
            debug('Run %d: non-existent', run)
            return
        if not info: warning('Run %d: probably parsing failed', run)
        return info


    def get_valid_runs(self, time_threshold=None, timefmt='%Y-%m-%d %H:%M:%S'):
        """Return valid runs longer than threshold seconds.

        List of valid runs include runs started at least an hour ago
        from now.  If no threshold is passed, duration is not checked
        and all such runs are included.

        """

        from time import time, strptime, mktime
        runs_in_bkk, fresh_runs = [], []

        for run in range(self.runs[0], self.runs[-1]+1):
            info = self.get_run_info(run)
            if not info: continue

            # runs in book keeping, destination offline
            if (info['state'] == 'IN BKK' and
                (info['destination'] == 'OFFLINE' or
                 info['destination'] == 'CASTOR')):
                runs_in_bkk.append(run)

            # fresh runs (fallback)
            if (info['state'] == 'ENDED' and
                info['destination'] == 'OFFLINE'):
                fresh_runs.append(run)

        # new runs in book keeping
        runlist = runs_in_bkk if runs_in_bkk else fresh_runs

        def _filter_runs(run):
            """Filter to trim runlist"""
            if time_threshold:
                # end-of-fill calibration runs with missing time info.
                info = self.get_run_info(run)
                if (info['startTime'] == 'None' or info['endTime'] == 'None'):
                    info('Run %d: end-of-fill calibration, skipping', run)
                    return False
                # check duration
                epoch = (mktime(strptime(info['startTime'], timefmt)),
                         mktime(strptime(info['endTime'], timefmt)))
                if epoch[1] - epoch[0] < time_threshold: # too short
                    info('Run %d: shorter than threshold (%d), skipping',
                         run, time_threshold)
                    return False

            if not runs_in_bkk: # no new runs in book keeping
                if time() - epoch[1] < 3600: # run too recent
                    info('Run %d: younger than 1h, skipping', run)
                    return False

            return True

        return filter(_filter_runs, runlist)
