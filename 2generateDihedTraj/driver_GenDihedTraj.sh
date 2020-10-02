#!/bin/sh
source ~/compute.sh
echo "Sequence Length: "
read seqLength

echo "Enter the sequence: "
read prot

#copy
cp ../1trim*/curr.gro prot.gro

#write NDX file
echo "writing dpca.ndx file..."
dihedralNum=$(((seqLength*4+2)/3))
string="[dummy]\n"
for i in `seq 1 $dihedralNum`; do
  string+="${i}whitespace"
done

printf ${string} > dpca.ndx
sed -i 's/whitespace/ /g' dpca.ndx

#trjconv
echo "generating dpca.gro..."
gmx_mpi trjconv -f prot.gro -s prot.gro -o prot.gro << EOF
1
EOF
gmx_mpi trjconv -f prot.gro -n dpca.ndx -s prot.gro -o dpca.gro &>trjconv.log

python writeIndices.py --gro prot.gro --PhiPsi True
first=$((seqLength*2))

#Generate Trajectory
for i in `seq ${first} $((seqLength*2+4))`; do
  for j in `seq 1 2`; do
    echo "writing dihedral trajectory for s${j}prod${i}"
    inputNDX=../1*/s${j}/prod${i}.xtc
    outputDir=../3dihed_traj/s${j}
    mkdir -p $outputDir
    outputFile=${outputDir}/${prot}_${i}.trr
    gmx_mpi angle -f $inputNDX -n PhiPsi.ndx -or $outputFile -type dihedral &> angle_s${j}_${i}.log
  done
done

#concatenate trajectory
for i in `seq 1 2`; do
  echo "concatenating s${i} dihedral trajectories"
  dir=../3*/s${i}
  gmx_mpi trjcat -f $dir/${prot}_${first}.trr $dir/${prot}_$((first+1)).trr $dir/${prot}_$((first+2)).trr $dir/${prot}_$((first+3)).trr $dir/${prot}_$((first+4)).trr -cat -o s${i}${prot}_all.trr &> trjcat_s${i}.log
  cp s${i}${prot}_all.trr ${dir}/
done

echo "concatenating all dihedral trajectories"
gmx_mpi trjcat -f s1${prot}_all.trr s2${prot}_all.trr -cat -o all.trr -nosort &> trjcat_all.log
cp all.trr ../3*/
