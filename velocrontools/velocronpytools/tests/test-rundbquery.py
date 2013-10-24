#!/usr/bin/env python

import sys
import os

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


from velocrontools.velocronpytools.rundbquery import (RunDBQuery)
import unittest

class TestQuery(unittest.TestCase):

    def setUp(self):
        self.good_runno = 137259
        self.good_runrange = (137250, 137300)
        self.bad_runno = 150000

    def test_good_run_get_run_list(self):
        query = RunDBQuery(self.good_runno)
        query.parse()
        self.assertTrue(query.get_valid_runs(1800))

    def test_good_range_get_run_list(self):
        query = RunDBQuery(self.good_runrange)
        query.parse()
        self.assertTrue(query.get_valid_runs(1800))

    def test_nonexistent_run_get_run_list(self):
        query = RunDBQuery(self.bad_runno)
        query.parse()
        self.assertFalse(query.get_valid_runs(1800))

    def test_incorrect_range(self):
        self.assertRaises(TypeError, RunDBQuery, (1, 2, 3))

    def test_range_wrong_order(self):
        self.assertRaises(ValueError, RunDBQuery, (3, 2))


if __name__ == '__main__':
    hdr_fmt = '='*5 + '{0:^{width}}' + '='*5
    print hdr_fmt.format('RunDBQuery, rdbt backend', width=40)
    unittest.main()
