#!/usr/bin/env python
# coding=utf-8

"""Test DQ algorithms

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

from VeloState.algorithms import (Threshold)
import unittest


class TestThreshold(unittest.TestCase):

    def setUp(self):
        self.floor_threshold = Threshold(42, True)
        self.ceiling_threshold = Threshold(42, False)

    def test_value(self):
        self.assertEqual(self.floor_threshold.value, 42)

    def test_floor(self):
        self.assertTrue(self.floor_threshold.floor)

    def test_ceiling(self):
        self.assertFalse(self.ceiling_threshold.floor)


if __name__ == '__main__':
    hdr_fmt = '='*5 + '{0:^{width}}' + '='*5
    print hdr_fmt.format('Algorithms', width=40)
    unittest.main()
