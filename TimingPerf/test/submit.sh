#!/bin/bash

if [ $# -lt 1 ]; then
  echo "$0 SUFFIX"
  echo $#
  exit
fi

cmsDriver.py step2 --conditions auto:startup -s RAW2DIGI,L1Reco,RECO,ENDJOB --process RECO --mc --eventcontent AODSIM -n -1 --filein step1.root --fileout AODSIM.root --no_exec --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1,SKKU/MuonIdentification/perfCheck.customisePerf --geometry Extended2015 --magField 38T_PostLS1 --python_filename step2_cfg.py

SEL=$1

for i in ls ../data/*.txt; do
  CAT=`basename $i .txt`
  echo create-batch --transferFiles detailedInfo.log --maxFiles 1 --cfg step2_cfg.py --jobName $CAT/$SEL --fileList $i
done
