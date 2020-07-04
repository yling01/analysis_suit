echo "Top directory: "
read dir

echo "Sequence Length: "
read seqLength

echo "Sequence: "
read seq

echo "Enter the start time in ps: "
read start

echo "Enter end time in ps: "
read end

sed -i s.STARTTOCHANGE.${start}.g trim.sh
sed -i s.ENDTOCHANGE.${end}.g trim.sh
sed -i s.DIRTOCHANGE.${dir}.g trim.sh
sed -i s.LENGTHTOCHANGE.${seqLength}.g trim.sh
sed -i s.SEQUENCETOCHANGE.${seq}.g trim.sh

echo "Getting backbone atoms ..."
cp ${dir}/s1/9*/npt.gro curr.gro
python writeIndices.py --Omega True --gro curr.gro

sbatch submit.job
