#!/usr/bin/env python

import os

if __name__ == '__main__':
    import sys

    # fiddle with sys.path so that package is importable
    if __file__.startswith('/'):
        sys.path.insert(0, os.path.join('/', *__file__.split('/')[:-3]))
    else:
        __path_to_script__ = __file__.split('/')[:-1]  # test directory
        __path_to_script__ += ['..', '..'] # package directory parent
        sys.path.insert(0, os.path.join(os.getcwd(), *__path_to_script__))

from veloview.core.score_manipulation import ERROR_LEVELS, Score
from veloview.core.interface import *
from ROOT import TH1D
import unittest


class TestInterface(unittest.TestCase):

    def setUp(self):
        self.hdata = TH1D('hdata1', '', 100, -10 ,10)
        self.href = TH1D('href1', '', 100, -10, 10)

    def tearDown(self):
        del self.hdata
        del self.href

    def test_check_hists1(self):
        """Test decorator to check only valid data histogram"""
        class dummy(ComparisonFunction):
            @check_hists1
            def compare(dummy_self, data_hist, ref_hist):
                return dummy_self.create_final_dict(Score(100), ERROR_LEVELS.OK)
        result = dummy().compare(self.hdata, None)
        self.assertEqual(result['lvl'], ERROR_LEVELS.OK)
        result = dummy().compare(None, None)
        self.assertEqual(result['lvl'], ERROR_LEVELS.ERROR)

    def test_check_hists2(self):
        """Test decorator to check valid data and reference histograms"""
        class dummy(ComparisonFunction):
            @check_hists2
            def compare(dummy_self, data_hist, ref_hist):
                return dummy_self.create_final_dict(Score(100), ERROR_LEVELS.OK)
        result = dummy().compare(self.hdata, self.href)
        self.assertEqual(result['lvl'], ERROR_LEVELS.OK)
        result = dummy().compare(self.hdata, None)
        self.assertEqual(result['lvl'], ERROR_LEVELS.ERROR)

    def test_check_binning(self):
        """Test decorator to check consistent histogram binning"""
        class dummy(ComparisonFunction):
            @check_hists2
            @check_binning
            def compare(dummy_self, data_hist, ref_hist):
                return dummy_self.create_final_dict(Score(100), ERROR_LEVELS.OK)
        # all OK
        result = dummy().compare(self.hdata, self.href)
        self.assertEqual(result['lvl'], ERROR_LEVELS.OK)
        # bad binning
        bad_href = self.href.Rebin(2, 'hdata_cl')
        result = dummy().compare(self.hdata, bad_href)
        self.assertEqual(result['lvl'], ERROR_LEVELS.ERROR)
        # bad histogram
        result = dummy().compare(self.hdata, None)
        self.assertEqual(result['lvl'], ERROR_LEVELS.ERROR)

    def test_base_class(self):
        """Test base class"""
        self.assertRaises(NotImplementedError, ComparisonFunction().compare,
                          self.hdata, self.href, None)


if __name__ == '__main__':
    hdr_fmt = '='*5 + '{0:^{width}}' + '='*5
    print hdr_fmt.format('TestInterface', width=40)
    unittest.main()
