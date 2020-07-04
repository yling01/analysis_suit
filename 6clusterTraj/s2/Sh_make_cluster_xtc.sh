#!/bin/bash
#Assuming the cluster.ndx file has clusters named as "state"
#-1 is here because there is a state 0 that has all frames
cp ../../5*/Result/s2/*ndx cluster.ndx
max_cluster=$(($(grep state cluster.ndx | wc -l)-1))
xtc=../../1trimTrajectory/s2/*all.xtc
gro=../../2*/prot.gro
ndx=cluster.ndx

clusters=( 1 2 3 4 5 )

##############################################

for c in ${clusters[@]}; do
   #echo $c,$max_cluster
   echo $max_cluster 0 | gmx_mpi trjconv -f $xtc -s $gro -fr $ndx -o cluster${c}.xtc &> cluster${c}.log
   max_cluster=$((${max_cluster}-1))
done
