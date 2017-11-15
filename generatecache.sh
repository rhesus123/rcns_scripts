#!/bin/bash

for gene in `cat genes.txt`
do
	for cancerid in `seq 1 12`
	do
		Rscript genotype.R ./cache.${gene}.${cancerid} $gene 12 $cancerid 0.05 1.44 all 10
	done
done
