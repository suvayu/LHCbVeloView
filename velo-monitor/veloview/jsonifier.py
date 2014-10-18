def data_for_object(obj):
    """Return a dictionary representing the data inside the object."""
    obj_class = obj.ClassName()
    d = {}
    if obj_class.startswith('TH1'):
        d = data_for_th1(obj)
    elif obj_class.startswith('TH2'):
        d = data_for_th2(obj)
    elif obj_class.startswith('TProfile'):
        d = data_for_th1(obj)
    return d


def data_for_th1(th1):
    """Return a data dictionary for TH1 objects.

    For histograms, we provide
      binning: List of 2-tuples defining the (low, high) binning edges,
      values: List of bin contents, ith entry falling in the ith bin
      uncertainties: List of 2-tuples of (low, high) errors on the values
      axis_titles: 2-tuple of (x, y) axis titles
    Keyword arguments:
    th1 -- ROOT.TH1 object or a that of deriving class (like TProfile)
    """
    xaxis = th1.GetXaxis()
    yaxis = th1.GetYaxis()
    nbins = xaxis.GetNbins()
    binning = [
        (xaxis.GetBinLowEdge(i), xaxis.GetBinUpEdge(i))
        for i in range(nbins)
    ]
    values = [th1.GetBinContent(i) for i in range(nbins)]
    uncertainties = [
        (th1.GetBinErrorLow(i), th1.GetBinErrorUp(i))
        for i in range(nbins)
    ]
    axis_titles = (xaxis.GetTitle(), yaxis.GetTitle())

    # Histogram 'metadata'
    entries = th1.GetEntries()
    mean = th1.GetMean()
    rms = th1.GetRMS()
    # For bin number conventions see TH1::GetBinContent
    overflow = th1.GetBinContent(0)
    underflow = th1.GetBinContent(nbins + 1)

    d = dict(
        entries=entries,
        mean=mean,
        rms=rms,
        underflow=underflow,
        overflow=overflow,
        binning=binning,
        values=values,
        uncertainties=uncertainties,
        axis_titles=axis_titles
    )
    return d


def data_for_th2(th2):
    """Return a data dictionary for TH2 objects.

    For histograms, we provide
      xbinning: List of 2-tuples defining the (low, high) x bin edges,
      ybinning: List of 2-tuples defining the (low, high) y bin edges,
      values: List of list of bin contents, (ith, jth) entry falling in the
              (ith, jth) bin
      axis_titles: 2-tuple of (x, y) axis titles
    Keyword arguments:
    th2 -- ROOT.TH1 object or a that of deriving class (like TProfile2D)
    """
    xaxis = th2.GetXaxis()
    yaxis = th2.GetYaxis()
    axis_titles = (xaxis.GetTitle(), yaxis.GetTitle())
    nbinsx = th2.GetNbinsX()
    nbinsy = th2.GetNbinsY()
    xbins = [
        (xaxis.GetBinLowEdge(i), xaxis.GetBinUpEdge(i))
        for i in range(nbinsx)
    ]
    ybins = [
        (yaxis.GetBinLowEdge(i), yaxis.GetBinUpEdge(i))
        for i in range(nbinsy)
    ]
    values = [
        [th2.GetBinContent(th2.GetBin(x, y)) for y in range(1, nbinsy + 1)]
        for x in range(1, nbinsx + 1)
    ]

    # Histogram 'metadata'
    entries = th2.GetEntries()

    d = dict(
        entries=entries,
        xbinning=xbins,
        ybinning=ybins,
        values=values,
        axis_titles=axis_titles
    )
    return d
