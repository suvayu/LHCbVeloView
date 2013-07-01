#!/usr/bin/env python
# coding=utf-8

"""Tests for Velo expected state module

"""

import sys, os

# fiddle with sys.path so that package is importable
if __file__.startswith('/'):
    # FIXME: clean up
    sys.path.insert(0, os.path.join('/', *__file__.split('/')[:-3]))
else:
    __path_to_script__ = __file__.split('/')[:-1] # test directory
    __path_to_script__ += ['..', '..']            # package directory parent
    sys.path.insert(0, os.path.join(os.getcwd(), *__path_to_script__))

from VeloState.velostate import (DQTree, VeloState)
import unittest


class TestDQTree(unittest.TestCase):

    def setUp(self):
        self.dqtree = DQTree()

    def test_add_node(self):
        self.dqtree.add_node('good', 42)
        self.assertEqual(self.dqtree, DQTree(good=42))


from VeloState.algorithms import (Threshold)

class TestVeloState(unittest.TestCase):
# class TestVeloState(TestDQTree):

    def setUp(self):
        self.dqtree = DQTree()
        # super(TestVeloState, self).setUp()
        self.state = VeloState()
        # x is the monitored quantity (i.e. dqtree[key][0])
        self.threshold_floor = Threshold(42, True)
        self.threshold_ceiling = Threshold(42, False)

    def test_DQ_flag_pass(self):
        self.dqtree.add_node('FOO', 42.1)
        self.state.add_node_state('FOO', self.threshold_floor)
        self.state.set_DQ_tree(self.dqtree)
        self.assertEqual(self.state.get_score('FOO'), 42.1 > 42.0)

    def test_DQ_flag_fail(self):
        self.dqtree.add_node('FOO', 4.2)
        self.state.add_node_state('FOO', self.threshold_floor)
        self.state.set_DQ_tree(self.dqtree)
        self.assertEqual(self.state.get_score('FOO'), 4.2 > 42)


if __name__ == '__main__':
    hdr_fmt = '='*5 + '{0:^{width}}' + '='*5
    print hdr_fmt.format('DQTree', width=40)
    unittest.main()
