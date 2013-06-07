#!/usr/bin/env python

import sys, os

# fiddle with sys.path so that package is importable
if __file__.startswith('/'):
    # FIXME: clean up
    sys.path.insert(0, os.path.join('/', *__file__.split('/')[:-3]))
else:
    __path_to_script__ = __file__.split('/')[:-1] # test directory
    __path_to_script__ += ['..', '..']            # package directory parent
    sys.path.insert(0, os.path.join(os.getcwd(), *__path_to_script__))

from VeloCronPyTools.runlock import (RunLock, UnknownRunLock, RunLockExists)
import unittest


class TestExceptions(unittest.TestCase):

    def setUp(self):
        self.good_runno = 137259
        self.good_stream = 'NZS'
        self.bad_runno = 2.0
        self.bad_stream = 'FOO'

    def test_bad_run_number(self):
        self.assertRaises(UnknownRunLock, RunLock, self.bad_runno,
                          self.good_stream)

    def test_unsupported_stream(self):
        self.assertRaises(UnknownRunLock, RunLock, self.good_runno,
                          self.bad_stream)


    def test_existing_lock_files(self):
        def __existing_lock_files__():
            """Internal method."""
            with RunLock(self.good_runno, self.good_stream):
                with RunLock(self.good_runno, self.good_stream):
                    pass
        self.assertRaises(RunLockExists, __existing_lock_files__)


    def test_permission_problems(self):
        return
        # FIXME: write to non-existent directory (how?)
        def __permission_problems__():
            """Try acquiring a lock in a read only directory and fail."""
            __tmpdir__ = os.path.join(os.getcwd(), 'tmp')
            os.mkdir(__tmpdir__, 0555)
            with os.chdir(__tmpdir__):
                with RunLock(self.good_runno, self.good_stream):
                    pass
        self.assertRaises(OSError, __permission_problems__)


if __name__ == '__main__':
    unittest.main()
