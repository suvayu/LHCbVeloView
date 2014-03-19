"""This module will hold complex comparison functions"""

from interface import ComparisonFunction, check_hists2, check_binning
from veloview.analysis.score_manipulation import ERROR_LEVELS, Score


class Chi2Test(ComparisonFunction):
    """Chi^2 test.

    """

    @check_hists2
    @check_binning
    def compare(self, data_hist, ref_hist, options):
        """
        data_hist -- data histogram
        ref_hist  -- reference histogram (ignored)
        options   -- options for TH1::Chi2Test()

        """

        options = options.lower()
        pvalue_or_chi2 = ref_hist.Chi2Test(data_hist, options)

        if options.find('chi2') < 0: # p-value
            score = Score(pvalue_or_chi2 * 100) # FIXME: is this correct?
            if pvalue_or_chi2 < 0.8:
                lvl = ERROR_LEVELS.ERROR
            else:
                lvl = ERROR_LEVELS.OK
        else:                   # chi2
            if options.find('chi2/ndf') < 0: # not chi2/ndf
                ndf = data_hist.GetNbinsX()
                pvalue_or_chi2 = pvalue_or_chi2/ndf
            score = Score(100 - pvalue_or_chi2*20)
            if pvalue_or_chi2 > 2:
                lvl = ERROR_LEVELS.ERROR
            elif pvalue_or_chi2 > 1:
                lvl = ERROR_LEVELS.WARNING
            else:
                lvl = ERROR_LEVELS.OK
            
        return self.create_final_dict(score, lvl)
