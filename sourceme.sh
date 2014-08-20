#!/bin/sh

# set -o xtrace

# FIXME: Only bash stuff here; should add zsh and other popular shells
# (except C-shells, do not use them!)

[[ $0 == sourceme.bash ]] && {
    echo "This script should be sourced, not executed.";
    exit -1;
}

# find project directory
projdir=$(readlink -f ${BASH_SOURCE})
projdir=${projdir%/sourceme.sh}

# setup python path
PYTHONPATH=$projdir:$PYTHONPATH
export PYTHONPATH

# find ROOT
which root-config &> /dev/null || echo "No ROOT installation found."

# setup LD_LIBRARY_PATH
LD_LIBRARY_PATH=${projdir}/GiantRootFileIO:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH
# if the user forgot to setup ROOT before, they can still do it after

# set +o xtrace
