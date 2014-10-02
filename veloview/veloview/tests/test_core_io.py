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
    ROOT.gSystem.Load('libCintex')
    ROOT.Cintex.Enable()
    ROOT.gSystem.Load('libVeloGUIUtils')

from veloview.GiantRootFileIO.GUITree import Tree
from veloview.core.io import GRFIO

__brscheme__ = {
    'runnr':	'UInt_t', # this never gets updated, so no VersionedObject here
    'checked':	'VersionedObject<UShort_t, TimeStamp, std::greater<TimeStamp> >',
    'comment':	'VersionedObject<std::string, TimeStamp, std::greater<TimeStamp> >',
    'score':    'VersionedObject<float, TimeStamp, std::greater<TimeStamp> >'
}

import unittest
class TestGRFIO(unittest.TestCase):
    
    def setUp(self):
        self.d = {'l': 9,
                  'm': {'g': 7, 'h':8,
                        'i': {'a':1, 'b':2},
                        'j': {'c':3, 'd':4},
                        'k': {'e':5, 'f':6}
                    }}

    def tearDown(self):
        if os.path.exists('/tmp/test.root'):
            os.remove('/tmp/test.root')

    def test_write_dqtree(self):
        io = GRFIO('/tmp/test.root', mode = 'update', scheme = __brscheme__)
        io.write_dqtree(self.d)

    @unittest.skip('Not implemented')
    def test_read_leaf(self):
        pass

    @unittest.skip('Not implemented')
    def test_read_dqtree(self):
        pass

if __name__ == '__main__':
    hdr_fmt = '='*5 + '{0:^{width}}' + '='*5
    print hdr_fmt.format('TestGRFIO', width=40)
    unittest.main()
