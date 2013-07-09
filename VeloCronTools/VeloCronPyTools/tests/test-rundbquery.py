#!/usr/bin/env python

import sys, os

# fiddle with sys.path so that package is importable
if __file__.startswith('/'):
    # FIXME: clean up
    sys.path.insert(0, os.path.join('/', *__file__.split('/')[:-3]))
else:
    __pkg_dir__ = __file__.split('/')[:-1] # test directory
    __pkg_dir__ += ['..', '..']            # package directory parent
    sys.path.insert(0, os.path.join(os.getcwd(), *__pkg_dir__))

__test_dir__ = os.path.dirname(__file__) # test directory
if __test_dir__ == '':
    __test_dir__ = './'

from socket import gethostname
__hostname__ = gethostname()


from VeloCronPyTools.rundbquery import (RunDBQuery)
import unittest

class TestQuery(unittest.TestCase):

    def setUp(self):
        self.good_runno = 137259
        self.good_runlist = range(137250, 137300)
        self.bad_runno = 150000
        self.cmd = ['grep', __test_dir__ + '/rdbt_run_range.txt', '-B2', '-A6', '-e']

    def hack_query_cmd(self, query):
        if __hostname__.find('plus') != 0:
            query.__cmd__ = self.cmd

    def test_good_run_number(self):
        query = RunDBQuery(self.good_runno)
        self.hack_query_cmd(query)
        self.assertTrue(query.get_valid_runs(1800))

    def test_good_run_list(self):
        query = RunDBQuery(self.good_runlist)
        self.hack_query_cmd(query)
        self.assertTrue(query.get_valid_runs(1800))

    def test_bad_run_number(self):
        query = RunDBQuery(self.bad_runno)
        self.hack_query_cmd(query)
        self.assertFalse(query.get_valid_runs(1800))


if __name__ == '__main__':
    hdr_fmt = '='*5 + '{0:^{width}}' + '='*5
    print hdr_fmt.format('RunDBQuery, rdbt backend', width=40)
    unittest.main()
