#$ -S /bin/bash -t 1-869 -cwd -N quant

export PATH="~/.local/bin:/home/other/tnagy/bigdisk/softwares/mirdeep2_0_0_8/bin:$PATH"

cd /home/other/tnagy/bigdisk/goel2018/processed

FASTA=`ls *.fasta | head -n $SGE_TASK_ID | tail -n 1`

mkdir $SGE_TASK_ID
cd $SGE_TASK_ID

quantifier.pl -p ../../hsa.precursor.fa -m ../../hsa.mature.fa -r ../$FASTA -t hsa -j
find . -name miRNA_expressed.csv -exec mv {} /home/other/tnagy/bigdisk/goel2018/expression/${FASTA%fasta}csv \;
cd ..
rm -fr $SGE_TASK_ID
