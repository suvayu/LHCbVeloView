# VELO monitor

A monitoring application for the LHCb Vertex Locator, deriving from the [WebMonitor](https://github.com/alexpearce/root-web-monitoring).

Currently the application uses the dummy `veloview` module, which contains very basic methods for fetching objects from ROOT files.
The vision is that the functionality provided by the dummy module will be migrated to the actual `veloview` module, part of the [LHCbVeloView repository](https://git.cern.ch/web/LHCbVeloView.git).

Setup
-----

Clone the repository, set up a [`virtualenv`](http://virtualenv.readthedocs.org/en/latest/) (with [`virtualenvwrapper`](http://virtualenvwrapper.readthedocs.org/en/latest/)), then run the application. (You can skip the creation of the `virtualenv` to install the requirements globally.)

```bash
$ git clone https://path/to/repo/velo-monitor.git
$ cd velo-monitor
$ mkvirtualenv velo-monitor
$ pip install -r requirements.txt
$ honcho start
```

The `honcho start` command will initialise the application, a [Redis](http://redis.io/) server, and one worker.
To start more than one worker you can use the `-c` option, like `honcho start -c worker=4`.

Requirements
------------

A [Redis](http://redis.io/) server is used to queuing jobs and storing their results.
[ROOT](http://root.cern.ch/) is used to perform the tasks, namely getting data out of histograms, and to generate the data in the first place.

Deployment
----------

The VELO monitor will be deployed on a machine running [Scientific Linux](https://www.scientificlinux.org/), but should by deployable on any Linux distribution. The [dependencies](#requirements) must be satisfied.

With a copy/clone of this repository on the machine, first install the [required Python packages](requirements.txt) and then generate the appropriate init files.

```bash
# Inside the velo-monitor repository
$ pip install -r requirements.txt
$ honcho export -a velo -u deploy -c web=1,worker=4,redis=1 -p 8000 -s /bin/bash upstart ./init
```

This example `honcho` command creates init files, in the `init/` directory, for [`upstart`](http://upstart.ubuntu.com/), a service/task manager installed on several distributions. Once these files are copied to the appropriate location for your distribution (`/etc/init` on Scientific Linux), you can start the `velo` process, which will start the workers, web server, and Redis database.

```bash
$ sudo cp init/* /etc/init
$ sudo start velo
```

### Virtualenv

To isolate `velo_monitor` dependencies from other Python applications, you can use a [`virtualenv`](http://virtualenv.readthedocs.org/en/latest/). It is most useful when combined with [`virtualenvwrapper`](http://virtualenvwrapper.readthedocs.org/en/latest/).

```bash
$ mkvirtualenv velo-monitor
```

You can then proceed to deploy as usual (`pip install -r ...`). To resume working in the virtual environment, use `workon velo-monitor`.

One caveat when using a `virtualenv` is that one must ‘activate’ the environment before using any binaries within, such as `gunicorn`. This means the init scripts must be modified. For the upstart scripts mentioned above, this means sourcing the activation script for the virtual environment, e.g.:

```bash
. /home/deploy/virtualenvs/velo-monitor/bin/activate
```
