#!/bin/bash

# environment: LbLogin et al.
# initialise environment
source /sw/lib/lhcb/LBSCRIPTS/LBSCRIPTS_v6r1p3/InstallArea/scripts/LbLogin.sh
echo ${LBSCRIPTS_HOME}

SETSHIFTERVERSION=`grep "export SHIFTERVETRAVERSION" /group/velo/sw/scripts/velo_login.sh`
eval $SETSHIFTERVERSION
echo "shifter vetra version" $SHIFTERVETRAVERSION


# resource limits: ulimit stuff
source /sw/lib/lhcb/VETRA/VETRA_${SHIFTERVETRAVERSION}/Velo/VetraScripts/scripts/setup_shifters.sh
ulimit -Sm 2000000
ulimit -Sv 2000000
echo "host1" $HOSTNAME
export HOSTNAME;echo "import os;print os.environ['HOSTNAME']" | /sw/lib/lcg/external/Python/2.6.5/x86_64-slc5-gcc43-opt/bin/python
echo "host2" $HOSTNAME

exec python ./vetra_analysis.py "$@"
