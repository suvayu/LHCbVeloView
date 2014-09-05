# TODO

There are a few tasks that Alex couldn't finish before his holiday.

1. Finish writing the run view tests and fix failing tests; and
2. Migrate dummy `veloview` module functionality to the actual `veloview` module in the LHCbVeloView repository.

Number 1 is straightforward.

Number 2 is less so. It requires a little more thought in the deployment strategy. The worker instances need to ‘know’ about the `veloview` module so they can execute the methods within as specified by a job. This isn't a problem when running them in the `velo-monitor` directory as the dummy module is picked up, but switching to the actual `veloview` module will require either installing the module globally on the production server or modifying the `PYTHONPATH` environment variable.

Alternatively what could be done is create a ‘mapping’ module in the `velo-monitor` folder. The jobs execute methods within the mapping module, and this can source the actual `veloview` module in some way, calling the appropriate method for the job.
