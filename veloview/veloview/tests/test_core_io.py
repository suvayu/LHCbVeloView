import os

if __name__ == '__main__':
    import sys

    # fiddle with sys.path so that package is importable
    if __file__.startswith('/'):
        sys.path.insert(0, os.path.join('/', *__file__.split('/')[:-3]))
    else:
        __path_to_script__ = __file__.split('/')[:-1]  # test directory
        __path_to_script__ += ['..', '..'] # package directory parent
        sys.path.insert(0, os.path.join(os.getcwd(), *__path_to_script__))

from veloview.utils.rootutils import ROOT

def setUpModule():
    ROOT.SetMemoryPolicy(ROOT.kMemoryStrict)
    status = ROOT.gSystem.Load('libCintex')
    if status >= 0: ROOT.Cintex.Enable()
    else: raise RuntimeError('Couldn\'t load libCintex')
    status = ROOT.gSystem.Load('libVeloGUIUtils')
    if status < 0: raise RuntimeError('Couldn\'t load libVeloGUIUtils')


from veloview.GiantRootFileIO.GUITree import Tree
from veloview.core.io import GRFIO

import unittest
class TestGRFIO(unittest.TestCase):
    
    def setUp(self):
        self.branches = {
            'runnr':   'UInt_t', # this never gets updated, so no VersionedObject here
            'checked': 'VersionedObject<UShort_t, TimeStamp, std::greater<TimeStamp> >',
            'comment': 'VersionedObject<std::string, TimeStamp, std::greater<TimeStamp> >',
            'score':   'VersionedObject<float, TimeStamp, std::greater<TimeStamp> >'
        }
        entry = {
            'runnr':   142467,
            'checked': 1,
            'comment': 'Okay',
            'score':   98.5
        }
        self.entries = []
        for i in xrange(5):
            entry['runnr'] += 1
            self.entries.append(entry)

    def tearDown(self):
        if os.path.exists('/tmp/test.root'):
            os.remove('/tmp/test.root')

    def test_flatten_unflatten(self):
        d = {'l': 9,
             'm': {'g': 7, 'h':8,
                   'i': {'a':1, 'b':2},
               }}
        f = {'l'    : 9,
             'm.g'  : 7,
             'm.h'  : 8,
             'm.i.a': 1,
             'm.i.b': 2
         }
        from veloview.core.io import flatten, unflatten
        self.assertEqual(flatten(d), f)
        self.assertEqual(unflatten(f), d)

    def test_read_write(self):
        grf = GRFIO('/tmp/test.root', mode = 'new', branches = self.branches)
        for entry in self.entries:
            grf.fill_dqtree(entry)
        grf.tree.Write()
        branches = [key for key in self.entries[0]]
        nentry = 0
        for dummy in grf.tree:
            res = grf.read_dqtree(branches)
            self.assertEqual(self.entries[nentry], res)
            nentry += 1

    @unittest.skip('Not implemented')
    def test_version_browsing(self):
        pass

    @unittest.skip('Not implemented')
    def test_update(self):
        pass


if __name__ == '__main__':
    hdr_fmt = '='*5 + '{0:^{width}}' + '='*5
    print hdr_fmt.format('TestGRFIO', width=40)
    unittest.main()
