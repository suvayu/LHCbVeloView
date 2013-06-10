# coding=utf-8
"""This module provides a book keeping output parser.

@author:  Suvayu Ali
@date:    2013-06-10

"""


## rundb.RunDB(): works only at the pit
# 1. get last processed run

# 2. get run fill from (1)

# 3. get latest fill (is getting latest physics fill sufficient?
# probably not)

# 4. generate list of runs from fill id (2), last processed run (1)
# and latest fill (3).

# 5. trim list of runs by run duration.

# 6. Check if another job is already processing before starting to
# process (use lock files)

## alternate approach: use rundb web api (courtesy Gerhard)
# <https://twiki.cern.ch/twiki/bin/view/LHCb/RunDb>
#
# def getRunDBRunInfo(run):
#    import urllib, json
#    info = json.loads( urllib.urlopen("http://lbrundb.cern.ch/api/run/"+str(run)).read() )
#    info['tck'] = int(info['tck'])
#    return info
#
# import sys
# try:
#     info = getRunDBRunInfo(sys.argv[1])
#     print 'run = %(runid)s    ->  DDDB = %(dddbTag)s    CondDB = %(conddbTag)s   starttime = %(starttime)s endtime= %(endtime)s  %(program)s %(programVersion)s  TCK=0x%(tck)08x' % info
# except ValueError as err:
#     print sys.exc_info()[1]
#     print 'Probably %s is an invalid run number' % sys.argv[1]


import sys, os


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


    def get_valid_runs(self, time_threshold):
        """Return valid runs which are longer than threshold duration.

        """
        from timemodule import strptime, mktime
        validruns = []
        for run in self.runs:
            try:
                info = RunInfo(run, self.__use_json__)
            except ValueError:
                print 'Probably %s is not a valid run number' % run
                continue
            epoch = (mktime(strptime(info['starttime'], '%Y-%m-%dT%H:%M:%S')),
                     mktime(strptime(info['endtime'], '%Y-%m-%dT%H:%M:%S')))
            if epoch[1] - epoch[0] > time_threshold:
                validruns.append(run)
        return validruns
