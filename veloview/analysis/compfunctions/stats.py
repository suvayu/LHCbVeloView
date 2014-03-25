# coding=utf-8
"""This module will hold complex comparison functions"""

from interface import ComparisonFunction, check_hists2, check_binning
from veloview.analysis.score_manipulation import ERROR_LEVELS, Score


# /**
#  * Kolmogorov-Smirnov goodness of fit test.
#  * Max distance b/w distributions
#  *
#  * @param parent
#  * @param test
#  *
#  * @return
#  */
# Double_t cdfKSDist(const TH1 *parent, const TH1 *test)
# {
#   if (parent->GetNbinsX() != test->GetNbinsX()) return -9E20;

#   //Get the KS distance
#   Double_t sumParent = 0.0, sumTest = 0.0;

#   for (int i = 1; i <= parent->GetNbinsX(); ++i)
#     {
#       sumParent += parent->GetBinContent(i);
#       sumTest += test->GetBinContent(i);
#     }

#   Double_t sParent = 1/sumParent;
#   Double_t sTest = 1/sumTest;

#   Double_t rSumParent = 0.0, rSumTest = 0.0, maxDiff = -9E20;
#   for (int i = 1; i <= parent->GetNbinsX(); ++i)
#     {
#       rSumParent += sParent*parent->GetBinContent(i);
#       rSumTest += sTest*test->GetBinContent(i);
#       Double_t diff = TMath::Abs(rSumParent-rSumTest);
#       if (diff > maxDiff) maxDiff = diff;
#     }

#   return maxDiff;
# }


# /**
#  * Kolmogorov-Smirnov goodness of fit test with 1000 pseudo experiments.
#  *
#  * @param parent
#  * @param test
#  *
#  * @return
#  */
# Double_t cdfKS(TH1 *parent, const TH1 *test)
# {
#   Double_t ksDist = cdfKSDist(parent,test);

#   //Run the pseudo-experiments
#   TH1 *peTest = (TH1*)test->Clone("peTest");
#   peTest->SetDirectory(0); //We'll delete this ourselves at the end

#   int nBigger = 0;
#   for (int i = 0; i<1000; ++i)
#     {
#       peTest->Reset();
#       peTest->FillRandom(parent,(int)test->Integral());
#       Double_t ksPEDist = cdfKSDist(parent,peTest);
#       if (ksPEDist > ksDist) nBigger++;
#     }

#   delete peTest;

#   return ((Double_t)nBigger)/1000;
# }


class KolmogorovSmirnovTest(ComparisonFunction):
    """Kolmogorov-Smirnov test.

    """

    @check_hists2
    def compare(self, data_hist, ref_hist, options=''):
        """
        data_hist -- data histogram
        ref_hist  -- reference histogram (ignored)
        options   -- options for TH1::KolmogorovTest()

        """

        options = options.lower()
        KS_prob_or_dist = ref_hist.KolmogorovTest(data_hist, options)

        if options.find('m') < 0: # KS probability
            score = Score((1-abs(KS_prob_or_dist-0.5)) * 100)
            if KS_prob_or_dist < 0.5: # FIXME: not sure about this condition
                lvl = ERROR_LEVELS.ERROR
            else:
                lvl = ERROR_LEVELS.OK
        else:
            raise NotImplementedError('KS distance option not implemented yet')

        return self.create_final_dict(score, lvl)


class Chi2Test(ComparisonFunction):
    """χ² comparison test between data and reference histograms.

    If no option is passed, a p-value is used to do the comparison.
    ROOT calculates this from the cumulative χ² distribution,
    precisely: 1 - ∫f(χ²,ndf)dχ² (ndf = number of degrees of freedom).
    So we accept all p-values ≥ 0.05 (a 2σ deviation).

    Approximately the above corresponds to χ²/ndf ≤ 2.  If we want to
    enforce this precisely, we have to pass options 'chi2' or
    'chi2/ndf' (the latter is preferred, since it accounts for empty
    bins).

    The threshold χ²/ndf or p-value is mapped to a DQ score of 50 and
    5 respectively; a perfect match (OK) is 100.  For a p-value based
    comparison, a DQ score between 5 and 1 is a WARNING, and a score
    below 1 (i.e. outside 3σ) is an ERROR.  Similarly for a χ² based
    comparison, a score between 50 and 25 is a WARNING, and a score
    below 25 is (χ²/ndf > 3, or 3σ deviation) is an ERROR.

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
            # p-value remapped such than 0.05 -> 5, 1 -> 100
            score = Score(pvalue_or_chi2 * 100)
            if pvalue_or_chi2 < 0.01: # outside 3 sigma
                lvl = ERROR_LEVELS.ERROR
            elif pvalue_or_chi2 < 0.05:
                lvl = ERROR_LEVELS.WARNING
            else:
                lvl = ERROR_LEVELS.OK
        else:                   # chi2
            if options.find('chi2/ndf') < 0: # chi2
                ndf = data_hist.GetNbinsX()
                pvalue_or_chi2 = pvalue_or_chi2/ndf
            # chi2/ndf = 2 --> Score(50),  0 --> Score(100)
            score = Score(100 - pvalue_or_chi2*25)
            if pvalue_or_chi2 > 3: # < Score(25)
                lvl = ERROR_LEVELS.ERROR
            elif pvalue_or_chi2 > 2: # < Score(50)
                lvl = ERROR_LEVELS.WARNING
            else:
                lvl = ERROR_LEVELS.OK
            
        return self.create_final_dict(score, lvl)
