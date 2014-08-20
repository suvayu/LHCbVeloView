"""Interface for the comparison functions"""
from .score_manipulation import Score, ERROR_LEVELS
from functools import wraps
from logging import getLogger, warning
logger = getLogger(__name__)


def check_hists1(comparefn):
    """Decorator for comparison functions.

    Check data histogram

    """
    @wraps(comparefn)
    def wrapper(*args, **kwargs):
        # args[0] is self, since comparefn is member of a class
        if args[1]:
            return comparefn(*args, **kwargs)
        else:
            warning('Bad data histogram: {}'.format(args[1]))
            return ComparisonFunction().create_error_dict()
    return wrapper


def check_hists2(comparefn):
    """Decorator for comparison functions.

    Check both data and reference histogram

    """
    @wraps(comparefn)
    def wrapper(*args, **kwargs):
        # args[0] is self, since comparefn is member of a class
        if args[1] and args[2]:
            return comparefn(*args, **kwargs)
        else:
            warning('Bad histogram, data: {}, ref: {}'.format(args[1], args[2]))
            return ComparisonFunction().create_error_dict()
    return wrapper


def check_binning(comparefn):
    """Decorator for comparison functions.

    Check data and reference histogram binning

    """
    @wraps(comparefn)
    def wrapper(*args, **kwargs):
        # args[0] is self, since comparefn is member of a class
        if args[2].GetNbinsX() == args[1].GetNbinsX():
            return comparefn(*args, **kwargs)
            # FIXME: this check is incomplete, bin boundaries can also
            # be different: see TH1::CheckConsistency() (cannot use
            # this though, protected member)
        else:
            warning('Histograms with different number of bins.')
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
