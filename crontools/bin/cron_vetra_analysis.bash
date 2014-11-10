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
source /cvmfs/lhcb.cern.ch/group_login.sh
echo ${LBSCRIPTS_HOME}
declare vetra=$(sed -ne 's/.\+export \+SHIFTERVETRAVERSION=\(.\+\)/\1/p' /group/velo/sw/scripts/velo_login.sh)
echo "Vetra version:" $vetra
SetupProject Vetra $vetra


# set resource limits
ulimit -Sm 2000000
ulimit -Sv 2000000
echo "Running on:" $HOSTNAME


# run job
exec python $srcdir/vetra_analysis.py -c $jobargs
