#!/usr/bin/env python

import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

AUTHORS = [
    'Suvayu Ali',
    'Marco Gersabeck',
    'Alex Pearce',
    'Manuel Schiller',
    'Michal Wysokinski'
]

setup(name='veloview',
    version='0.0.1',
    description='A framework for analysing data from the LHCb Vertex Locator.',
    # Sort the author list by last name
    author=', '.join(sorted(AUTHORS, key=lambda x: x.split()[1])),
    author_email='marco.gersabeck@cern.ch',
    url='https://git.cern.ch/web/LHCbVeloView.git',
    long_description=read('README.md'),
    packages=[
        'veloview',
        'veloview.analysis',
        'veloview.core',
        'veloview.utils',
    ],
    scripts=[
        'bin/retrieve_run_view_plot.py',
        'bin/veloview_configuration.py'
    ]
)
