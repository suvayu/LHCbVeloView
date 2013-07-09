# coding=utf-8
"""This module provides a book keeping output parser.

@author:  Suvayu Ali
@date:    2013-06-10

"""


# for printing exceptions
from traceback import print_exc


class RunDBQuery(object):
    """Query the run database and determine valid runs from given list.

    The rdbt cli tool is used to perform the query.  Note that the
    tool is called once per entry in the run list.

    """

    def __init__(self, runs):
        """`runs` can be a single run or a list of runs.

        """

        try:
            self.runs = list(runs)
        except TypeError:
            self.runs = [runs]
        self.__cmd__ = ['rdbt', '-n']
        self._info_regexps_ = {
            'run' : 'run ([0-9]+)',
            'startTime' : 'startTime:\s+([^\t]+)',
            'endTime' : '.+endTime:\s+([^\t]+)',
            'state' : 'state:\s+([^\t]+)'
        }


    def get_run_info(self, run, strict=True):
        """Return run information.

        Returns None when rdbt command fails.  Returns an empty
        dictionary when parsing of the rdbt output fails.  Returns a
        dictionary with run info with the fileds: run, startTime,
        endTime, and state.

        """

        import re
        from subprocess import (check_output, STDOUT,
                                CalledProcessError)
        try:
            output = check_output(self.__cmd__ + [str(run)],
                                  stderr=STDOUT).splitlines()[1:]
        except CalledProcessError:
            # print 'Oops! Bad rdbt command.'
            # print_exc()
            return

        info = {}
        regexps = self._info_regexps_.copy()
        for line in output:
            regexps_tmp = regexps.copy()
            for field in regexps:
                pat = re.compile(regexps[field])
                match = pat.match(line)
                if match:
                    regexps_tmp.pop(field)
                    info[field] = match.groups()[0]
            if match:           # a field can be matched only once
                regexps = regexps_tmp
        if not info:
            print 'Failed to parse info, run: %s (strict check: %s)' \
                % (run, strict)
            return info

        # protect against end-of-fill calibration runs with
        # missing time info
        if (strict and (info['startTime'] == 'None' or
                        info['endTime'] == 'None')):
            raise ValueError('Bad run number %s (strict check: %s)' %
                             (run, strict))

        return info


    def get_valid_runs(self, time_threshold=None, timefmt='%Y-%m-%d %H:%M:%S'):
        """Return valid runs which are longer than threshold duration.

        If no threshold is passed, list of valid runs include all runs
        started at least an hour ago from now.

        """

        from time import time, strptime, mktime
        validruns, fresh_validruns = [], []
        for run in self.runs:
            try:
                info = self.get_run_info(run, time_threshold)
                if not info:
                    continue
            except ValueError as err:
                # print 'ValueError: %s.  Run %s may be invalid.' % (err, run)
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
