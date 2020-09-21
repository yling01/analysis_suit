seqLength=LENGTHTOCHANGE
seq=SEQUENCETOCHANGE

first=$((seqLength*2))

inputS1="../../s1"
inputS2="../../s2"

outputS1="s1"
outputS2="s2"

for i in `seq $((seqLength*2)) $((seqLength*2+4))`;
do
	echo "Trimming s1/prod${i}"
	echo 1 | gmx_mpi trjconv -f ${inputS1}/prod${i}*.xtc -s ${inputS1}/start${i}.tpr -o ${outputS1}/prod${i}_temp.xtc -pbc mol -ur compact -fr ${inputS1}/prod${i}.ndx &> ${outputS1}/trjconv${i}_temp.log
    echo 1 | gmx_mpi trjconv -f ${outputS1}/prod${i}_temp.xtc -s ${inputS1}/start${i}.tpr -b STARTTOCHANGE -e ENDTOCHANGE -o ${outputS1}/prod${i}.xtc &> ${outputS1}/trjconv${i}.log

	echo "Trimming s2/prod${i}"
	echo 1 | gmx_mpi trjconv -f ${inputS2}/prod${i}*.xtc -s ${inputS2}/start${i}.tpr -o ${outputS2}/prod${i}_temp.xtc -pbc mol -ur compact -fr ${inputS2}/prod${i}.ndx &> ${outputS2}/trjconv${i}_temp.log
   	echo 1 | gmx_mpi trjconv -f ${outputS2}/prod${i}_temp.xtc -s ${inputS2}/start${i}.tpr -b STARTTOCHANGE -e ENDTOCHANGE -o ${outputS2}/prod${i}.xtc &> ${outputS2}/trjconv${i}.log

done

echo "Concatenating s1/xtc's"
gmx_mpi trjcat -f ${outputS1}/prod${first}.xtc ${outputS1}/prod$((first+1)).xtc ${outputS1}/prod$((first+2)).xtc ${outputS1}/prod$((first+3)).xtc ${outputS1}/prod$((first+4)).xtc -cat -nosort -o ${outputS1}/all.xtc &> ${outputS1}/trjcat.log
echo "Concatenating s2/xtc's"
gmx_mpi trjcat -f ${outputS2}/prod${first}.xtc ${outputS2}/prod$((first+1)).xtc ${outputS2}/prod$((first+2)).xtc ${outputS2}/prod$((first+3)).xtc ${outputS2}/prod$((first+4)).xtc -cat -nosort -o ${outputS2}/all.xtc &> ${outputS2}/trjcat.log

gmx_mpi angle -f ${outputS1}/all.xtc -n Omega.ndx -ov ${outputS1}/struct_omega.xvg -all -type dihedral &> ${outputS1}/angle.log
gmx_mpi angle -f ${outputS2}/all.xtc -n Omega.ndx -ov ${outputS2}/struct_omega.xvg -all -type dihedral &> ${outputS2}/angle.log
