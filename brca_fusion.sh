#!/bin/bash

# This script try to download all BAM files from GDC and run STAR-Fusion on it

MANIFEST=/home/tibor/work/fusion_breast/gdc_files/gdc_manifest.2017-10-26T08_52_49.606354.txt
TOKEN=/home/tibor/work/fusion_breast/gdc_files/gdc-user-token.2017-10-30T07_27_19.565Z.txt
GENOME=/home/tibor/work/genomes/human/starfusion

for i in `seq 2 1223`
do
	head -n 1 $MANIFEST >tmp.mani
	head -n $i $MANIFEST | tail -n 1 >>tmp.mani

	gdc-client download -d ../bams/ -m tmp.mani -t $TOKEN --retry-amount 100 --wait-time 10 --log-file tmp.log >/dev/null
	BAM=`tail -n 1 tmp.mani | awk '{print $2}'`
	OUT=`tail -n 1 tmp.mani | awk '{print $1}'`
	F1=../seq/${BAM%_gdc_realn_rehead.bam}.1.fastq # first  read pair name
	F2=../seq/${BAM%_gdc_realn_rehead.bam}.2.fastq # second read pair name
	bamtofastq filename=../bams/$OUT/$BAM F=$F1 F2=$F2 >/dev/null
	mkdir /home/tibor/work/fusion_breast/out/$OUT
	/opt/STAR-Fusion_v1.1.0/STAR-Fusion --genome_lib_dir $GENOME --left_fq $F1 --right_fq $F2 --annotate --examine_coding_effect --output_dir /home/tibor/work/fusion_breast/out/$OUT
	rm -fr ../bams/$OUT $F1 $F2
done
