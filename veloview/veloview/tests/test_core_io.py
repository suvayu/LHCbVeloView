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


import unittest
class TestGRFIOutils(unittest.TestCase):

    def test_flatten_unflatten(self):
        from veloview.core.io import flatten, unflatten
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
        self.assertEqual(flatten(d), f)
        self.assertEqual(unflatten(f), d)


class TestGRFIO(unittest.TestCase):
    
    def setUp(self):
        from veloview.core.io import GRFIO
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
        self.grf = GRFIO('/tmp/test.root', mode = 'new', branches = self.branches)

    def tearDown(self):
        if os.path.exists('/tmp/test.root'):
            os.remove('/tmp/test.root')

    def test_read_write(self):
        for entry in self.entries:
            self.grf.fill(entry)
        self.grf.write()
        branches = [key for key in self.entries[0]]
        nentry = 0
        for dummy in self.grf.tree:
            res = self.grf.read(branches)
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
