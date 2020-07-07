#!/bin/env bash
source ~/compute.sh
echo "number of residues: "
read numRes
echo "sequence: "
read seq
#calculate dihedral angle
function calcDihed () {
  local ir=$1

  out_dir1=s1_phipsi
  out_dir2=s2_phipsi
  xtc1=../6*/s1*/cluster${ir}.xtc
  xtc2=../6*/s2*/cluster${ir}.xtc
  ndx=../2*/PhiPsi.ndx
  [[ ! -e $out_dir1 ]] && mkdir -p $out_dir1
  [[ ! -e $out_dir2 ]] && mkdir -p $out_dir2

  out1=${out_dir1}/cluster${ir}.xvg
  out2=${out_dir2}/cluster${ir}.xvg
  gmx_mpi angle -f $xtc1 -n $ndx -type dihedral -all -ov $out1 &> ${out_dir1}/cluster${ir}.log
  gmx_mpi angle -f $xtc2 -n $ndx -type dihedral -all -ov $out2 &> ${out_dir2}/cluster${ir}.log
  rm -rf angdist*.xvg
}


for (( ir=1; ir<=5; ir++ )); do
   calcDihed $ir
done

#clean the output
for f in */*.xvg; do
   out=${f/.xvg/.txt}
   tail -n +18 $f > $out
done

#get the ramachandran plot
for ((i=1; i<=5; i++))
   do
   for ((j=1; j<=2; j++))
      do
      echo 'Calculating cluster' ${i} 's'${j}
      if [ ${i} == 1  ]; then
          python plot.py --input s${j}_phipsi/cluster$i.txt --output s${j}_cluster${i}.png \
              --numRes ${numRes} --seq ${seq} --degreeFile SESE.txt \
              --NIP ../5*/Result/s${j}/NIP.txt --RMSD ../7sample/s${j}cluster${i}/stat.txt \
              --population ../5*/Result/s${j}/cluster${i}.txt --WriteDescription True
      else
          python plot.py --input s${j}_phipsi/cluster$i.txt --output s${j}_cluster${i}.png \
              --numRes ${numRes} --seq ${seq} --degreeFile SESE.txt \
              --NIP ../5*/Result/s${j}/NIP.txt --RMSD ../7sample/s${j}cluster${i}/stat.txt \
              --population ../5*/Result/s${j}/cluster${i}.txt --WriteDescription False
      fi
   done
done
