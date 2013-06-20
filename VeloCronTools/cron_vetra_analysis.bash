#!/bin/bash

# for debugging
# set -o xtrace

# setup
declare script=$(readlink -e $BASH_SOURCE)
declare srcdir="${script%/*}"

# save job arguments
declare jobargs="$@"
shift $#


# initialise environment; LbLogin et al.
source /sw/lib/lhcb/LBSCRIPTS/LBSCRIPTS_v6r1p3/InstallArea/scripts/LbLogin.sh
echo ${LBSCRIPTS_HOME}

SETSHIFTERVERSION=`grep "export SHIFTERVETRAVERSION" /group/velo/sw/scripts/velo_login.sh`
eval $SETSHIFTERVERSION
echo "shifter vetra version" $SHIFTERVETRAVERSION
source /sw/lib/lhcb/VETRA/VETRA_${SHIFTERVETRAVERSION}/Velo/VetraScripts/scripts/setup_shifters.sh


# set resource limits
ulimit -Sm 2000000
ulimit -Sv 2000000
echo "Running on:" $HOSTNAME


# run job
exec python $srcdir/vetra_analysis.py -c $jobargs
