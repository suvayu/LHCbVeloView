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
from veloview.analysis.compfunctions import *
from veloview.analysis.compfunctions.rootutils import get_fns
from ROOT import TH1D
import unittest


class TestThresholds(unittest.TestCase):

    def setUp(self):
        self.hdata = TH1D('hdata1', '', 100, -10 ,10)
        self.href = TH1D('href1', '', 100, -10, 10)

    def tearDown(self):
        del self.hdata
        del self.href
        
    def test_floor_both(self):
        self.hdata.FillRandom('pol0', 10000)
        cmpfn = FloorThreshold()
        # each bin has ~100 (=10000/100) entires, +/- 3*sqrt(100)=30
        dqscore = cmpfn.compare(self.hdata, self.href, 100-30)
        self.assertEqual(Score(100), dqscore['score'])
        self.assertEqual(ERROR_LEVELS.OK, dqscore['lvl'])
        dqscore = cmpfn.compare(self.hdata, self.href, 100-10)
        self.assertEqual(Score(0), dqscore['score'])
        self.assertEqual(ERROR_LEVELS.ERROR, dqscore['lvl'])

    def test_ceiling_both(self):
        self.hdata.FillRandom('pol0', 10000)
        cmpfn = CeilingThreshold()
        # each bin has ~100 (=10000/100) entires, +/- 3*sqrt(100)=30
        dqscore = cmpfn.compare(self.hdata, self.href, 100+30)
        self.assertEqual(Score(100), dqscore['score'])
        self.assertEqual(ERROR_LEVELS.OK, dqscore['lvl'])
        dqscore = cmpfn.compare(self.hdata, self.href, 100+10)
        self.assertEqual(Score(0), dqscore['score'])
        self.assertEqual(ERROR_LEVELS.ERROR, dqscore['lvl'])

    def test_mean_width_diff_ok(self):
        fn = get_fns('TMath::Gaus', (0, 3), (-10, 10))
        self.hdata.FillRandom(fn[0], 20000)
        self.href.FillRandom(fn[0], 10000)
        cmpfn = MeanWidthDiffRef()
        # mean = 0, width = 3 (RMS)
        dqscore = cmpfn.compare(self.hdata, self.href, 0.1)
        self.assertTrue(dqscore['score'] > Score(90))
        self.assertEqual(dqscore['lvl'], ERROR_LEVELS.OK)

    def test_mean_width_diff_warn(self):
        fn0 = get_fns('TMath::Gaus', (0, 3), (-10, 10))
        fn1 = get_fns('TMath::Gaus', (1, 3), (-10, 10))
        self.hdata.FillRandom(fn0[0], 20000)
        self.href.FillRandom(fn1[0], 10000)
        cmpfn = MeanWidthDiffRef()
        # mean = 0 & 1, width = 3 (RMS)
        dqscore = cmpfn.compare(self.hdata, self.href, 0.1)
        self.assertTrue(dqscore['score'] < Score(40)
                        and dqscore['score'] > Score(20))
        self.assertEqual(dqscore['lvl'], ERROR_LEVELS.WARNING)

    def test_mean_width_diff_error(self):
        fn0 = get_fns('TMath::Gaus', (0, 3), (-10, 10))
        fn1 = get_fns('TMath::Gaus', (1, 2), (-10, 10))
        self.hdata.FillRandom(fn0[0], 20000)
        self.href.FillRandom(fn1[0], 10000)
        cmpfn = MeanWidthDiffRef()
        # mean = 0 & 1, width = 3 & 2 (RMS)
        dqscore = cmpfn.compare(self.hdata, self.href, 0.1)
        self.assertTrue(dqscore['score'] < Score(30))
        self.assertEqual(dqscore['lvl'], ERROR_LEVELS.ERROR)

    @unittest.skip('Test not implemented')
    def test_zero_centred(self):
        pass


if __name__ == '__main__':
    hdr_fmt = '='*5 + '{0:^{width}}' + '='*5
    print hdr_fmt.format('TestThresholds', width=40)
    unittest.main()