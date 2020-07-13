#!/bin/sh
module load python/3.6.0
module load gcc/7.3.0
module load cuda/10.2
module load openmpi/2.1.2
module load libmatheval
export PATH
source /cluster/tufts/ysl8/jovan/gromacs_linlab_avx512/bin/GMXRC.bash
export PLUMED_KERNEL=/cluster/tufts/ysl8/jovan/gromacs_linlab_avx2/plumed/lib/libplumedKernel.so
export GMXLIB=/cluster/tufts/ylin12/tim/localGMXLIB
for i in {1..2}
do
    cd s${i}
    ./Sh_make_cluster_xtc.sh
    cd ../
done
