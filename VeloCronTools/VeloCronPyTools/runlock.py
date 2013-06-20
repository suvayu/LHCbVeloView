# coding=utf-8
"""This module provides run locks for analysis and merge jobs.

Functionality:
1. Acquire lock for a run.
2. If lock already exists, raise an exception.
3. Release lock when done with the job.

Adapted from a file locking class by Evan Fosmark.

@author:  Suvayu Ali
@date:    2013-06-05

"""


import os, errno

class RunLockExists(Exception):
    """Exception when a run lock already exists.

    Reads and prints job information from existing lock file.

    """
    pass

    # def __init__(self, filename):
    #     tokens = filename.split('.')
    #     self.runno, self.stream = tokens[0], tokens[1]
    #     # self.node, self.job_pid = <read filename>


class UndefinedRunLock(Exception):
    """Exception when attempt to create bad RunLock."""
    pass


class RunLock(object):
    """RunLock object creates a lock file before a run is processed.

    The lock file name uniquely identifies the run number, data
    stream, and the job type owning the lock file.  The contents of
    the file may have information on the node and process id the job
    is running on.

    If it is not possible to `acquire' the lock, an exception is
    raised.  If there is an existing lock file, information on the job
    holding the lock file is shown.  If the lock file cannot be
    created because of other reasons, e.g. insufficient permissions,
    the original exception (OSError) is forwarded.

    Lock file template: $PWD/<run>.<stream>.lock

    Job info: <node_name>, <job_pid>

    NB: Specific streams (ZS and NZS) are supported to prevent errors
    due to typos.

    Usage:

        lock = RunLock(runno, stream)
        lock.acquire()
        # do stuff
        lock.release()

    or,

        with RunLock(runno, stream):
            # do stuff

    """

    def __init__(self, runno, stream, job=None):
        """Initialise a run lock for `runno' and `stream'.

        A simple run number and stream validity check is performed.
        Failing the test, an `UndefinedRunLock` exception is raised.
        `job' is ignored for now.

        """

        self.is_locked = False
        runno = int(runno)      # ensure integer
        if runno > 99999:       # 6-digit run numbers
            self.runno = runno
            self.stream = stream
            self.lockfile = os.path.join(os.getcwd(), "%d.%s.lock" % (runno, stream))
        else:
            raise UndefinedRunLock('Oops! Bad run number: %s' % runno)


    def acquire(self):
        """Acquire the lock, if possible.

        This is gets called automatically when used with the `with`
        statement.  If another instance has the RunLock, raise a
        `RunLockExists` exception.

        """
        try:
            self.__fd__ = os.open(self.lockfile, os.O_CREAT|os.O_EXCL, 0644)
            self.is_locked = True
        except OSError as err:
            if err.errno == errno.EEXIST:
                raise RunLockExists(err.filename)


    def release(self):
        """Release the lock by deleting the lockfile.

        This gets called automatically at the end of a `with`
        statement block.

        """
        if self.is_locked:
            os.close(self.__fd__)
            os.unlink(self.lockfile)
            self.is_locked = False


    def __enter__(self):
        """Activated when used in the with statement to acquire a lock."""
        if not self.is_locked:
            self.acquire()
            return self


    def __exit__(self, type, value, traceback):
        """Activated at the end of the with statement to releases the lock."""
        if self.is_locked:
            self.release()


    def __del__(self):
        """Make sure the lock is released when destroying."""
        self.release()
