"""This module will define containers used for the project. They will store histograms and their corresponding scores."""
from veloview.analysis.score_manipulation import Score
from veloview.core.errors.exceptions import RootGraphicListArgumentException, ScoreAssignmentException, WeightContainerLackingWeightException


class NamedContainerWithWeight(object):
    def __init__(self, name):
        self.name = name
        self.weight = None

    def assign_weight(self, weight):
        self.weight = weight


class Combiner(NamedContainerWithWeight):
    """Responsible for storing rootgraphic objects and other combainers"""

    def __init__(self, name, *args):
        """Parameters:
            weight      :   Weight object
            *args       :   objects to add to the combiner container (RootGraphics, Combainers)"""
        super(Combiner, self).__init__(name)
        self.score = None
        self.warnings = []
        self.errors = []
        self.elements = []
        self.append(*args)

    def append(self, *args):
        """Appends new elements"""
        for arg in args:
            self.elements.append(arg)
            self.warnings.extend(arg.warnings)
            self.errors.extend(arg.errors)

    def calc_score(self):
        """Calculates combiner's score"""
        if self.weight:
            self.score = Score(0)
            summed_weights = self.calc_summed_weights()
            for elem in self.elements:
                self.score += elem.score * elem.weight / summed_weights
        else:
            raise WeightContainerLackingWeightException

    def calc_summed_weights(self):
        summed_weights = 0
        for elem in self.elements:
            summed_weights += elem.weight
        return summed_weights

    def get_nr_of_warnings(self):
        return len(self.warnings) + len(self.errors)

    def get_nr_of_errors(self):
        return len(self.errors)


class RootGraphic(NamedContainerWithWeight):
    """Class storing a root objects with its additional information (score, warnings, errors)"""

    def __init__(self, name, root_obj, score, warnings, errors):
        """Parameters:
            root_obj    :   root object(histogram, graph)
            score       :   Score object
            weight      :   Weight object
            warnings    :   a list with string warnings
            errors      :   a list with string errors"""
        super(RootGraphic, self).__init__(name)
        self.graph = root_obj
        self.score = score
        if self.check_if_arg_is_a_list(warnings) and self.check_if_arg_is_a_list(errors):
            self.warnings = warnings
            self.errors = errors
        else:
            raise RootGraphicListArgumentException

    @staticmethod
    def check_if_arg_is_a_list(arg):  # TODO It would be useful to create a type validation template
        if isinstance(arg, list):
            return True
        else:
            return False

    def assign_score(self, score):
        if self.check_score(score):
            self.score = score
        else:
            raise ScoreAssignmentException

    @staticmethod
    def check_score(score):
        if isinstance(score, Score):
            return True
        else:
            return False