"""This is an example of a combiner description dictionary (expected state dictionary)"""

EXAMPLE_COMBINER_DESCRIPTION_DICTIONARY = {
    "MasterCombiner": { "weight" : 1.0, "minWW": 10, "minWE": 25, "minEW": 1, "minEE": 2,
    "PedestalCombiner": {"weight" : 1.0, "maxError" : 0.5, "maxWarning" : 0.8, "path" : "Quality_Check"},
    "OccupanciesCombiner" : {"weight" : 0.5, "maxError" : 0.5, "maxWarning" : 0.8, "path" : "OccAvrgSens"},
    "NoiseCombiner" : {"weight" : 0.7, "maxError" : 0.5, "maxWarning" : 0.8, "path" : "RMSNoise_vs_Strip"},
    "TracksCombiner" : {"weight" : 0.2, "maxError" : 0.5, "maxWarning" : 0.8, "path" : "track IP X"},
    }
}