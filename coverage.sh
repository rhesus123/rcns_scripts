#$ -S /bin/bash -t 1-48 -cwd -N coverage

export PATH="/bigdisk/programs/bin/samtools:$PATH"
BED=/home/other/tnagy/bigdisk/paraffin/hglft_genome_36e9_ade550.bed

cd ../bams
BAM=`ls *.bam | head -n $SGE_TASK_ID | tail -n 1`

samtools depth -b $BED $BAM >../coverage/${BAM%bam}cov
