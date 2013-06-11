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


def RunInfo(run, json=False):
    """Return run information.  Use the JSON backend if `json` is True."""

    if json:
        import urllib, json
        info = json.loads(urllib.urlopen('http://lbrundb.cern.ch/api/run/'
                                         + str(run)).read())
    else:
        from rundb import RunDB
        db = RunDB()
        info = db.getrun(run)[0]
        if not isinstance(info, dict):
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


    def get_valid_runs(self, time_threshold, timefmt='%Y-%m-%dT%H:%M:%S'):
        """Return valid runs which are longer than threshold duration."""

        from timemodule import strptime, mktime
        validruns = []
        for run in self.runs:
            try:
                info = RunInfo(run, self.__use_json__)
            except ValueError as err:
                print 'ValueError: %s.  Run %s may be invalid.' % (err, run)
                continue
            epoch = (mktime(strptime(info['starttime'], timefmt)),
                     mktime(strptime(info['endtime'], timefmt)))
            if epoch[1] - epoch[0] > time_threshold:
                validruns.append(run)
        return validruns
