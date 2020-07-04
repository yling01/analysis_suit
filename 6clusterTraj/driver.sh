#!/bin/sh
echo "What is the directory of this dPCA process"
read DIR
for i in {1..2}
do
    cd ${DIR}/7clusterTraj/s${i}
    ./Sh_make_cluster_xtc.sh
done

