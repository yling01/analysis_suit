#!/bin/sh
xtc=../3*/all.trr
gro=../2*/dpca.gro
ndx=../2*/dpca.ndx

vec=eigenvec.trr
DNAME=pc1_pc2_pc3

gmx_mpi covar -n $ndx -f $xtc -s $gro -ascii -xpm -xpma -nofit -nomwa -noref -nopbc &> covar.log


echo "Enter the sequence name: "
read PROT



mkdir $DNAME

function project_all () {
  local dname=$1

  out1=$dname/all_1.xvg
  out2=$dname/all_2.xvg
  gmx_mpi anaeig -s $gro -n $ndx -v $vec -f $xtc -2d $out1 -first 1 -last 2 &> anaeig_all1.log
  gmx_mpi anaeig -s $gro -n $ndx -v $vec -f $xtc -2d $out2 -first 1 -last 3 &> anaeig_all2.log

  xtc=../3*/s1/s1${PROT}_all.trr
  out1=$dname/s1${PROT}_1.xvg
  out2=$dname/s1${PROT}_2.xvg
  gmx_mpi anaeig -s $gro -n $ndx -v $vec -f $xtc -2d $out1 -first 1 -last 2 &> anaeig_s11.log
  gmx_mpi anaeig -s $gro -n $ndx -v $vec -f $xtc -2d $out2 -first 1 -last 3 &> anaeig_s12.log

  xtc=../3*/s2/s2${PROT}_all.trr
  out1=$dname/s2${PROT}_1.xvg
  out2=$dname/s2${PROT}_2.xvg
  gmx_mpi anaeig -s $gro -n $ndx -v $vec -f $xtc -2d $out1 -first 1 -last 2 &> anaeig_s21.log
  gmx_mpi anaeig -s $gro -n $ndx -v $vec -f $xtc -2d $out2 -first 1 -last 3 &> anaeig_s22.log

}



project_all $DNAME

function combine(){
   local fname=$1
   inp1=pc1_pc2_pc3/${fname}_1.xvg
   inp2=pc1_pc2_pc3/${fname}_2.xvg

   tail -n +18 $inp1 > tmp1
   tail -n +18 $inp2 > tmp2

   echo "   Processing $inp1 $inp2 ..."
   python Py_combine.py tmp1 tmp2 > pc1_pc2_pc3/$fname.txt
}

combine all
combine s1${PROT}
combine s2${PROT}

rm tmp*
