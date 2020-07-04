#!/bin/sh
source ~/compute.sh
#cp ../1trim*/curr.gro .
#python writeIndices.py --PhiPsi True --gro curr.gro
#gmx_mpi trjcat -f ../1trimTrajectory/s1/all.xtc ../1trimTrajectory/s2/all.xtc -cat -nosort -o all.xtc
#gmx_mpi angle -f all.xtc -n PhiPsi.ndx -all -type dihedral -ov phipsi.xvg
cp ../4*/pc1_pc2_pc3/all.txt .
python dPCA.py
