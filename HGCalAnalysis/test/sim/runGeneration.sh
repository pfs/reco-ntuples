#!/bin/bash

GRANULARITY=${1}
JOB=${2}
WORKDIR=`pwd`
MAXEVENTS=1400

echo "Granularity for this job is ${GRANULARITY}"
echo "Job number is ${JOB}"
echo "Work dir: ${WORKDIR} at `hostname`"

eos mkdir /store/cmst3/user/psilva/HGCal/MinBias_${GRANULARITY}

cd /afs/cern.ch/user/p/psilva/work/HGCal/CMSSW_6_2_0_SLHC28_patch1/src
eval `scram r -sh`
cd ${WORKDIR}

cmsRun ${CMSSW_BASE}/src/MinBias_GEN_SIM.py granularity=${GRANULARITY} maxEvents=${MAXEVENTS}
xrdcp step1.root root://eoscms//eos/cms/store/cmst3/user/psilva/HGCal/MinBias_${GRANULARITY}/GEN-SIM/Events_${JOB}.root
rm step1.root