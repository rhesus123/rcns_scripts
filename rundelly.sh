#$ -S /bin/bash -t 1-16 -tc 1 -cwd -N delly -l cpu=7

export PATH="~/.local/bin:/bigdisk/programs/bin/bwa:/bigdisk/programs/bin/samtools:$PATH"

cd /home/other/tnagy/bigdisk/fusion_breast

LINE=`head -n $SGE_TASK_ID master.tsv | tail -n 1`
TUMOUR=`echo $LINE | awk '{print $1}'`
NORMAL=`echo $LINE | awk '{print $2}'`
OUTPREFIX=`basename $TUMOUR | sed 's/.bam//'`

bamtofastq filename=bams/$TUMOUR F=tum.${SGE_TASK_ID}_1.fastq.gz F2=tum.${SGE_TASK_ID}_2.fastq.gz gz=1 >/dev/null
bwa mem -t 6 /home/other/tnagy/bigdisk/genomes/human/bwa/Homo_sapiens.GRCh38.dna.primary_assembly.fa tum.${SGE_TASK_ID}_1.fastq.gz tum.${SGE_TASK_ID}_2.fastq.gz | samtools view -Sb - >tum.${SGE_TASK_ID}.raw.bam
rm tum.${SGE_TASK_ID}_1.fastq.gz tum.${SGE_TASK_ID}_2.fastq.gz

bamtofastq filename=bams/$NORMAL F=nor.${SGE_TASK_ID}_1.fastq.gz F2=nor.${SGE_TASK_ID}_2.fastq.gz gz=1 >/dev/null
bwa mem -t 6 /home/other/tnagy/bigdisk/genomes/human/bwa/Homo_sapiens.GRCh38.dna.primary_assembly.fa nor.${SGE_TASK_ID}_1.fastq.gz nor.${SGE_TASK_ID}_2.fastq.gz | samtools view -Sb - >nor.${SGE_TASK_ID}.raw.bam

rm nor.${SGE_TASK_ID}_1.fastq.gz nor.${SGE_TASK_ID}_2.fastq.gz

samtools sort tum.${SGE_TASK_ID}.raw.bam tum.${SGE_TASK_ID}
samtools sort nor.${SGE_TASK_ID}.raw.bam nor.${SGE_TASK_ID}
samtools index tum.${SGE_TASK_ID}.bam
samtools index nor.${SGE_TASK_ID}.bam

rm tum.${SGE_TASK_ID}.raw.bam nor.${SGE_TASK_ID}.raw.bam

delly call -o dellyout/${OUTPREFIX}bcf -x human.hg38.excl.tsv -n -t BND -g /home/other/tnagy/bigdisk/genomes/human/text/Homo_sapiens.GRCh38.dna.primary_assembly.fa tum.${SGE_TASK_ID}.bam nor.${SGE_TASK_ID}.bam

rm tum.${SGE_TASK_ID}.bam nor.${SGE_TASK_ID}.bam
