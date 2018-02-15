#!/usr/bin/env bash

# Automatically generated on {{ timestamp }}

# Capture the executable name and job input file from the command line.
CONDOR_EXEC="$(basename $0)"

# Setup the CMS software environment.
echo "$(date) - $CONDOR_EXEC - INFO - Setting up {{ CMSSW_VERSION }}"
export SCRAM_ARCH="{{ SCRAM_ARCH }}"
source /cvmfs/cms.cern.ch/cmsset_default.sh

# Checkout the CMSSW release and set the runtime environment. These
# commands are often invoked by their aliases "cmsrel" and "cmsenv".
scram project CMSSW {{ CMSSW_VERSION }}
cd {{ CMSSW_VERSION }}/src
eval "$(scramv1 runtime -sh)"

# Change back to the worker node's scratch directory.
cd "$_CONDOR_SCRATCH_DIR"

# Preprocess the ntuple.
echo "$(date) - $CONDOR_EXEC - INFO - Analyzing ntuple"
python efficiency_analyzer.py "$1" "$2"

