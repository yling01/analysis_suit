#!/bin/sh
for i in {1..2}
do
    cd s${i}
    ./Sh_make_cluster_xtc.sh
    cd ../
done

