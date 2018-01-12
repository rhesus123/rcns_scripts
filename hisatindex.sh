#!/bin/bash

#SBATCH -A biomarker_1
#SBATCH --job-name=hisat2index
#SBATCH --time 1-10
#SBATCH --mem-per-cpu=8000
#SBATCH -o log
#SBATCH -e err

/home/oqqn0bf/.local/bin/hisat2-build Homo_sapiens.GRCh38.dna.primary_assembly.fa hisat2index
