"""This module will define containers used for the project. They will store histograms and their corresponding scores."""
from veloview.analysis.score_manipulation import Score, Weight
from veloview.core.errors.exceptions import WeightedContainerWeightAssignmentException, RootGraphicListArgumentException, ScoreAssignmentException


class ContainerWithWeight(object):
    def __init__(self, weight):
        self.weight = None
        self.assign_weight(weight)

    def assign_weight(self, weight):
        if self.check_weight(weight):
            self.weight = weight
        else:
            raise WeightedContainerWeightAssignmentException

    @staticmethod
    def check_weight(weight):
        if isinstance(weight, Weight):
            return True
        else:
            return False


class Combiner(ContainerWithWeight):
    """Responsible for storing rootgraphic objects and other combainers"""

    def __init__(self, weight, *args):
        """Parameters:
            weight      :   Weight object
            *args       :   objects to add to the combiner container (RootGraphics, Combainers)"""
        super(Combiner, self).__init__(weight)
        self.score = None
        self.warnings = []
        self.errors = []
        self.elements = []
        self.append(*args)

    def append(self, *args):
        """Appends new elements and recalculates combainer's properties"""
        for arg in args:
            self.elements.append(arg)
            self.warnings.extend(arg.warnings)
            self.errors.extend(arg.errors)
        self.calc_score()

    def calc_score(self):
        """Calculates combiner's score after adding new elements"""
        self.score = Score(0)
        for elem in self.elements:
            self.score += elem.score * elem.weight

    def get_nr_of_warning(self):
        return len(self.warnings) + len(self.errors)

    def get_nr_of_errors(self):
        return len(self.errors)


class RootGraphic(ContainerWithWeight):
    """Class storing a root objects with its additional information (score, warnings, errors)"""

    def __init__(self, root_obj, score, weight, warnings, errors):
        """Parameters:
            root_obj    :   root object(histogram, graph)
            score       :   Score object
            weight      :   Weight object
            warnings    :   a list with string warnings
            errors      :   a list with string errors"""
        super(RootGraphic, self).__init__(weight)
        self.graph = root_obj
        self.score = score
        if self.check_if_arg_is_a_list(warnings) and self.check_if_arg_is_a_list(errors):
            self.warnings = warnings
            self.errors = errors
        else:
            raise RootGraphicListArgumentException

    @staticmethod
    def check_if_arg_is_a_list(arg):  # TODO It would be useful to create type validation template
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