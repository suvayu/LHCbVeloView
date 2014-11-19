from math import sqrt
import unittest

import ROOT

from veloview.runview import response_formatters


class TestRunViewPlots(unittest.TestCase):
    def setUp(self):
        # Create TObjects for testing
        th1 = ROOT.TH1F('test_th1f', 'Test TH1F;Foo;Bar', 2, 0, 1)
        th1.SetBinContent(0, 1)
        th1.SetBinContent(1, 4)
        th1.SetBinContent(2, 9)
        th1.SetBinContent(3, 2)
        self.th1 = th1

        th2 = ROOT.TH2F('test_th2f', 'Test TH2F;Foo;Bar', 2, 0, 1, 2, 0, 1)
        th2.SetBinContent(th2.GetBin(1, 1), 4)
        th2.SetBinContent(th2.GetBin(1, 2), 9)
        th2.SetBinContent(th2.GetBin(2, 1), 4)
        th2.SetBinContent(th2.GetBin(2, 2), 1)
        self.th2 = th2

        self.tprofile = ROOT.TProfile(
            'test_tprofile', 'Test TProfile', 2, 0, 1
        )

        self.taxis = ROOT.TAxis(10, -1, 1)

    def tearDown(self):
        del self.th1
        del self.th2
        del self.tprofile
        del self.taxis

    def test_json_formatter(self):
        """Should return a JSON representation of the TObject."""
        rep = response_formatters.json_formatter(self.th1)
        self.assertIsInstance(rep, str)

    def test_dictionary_formatter(self):
        """Should return Python dictionary representation of the TObject."""
        pydict = response_formatters.dictionary_formatter(self.th1)
        self.assertIsInstance(pydict, dict)

    def test_tobject_formatter_th1(self):
        """Should successfully return a TH1 representation."""
        rep = response_formatters.tobject_formatter(self.th1)
        exp = dict(
            success=True,
            data=dict(
                name='test_th1f',
                title='Test TH1F',
                object_class='TH1F',
                data=response_formatters.th1_formatter(self.th1)
            )
        )
        self.assertEqual(rep, exp)

    def test_tobject_formatter_th2(self):
        """Should successfully return a TH1 representation."""
        rep = response_formatters.tobject_formatter(self.th2)
        exp = dict(
            success=True,
            data=dict(
                name='test_th2f',
                title='Test TH2F',
                object_class='TH2F',
                data=response_formatters.th2_formatter(self.th2)
            )
        )
        self.assertEqual(rep, exp)

    def test_tobject_formatter_tprofile(self):
        """Should successfully return a TProfile representation."""
        rep = response_formatters.tobject_formatter(self.tprofile)
        exp = dict(
            success=True,
            data=dict(
                name='test_tprofile',
                title='Test TProfile',
                object_class='TProfile',
                data=response_formatters.th1_formatter(self.tprofile)
            )
        )
        self.assertEqual(rep, exp)

    def test_tobject_formatter_unknown_tobject(self):
        """Should raise TypeError for an unsupported TObject."""
        with self.assertRaises(TypeError):
            response_formatters.tobject_formatter(self.taxis)

    def test_th1_formatter(self):
        """Should correctly format a TH1 dictionary representation."""
        rep = response_formatters.th1_formatter(self.th1)
        exp = dict(
            entries=self.th1.GetEntries(),
            mean=self.th1.GetMean(),
            rms=self.th1.GetRMS(),
            underflow=1.0,
            overflow=2.0,
            binning=[(0.0, 0.5), (0.5, 1.0)],
            values=[4.0, 9.0],
            uncertainties=[(sqrt(4), sqrt(4)), (sqrt(9), sqrt(9))],
            axis_titles=('Foo', 'Bar')
        )
        self.assertEqual(rep, exp)

    def test_th2_formatter(self):
        """Should correctly format a TH2 dictionary representation."""
        rep = response_formatters.th2_formatter(self.th2)
        exp = dict(
            entries=self.th2.GetEntries(),
            mean=self.th2.GetMean(),
            rms=self.th2.GetRMS(),
            xbinning=[(0.0, 0.5), (0.5, 1.0)],
            ybinning=[(0.0, 0.5), (0.5, 1.0)],
            values=[[4.0, 9.0], [4.0, 1.0]],
            axis_titles=('Foo', 'Bar')
        )
        self.assertEqual(rep, exp)
