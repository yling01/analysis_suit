#!/bin/bash
pathtogro=../2*/prot.gro
echo "1 for SESE 2 for ESE"
read sys
if [ ${sys} -eq 1 ]
then
    file=SESE.pdb
else
    file=ESE.pdb
fi

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
		echo 4 4 | gmx_mpi rms -s ${file} -f s${i}cluster${j}/100random.pdb -nomw -o s${i}cluster${j}/rmsd.xvg
		python calcStat.py s${i}cluster${j}/rmsd.xvg &> s${i}cluster${j}/stat
		cd s${i}cluster${j}
		vmd -m 100random.pdb ../Cks1.pdb < ../script.vmd
		cd ../
	done
done




