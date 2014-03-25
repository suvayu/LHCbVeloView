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
from veloview.analysis.compfunctions.stats import *
from veloview.analysis.compfunctions.rootutils import get_fns
from ROOT import TH1D
import unittest


class TestComparisons(unittest.TestCase):

    def setUp(self):
        self.href = TH1D('href1', '', 100, -10, 10)
        self.hdata = TH1D('hdata1', '', 100, -10 ,10)
        self.hdata_bad = TH1D('hdata_bad', '', 100, -10 ,10)

        fn = get_fns('TMath::Gaus', (0, 3), (-10, 10))
        self.href.FillRandom(fn[0], 10000)
        fn = get_fns('TMath::Gaus', (0, 3), (-10, 10))
        self.hdata.FillRandom(fn[0], 10000)
        fn = get_fns('TMath::Gaus', (1, 3), (-10, 10))
        self.hdata_bad.FillRandom(fn[0], 10000)

    def tearDown(self):
        del self.href
        del self.hdata
        del self.hdata_bad

    def test_KolmogorovSmirnovTest(self):
        cmpfn = KolmogorovSmirnovTest()
        dqscore = cmpfn.compare(self.hdata, self.href, '')
        self.assertGreaterEqual(dqscore['score'], Score(5))
        self.assertEqual(dqscore['lvl'], ERROR_LEVELS.OK)
        dqscore = cmpfn.compare(self.hdata_bad, self.href, '')
        self.assertLess(dqscore['score'], Score(5))
        self.assertNotEqual(dqscore['lvl'], ERROR_LEVELS.OK)

    def test_Chi2Test_pvalue(self):
        cmpfn = Chi2Test()
        dqscore = cmpfn.compare(self.hdata, self.href, '')
        self.assertGreaterEqual(dqscore['score'], Score(5))
        self.assertEqual(dqscore['lvl'], ERROR_LEVELS.OK)
        dqscore = cmpfn.compare(self.hdata_bad, self.href, '')
        self.assertLess(dqscore['score'], Score(5))
        self.assertNotEqual(dqscore['lvl'], ERROR_LEVELS.OK)

    def test_Chi2Test_chi2(self):
        cmpfn = Chi2Test()
        dqscore = cmpfn.compare(self.hdata, self.href, 'chi2')
        self.assertGreaterEqual(dqscore['score'], Score(50))
        self.assertEqual(dqscore['lvl'], ERROR_LEVELS.OK)
        dqscore = cmpfn.compare(self.hdata, self.href, 'chi2/ndf')
        self.assertGreaterEqual(dqscore['score'], Score(50))
        self.assertEqual(dqscore['lvl'], ERROR_LEVELS.OK)


if __name__ == '__main__':
    hdr_fmt = '='*5 + '{0:^{width}}' + '='*5
    print hdr_fmt.format('TestComparisons', width=40)
    unittest.main()
