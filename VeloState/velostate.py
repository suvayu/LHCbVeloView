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

    Each leave has:
    1) a name, and
    2) a 2-tuple: (monitored quantity, function)

    Each node has:
    1) a name,
    2) a 2-tuple: (list of leaves, function)

    The function in both cases assigns/calculates the DQ score/flag
    for the leaf/node.

    """

    def add_leaf_or_node(self, name, qty, score_fn, isnode=False):
        """Add a leaf or node.

        Basic type check is done before filling.

        """

        if isnode and not hasattr(qty, '__iter__'):
            raise TypeError('Expecting an iterable as `qty`, found %s instead.'
                            % type(qty))
        if hasattr(score_fn, '__call__'):
            self.__setitem__(name, (qty, score_fn))
        else:
            raise TypeError('Expecting a callable as `score_fn`,'
                            ' found %s instead.' % type(score_fn))


    def get_leaves_or_nodes(self, regex):
        """Return leaves or nodes matching name regex."""

        pass


class VeloState(object):
    """This class interprets external inputs into a Velo state.

    """

    def __init__(self):
        self.__dqtree__ = DQTree()
        pass
