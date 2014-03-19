"""Interface for the comparison functions"""
from veloview.analysis.score_manipulation import Score, ERROR_LEVELS
from functools import wraps


def check_hists1(comparefn):
    """Decorator for comparison functions, check data histogram"""
    @wraps(comparefn)
    def wrapper(*args, **kwargs):
        # args[0] is self, since comparefn is member of a class
        if args[1]:
            return comparefn(*args, **kwargs)
        else:
            return ComparisonFunction().create_error_dict()
    return wrapper


def check_hists2(comparefn):
    """Decorator for comparison functions, check both data and reference histogram"""
    @wraps(comparefn)
    def wrapper(*args, **kwargs):
        # args[0] is self, since comparefn is member of a class
        if args[1] and args[2]:
            return comparefn(*args, **kwargs)
        else:
            return ComparisonFunction().create_error_dict()
    return wrapper


def check_binning(comparefn):
    """Decorator for comparison functions, check data and reference histogram binning"""
    @wraps(comparefn)
    def wrapper(*args, **kwargs):
        if args[0].GetNbinsX() == args[1].GetNbinsX():
            return comparefn(*args, **kwargs)
        else:
            # raise ValueError('Histograms with unequal number of bins')
            return ComparisonFunction().create_error_dict()
    return wrapper


class ComparisonFunction(object):
    """This is an interface for all comparison functions. It mimics a normal function and returns data from the compare
     method written specifficaly for every comparison function."""

    def compare(self, data_hist, ref_hist, param):
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
