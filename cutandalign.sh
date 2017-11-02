#$ -S /bin/bash -t 1-48 -cwd -N cutalign

export PATH="~/.local/bin:/bigdisk/programs/bin/bwa:/bigdisk/programs/bin/samtools:$PATH"
INDEX=/home/other/tnagy/bigdisk/genomes/human/bwa/Homo_sapiens.GRCh38.dna.primary_assembly.fa

cd /home/other/tnagy/bigdisk/paraffin/fastq

F1=`ls *R1_001.fastq.gz | head -n $SGE_TASK_ID | tail -n 1`
F2=${F1%R1_001.fastq.gz}R2_001.fastq.gz

cutadapt -a AGATCGGAAGAGCACACGTCTGAACTCCAGTCA -A AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGT -o read1.${SGE_TASK_ID}.fastq -p read2.${SGE_TASK_ID}.fastq $F1 $F2
bwa mem $INDEX read1.${SGE_TASK_ID}.fastq read2.${SGE_TASK_ID}.fastq | samtools view -Sb - >/home/other/tnagy/bigdisk/paraffin/bams/tmp.${SGE_TASK_ID}.bam
rm read1.${SGE_TASK_ID}.fastq read2.${SGE_TASK_ID}.fastq
cd /home/other/tnagy/bigdisk/paraffin/bams/

samtools sort tmp.${SGE_TASK_ID}.bam ${F1%_R1_001.fastq.gz}
samtools index ${F1%_R1_001.fastq.gz}.bam
rm tmp.${SGE_TASK_ID}.bam
