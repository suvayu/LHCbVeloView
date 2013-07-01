# coding=utf-8
"""This module implements DQ algorithms.

These algorithms can be used for calculate DQ score/flags for nodes in
a DQ tree.  For a leaf, the calculation is a matter of simply
determining the state of the leaf.  For a node, however, the
calculation involves combining all the daughter score/flags into an
overall score.

@author Suvayu Ali
@email  Suvayu dot Ali at cern dot ch
@date   2013-07-01 Sun

"""


class DummyAlgorithm:
    """A dummy algorithm."""

    def __init__(self):
        pass

    def __call__(self, mon):
        return mon


class Threshold:
    """A threshold with the notion of floor or ceiling."""

    def __init__(self, value, floor=True):
        self.value = float(value)
        self.floor = floor

    def __call__(self, mon):
        if self.floor:
            return self.value < mon
        else:
            return mon < self.value
