#!/bin/bash

#BSUB -J "fusion[1013,1022,1023,1033,1045,1061,1073,1128,1131,1141,1142,1191,153,159,197,20,252,260,281,303,322,340,409,418,428,429,546,558,610,611,631,632,633,651,676,682,7,714,719,720,744,763,777,794,816,819,857,867,87,88,893,915,938,982]%20"
#BSUB -M 70000
#BSUB -R "select[mem>70000] rusage[mem=70000] span[ptile=8]"
#BSUB -q basement
#BSUB -n 8
#BSUB -o out.%I
#BSUB -e err.%I

export PATH="/nfs/users/nfs_t/tn5/apps/STAR-2.5.3a/bin/Linux_x86_64_static:$PATH"
cd /lustre/scratch117/casm/team219/tn5/fusion_breast/bams

BAM=`find . -name "*.bam" | head -n $LSB_JOBINDEX | tail -n 1`
SAMPLE=`basename $BAM | sed 's/_gdc_realn_rehead.bam//'`

/software/hpag/biobambam/latest/bin/bamtofastq filename=${BAM} F=${SAMPLE}.1.fastq F2=${SAMPLE}.2.fastq >/dev/null

mkdir ../fusion_results/${SAMPLE}

STAR --genomeDir /lustre/scratch117/casm/team219/tn5/fusion_breast/ctat_grch38/ref_genome.fa.star.idx  --readFilesIn ${SAMPLE}.1.fastq ${SAMPLE}.2.fastq  --outReadsUnmapped None  --chimSegmentMin 12  --chimJunctionOverhangMin 12  --alignSJDBoverhangMin 10  --alignMatesGapMax 100000  --alignIntronMax 100000  --chimSegmentReadGapMax 3  --alignSJstitchMismatchNmax 5 -1 5 5  --runThreadN 8 --limitBAMsortRAM 54171586026  --outSAMstrandField intronMotif  --outSAMtype BAM SortedByCoordinate  --twopassMode Basic --outFileNamePrefix ../fusion_results/${SAMPLE}/

/lustre/scratch117/casm/team219/tn5/fusion_breast/softwares/STAR-Fusion_v1.1.0/STAR-Fusion --genome_lib_dir /lustre/scratch117/casm/team219/tn5/fusion_breast/ctat_grch38 -J ../fusion_results/${SAMPLE}/Chimeric.out.junction --left_fq ${SAMPLE}.1.fastq --right_fq ${SAMPLE}.2.fastq --output_dir ../fusion_results/${SAMPLE} --CPU 8

mv ../fusion_results/${SAMPLE}/star-fusion.fusion_predictions.abridged.tsv ../fusion_results/${SAMPLE}.abridged.tsv
mv ../fusion_results/${SAMPLE}/star-fusion.fusion_predictions.tsv ../fusion_results/${SAMPLE}.tsv

rm ${SAMPLE}.1.fastq ${SAMPLE}.2.fastq
rm -fr ../fusion_results/${SAMPLE}
