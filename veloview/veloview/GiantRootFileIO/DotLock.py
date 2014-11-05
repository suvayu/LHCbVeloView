class DotLock:
    """ very primitive port of C++ DotLock class to Python """
    def __init__(self, filename, timeout = None):
        """ acquire a DotLock on filename """
        self._cleanups = []
        self._getlock('%s.lock' % filename, timeout)

    def __del__(self):
        """ release lock held """
        import os
        for f in self._cleanups:
            os.unlink(f)

    def _gethostname(self):
        """ return as much of this host's name as we can gather """
        import socket
        hname = socket.gethostname()
        gai = socket.getaddrinfo(hname, 'http',
                socket.AF_UNSPEC, socket.SOCK_STREAM, 0, socket.AI_CANONNAME)
        for t in gai:
            # skip entries which contain localhost, as they contain no useful
            # information
            if 'localhost' not in t[3]:
                return t[3]
        # result of gethostname as fallback
        return hname

    def _xor_in(self, buf, val):
        """ xor in value val into buffer """
        for i in xrange(0, 8):
            buf = buf[0:i] + chr(ord(buf[i]) ^ (val & 0xff)) + buf[(i+1):8]
            val = val >> 8
        return buf

    def _xfer(self, fname, read, sz, buf = None):
        """ read/write from/to given file, return result """
        import os
        # open file for reading/writing
        if read:
            fd = os.open(fname, os.O_RDONLY, 0600)
        else:
            fd = os.open(fname, os.O_CREAT | os.O_WRONLY | os.O_TRUNC,
                    0600)
        try:
            if read:
                buf = ""
                while (len(buf) < sz):
                    buf = buf + os.read(fd, sz - len(buf));
            else:
                xfer = 0
                while (xfer < sz):
                    xfer = xfer + os.write(fd, buf[xfer:sz])
            os.close(fd)
            return buf if read else xfer
        except:
            # don't leak file descriptors, and re-throw
            os.close(fd)
            raise

    def _gettimeofday(self):
        """ hackish way to get back what gettimeofday does in C """
        import datetime
        sinceepoch = (datetime.datetime.now() -
                datetime.datetime(1970, 1, 1, 0, 0, 0, 0))
        return (86400 * sinceepoch.days + sinceepoch.seconds,
                sinceepoch.microseconds)

    def _getlock(self, fname, timeout):
        """ go through the motions to acquire the lock """
        import os, time, exceptions
        to = timeout
        hostname = self._gethostname()
        while True:
            # get some randomness
            cookie = self._xfer('/dev/urandom', True, 8)
            # pointer to instance
            cookie = self._xor_in(cookie, id(self))
            # pid
            pid = os.getpid()
            cookie = self._xor_in(cookie, pid)
            # uid
            uid = os.getuid()
            cookie = self._xor_in(cookie, uid)
            # time (tv_sec and tv_usec)
            tv = self._gettimeofday()
            cookie = self._xor_in(cookie, tv[0])
            cookie = self._xor_in(cookie, tv[1])
            # construct unique filename from
            ftmpname = ("%s.uid%09d.pid%09d.%s.%02x%02x%02x%02x%02x%02x%02x%02x" %
                    ((fname, uid, pid, hostname) +
                        tuple((ord(cookie[i]) for i in xrange(0, 8)))) )
            # write to file
            self._cleanups.append(ftmpname)
            self._xfer(ftmpname, False, len(ftmpname), ftmpname)
            # sleep until we can no longer stat the lock file
            while True:
                try:
                    flags = os.stat(fname)
                except:
                    break
                if (None != timeout):
                    if (0 < to): to = to - 1
                    else:
                        raise exceptions.OSError(0 + os.errno.EBUSY,
                                'File \'%s\' is busy' % fname)
                time.sleep(1)
            # try to link ftmpname to fname
            try:
                os.link(ftmpname, fname)
                self._cleanups.append(fname)
                e = exceptions.OSError(0, 'Success')
            except Exception as e:
                if (type(e) == exceptions.OSError and
                        e.errno == os.errno.EEXIST):
                    break
                raise e
            if os.errno.EEXIST == e.errno:
                # clean up after ourselves
                os.unlink(ftmpname)
                self._cleanups.remove(ftmpname)
                continue
            ftmpname2 = self._xfer(fname, True, len(ftmpname))
            if ftmpname2 != ftmpname:
                # lost arbitration
                continue
            # successfully acquired lock
            break
        # clean up after ourselves
        os.unlink(ftmpname) 
        self._cleanups.remove(ftmpname)
