# coding=utf-8
"""This module provides a book keeping output parser.

@author:  Suvayu Ali
@date:    2013-06-10

"""


## Accessing the run database
## <https://twiki.cern.ch/twiki/bin/view/LHCb/RunDb>
## <https://lbtwiki.cern.ch/bin/view/Online/RunDataBase>
# 1. rundb.RunDB(): works only at the pit


## Run states (copied from RunDatabase.RunDatabase_Defines)
# The default run lifecycle is:
#    Not existing -> CREATED -> ACTIVE -> (DEFERRED Optional) -> ENDED -> BKK_ADDED
#
RUN_ACTIVE          = 1
RUN_ENDED           = 2
RUN_MIGRATING       = 3
RUN_WAITDELETE      = 4
RUN_CREATED         = 5
RUN_IN_BKK          = 6
RUN_DEFERRED        = 7


def RunInfo(run, strict=True):
    """Return run information."""

    from rundb import RunDB
    db = RunDB()
    info = db.getrun(run)[0]
    if (not isinstance(info, dict) or
        # protect against end-of-fill calibration runs with missing
        # time info when using rundb.RunDB
        (strict and (info['startTime'] == '' or info['endTime'] == ''))):
        raise ValueError('Bad run number %s (strict check: %s)'
                         % (run, strict))
    # fix tck type
    info['tck'] = int(info['tck'])
    # strip milliseconds from time string
    info['startTime'] = info['startTime'][:-5]
    info['endTime'] = info['endTime'][:-5]

    return info


class RunDBQuery(object):
    """Query the run database and determine valid runs from provided list."""

    def __init__(self, runs):
        """`runs` can be a single run or a list of runs.

        """

        self.__trimmed__ = False
        try:
            self.runs = list(runs)
        except TypeError:
            self.runs = [runs]


    def get_valid_runs(self, time_threshold=None, timefmt='%Y-%m-%d %H:%M:%S'):
        """Return valid runs which are longer than threshold duration."""

        from time import time, strptime, mktime
        validruns, fresh_validruns = [], []
        for run in self.runs:
            try:
                info = RunInfo(run, bool(time_threshold))
            except ValueError as err:
                print 'ValueError: %s.  Run %s may be invalid.' % (err, run)
                continue
            if time_threshold:
                epoch = (mktime(strptime(info['startTime'], timefmt)),
                         mktime(strptime(info['endTime'], timefmt)))
                if epoch[1] - epoch[0] > time_threshold:
                    if info['state'] == RUN_IN_BKK:
                        validruns.append(run)
                    elif (info['state'] == RUN_ENDED and
                          time() - epoch[1] > 3600):
                        fresh_validruns.append(run)
            else:
                validruns.append(run)
        if validruns:
            return validruns
        else:
            return fresh_validruns
