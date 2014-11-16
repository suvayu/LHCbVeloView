import mock
import unittest

from veloview.core import config
from veloview.runview import utils


RUNS = [123987, 123998]
SENSORS = range(0, 47) + range(64, 107)


class TestRunViewUtils(unittest.TestCase):
    def setUp(self):
        self.old_prlf = config.processed_run_list_file
        config.processed_run_list_file = "/tmp/runList.txt"
        with open(config.processed_run_list_file, "w") as f:
            for r in RUNS:
                f.write("{0}\n".format(r))

    def tearDown(self):
        config.processed_run_list_file = self.old_prlf

    def test_run_list(self):
        """Should return a list of high-low sorted run numbers as integers."""
        self.assertEqual(utils.run_list(), sorted(RUNS, reverse=True))

    def test_valid_run(self):
        """Should return True if run is present in the run number file."""
        for r in RUNS:
            self.assertTrue(utils.valid_run(r))

    def test_invalid_run(self):
        """Should return False if run isn't present in the run number file."""
        self.assertTrue(1233321 not in RUNS)
        self.assertFalse(utils.valid_run(123321))

    def test_sensor_list(self):
        """Should return a number between 0-46 and 64-106 inclusive."""
        self.assertEqual(SENSORS, utils.sensor_list())

    def test_valid_sensor(self):
        """Return True if sensor is a valid sensor number."""
        for s in SENSORS:
            self.assertTrue(utils.valid_sensor(s))

    # def test_reference_run(plot, run):
    #     """Return the reference run number for the plot and nominal run number."""
    #     # TODO need to implement the reference database
    #     # The method can then query that DB and return the run number
    #     return run

    # def test_run_file_path(run):
    #     """Return TFile object for the given run."""
    #     # TODO this doesn't append the filename, where will that come from?
    #     return paths.make_dir_tree(run, config.run_data_dir)
