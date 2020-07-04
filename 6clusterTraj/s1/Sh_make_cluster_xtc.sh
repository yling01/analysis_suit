#!/bin/bash
cp ../../5*/Result/s1/*ndx cluster.ndx

max_cluster=$(($(grep state cluster.ndx | wc -l)-1))
xtc=../../1trimTrajectory/s1/*all.xtc
gro=../../2*/prot.gro
ndx=cluster.ndx

clusters=( 1 2 3 4 5 )

##############################################

for c in ${clusters[@]}; do
   #echo $c,$max_cluster
   echo $max_cluster 0 | gmx_mpi trjconv -f $xtc -s $gro -fr $ndx -o cluster${c}.xtc &> cluster${c}.log
   max_cluster=$((${max_cluster}-1))
done
