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

from VeloCronPyTools.runlock import (RunLock, UndefinedRunLock, RunLockExists)
import unittest


class TestExceptions(unittest.TestCase):

    def setUp(self):
        self.stream = 'FOO'
        self.good_runno = 137259
        self.bad_runno = 2.0

    def test_bad_run_number(self):
        self.assertRaises(UndefinedRunLock, RunLock, self.bad_runno,
                          self.stream)

    def test_existing_lock_files(self):
        def __existing_lock_files__():
            """Internal method."""
            with RunLock(self.good_runno, self.stream):
                with RunLock(self.good_runno, self.stream):
                    pass
        self.assertRaises(RunLockExists, __existing_lock_files__)

    @unittest.skip('Test not finalised')
    def test_permission_problems(self):
        # FIXME: write to non-existent directory (how?)
        def __permission_problems__():
            """Try acquiring a lock in a read only directory and fail."""
            __tmpdir__ = os.path.join(os.getcwd(), 'tmp')
            os.mkdir(__tmpdir__, 0555)
            with os.chdir(__tmpdir__):
                with RunLock(self.good_runno, self.stream):
                    pass
        self.assertRaises(OSError, __permission_problems__)


if __name__ == '__main__':
    print '='*5, '{0:^{width}}'.format('RunLock', width=40), '='*5
    unittest.main()
