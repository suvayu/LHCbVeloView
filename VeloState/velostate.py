"""This module defines Velo state for DQ analysis.

It also introduces the concept of expected state for the Velo.
Finally it implements a class to set and propagate DQ flags through
automatic analysis based on the `Velo expected state'.

@author Suvayu Ali
@email  Suvayu dot Ali at cern dot ch
@date   2013-03-15 Fri

"""


class state(object):
    """This class defines Velo state.

    The Velo has components, each component has properties and an
    overall DQ state.  Each property has a value and a DQ state.  Each
    node is represented by a list of heterogeneous objects; one of the
    elements is a DQ flag, the other can be anything including a list
    of other (contained) nodes.

    velostate = [list(components), <overall dqflag>]

    component = [list(properties), <overall dqflag>]

    property = list or tuple (<property state>, <property DQ flag>)

    property can be tuple for expected state (want it to immutable)
    and a list when representing current state (want it to be mutable)

    """

    def __init__(self):
        self.__components__ = [[], True]
        self.__velo__ = [self.__components__, True]

    def add_component(self, component):
        self.__components__[0] += component
        # # What to do with DQ flag?
        # self.__components__[1]

    def get_component(self):
        pass
