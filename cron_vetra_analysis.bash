#!/bin/bash

# for debugging
# set -o xtrace

# setup
declare script=$(readlink -e $BASH_SOURCE)
declare srcdir="${script%/*}"

# save job arguments
declare jobargs="$@"
shift $#


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
echo "Running on:" $HOSTNAME

exec python $srcdir/vetra_analysis.py -c $jobargs
