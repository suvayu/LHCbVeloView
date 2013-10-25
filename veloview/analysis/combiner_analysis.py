"""This module will provide functionality for analysing combiners (apply warning and error thresholds, map expected states."""


class CombinerAnalyser(object):
    """This class will analyse a given combiner according and apply expected states mapping"""

    def __init__(self, combiner, exp_states):
        self.combiner = combiner
        self.exp_states = exp_states

    def analyse_combiner(self):
        pass

    def apply_exp_states(self):
        pass