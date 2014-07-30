# coding=utf-8
"""This module provides functions for trending information"""

from logging import debug, getLogger
logger = getLogger(__name__)


# class Trending(object):
#     """Base class for trending functions"""

#     def __call__(self, hist):
#         """Reimplement in derived class"""
#         return NotImplemented


def Median(hist):
    """Get median"""
    return dict(median = NotImplemented)


def Mean(hist):
    """Get mean"""
    return dict(mean = hist.GetMean())


def Variance(hist):
    """Get variance (RMS)"""
    return dict(var = hist.GetRMS())


def MPV(hist):
    """Get most probable value"""
    return dict(mpv = NotImplemented)


def Landau(hist):
    """Get Landau fit parameters"""
    return dict(landau = NotImplemented)
