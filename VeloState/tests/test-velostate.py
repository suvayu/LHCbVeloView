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


import unittest
from VeloState.velostate import (DQTree, VeloState)
from VeloState.algorithms import (DummyAlgorithm, Threshold)


class TestDQTree(unittest.TestCase):

    def setUp(self):
        self.dqtree = DQTree()

    def test_add_node(self):
        self.dqtree.add_node('good', 42)
        self.assertEqual(self.dqtree, DQTree(good=42))


class TestVeloState(unittest.TestCase):

    def setUp(self):
        self.dqtree = DQTree(FOO=42)
        self.state = VeloState()
        self.state.set_DQ_tree(self.dqtree)
        self.threshold_floor = Threshold(39, True)
        self.threshold_ceiling = Threshold(39, False)

    def test_DQ_flag_pass(self):
        self.state.add_node_state('FOO', self.threshold_floor)
        self.assertTrue(self.state.get_score('FOO'))

    def test_DQ_flag_fail(self):
        self.state.add_node_state('FOO', self.threshold_ceiling)
        self.assertFalse(self.state.get_score('FOO'))

    def test_not_implemented(self):
        self.state.add_node_state('FOO', DummyAlgorithm())
        self.assertEqual(self.state.get_score('FOO'), NotImplemented)


if __name__ == '__main__':
    hdr_fmt = '='*5 + '{0:^{width}}' + '='*5
    print hdr_fmt.format('DQTree', width=40)
    unittest.main()
