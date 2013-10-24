"""This module will define project specific exceptions"""


class ScoreAssignmentException(Exception):
    def __str__(self):
        return "A score must be an integer value between 0 and 100"


class AddingScoreException(Exception):
    def __str__(self):
        return "Added scores sum to more than 100%"


class MultiplyingScoreException(Exception):
    def __str__(self):
        return "Scores can be multiplied only by weights"


class WeightedScoreException(Exception):
    def __str__(self):
        return "A score combined with its weight must be a value between 0 and 100"


class WeightAssignmentException(Exception):
    def __str__(self):
        return "A weight must be a float value between 0 and 1"


class CombinerWeightAssignmentException(Exception):
    def __str__(self):
        return "The combiner object needs a weight object as its weight"