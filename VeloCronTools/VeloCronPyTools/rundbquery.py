# coding=utf-8
"""This module provides a book keeping output parser.

@author:  Suvayu Ali
@date:    2013-06-10

"""


# for printing exceptions
from traceback import print_exc

## Note: works only at the pit
# Oracle database
from DbModel import createEngine_Oracle

# Interface to database
from RunDatabase import RunDbServer

## Run states
from RunDatabase_Defines import (RUN_ACTIVE, RUN_ENDED, RUN_MIGRATING,
                                 RUN_WAITDELETE, RUN_CREATED,
                                 RUN_IN_BKK, RUN_DEFERRED)
# The default run lifecycle is:
#    Not existing -> CREATED -> ACTIVE -> (DEFERRED Optional) -> ENDED -> BKK_ADDED
#
# RUN_ACTIVE          = 1
# RUN_ENDED           = 2
# RUN_MIGRATING       = 3
# RUN_WAITDELETE      = 4
# RUN_CREATED         = 5
# RUN_IN_BKK          = 6
# RUN_DEFERRED        = 7


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
        try:
            self.__rundb__ = RunDbServer(engine=createEngine_Oracle())
        except Exception:
            print 'Oops! Could not connect to rundb.'
            print_exc()


    def get_run_info(self, run, strict=True):
        """Return run information."""

        infofields = ['runID', 'startTime', 'endTime', 'state']
        status, infolist = self.__rundb__.getRuns(fields = infofields, runID = run)
        if not status:
            print 'Failed to get run info, run: %s (strict check: %s)' \
                % (run, strict)

        # convert list to dictionary
        info = {}
        for idx, field in enumerate(infofields):
            info[field] = infolist[0][idx]

        # protect against end-of-fill calibration runs with
        # missing time info
        if (strict and (info['startTime'] == '' or info['endTime'] == '')):
            raise ValueError('Bad run number %s (strict check: %s)' %
                             (run, strict))

        return info


    def get_valid_runs(self, time_threshold=None):
        """Return valid runs which are longer than threshold duration."""

        from time import time, strptime, mktime
        validruns, fresh_validruns = [], []
        for run in self.runs:
            try:
                info = self.get_run_info(run, time_threshold)
            except ValueError, err:
                print 'ValueError: %s.  Run %s may be invalid.' % (err, run)
                continue
            if time_threshold:
                epoch = (mktime(info['startTime'].timetuple()),
                         mktime(info['endTime'].timetuple()))
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
