"""This module contains simple comparison functions"""

from interface import ComparisonFunction
from veloview.analysis.score_manipulation import ERROR_LEVELS, Score


class ReturnAlwaysHighScore(ComparisonFunction):
    def compare(self, data_hist, ref_hist):
        if self.check_if_two_hists_exist(data_hist, ref_hist):
            from random import randint
            return self.create_final_dict(Score(randint(80, 100)), ERROR_LEVELS.OK)
        else:
            return self.create_error_dict()


class ReturnAlwaysLowScore(ComparisonFunction):
    def compare(self, data_hist, ref_hist):
        if self.check_if_two_hists_exist(data_hist, ref_hist):
            from random import randint
            return self.create_final_dict(Score(randint(0, 20)), ERROR_LEVELS.ERROR)
        else:
            return self.create_error_dict()