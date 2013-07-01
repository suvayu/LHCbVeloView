# coding=utf-8
"""This module defines a Velo state for Data Quality Monitoring.

It also introduces the notion of an expected state based on the Velo
state.  It implements a data quality tree (DQTree) and provides an
interface to assign and propagate data quality scores/flags based on
the expectation from the Velo state.

@author Suvayu Ali
@email  Suvayu dot Ali at cern dot ch
@date   2013-06-27 Thu

"""


class DQTree(dict):
    """This is a glorified dictionary.

    It serves as the underlying data structure used by VeloState.  The
    idea is to represent all monitored quantities as leaves.  The
    leaves are grouped by `points of failure` or `symptoms` into a
    node to form a data quality tree.

    The DQ tree nodes are represented in the dictionary by holding a
    list of names for each daughter.  The leaf/node names serve as
    keys for easy look-up.  NB: Performance wise, this is probably not
    optimal for very large trees.  For now, we work under the
    assumption DQ trees are always "reasonable".

    Each leaf has:
    1) a name, and
    2) a monitored quantity

    Each node has:
    1) a name,
    2) a list of leaf/node names

    The DQ tree can be initialised like any regular dictionary.
    However a few methods are provided can add further leaves/nodes
    "safely".  These safety checks are _absent_ when using the
    constructor to initialise.

    """

    def add_node(self, name, qty, isnode=False):
        """Add a leaf or node.

        Basic type check is done before filling.

        """

        if isnode and not hasattr(qty, '__iter__'):
            raise TypeError('Expecting an iterable as `qty`, found %s instead.'
                            % type(qty))
        self.__setitem__(name, qty)
        # self[name] = qty

    def get_leaves_or_nodes(self, regex):
        """Return leaves or nodes matching name regex."""

        pass


from algorithms import (Threshold)

class VeloState(object):
    """This class interprets external inputs into a Velo state.

    """

    def __init__(self):
        self.__state__ = {}     # expected state

    def add_node_state(self, name, algorithm):
        """Add expected state for a leaf or node."""
        ## FIXME: not yet decided how to store the expected state.
        # Idea: Simple classes for each DQ algorithm; e.g. a Threshold
        # object will tell VeloState if the monitored quantity should
        # be higher or lower than a value.  Flag as "green" (True)
        # when condition is met, "red" (False) otherwise.
        self.__state__[name] = algorithm

    def set_DQ_tree(self, dqtree):
        """Set DQTree to compare with."""
        if isinstance(dqtree, DQTree):
            self.__dqtree__ = dqtree
            self.__leaves_or_nodes__ = dqtree.keys() # for easy lookup
        else:
            raise TypeError('Expecting a DQTree instance, found %s instead.'
                            % type(dqtree))

    def get_score(self, name):
        """Calculate and return the DQ score/flag for a leaf or node."""

        # FIXME: dumb comparison, hand coded.  Define an interface for
        # the algorithm that allows generic calls to get the score
        if isinstance(self.__state__[name], Threshold):
            return self.__state__[name](self.__dqtree__[name])
        else:
            NotImplemented
