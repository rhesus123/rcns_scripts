#$ -S /bin/bash -t 1-869 -cwd -N mapper -l cpu=4

export PATH="~/.local/bin:/home/other/tnagy/bigdisk/softwares/mirdeep2_0_0_8/bin:$PATH"

cd /home/other/tnagy/bigdisk/goel2018/trimmed

FQ=`ls *.fastq.gz | head -n $SGE_TASK_ID | tail -n 1`

zcat $FQ >${SGE_TASK_ID}.fq

mapper.pl ${SGE_TASK_ID}.fq -e -h -i -m -p /home/other/tnagy/bigdisk/genomes/hs.grch38.92 -s ../processed/${FQ%fastq.gz}fasta -t ../align/${FQ%fastq.gz}arf -o 4

rm ${SGE_TASK_ID}.fq
