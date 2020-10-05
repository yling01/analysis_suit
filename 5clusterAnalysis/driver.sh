#!/bin/sh
echo "Enter the sequence:"
read sequence
sed -i s/SEQUENCETOCHANGE/${sequence}/g submit.job
sbatch submit.job
