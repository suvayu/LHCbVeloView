#!/usr/local/bin/pyroot


def fillTree(filename, treename):
    from ROOT import TFile, TTree, TRandom3
    from ctypes import c_double, c_int
    rnd = TRandom3()
    f = TFile(filename, 'RECREATE')
    t = TTree(treename, treename)
    evnr = c_int(0)
    data1 = c_double(0.)
    data2 = c_double(0.)
    data3 = c_double(0.)
    t.Branch('evnr', evnr, 'evnr/i')
    t.Branch('data1', data1, 'data1/D')
    t.Branch('data2', data2, 'data2/D')
    t.Branch('data3', data3, 'data3/D')
    for i in xrange(0, 1024 * 1024):
	evnr.value = i
	data1.value = rnd.Uniform()
	data2.value = rnd.Uniform()
	data3.value = rnd.Uniform()
	t.Fill()
    t.Write()
    del t
    f.Close()
    del f

def modtree(filename, treename, evnrv, data1v, data2v, data3v):
    from ROOT import TFile, TTree, TRandom3
    from ctypes import c_double, c_int
    rnd = TRandom3()
    f = TFile(filename, 'READ')
    t = f.Get(treename)
    ff = TFile('%s.new' % filename, 'RECREATE')
    # copy all but the entry we want to change
    ct = t.CopyTree('evnr != %u' % evnrv, '', t.GetEntries(), 0)
    evnr = c_int(0)
    data1 = c_double(0.)
    data2 = c_double(0.)
    data3 = c_double(0.)
    t.SetBranchAddress('evnr', evnr)
    t.SetBranchAddress('data1', data1)
    t.SetBranchAddress('data2', data2)
    t.SetBranchAddress('data3', data3)
    for i in xrange(0, t.GetEntries()):
	t.GetEntry(evnrv)
	if evnr.value != evnrv: continue
	data1.value = data1v
	data2.value = data2v
	data3.value = data3v
	ct.Fill()
    ct.Write()
    del ct
    ff.Close()
    del ff
    del t
    f.Close()
    del f
    from os import rename
    rename('%s.new' % filename, filename)

#fillTree('test.root', 'testtree')
modtree('test.root', 'testtree', 42, 42., 17., 78.)
