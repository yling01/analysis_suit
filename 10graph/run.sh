#!/bin/sh
s1R=s1rmsdHotLoop.xvg
s1C=s1result.txt

s2R=s2rmsdHotLoop.xvg
s2C=s2result.txt

dir1=/cluster/tufts/ylin12/tim/dPCA_final/SESEG1/50-100/10furtherAnalysis
dir2=/cluster/tufts/ylin12/tim/dPCA_final/SESEG2/100-150ns/10furtherAnalysis
dir3=/cluster/tufts/ylin12/tim/dPCA_final/SESEG3/150-250/10furtherAnalysis
dir4=/cluster/tufts/ylin12/tim/dPCA_final/SESEG4/50-100/10furtherAnalysis
dir5=/cluster/tufts/ylin12/tim/dPCA_final/SESEG5/50-100/10furtherAnalysis
dir6=/cluster/tufts/ylin12/tim/dPCA_final/SESEG6/50-100/10furtherAnalysis


system1=SESEG
system2=SESEGG
system3=SESEEGGG
system4=SESEGGGG
system5=SESEGGGGG
system6=SESEGGGGGG


long_arg="graph.py --RMSDFile_s1 ${dir1}/${s1R},${dir2}/${s1R},${dir3}/${s1R},${dir4}/${s1R},${dir5}/${s1R},${dir6}/${s1R} --RMSDFile_s2 ${dir1}/${s2R},${dir2}/${s2R},${dir3}/${s2R},${dir4}/${s2R},${dir5}/${s2R},${dir6}/${s2R} --clashFile_s1 ${dir1}/${s1C},${dir2}/${s1C},${dir3}/${s1C},${dir4}/${s1C},${dir5}/${s1C},${dir6}/${s1C} --clashFile_s2 ${dir1}/${s2C},${dir2}/${s2C},${dir3}/${s2C},${dir4}/${s2C},${dir5}/${s2C},${dir6}/${s2C} --seq
SESEG,SESEGG,SESEGGG,SESEGGGG,SESEGGGGG,SESEGGGGGG"

python $long_arg
