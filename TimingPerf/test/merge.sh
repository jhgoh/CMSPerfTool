#!/bin/bash

DIRS=(BsToMuMu JpsiMuMu TTbarLepton Wjet ZMM)
REF=740
CMPS=(Deta05)

DOTIMING=NO
DONTUPLE=YES
DOEDM=NO

if [ $DOTIMING == YES ]; then
  echo -e "\n\n@@@@@ Creating timing ntuple"
  for i in ${DIRS[*]}; do
    pushd $i
    for j in $REF ${CMPS[*]}; do
      [ -f timing_$j.root ] || ../timingToNtuple.py $j &
    done
    popd
  done

  echo -e "\n\n@@@@@ Waiting to finish timing ntuple"
  wait
fi

if [ $DONTUPLE == YES ]; then
  echo -e "\n\n@@@@@ Creating flat ntuple from AOD"
  for i in ${DIRS[*]}; do
    pushd $i
    for j in $REF ${CMPS[*]}; do
      #[ -f ntuple_$j.root ] && continue
      pushd $j
        $(cmsRun ../../ntuple_cfg.py; mv ntuple.root ../ntuple_$j.root) &
      popd
    done
    popd
  done

  echo -e "\n\n@@@@@ Waiting to finish flat ntuple"
  wait
fi

if [ $DOEDM == YES ]; then
  echo -e "\n\n@@@@@ Creating One to one comparison"
  for i in ${DIRS[*]}; do
    pushd $i
    for j in ${CMPS[*]}; do
      cat > runScript.sh <<EOF
  #!/bin/bash
  for k in \`ls $j/AODSIM_*.root\`; do
    FILE=\`basename \$k\`
    runEdmFileComparison.py --prefix=recoTest $REF/\$FILE $j/\$FILE --regex=recoMuon
    edmOneToOneComparison.py recoMuon.txt $REF/\$FILE $j/\$FILE --compare --label=reco^recoMuon^muons,,RECO --compRoot=cmp_\$FILE
  done
  hadd -f cmp_$j.root cmp_AODSIM_*.root && rm -f cmp_AODSIM_*.root
EOF
      bash runScript.sh &
    done
    popd
  done
  echo -e "\n\n@@@@@ Waiting one to one comparisons to be finished"
  wait
fi
