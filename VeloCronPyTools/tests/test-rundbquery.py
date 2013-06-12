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

from socket import gethostname
__hostname__ = gethostname()


from VeloCronPyTools.rundbquery import (RunDBQuery)
import unittest


class TestJSONQuery(unittest.TestCase):

    def setUp(self):
        self.good_runno = 137259
        self.good_runlist = range(137259, 137301)
        self.bad_runno = 150000
        self.json = True

    def test_good_run_number(self):
        query = RunDBQuery(self.good_runno, self.json)
        self.assertTrue(query.get_valid_runs(1800))

    def test_good_run_list(self):
        query = RunDBQuery(self.good_runlist, self.json)
        self.assertTrue(query.get_valid_runs(1800))

    def test_bad_run_number(self):
        query = RunDBQuery(self.bad_runno, self.json)
        self.assertFalse(query.get_valid_runs(1800))


# @unittest.expectedFailure
@unittest.skipIf(__hostname__.find('plus') < 0,
                 'rundb.RunDB is not supported outside plus* nodes')
class TestQuery(TestJSONQuery):

    def setUp(self):
        super(TestQuery, self).setUp()
        self.json = False


if __name__ == '__main__':
    print '='*5, '{0:^{width}}'.format('RunDBQuery, JSON & rundb.RunDB backend', width=40), '='*5
    unittest.main()
