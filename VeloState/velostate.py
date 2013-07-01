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
    2) a 2-tuple: (monitored quantity, function)

    Each node has:
    1) a name,
    2) a 2-tuple: (list of leaf/node names, function)

    The function in both case calculates and assigns the DQ score/flag
    for the leaf/node.  For a leaf, the calculation is a matter of
    simply determining the state of the leaf.  For a node, however,
    the calculation involves combining all the daughter score/flags
    into an overall score.

    The DQ tree can be initialised like any regular dictionary.
    However a few methods are provided can add further leaves/nodes
    "safely".  These safety checks are _absent_ when using the
    constructor to initialise.

    """

    def add_node(self, name, qty, score_fn, isnode=False):
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

    def call_score_fn(self, leaf, *sf_args, **sf_kw_args):
        """Call `score_fn' associated with `leaf' with given arguments.

        Leaf can also be a node.  The return value of `score_fn' is
        forwarded.

        """

        return self[leaf][1](self[leaf][0], *sf_args, **sf_kw_args)

    def get_leaves_or_nodes(self, regex):
        """Return leaves or nodes matching name regex."""

        pass


class VeloState(object):
    """This class interprets external inputs into a Velo state.

    """

    def __init__(self):
        self.__dqtree__ = DQTree()
