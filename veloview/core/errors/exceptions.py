"""This module will define project specific exceptions"""


class ScoreAssignmentException(Exception):
    def __str__(self):
        return "A score must be an integer value between 0 and 100"


class AddingScoreException(Exception):
    def __str__(self):
        return "Added scores sum to more than 100%"


class WeightedScoreException(Exception):
    def __str__(self):
        return "A score combined with its weight must be a value between 0 and 100"


class RootGraphicListArgumentException(Exception):
    def __str__(self):
        return "Error and warning parameters need to be lists"


class WeightContainerLackingWeightException(Exception):
    def __str__(self):
        return "Weight needs to be assigned to the container before calculating its score"