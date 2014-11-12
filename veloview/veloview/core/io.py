"""This module implements an interface to GiantRootFileIO"""

from ..utils.rootutils import ROOT
from ..GiantRootFileIO.GUITree import Tree

def flatten(pydict):
    from copy import deepcopy
    pydict = deepcopy(pydict)
    if not isinstance(pydict, dict):
        raise ValueError('Only dictionaries are supported: {}'.format(type(pydict)))
    children = {}
    for key in pydict:
        if isinstance(pydict[key], dict):
            children[key] = flatten(pydict[key])
    for key, value in children.iteritems():
        pydict.update([('.'.join([key,k]), v) for k,v in value.iteritems()])
        del pydict[key]
    return pydict

def unflatten(pydict):
    from copy import deepcopy
    pydict = deepcopy(pydict)
    if not isinstance(pydict, dict):
        raise ValueError('Only dictionaries are supported: {}'.format(type(pydict)))
    def nestkey(key, value):
        keys = key.split('.')
        res = {}
        for k in reversed(keys):
            res = {k: value}
            value = res
        return res
    def mergedicts(res, new):
        for k in new:
            if res.has_key(k):
                mergedicts(res[k], new[k])
            else:
                res.update({k: new[k]})
    rows = [nestkey(key, pydict[key]) for key in pydict]
    res = {}
    for row in rows:
        mergedicts(res, row)
    return res
    
class GRFIO(object):
    """interface for versioned objects implemented by GiantRootFileIO."""

    def __init__(self, fname, tname='DQTree', mode='read', scheme = None):
        """Instantiating GRFIO needs the filename, mode, and tree name.

        fname -- The ROOT file with versioned objects
        mode  -- Mode to open the file (read, update)
        tname -- Name of tree with versioned objects 

        """
        mode = mode.lower()
        if mode == 'recreate':
            raise ValueError('Only read or update modes are allowed')
        if mode != 'read' and not scheme:
            raise ValueError('Branch scheme is missing')

        self.lock = ROOT.DotLock(fname)
        self.rfile = ROOT.TFile.Open(fname, mode)
        try:
            self.tree = Tree(tname)
        except TypeError:
            if mode == 'read':
                raise ValueError('Cannot find valid tree: {}'.format(tname))
            self.tree = Tree(tname, branches = scheme)

    def write_dqtree(self, dqdict):
        dqflat = flatten(dqdict)
        # FIXME: verify dqflat matches branch scheme
        for key, value in dqflat.iteritems():
            # NOTE: when writing, timestamp is now by default
            setattr(self.tree, key, value)
        self.tree.Fill()
        self.tree.Write()

    def read_leaf(self, leaf, timestamp = None):
        # FIXME: check if leaf is versioned
        if timestamp:
            return getattr(self.tree, leaf)[timestamp]
        else:
            return getattr(self.tree, leaf)

    def read_dqtree(self, branches, timestamp = None):
        res = {}
        for br in branches:
            # FIXME: check if leaf is versioned
            if timestamp:
                res[br] = getattr(self.tree, br)[timestamp]
            else:
                res[br] = getattr(self.tree, br)
        return res
