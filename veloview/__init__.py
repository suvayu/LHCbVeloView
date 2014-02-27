# Import stuff needed for monitoring

# Combiner and writer
from veloview.analysis.combiners import (Combiner, GRFWriter)

# comparison functions
from veloview.analysis.compfunctions.basic import (ReturnAlwaysHighScore,
                                                        ReturnAlwaysLowScore)

from veloview.analysis.compfunctions.thresholds import (FloorThreshold,
                                                        CeilingThreshold,
                                                        MeanWidthDiffRef,
                                                        AbsoluteBandRef,
                                                        ZeroCentredBandRef)
