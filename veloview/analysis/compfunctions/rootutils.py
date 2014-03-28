#coding=utf-8
"""ROOT utilities

This module is a collection of ROOT utilities to manipulate or extract
information from ROOT histograms and trees.

"""

## Comments
# author: Suvayu Ali
# email:  Suvayu dot Ali at cern dot ch
# date:   [2013-12-03 Tue]


## ROOT boiler plate
from ROOT import TNamed
TNamed.Clone._creates = True


## Functions
from uuid import uuid4
from ROOT import TF1

def get_simple_fns(fname, range_tp, num=1):
    """Return functions without parameters.

    fname    -- function name as understood by TFormula
    range_tp -- tuple specifying function range
    num      -- number of functions to generate

    """

    lst = []
    for i in range(num):
        uuidname = 'fn-{}'.format(uuid4())
        lst.append((uuidname, TF1(uuidname, fname, *range_tp)))
    if len(lst) == 1: lst = lst[0]
    return lst

def get_fns(fname, arg_tp, range_tp, num=1):
    """Return named TMath functions.

    fname    -- name of a TMath function
    arg_tp   -- tuple with function arguments
    range_tp -- tuple specifying function range
    num      -- number of functions to generate

    """

    arg_tp = ('x',) + arg_tp
    lst = []
    for i in range(num):
        uuidname = 'fn-{}'.format(uuid4())
        lst.append((uuidname, TF1(uuidname, '{}({})'.format(fname, ','.join(str(i) for i in arg_tp)), *range_tp)))
    if len(lst) == 1: lst = lst[0]
    return lst


## Histogram utils
from ROOT import TH1

def diff_hist(hist1, hist2, name='velomonidq_hdiff'):
    """Return the difference histogram."""
    hdiff = hist1.Clone(name)
    hdiff.Add(hist2, -1)
    return hdiff

def maximum(hist):
    """Return the maximum content ignoring explicit overrides."""
    return hist.GetBinContent(hist.GetMaximumBin())

def minimum(hist):
    """Return the minimum content ignoring explicit overrides."""
    return hist.GetBinContent(hist.GetMinimumBin())

def minmax(hist):
    """Return a tuple with minimum and maximum (ignores overrides)."""
    return (minimum(hist), maximum(hist))

def max_skip_empty(hist):
    """Return the maximum content skipping empty bins."""
    bincs = [ hist.GetBinContent(i) for i in range(hist.GetNbinsX()+1)
              if hist.GetBinContent(i) != 0 ]
    return max(bincs)

def min_skip_empty(hist):
    """Return the minimum content skipping empty bins."""
    bincs = [ hist.GetBinContent(i) for i in range(hist.GetNbinsX()+1)
              if hist.GetBinContent(i) != 0 ]
    return min(bincs)

def frac_above_threshold(hist, threshold):
    """Return fraction above threshold."""
    tbin = hist.FindBin(threshold)
    return hist.Integral(tbin, hist.GetNbinsX())/hist.Integral()

def frac_below_threshold(hist, threshold):
    """Return fraction below threshold."""
    tbin = hist.FindBin(threshold)
    return hist.Integral(1, tbin)/hist.Integral()


## Tree utils
