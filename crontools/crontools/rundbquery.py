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

    _cmd_ is the rdbt shell command used to talk to the run database.
    You can override this, although it is not recommended.

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

        self._cmd_ = ['rdbt', '-n', '-f'] + [str(run) for run in self.runs]

        import re
        self._regexps_ = {
            'marker' : re.compile('^=+$'),
            'run' : re.compile('^run ([0-9]+)'),
            'destination' : re.compile('destination:\s+([^\t]+)'),
            'state' : re.compile('state:\s+([^\t]+)'),
            'startTime' : re.compile('startTime:\s+([^\t]+)'),
            'endTime' : re.compile('.+endTime:\s+([^\t]+)'),
            'files' : re.compile('(^([0-9]+)_([0-9]+)\.raw$)')
        }

    def call_rdbt(self):
        """Run rdbt command"""
        try:
            from subprocess import (check_output, STDOUT, CalledProcessError)
            self.output = check_output(self._cmd_, stderr=STDOUT).splitlines()[1:]
        except CalledProcessError:
            error('Oops! Bad rdbt command.')
            raise

    def parse(self):
        """Parse rdbt output and get run information.

        Saves an empty dictionary when parsing fails.  On success,
        saves a dictionary with the fields: startTime, endTime, and
        state for each run.  Hack _regexps_ to include more fields.

        """

        self.call_rdbt()
        self.run_info = {}
        rinfo = {}               # for first line (needed when no output)
        for line in range(0, len(self.output)):
            # each run info block starts with marker.  The length of a
            # block can vary, can't rely on that.
            for field in self._regexps_:
                match = self._regexps_[field].match(self.output[line])
                if match:
                    if field == 'marker': # always the first to match
                        rinfo = {}
                    else:
                        if 'files' == field:
                            if rinfo.has_key('files'):
                                rinfo[field] += [match.groups()[0]]
                            else:
                                rinfo[field] = [match.groups()[0]]
                        else:
                            rinfo[field] = match.groups()[0]
                if len(rinfo) >= len(self._regexps_)-2:
                    # 1 less because of marker, maybe another less
                    # when files are deleted
                    self.run_info[int(rinfo['run'])] = rinfo

    def get_run_info(self, run):
        """Retrive run info with necessary protections.

        Returns None when run does not exist, an empty dictionary when
        parsing failed.

        """

        try:
            rinfo = self.run_info[run]
        except KeyError:
            debug('Run %d: non-existent', run)
            return
        if not rinfo: warning('Run %d: probably parsing failed', run)
        return rinfo

    def get_files(self, run):
        """Get RAW file names"""
        rinfo = self.get_run_info(run)
        if rinfo: return rinfo.get('files', None)
        else: return None

    def get_time(self, run, timefmt='%Y-%m-%d %H:%M:%S', epoch=False):
        """Get run time."""
        rinfo = self.get_run_info(run)
        from time import time, strptime, mktime
        if epoch:
            run_duration = (mktime(strptime(rinfo['startTime'], timefmt)),
                            mktime(strptime(rinfo['endTime'], timefmt)))
        else:
            run_duration = (strptime(rinfo['startTime'], timefmt),
                            strptime(rinfo['endTime'], timefmt))
        return run_duration

    def get_valid_runs(self, time_threshold=None, timefmt='%Y-%m-%d %H:%M:%S'):
        """Return valid runs longer than threshold seconds.

        List of valid runs include runs started at least an hour ago
        from now.  If no threshold is passed, duration is not checked
        and all such runs are included.

        """

        runs_in_bkk, fresh_runs = [], []
        for run in range(self.runs[0], self.runs[-1]+1):
            rinfo = self.get_run_info(run)
            if not rinfo: continue
            # runs in book keeping, destination offline
            if (rinfo['state'] == 'IN BKK' and
                (rinfo['destination'] == 'OFFLINE' or
                 rinfo['destination'] == 'CASTOR')):
                runs_in_bkk.append(run)
            # fresh runs (fallback)
            if (rinfo['state'] == 'ENDED' and
                (rinfo['destination'] == 'OFFLINE' or
                 rinfo['destination'] == 'CASTOR')):
                fresh_runs.append(run)
        # new runs in book keeping
        runlist = runs_in_bkk if runs_in_bkk else fresh_runs

        def _filter_runs(run):
            """Filter to trim runlist"""
            epoch = self.get_time(run, timefmt, epoch=True)
            if time_threshold:
                # end-of-fill calibration runs with missing time info.
                rinfo = self.get_run_info(run)
                if (rinfo['startTime'] == 'None' or rinfo['endTime'] == 'None'):
                    info('Run %d: end-of-fill calibration, skipping', run)
                    return False
                # check duration
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
