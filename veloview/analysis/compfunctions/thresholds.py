"""This module will hold complex comparison functions"""

from interface import ComparisonFunction, check_hists
from veloview.analysis.score_manipulation import ERROR_LEVELS, Score

from rootutils import *


class FloorThreshold(ComparisonFunction):
    """This comparison function checks if mean is above threshold.

    """

    @check_hists
    def compare(self, data_hist, ref_hist, floor):
        """Reference histogram is ignored."""
        # pdb.set_trace()
        if minimum(data_hist) > floor:
            return self.create_final_dict(Score(100), ERROR_LEVELS.OK)
        else:
            return self.create_final_dict(Score(0), ERROR_LEVELS.ERROR)


class CeilingThreshold(ComparisonFunction):
    """This comparison function checks if mean is below threshold.

    """

    @check_hists
    def compare(self, data_hist, ref_hist, ceiling):
        """Reference histogram is ignored."""
        if maximum(data_hist) < ceiling:
            return self.create_final_dict(Score(100), ERROR_LEVELS.OK)
        else:
            return self.create_final_dict(Score(0), ERROR_LEVELS.ERROR)


class MeanWidthDiffRef(ComparisonFunction):
    """Check the mean and width w.r.t. reference.

    """

    @check_hists
    def compare(self, data_hist, ref_hist, tolerance):
        """Check mean/width is compatible with reference.

        The all comparisons are done with respect to
        tolerance*ref_hist.GetRMS().  Weights associated to each
        comparison: mean - 70%, width - 30%.

        """

        dmean = abs(data_hist.GetMean() - ref_hist.GetMean())
        dwidth = abs(data_hist.GetRMS() - ref_hist.GetRMS())
        score = 70.0 * (dmean < abs(tolerance*ref_hist.GetRMS()))
        score += 30.0 * (dwidth < abs(tolerance*ref_hist.GetRMS()))
        if score > 70.0:        # both passes: 100
            level = ERROR_LEVELS.OK
        elif score >= 30.0:      # only one passes: 70 or 30
            level = ERROR_LEVELS.WARNING
        else:                   # both fails: 0
            level = ERROR_LEVELS.ERROR
        return self.create_final_dict(Score(score), level)


class AbsoluteBandRef(ComparisonFunction):
    """Check if absolute values inside band.

    """
    pass


class ZeroCentredBandRef(ComparisonFunction):
    """Check fraction outside 0-centred band.

    """

    @check_hists
    def compare(self, data_hist, ref_hist, abs_band):
        """If abs_band is True, reference histogram is ignored."""

        if not abs_band:            # 3*sigma tolerance band from reference
            abs_band = 3*ref_hist.GetRMS()
        abs_band = abs(abs_band)    # force +ve definite band
        frac_outside = frac_above_threshold(data_hist, abs_band) \
                       + frac_below_threshold(data_hist, -abs_band)
        if frac_outside > 0.01:
            return self.create_final_dict(Score(0), ERROR_LEVELS.ERROR)
        else:
            return self.create_final_dict(Score(100), ERROR_LEVELS.OK)
