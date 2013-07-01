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
        self.bad_callable = 'not a callable'
        self.good_callable = lambda x : 'callable'

    def test_bad_compare_fn(self):
        self.assertRaises(TypeError, self.dqtree.add_node, 'bad', 0,
                          self.bad_callable)

    def test_good_compare_fn(self):
        self.dqtree.add_node('good', 0, self.good_callable)
        self.assertEqual(self.dqtree, DQTree(good=(0, self.good_callable)))

    def test_score_fn_call(self):
        self.dqtree.add_node('GOO', 42, self.good_callable)
        self.assertEqual(self.dqtree.call_score_fn('GOO'), 'callable')


from VeloState.algorithms import (Threshold)

class TestVeloState(unittest.TestCase):
# class TestVeloState(TestDQTree):

    def setUp(self):
        self.dqtree = DQTree()
        # super(TestVeloState, self).setUp()
        self.state = VeloState()
        # x is the monitored quantity (i.e. dqtree[key][0])
        self.gt_fn = lambda x, y : x > y
        self.lt_fn = lambda x, y : x < y
        self.eq_fn = lambda x, y : x == y

    def test_DQ_flag_pass(self):
        self.dqtree.add_node('FOO', 4.2, self.gt_fn)
        self.state.add_node_state('FOO', Threshold(1.0, True))
        self.state.set_DQ_tree(self.dqtree)
        self.assertEqual(self.state.get_score('FOO'), 4.2 > 1.0)

    def test_DQ_flag_fail(self):
        self.dqtree.add_node('FOO', 4.2, self.gt_fn)
        self.state.add_node_state('FOO', Threshold(42, True))
        self.state.set_DQ_tree(self.dqtree)
        self.assertEqual(self.state.get_score('FOO'), 4.2 > 42)


if __name__ == '__main__':
    hdr_fmt = '='*5 + '{0:^{width}}' + '='*5
    print hdr_fmt.format('DQTree', width=40)
    unittest.main()
