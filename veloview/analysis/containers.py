"""This module will define containers used for the project. They will store histograms and their corresponding scores."""
from veloview.analysis.score_manipulation import Score, Weight
from veloview.core.errors.exceptions import CombinerWeightAssignmentException


class Combiner(object):
    """Responsible for storing histograms and their scores"""
    def __init__(self, weight, *args):
        if isinstance(weight, Weight):
            self.weight = weight
        else:
            raise CombinerWeightAssignmentException
        self.score = None
        self.elements = []
        self.append(*args)

    def append(self, *args):
        for arg in args:
            self.elements.append(arg)
        self.calc_score()

    def calc_score(self):
        self.score = Score(0)
        for elem in self.elements:
            self.score += elem.score * elem.weight


class RootGraphic(object):
    def __init__(self, root_obj, score, weight):
        self.graph = root_obj
        self.score = score
        self.weight = weight