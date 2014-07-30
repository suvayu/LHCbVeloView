VELO view
=========

A framework for analysing data from the LHCb Vertex Locator.

Usage
-----

To install the `veloview` module, you can use the [git repository](https://git.cern.ch/web/LHCbVeloView.git).

```bash
$ git clone https://git.cern.ch/reps/LHCbVeloView
$ cd LHCbVeloView/veloview
$ python setup.py build
$ python setup.py install
```

Ideally we would recommend installation with [`pip`](https://pypi.python.org/pypi/pip), but there is a [bug installing modules in subdirectories](https://github.com/pypa/pip/issues/1600) which, whilst fixed in the development branch, has not been fixed in a release (as of pip 1.5.6).
When the fix is released, you should be able to install `veloview` with

```bash
$ pip install -e "git+https://git.cern.ch/reps/LHCbVeloView#egg=veloview&subdirectory=veloview"
```

To use the module once it's installed, just `import` it.

```python
import veloview
```

Dependencies
------------

The dependencies for the `veloview` module are given in the [`requirements.txt`](requirements.txt) file.
You can use `pip` to install them.

```bash
$ pip install -r requirements.txt
```

Testing
-------

The test suite for the `veloview` module is contained within the [`tests`](tests) directory of this package.

To run the test suite, you need to install the test dependencies in addition to the [runtime dependencies](#dependencies).
Currently these are single package, [`tox`](https://testrun.org/tox/latest/), for running the tests.

```bash
$ pip install tox
# Run the tests
$ tox
```

Running `tox` will build the package for distribution and run the test suite under Python 2.7.

### Running the tests under multiple Python versions

Tox allows for simple running of the test suites under multiple Python versions with the `envlist` configuration key.

```
envlist=py26,py27,flake8
```

It's not as simple as that for us though, as the ROOT version installed will be linked to a particular version of Python.
There are ways around this, namely making available [different ROOT versions for each test environment](https://github.com/alexpearce/travis-ci-root-builds), but setting this up on something other than [Travis CI](https://travis-ci.org/) is work that's yet to be undertaken.
