"""This module is responsible for score manipulations"""

from veloview.core.errors.exceptions import AddingScoreException, ScoreAssignmentException, WeightAssignmentException, \
    WeightedScoreException, MultiplyingScoreException
from veloview.core.tools.utils import enum


class Score(object):
    """A class that will hold a score (integer value between 0 and 100). Scores will be later assigned to histograms."""

    def __init__(self, val):
        if isinstance(val, int):
            if self.check_if_in_range(val):
                self.value = val
                return

        raise ScoreAssignmentException

    def __add__(self, other):
        temp_val = self.value + other.value

        if self.check_if_in_range(temp_val):
            return Score(temp_val)
        else:
            raise AddingScoreException

    def __iadd__(self, other):
        temp_val = self.value + other.value

        if self.check_if_in_range(temp_val):
            self.value = temp_val
            return self
        else:
            raise AddingScoreException

    def __mul__(self, other):
        if isinstance(other, Weight):
            temp_val = int(self.value * other.value)
            if self.check_if_in_range(temp_val):
                return Score(temp_val)
            else:
                raise WeightedScoreException
        else:
            raise MultiplyingScoreException

    def __cmp__(self, other):
        return cmp(self.value, other.value)

    def __repr__(self):
        return "{}%".format(self.value)

    def __str__(self):
        return repr(self)

    @staticmethod
    def check_if_in_range(value):
        return 0 <= value <= 100


class Weight(object):
    """A class representing a weight (value between 0 and 1)"""

    def __init__(self, val):
        if isinstance(val, float):
            if 0.0 < val <= 1.0:
                self.value = val
                return

        raise WeightAssignmentException

    def __repr__(self):
        return "{}/1.0".format(self.value)

    def __str__(self):
        return repr(self)


# definition of the error levels for the project
error_levels = enum("OK", "Warning", "Error")