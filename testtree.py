#!/usr/local/bin/pyroot
import ROOT
ROOT.SetMemoryPolicy(ROOT.kMemoryStrict)
ROOT.gSystem.Load('libCintex')
ROOT.Cintex.Enable()
ROOT.gSystem.Load('libVeloGUIUtils')

# construct list of valid Velo sensor numbers
sensors = tuple(xrange(0, 42))
sensors += tuple(xrange(64, 64 + 42))
sensors += tuple(xrange(128, 132))

def createTree(filename, treename):
    from ROOT import TFile, TRandom3
    from ROOT import DotLock, TimeStamp, VersionedObject, std
    from GUITree import Tree
    # get RNG to generate some data to put into the tuple
    rnd = TRandom3()
    # acquire write lock
    dl = DotLock(filename)
    # open file for writing
    f = TFile(filename, 'RECREATE')
    f.SetCompressionSettings(ROOT.CompressionSettings(ROOT.kLZMA, 1))
    # create tree with given structure
    t = Tree(treename, 'Velo DQ Tree prototype', {
	# define branch names and types
	'runnr':	'UInt_t',
	'checked':	'VersionedObject<UShort_t, TimeStamp, std::greater<TimeStamp> >',
	'comment':	'VersionedObject<std::string, TimeStamp, std::greater<TimeStamp> >',
	'meanpedestal':	'VersionedObject<Float_t, TimeStamp, std::greater<TimeStamp> >',
	'occupancy':	'VersionedObject<std::map<int,std::vector<Float_t> >, TimeStamp, std::greater<TimeStamp> >'
	})
    # fill tree
    for i in xrange(0, 64):
	# clear out data from last run
	t.comment.clear()
	t.occupancy.clear()
	t.meanpedestal.clear()

	# fill new run: step 1: generate time stamp (now)
	now = TimeStamp()
	# fill branches
	t.runnr = 100000 + i
	print 'Generating dummy DQ data for run %u' % t.runnr
	t.checked[now] = 0
	t.comment[now] = 'initial DQ for run %u: UNCHECKED' % t.runnr
	t.meanpedestal[now] = rnd.Uniform(-5., 5.)
	# simulate about 3 permille dead, 5 permille noisy channels
	fdead = rnd.Uniform(0.003, 0.002)
	if fdead < 0.: fdead = 0.
	fnoisy = rnd.Uniform(0.005,0.002)
	if fnoisy < 0.: fnoisy = 0.
	for sensor in sensors:
	    # vector of per-strip occupancies
	    ov = std.vector('float')(2048)
	    for strip in xrange(0, 2048):
		# simulate dead, noisy and normal strips
		tmp = rnd.Uniform(0., 1.)
		if tmp > (fdead + fnoisy): ov[strip] = rnd.Gaus(0.01, 0.0025)
		elif tmp > fnoisy: ov[strip] = rnd.Uniform(0., 1.)
	        else: ov[strip] = 0.
	    # put that strip vector for the current sensor into the current
	    # version
	    t.occupancy[now][sensor] = ov
	t.Fill()
    t.Write()
    del t
    f.Close()
    del f
    del dl

def anatree(filename, treename):
    from ROOT import TFile, TRandom3
    from ROOT import DotLock, TimeStamp, VersionedObject, std
    from GUITree import Tree
    print "Doing dummy DQ on file %s, tree %s" % (filename, treename)
    # acquire write lock
    dl = DotLock(filename)
    # open file for writing
    f = TFile(filename, 'READ')
    t = Tree('testtree')
    ff = TFile('%s.new' % filename, 'RECREATE')
    ff.SetCompressionSettings(ROOT.CompressionSettings(ROOT.kLZMA, 1))
    tt = t.CloneTree(0)
    for i in xrange(0, t.GetEntries()):
	t.GetEntry(i)
	print 'Analysing run %u: %s (%s)' % (
		t.runnr, t.comment.value(), t.comment.active_version().toString())
	# work out average occupancy in run
	avgocc = 0.
	nstrips = 0
	for sensor in sensors:
	    ov = t.occupancy.value()[sensor]
	    avgocc += sum(ov)
	    nstrips += ov.size()
	avgocc = avgocc / float(nstrips)
	print '\taverage occupancy %4.2f%%' % (100. * avgocc)
	# find dead/noisy strips
	dead = ()
	noisy = ()
	thresh_noise = 3. * avgocc
	thresh_dead = 0.1 * avgocc
	for sensor in sensors:
	    ov = t.occupancy.value()[sensor]
	    strip = 0
	    for occ in ov:
		if thresh_noise < occ:
		    noisy += ((sensor, strip), )
		elif thresh_dead > occ:
		    dead += ((sensor, strip),)
		strip = strip + 1
	pdead = 100. * float(len(dead)) / float(nstrips)
	pnoisy = 100. * float(len(noisy)) / float(nstrips)
	print '\t dead channels (%4.2f%%)' % pdead
	print '\tnoisy channels (%4.2f%%)' % pnoisy
	# set the run OK threshold at 0.75% dead + noisy channels max.
	now = TimeStamp()
	if pdead + pnoisy < 0.75:
	    tt.comment[now] = 'DQ for run %u: OK' % tt.runnr
	    tt.checked[now] = 2
	else:
	    tt.comment[now] = 'DQ for run %u: BAD' % tt.runnr
	    tt.checked[now] = 1
	print 'Analysed run %u: %s (%s)' % (
		tt.runnr, tt.comment.value(), tt.comment.active_version().toString())
	# write to new tree
	tt.Fill()
    tt.Write()
    del tt
    ff.Close()
    del ff
    del t
    f.Close()
    del f
    from os import rename
    rename('%s.new' % filename, filename)
    del dl

print 'Creating DQ tree'
createTree('test.root', 'testtree')
print ''
print 'Analysing DQ tree'
anatree('test.root', 'testtree')
