"""Format run view plots in a format the GUIs can consume."""
import json


def json_formatter(plot):
    """Return a JSON representation of the plot data."""
    return json.dumps(tobject_formatter(plot))


def dictionary_formatter(plot):
    """Return a the data as a Python dictionary."""
    return tobject_formatter(plot)


def tobject_formatter(tobject):
    """Return Python Dictionary representation of the TObject.

    Defined keys:
    name -- TObject.GetName
    title -- TObject.GetTitle
    object_class -- TObject.GetClass
    data -- Data returned by the formatter appropriate for the class
    A TypeError is raised if a formatter cannot be found for the object.
    """
    obj_class = tobject.ClassName()
    if obj_class.startswith("TH1") or obj_class == "TProfile":
        data = th1_formatter(tobject)
    elif obj_class.startswith("TH2"):
        data = th2_formatter(tobject)
    else:
        raise TypeError("Could not format object {0}".format(tobject))
    return dict(
        success=True,
        data=dict(
            name=tobject.GetName(),
            title=tobject.GetTitle(),
            object_class=tobject.ClassName(),
            data=data
        )
    )


def th1_formatter(th1):
    """Return a data dictionary for TH1 objects.

    Defined keys:
    entries -- TH1.GetEntries
    mean -- TH1.GetMean
    underflow -- Number of entries in the underflow bin
    overflow -- Number of entries in the overflow bin
    binning -- List of 2-tuples of bins as (low edge, high edge)
    values -- List of bin contents
    uncertainties -- List of uncertainties on bin contents
    axis_titles -- 2-tuple of (x-axis title, y-axis title)
    Keyword arguments:
    th1 -- ROOT.TH1 object or a that of deriving class (like TProfile)
    """
    xaxis = th1.GetXaxis()
    yaxis = th1.GetYaxis()
    nbins = xaxis.GetNbins()
    binning = [
        (xaxis.GetBinLowEdge(i), xaxis.GetBinUpEdge(i))
        for i in range(1, nbins + 1)
    ]
    values = [th1.GetBinContent(i) for i in range(1, nbins + 1)]
    uncertainties = [
        (th1.GetBinErrorLow(i), th1.GetBinErrorUp(i))
        for i in range(1, nbins + 1)
    ]
    axis_titles = (xaxis.GetTitle(), yaxis.GetTitle())

    # Histogram 'metadata'
    entries = th1.GetEntries()
    mean = th1.GetMean()
    rms = th1.GetRMS()
    # For bin number conventions see TH1::GetBinContent
    underflow = th1.GetBinContent(0)
    overflow = th1.GetBinContent(nbins + 1)

    return dict(
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


def th2_formatter(th2):
    """Return a data dictionary for TH2 objects.

    Defined keys:
    entries -- TH1.GetEntries
    xbinning -- List of 2-tuples of bins as (low x edge, high x edge)
    ybinning -- List of 2-tuples of bins as (low y edge, high y edge)
    values -- List of list of bin contents, (ith, jth) entry falling in the
              (ith, jth) bin
    axis_titles -- 2-tuple of (x-axis title, y-axis title)
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
        for i in range(1, nbinsx + 1)
    ]
    ybins = [
        (yaxis.GetBinLowEdge(i), yaxis.GetBinUpEdge(i))
        for i in range(1, nbinsy + 1)
    ]
    values = [
        [th2.GetBinContent(th2.GetBin(x, y)) for y in range(1, nbinsy + 1)]
        for x in range(1, nbinsx + 1)
    ]

    # Histogram 'metadata'
    entries = th2.GetEntries()
    mean = th2.GetMean()
    rms = th2.GetRMS()

    return dict(
        entries=entries,
        mean=mean,
        rms=rms,
        xbinning=xbins,
        ybinning=ybins,
        values=values,
        axis_titles=axis_titles
    )
