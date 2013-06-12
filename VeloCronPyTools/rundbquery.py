# coding=utf-8
"""This module provides a book keeping output parser.

@author:  Suvayu Ali
@date:    2013-06-10

"""


## Accessing the run database
## <https://twiki.cern.ch/twiki/bin/view/LHCb/RunDb>
## <https://lbtwiki.cern.ch/bin/view/Online/RunDataBase>
# 1. rundb.RunDB(): works only at the pit
#
# 2. alternate approach: use rundb web api (courtesy Gerhard)


def __fix_info__(func):
    """Run info dict returned by 2 methods are different.  Fix it.

    | rundb.RunDB                             | JSON                               |   |
    |-----------------------------------------+------------------------------------+---|
    | 'conddbTag': 'cond-20120831'            | 'conddbTag': 'cond-20120831'       |   |
    | 'dddbTag': 'dddb-20120831'              | 'dddbTag': 'dddb-20120831'         |   |
    | 'destination': 'OFFLINE'                | 'destination': 'OFFLINE'           |   |
    | 'endTime': '2013-02-13 10:07:32.0000'   | 'endtime': '2013-02-13T10:07:32'   | * |
    | 'LHCState':   'PHYSICS'                 | 'LHCState': 'PHYSICS'              |   |
    | 'runID': 137259                         | 'runid': 137259                    | * |
    | 'runType': 'COLLISION13'                | 'runtype': 'COLLISION13'           | * |
    | 'startTime': '2013-02-13 09:07:28.0000' | 'starttime': '2013-02-13T09:07:28' | * |
    | 'state': 6                              | 'state': 'IN BKK'                  | * |
    | 'triggerConfiguration': 'Physics'       | 'triggerConfiguration': 'Physics'  |   |
    | 'veloPosition': 'Closed'                | 'veloPosition': 'Closed'           |   |

    state: ENDED = 2, CREATED = 5, IN_BKK = 6

    """

    def wrapper(*args):
        d = func(*args)
        # force all keys to lower case for consistency
        for key in d:
            d[key.lower()] = d.pop(key)
        if args[2] == False:    # using rundb.RunDB
            ## FIXME: unknown number of cases unhandled
            # handle special cases
            if d['state'] == 2:
                d['state'] == 'ENDED'
            elif d['state'] == 5:
                d['state'] == 'CREATED'
            elif d['state'] == 6:
                d['state'] == 'IN_BKK'
            # strip milliseconds from time string
            d['starttime'] = d['starttime'][:-5]
            d['endtime'] = d['endtime'][:-5]
        else:                # using JSON
            # replace separator between date and time
            d['starttime'] = d['starttime'].replace('T', ' ')
            d['endtime'] = d['endtime'].replace('T', ' ')
        return d
    return wrapper


@__fix_info__
def RunInfo(run, strict=True, json=False):
    """Return run information.  Use the JSON backend if `json` is True."""

    if json:
        import urllib, json
        info = json.loads(urllib.urlopen('http://lbrundb.cern.ch/api/run/'
                                         + str(run)).read())
    else:
        from rundb import RunDB
        db = RunDB()
        info = db.getrun(run)[0]
        if (not isinstance(info, dict) or
            # protect against end-of-fill calibration runs with missing
            # time info when using rundb.RunDB
            (strict and (info['startTime'] == '' or info['endTime'] == ''))):
            raise ValueError('Bad run number %s' % run)
    # fix tck type
    info['tck'] = int(info['tck'])
    return info


class RunDBQuery(object):
    """Query the run database and determine valid runs from provided list."""

    def __init__(self, runs, json=False):
        """`runs` can be a single run or a list of runs.

        `json` determines the backend.

        """

        self.__use_json__ = json
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
                info = RunInfo(run, bool(time_threshold), self.__use_json__)
            except ValueError as err:
                print 'ValueError: %s.  Run %s may be invalid.' % (err, run)
                continue
            if time_threshold:
                epoch = (mktime(strptime(info['starttime'], timefmt)),
                         mktime(strptime(info['endtime'], timefmt)))
                if epoch[1] - epoch[0] > time_threshold:
                    if info['state'] == 'IN BKK':
                        validruns.append(run)
                    elif (info['state'] == 'ENDED' and time() - epoch[1] > 3600):
                        fresh_validruns.append(run)
            else:
                validruns.append(run)
        if validruns:
            return validruns
        else:
            return fresh_validruns
