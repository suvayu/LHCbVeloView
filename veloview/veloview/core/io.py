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

    def __init__(self, fname, tree='DQTree', title='', mode='read', branches = None):
        """Instantiating GRFIO needs the filename, mode, and tree name.

        fname    -- The ROOT file with versioned objects
        tree     -- Name of tree with versioned objects
        mode     -- Mode to open the file (create/new, read, update)
        branches -- List of branches, or dictionary of name and types

        """
        mode = mode.lower()
        if mode == 'recreate':
            raise ValueError('recreating not allowed')
        if ((mode == 'create' or mode == 'new') and
            not isinstance(branches, dict)):
            raise ValueError('Branch name-type dictionary mandatory for creation')

        self.lock = ROOT.DotLock(fname)
        self.rfile = ROOT.TFile.Open(fname, mode)
        try:
            self.tree = Tree(tree, treetitle = title, branches = branches)
        except TypeError:
            raise ValueError('Cannot find valid tree: {}'.format(tree))

    def if_versioned(self, branchname):
        """Check if branch is versioned"""
        branch = getattr(self.tree, branchname)
        return (hasattr(branch, 'value'), branch)

    def fill(self, dqdict):
        """Flatten and fill dictionary

        FIXME: doesn't check if branches match type'

        """
        now = ROOT.TimeStamp()
        dqflat = flatten(dqdict)
        # FIXME: verify dqflat matches branch scheme
        for key, value in dqflat.iteritems():
            versioned, branch = self.if_versioned(key)
            if versioned: branch[now] = value
            else: setattr(self.tree, key, value)
        self.tree.Fill()

    def read(self, branches, version = None):
        """Read branches and return unflattened dictionaries."""
        res = {}
        for br in branches:
            versioned, branch = self.if_versioned(br)
            # FIXME: check if requested version is valid
            if version and versioned: value = branch[version]
            else: value = branch
            if versioned: res[br] = value.value()
            else: res[br] = value
        return unflatten(res)

    def write(self):
        """Write tree to disk"""
        self.tree.Write()

    def close(self):
        """Close ROOT file"""
        self.rfile.Close()
