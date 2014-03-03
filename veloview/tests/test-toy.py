#!/usr/bin/env python

import sys
import os

# fiddle with sys.path so that package is importable
if __file__.startswith('/'):
    sys.path.insert(0, os.path.join('/', *__file__.split('/')[:-3]))
else:
    __path_to_script__ = __file__.split('/')[:-1]  # test directory
    __path_to_script__ += ['..', '..'] # package directory parent
    sys.path.insert(0, os.path.join(os.getcwd(), *__path_to_script__))

from veloview import (Combiner, FloorThreshold, CeilingThreshold,
                      MeanWidthDiffRef, AbsoluteBandRef, ZeroCentredBandRef)
from veloview.analysis.compfunctions.rootutils import get_simple_fns, get_fns
from veloview.core.conf.env.combiner_description_dictionary import (STANDARD_BRANCH_DICT,
                                                                    STANDARD_LEAF_DICT,
                                                                    merge_dicts,
                                                                    create_leaf_dict_with_path)

from ROOT import TFile, TH1D, TF1
from math import sqrt
import unittest


class TestCombinersWToys(unittest.TestCase):

    def setUp(self):
        self.rfdata = TFile('/tmp/fdata.root', 'recreate')
        self.rfref = TFile('/tmp/fref.root', 'recreate')

        frefl, fdatal, comp_fns = [], [], []

        # fns = {}
        # fns['poly'] = get_simple_fns('pol0', (-10, 10)) # for basic threshold checks
        # fns['gauss01'] = get_fns('TMath::Gaus', (0, 1), (-10, 10))
        # fns['gauss02'] = get_fns('TMath::Gaus', (0, 2), (-10, 10))
        # fns['gauss03'] = get_fns('TMath::Gaus', (0, 3), (-10, 10))
        # fns['gauss12'] = get_fns('TMath::Gaus', (1, 2), (-10, 10))

        frefl.append(('fn-pol0', TF1('fn-pol0', '5', -10, 10)))
        fdatal.append(('fn-pol4', TF1('fn-pol4', '5', -10, 10)))
        comp_fns.append((FloorThreshold(), 200 - 3*sqrt(200))) # 3 sigma

        frefl.append(('fn-pol1', TF1('fn-pol1', '5', -10, 10)))
        fdatal.append(('fn-pol5', TF1('fn-pol5', '5', -10, 10)))
        comp_fns.append((FloorThreshold(), 200 - sqrt(200)))   # 1 sigma

        frefl.append(('fn-pol2', TF1('fn-pol2', '5', -10, 10)))
        fdatal.append(('fn-pol6', TF1('fn-pol6', '5', -10, 10)))
        comp_fns.append((CeilingThreshold(), 200 + 3*sqrt(200))) # 3 sigma

        frefl.append(('fn-pol3', TF1('fn-pol3', '5', -10, 10)))
        fdatal.append(('fn-pol7', TF1('fn-pol7', '5', -10, 10)))
        comp_fns.append((CeilingThreshold(), 200 + sqrt(200))) # 1 sigma

        frefl.append(get_fns('TMath::Gaus', (0, 3), (-10, 10)))
        fdatal.append(get_fns('TMath::Gaus', (0, 3), (-10, 10)))
        comp_fns.append((MeanWidthDiffRef(), 0.1))            # 10%

        frefl.append(get_fns('TMath::Gaus', (0, 3), (-10, 10)))
        fdatal.append(get_fns('TMath::Gaus', (1, 2), (-10, 10)))
        comp_fns.append((MeanWidthDiffRef(), 0.1))

        frefl.append(get_fns('TMath::Gaus', (0, 1), (-10, 10)))
        fdatal.append(get_fns('TMath::Gaus', (0, 1), (-10, 10)))
        comp_fns.append((ZeroCentredBandRef(), 5)) # 5 sigma

        frefl.append(get_fns('TMath::Gaus', (0, 1), (-10, 10)))
        fdatal.append(get_fns('TMath::Gaus', (0, 2), (-10, 10)))
        comp_fns.append((ZeroCentredBandRef(), 3)) # 3 sigma

        # frefl.append(get_fns('TMath::Landau', (0, 3), (-10, 10)))
        # fdatal.append(get_fns('TMath::Landau', (0, 3), (-10, 10)))
        # comp_fns.append()

        # frefl.append(get_fns('TMath::Landau', (0, 3), (-10, 10)))
        # fdatal.append(get_fns('TMath::Landau', (0, 3), (-10, 10)))
        # comp_fns.append()



        assert(len(frefl) == len(fdatal) == len(comp_fns))

        self.comb_dict = {}
        self.eval_dict = {}
        for i in range(len(frefl)):
            hname = frefl[i][0].replace('fn-', 'hist-', 1)
            self.comb_dict[frefl[i][0]+'Combiner'] = create_leaf_dict_with_path(hname)
            self.eval_dict[frefl[i][0]+'Combiner'] = {'Function': comp_fns[i][0], 'Argument': comp_fns[i][1]}

            href = TH1D(hname, '', 100, -10 ,10)
            href.FillRandom(frefl[i][0], 10000)
            self.rfref.WriteTObject(href)
            del href
            hdata = TH1D(hname, '', 100, -10 ,10)
            hdata.FillRandom(fdatal[i][0], 10000)
            self.rfdata.WriteTObject(hdata)
            del hdata

        self.comb_dict = {
            'MasterCombiner': merge_dicts(
                {"weight": 1.0, "minWW": 10, "minWE": 25, "minEW": 1, "minEE": 2},
                self.comb_dict)
        }

        # close files cleanly
        self.rfdata.Close()
        self.rfref.Close()

    def tearDown(self):
        del self.rfdata
        del self.rfref
        del self.comb_dict
        del self.eval_dict

    def test_combiner_w_toy(self):
        mycombiner = Combiner(self.comb_dict, self.eval_dict,
                              self.rfdata.GetName(), self.rfref.GetName())
        mycombiner.evaluate()
        # print mycombiner
        self.assertTrue(mycombiner)


if __name__ == '__main__':
    hdr_fmt = '='*5 + '{0:^{width}}' + '='*5
    print hdr_fmt.format('TestCombinersWToys', width=40)
    unittest.main()
