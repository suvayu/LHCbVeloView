# coding=utf-8
"""This module provides a book keeping output parser.

@author:  Suvayu Ali
@date:    2013-06-10

"""


# for printing exceptions
from traceback import print_exc


class RunDBQuery(object):
    """Query the run database and determine valid runs from provided list."""

    def __init__(self, runs, cmd):
        """`runs` can be a single run or a list of runs.

        """

        self.__trimmed__ = False
        try:
            self.runs = list(runs)
        except TypeError:
            self.runs = [runs]
        try:
            from subprocess import (check_output, STDOUT)
            self.__output__ = check_output(cmd, stderr=STDOUT).splitlines()
        except CalledProcessError:
            print 'Oops! Bad rdbt command.'
            print_exc()
        self._info_regexps_ = {
            'run' : 'run ([0-9]+)',
            'startTime' : 'startTime:\s+([^\t]+)',
            'endTime' : '.+endTime:\s+([^\t]+)',
            'state' : 'state:\s+([^\t]+)'
        }

    def get_run_info(self, run, strict=True):
        """Return run information."""

        import re
        info = {}
        regexps = self._info_regexps_.copy()
        for line in self.__output__:
            for field in regexps:
                pat = re.compile(regexps[field])
                match = pat.match(line)
                if match:
                    regexps_tmp = regexps.copy()
                    regexps_tmp.pop(field)
                    info[field] = match.groups()[0]
            if match:
                regexps = regexps_tmp
        if not info:
            print 'Failed to parse info, run: %s (strict check: %s)' \
                % (run, strict)

        # protect against end-of-fill calibration runs with
        # missing time info
        if (strict and (info['startTime'] == 'None' or
                        info['endTime'] == 'None')):
            raise ValueError('Bad run number %s (strict check: %s)' %
                             (run, strict))

        return info


    def get_valid_runs(self, time_threshold=None, timefmt='%Y-%m-%d %H:%M:%S'):
        """Return valid runs which are longer than threshold duration."""

        from time import time, strptime, mktime
        validruns, fresh_validruns = [], []
        for run in self.runs:
            try:
                info = self.get_run_info(run, time_threshold)
            except ValueError as err:
                print 'ValueError: %s.  Run %s may be invalid.' % (err, run)
                continue
            if time_threshold:
                epoch = (mktime(strptime(info['startTime'], timefmt)),
                         mktime(strptime(info['endTime'], timefmt)))
                if epoch[1] - epoch[0] > time_threshold:
                    if info['state'] == 'IN BKK':
                        validruns.append(run)
                    elif (info['state'] == 'ENDED' and
                          time() - epoch[1] > 3600):
                        fresh_validruns.append(run)
            else:
                validruns.append(run)
        if validruns:
            return validruns
        else:
            return fresh_validruns
