echo "Top directory: "
read dir

echo "Sequence Length: "
read seqLength

echo "Sequence: "
read seq

sed -i s.DIRTOCHANGE.${dir}.g trim.sh
sed -i s.LENGTHTOCHANGE.${seqLength}.g trim.sh
sed -i s.SEQUENCETOCHANGE.${seq}.g trim.sh

echo "Getting backbone atoms ..."
python writeIndices.py --Omega True --gro curr.gro

sbatch submit.job
