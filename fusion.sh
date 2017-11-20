#!/bin/bash

#BSUB -J "fusion[1-1221]%20"
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

/lustre/scratch117/casm/team219/tn5/fusion_breast/softwares/STAR-Fusion_v1.1.0/STAR-Fusion --genome_lib_dir /lustre/scratch117/casm/team219/tn5/fusion_breast/ctat_grch38 --left_fq ${SAMPLE}.1.fastq --right_fq ${SAMPLE}.2.fastq --output_dir ../fusion_results/${SAMPLE} --CPU 8

mv ../fusion_results/${SAMPLE}/star-fusion.fusion_predictions.abridged.tsv ../fusion_results/${SAMPLE}.abridged.tsv
mv ../fusion_results/${SAMPLE}/star-fusion.fusion_predictions.tsv ../fusion_results/${SAMPLE}.tsv

rm ${SAMPLE}.1.fastq ${SAMPLE}.2.fastq
rm -fr ../fusion_results/${SAMPLE}
