#!/bin/bash
source ~/m4.sh
pathtogro=../2*/prot.gro
file=ref_SESE.pdb

for i in {1..2}
do
	for j in {1..5}
	do
		mkdir -p s${i}cluster${j}
   		gmx_mpi check -f ../6*/s${i}*/cluster${j}.xtc &> gmxcheck.txt
		numframes=$(tail -5 gmxcheck.txt | head -1 | tr -dc '0-9')
		echo '[ frames ]' > frames.ndx
		shuf -i 1-${numframes} -n 100 >> frames.ndx
		echo 1 1 | gmx_mpi trjconv -f ../6*/s${i}*/cluster${j}.xtc -s $pathtogro -fr frames.ndx -o s${i}cluster${j}/100random.pdb -center
		rm gmxcheck.txt
	done
done

for i in {1..2}
do
	for j in {1..5}
	do
        	python calculateRMSD.py --ref ${file} --output s${i}cluster${j}/stat.txt --trajectory s${i}cluster${j}/100random.pdb
		cd s${i}cluster${j}
		vmd -m 100random.pdb ../ref_SESE.pdb < ../script.vmd
		cd ../
	done
done
