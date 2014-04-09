# no GUI
from ROOT import gROOT
gROOT.SetBatch(True)

# shutup ROOT
from ROOT import gErrorIgnoreLevel, kInfo, kWarning, kError
gErrorIgnoreLevel = kWarning

def draw_hist(h1, mystr):
    from uuid import uuid1
    from ROOT import gPad
    h1.Draw()
    gPad.Print('{}_{}.png'.format(mystr, uuid1()))

def draw_hists(h1, h2, mystr):
    from uuid import uuid1
    from ROOT import gPad
    h1.Draw()
    h2.Draw('same')
    gPad.Print('{}_{}.png'.format(mystr, uuid1()))

def print_hists(h1, h2):
    print '=' * 10
    h1.Print('all')
    print '-' * 10
    h2.Print('all')
    print '=' * 10

def print_ascii_hists(h1, h2):
    from rootpy.utils.extras import ascii_hist
    print '=' * 10
    h1.Print()
    ascii_hist(h1)
    print '-' * 10
    h2.Print()
    ascii_hist(h2)
    print '=' * 10
