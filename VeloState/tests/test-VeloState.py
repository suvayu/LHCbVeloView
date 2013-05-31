#!/usr/bin/env python
# coding=utf-8

"""Tests for Velo expected state module

"""

# FIXME: velostate needs to be importable (top level package
# accessible via sys.path).  Fiddle with sys.path to fix this.

# # boiler plate to allow relative imports from scripts
# if __name__ == "__main__" and __package__ is None:
#     __package__ = "velostate"

from ..velostate import state

## Tests
velostate = state()
velostate.add_component(list((1, True), (2, True), (3, False)), True)
velostate.add_component(list((4, True), (5, True), (6, False)), True)
velostate.add_component(list((7, True), (8, True), (9, False)), True)
