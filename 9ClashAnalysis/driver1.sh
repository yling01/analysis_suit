#!/bin/bash
echo "Make sure to change atoms in chimScript.py"
echo "Sequence Length: "
replace="5"
read seqLength
for (( i = 0; i < $seqLength+1; i++ )); do
   if [[ $i > 5 ]]; then
       replace+=",$i"
   fi
done
sed -i "s.TOREPLACE.$replace.g" chimScript.py
for i in {1..2}
do
  for j in {1..5}
  do
    mkdir -p s${i}/neutral${j}
    cd s${i}/neutral${j}
        cp ../../../1trimTrajectory/s${i}/prod$(($((seqLength*2))+$((j-1)))).xtc all_pbc.xtc
        cp ../../../../s${i}/start0.tpr .
    cp ../../submit1.job .
    cp ../../*.py .
    cp ../../*pdb .
    cp ../../*ndx .
    sed -i "s.JOBNAME.s${i}n${j}.g" submit1.job
    sbatch submit1.job
    cd ../../
  done
done
