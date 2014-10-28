#!/usr/bin/env python

import sys
import os

# fiddle with sys.path so that package is importable
if __file__.startswith('/'):
    # FIXME: clean up
    sys.path.insert(0, os.path.join('/', *__file__.split('/')[:-3]))
else:
    __path_to_script__ = __file__.split('/')[:-1] # test directory
    __path_to_script__ += ['..']            # package directory parent
    sys.path.insert(0, os.path.join(os.getcwd(), *__path_to_script__))

from crontools.runlock import (RunLock, RunLockExists)
import unittest


class TestExceptions(unittest.TestCase):

    def setUp(self):
        self.wdir = os.getcwd()
        self.stream = 'FOO'
        self.good_runno = 137259

    def test_existing_lock_files(self):
        l1 = RunLock(self.wdir, self.good_runno, self.stream)
        self.assertIs(l1.acquire(), None)
        l2 = RunLock(self.wdir, self.good_runno, self.stream)
        self.assertRaises(RunLockExists, l2.acquire)

    def test_with_statements(self):
        def __existing_lock_files__():
            """Existing lockfiles should be skipped safely."""
            with RunLock(self.wdir, self.good_runno, self.stream):
                with RunLock(self.wdir, self.good_runno, self.stream):
                    pass
        self.assertIs(__existing_lock_files__(), None)

    @unittest.skip('Test not finalised')
    def test_permission_problems(self):
        # FIXME: write to non-existent directory (how?)
        def __permission_problems__():
            """Try acquiring a lock in a read only directory and fail."""
            __tmpdir__ = os.path.join(os.getcwd(), 'tmp')
            os.mkdir(__tmpdir__, 0555)
            with os.chdir(__tmpdir__):
                with RunLock(self.wdir, self.good_runno, self.stream):
                    pass
        self.assertRaises(OSError, __permission_problems__)


if __name__ == '__main__':
    hdr_fmt = '='*5 + '{0:^{width}}' + '='*5
    print hdr_fmt.format('RunLock', width=40)
    unittest.main()
