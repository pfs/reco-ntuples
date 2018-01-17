#!/bin/bash

GRANULARITY=${1}
JOB=${2}
WORKDIR=`pwd`
MAXEVENTS=20

echo "Granularity for this job is ${GRANULARITY}"
echo "Job number is ${JOB}"
echo "Work dir: ${WORKDIR} at `hostname`"

eos mkdir /store/cmst3/user/psilva/HGCal/MinBias_${GRANULARITY}/RECO

cd /afs/cern.ch/user/p/psilva/work/HGCal/CMSSW_6_2_0_SLHC28_patch1/src
eval `scram r -sh`
cd ${WORKDIR}

for i in `seq 1 3`; do
    cmsRun ${CMSSW_BASE}/src/step${i}_cfg.py granularity=${GRANULARITY} maxEvents=${MAXEVENTS};
done

xrdcp step3.root root://eoscms//eos/cms/store/cmst3/user/psilva/HGCal/MinBias_${GRANULARITY}/RECO/Events_${JOB}.root
#rm step*.root