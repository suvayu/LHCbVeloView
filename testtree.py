#!/usr/local/bin/pyroot
import ROOT
ROOT.SetMemoryPolicy(ROOT.kMemoryStrict)
ROOT.gSystem.Load('libCintex')
ROOT.Cintex.Enable()
ROOT.gSystem.Load('libVeloGUIUtils')

from TypeHelper import getTypeFactory

def fillTree(filename, treename):
    from ROOT import TFile, TTree, TRandom3
    from ROOT import DotLock, TimeStamp, VersionedObject, std
    from GUITree import Tree
    sensors = []
    sensors += [ i for i in xrange(0, 42) ]
    sensors += [ i for i in xrange(64, 64 + 42) ]
    sensors += [ i for i in xrange(128, 132) ]
    rnd = TRandom3()
    dl = DotLock(filename)
    f = TFile(filename, 'RECREATE')
    t = Tree(treename, {
	# branch names and types
	'runnr':	'UInt_t',
	'comment':	'VersionedObject<std::string, TimeStamp, std::greater<TimeStamp> >',
	'meanpedestal':	'VersionedObject<double, TimeStamp, std::greater<TimeStamp> >',
	'occupancy':	'VersionedObject<std::map<int,std::vector<double> >, TimeStamp, std::greater<TimeStamp> >'
	})
    print 'File and tree open.'
    for i in xrange(0, 10):
	print 'Filling run %u' % i
	t.comment.clear()
	t.occupancy.clear()
	t.meanpedestal.clear()

	t.runnr = i
	now = TimeStamp()
	t.comment[now] = 'initial DQ for run %u' % i
	t.meanpedestal[now] = -5. + 10. * rnd.Rndm()
	for sensor in sensors:
	    # vector of per-strip occupancies
	    ov = std.vector('double')(2048)
	    for strip in xrange(0, 2048):
		# simulate dead, noisy and normal strips
		#
		# note: one has a small bug... ;)
		tmp = rnd.Uniform()
		if tmp < 0.0025: ov[strip] = 0.
		elif tmp < 0.0075: ov[strip] = -rnd.Uniform()
	        else: ov[strip] = -rnd.Gaus(0.01,0.0025)
	    # fill that vector into the current version
	    t.occupancy[now][sensor] = ov
	t.Fill()
    t.Write()
    del t
    f.Close()
    del f
    del dl

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

fillTree('test.root', 'testtree')
#modtree('test.root', 'testtree', 42, 42., 17., 78.)
