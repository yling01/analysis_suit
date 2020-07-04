#!/bin/bash
echo "Make sure to change atoms in chimScript.py"
echo "Top directory: "
read dir
echo "Sequence Length: "
read seqLength
for i in {1..2}
do
	for j in {1..5}
	do
		mkdir -p s${i}/neutral${j}
		cd s${i}/neutral${j}
		cp ${dir}/s${i}/bemeta/prod$(($((seqLength*2))+$((j-1)))).xtc all.xtc
		cp ${dir}/s${i}/bemeta/start0.tpr .
		cp ../../submit1.job .
		cp ../../*.py .
		cp ../../*pdb .
		cp ../../*ndx .
		sed -i "s.JOBNAME.s${i}n${j}.g" submit1.job
		sbatch submit1.job
		cd ../../
	done
done		
