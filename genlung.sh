#!/bin/bash

for gene in EGFR
do
	for muttype in 3 6 9 10 12 14 18 26 27
	do
		tmp_name="$gene.$muttype"
		./powermw onegroup $gene mut.8.1.$muttype.tsv exp.8.1.tsv $tmp_name.tsv
		Rscript createpic.R genotype $gene $tmp_name $tmp_name.tsv exp.8.1.tsv mut.8.1.$muttype.tsv 5 0
	done
done
