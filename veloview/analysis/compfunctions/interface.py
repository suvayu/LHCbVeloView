"""Interface for the comparison functions"""
from veloview.analysis.score_manipulation import Score, ERROR_LEVELS


class ComparisonFunction(object):
    """This is an interface for all comparison functions. It mimics a normal function and returns data from the compare
     method written specifficaly for every comparison function."""

    def compare(self, data_hist, ref_hist):
        """This method needs to be implemented for every single function and will need to return (score, lvl)"""
        raise NotImplementedError("This is an abstract function that needs to be implemented for each comparison function")

    @staticmethod
    def check_if_hist_exists(hist):
        if hist:
            return True
        else:
            return False

    @staticmethod
    def check_if_two_hists_exist(hist1, hist2):
        if hist1 and hist2:
            return True
        else:
            return False

    @staticmethod
    def create_final_dict(score, lvl):
        return {"score" : score, "lvl": lvl}

    def create_error_dict(self):
        return self.create_final_dict(Score(0), ERROR_LEVELS.ERROR)