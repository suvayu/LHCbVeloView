#!/usr/bin/env python

import sys
import os

# fiddle with sys.path so that package is importable
if __file__.startswith('/'):
    # FIXME: clean up
    sys.path.insert(0, os.path.join('/', *__file__.split('/')[:-3]))
else:
    __path_to_script__ = __file__.split('/')[:-1] # test directory
    __path_to_script__ += ['..']            # package directory parent
    sys.path.insert(0, os.path.join(os.getcwd(), *__path_to_script__))

from crontools.utils import *
import unittest


class TestUtils(unittest.TestCase):

    def setUp(self):
        self.runno = 54321
        self.runstr = str(self.runno)
        self.fname = '/tmp/RunList.txt'

    def tearDown(self):
        if os.path.exists(self.fname):
            os.remove(self.fname)

    def test_digit(self):
        digit = get_digit(self.runno, 3)
        self.assertEqual(self.runstr[-3], digit)
        self.assertEqual(self.runstr[-3]+'0'*2, get_mult_10(digit, 2))

    def test_ifs(self):
        self.assertTrue(if_ndigits(self.runno, 5))

    def test_dir_tree(self):
        self.assertEqual(make_dir_tree(self.runno),
                         '50000s/54000s/54300s/{}'.format(self.runno))

    def test_add_runs(self):
        add_runs(self.runno, self.fname, prefix='bin')
        runs = [41, 42, 43]
        add_runs(runs, self.fname, prefix='bin')
        runlist = open(self.fname, 'r')
        lines = [int(i) for i in runlist.readlines()]
        self.assertSequenceEqual(runs + [self.runno], lines)

    def test_last_run(self):
        runs = [str(i) + '\n' for i in xrange(50000, 55000)]
        testfile = file(self.fname, 'w')
        testfile.writelines(runs)
        testfile.close()
        self.assertEqual(54999, get_last_run(self.fname))


if __name__ == '__main__':
    hdr_fmt = '='*5 + '{0:^{width}}' + '='*5
    print hdr_fmt.format('utils', width=40)
    unittest.main()
