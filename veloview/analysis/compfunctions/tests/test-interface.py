#!/usr/bin/env python

import sys
import os

# fiddle with sys.path so that package is importable
if __file__.startswith('/'):
    sys.path.insert(0, os.path.join('/', *__file__.split('/')[:-3]))
else:
    __path_to_script__ = __file__.split('/')[:-1]  # test directory
    __path_to_script__ += ['..', '..', '..', '..'] # package directory parent
    sys.path.insert(0, os.path.join(os.getcwd(), *__path_to_script__))

from veloview.analysis.score_manipulation import ERROR_LEVELS, Score
from veloview.analysis.compfunctions.interface import *
from ROOT import TH1D
import unittest


class TestInterface(unittest.TestCase):

    def setUp(self):
        self.cmpfn = ComparisonFunction()
        self.hdata = TH1D('hdata1', '', 100, -10 ,10)
        self.href = TH1D('href1', '', 100, -10, 10)

    def tearDown(self):
        del self.cmpfn
        del self.hdata
        del self.href

    def test_check_hists(self):
        @check_hists
        def dummy(data_hist, ref_hist):
            return self.cmpfn.create_final_dict(Score(100), ERROR_LEVELS.OK)
        result = dummy(self.hdata, self.href)
        self.assertEqual(result['lvl'], ERROR_LEVELS.OK)
        result = dummy(self.hdata, None)
        self.assertEqual(result['lvl'], ERROR_LEVELS.ERROR)

    def test_base_class(self):
        self.assertRaises(NotImplementedError, self.cmpfn.compare,
                          self.hdata, self.href, None)


if __name__ == '__main__':
    hdr_fmt = '='*5 + '{0:^{width}}' + '='*5
    print hdr_fmt.format('TestInterface', width=40)
    unittest.main()
