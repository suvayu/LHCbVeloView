from socket import gethostname
__hostname__ = gethostname()

# fiddle with sys.path so that rundb.RunDB is importable
if __hostname__.find('plus') >= 0:
    import sys, os
    sys.path.insert(0, os.path.join('/group/online/rundb/RunDatabase/python'))
