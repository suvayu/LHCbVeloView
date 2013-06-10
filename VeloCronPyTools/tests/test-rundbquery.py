#!/usr/bin/env python

import sys, os

# fiddle with sys.path so that package is importable
if __file__.startswith('/'):
    # FIXME: clean up
    sys.path.insert(0, os.path.join('/', *__file__.split('/')[:-3]))
else:
    __path_to_script__ = __file__.split('/')[:-1] # test directory
    __path_to_script__ += ['..', '..']            # package directory parent
    sys.path.insert(0, os.path.join(os.getcwd(), *__path_to_script__))

from VeloCronPyTools.rundbquery import (RunDBQuery)
import unittest


class TestJSONQuery(unittest.TestCase):

    def setUp(self):
        self.good_runno = 137259
        self.good_runlist = range(137259, 137301)
        self.bad_runno = 150000

    def test_good_run_number(self):
        query = RunDBQuery(self.good_runno, True)
        self.assertTrue(query.get_valid_runs(1800))

    def test_good_run_list(self):
        query = RunDBQuery(self.good_runlist, True)
        self.assertTrue(query.get_valid_runs(1800))

    def test_bad_run_number(self):
        query = RunDBQuery(self.bad_runno, True)
        self.assertFalse(query.get_valid_runs(1800))


if __name__ == '__main__':
    print '='*5, '{0:^{width}}'.format('RunDBQuery with JSON backend', width=40), '='*5
    unittest.main()
