#!/bin/bash

#BSUB -J"prepare"
#BSUB -o prep.out
#BSUB -e prep.err
#BSUB -M 40000
#BSUB -n 4
#BSUB -R "select[mem>40000] rusage[mem=40000] span[ptile=4]"

export PATH="/nfs/users/nfs_t/tn5/apps/STAR-2.5.3a/bin/Linux_x86_64_static:$PATH"
cd /nfs/users/nfs_t/tn5/team219/fusion_breast/GRCh38_gencode_v26_CTAT_lib_July192017
../softwares/STAR-Fusion_v1.1.0/FusionFilter/prep_genome_lib.pl --genome_fa ref_genome.fa --gtf ref_annot.gtf --blast_pairs blast_pairs.gene_syms.outfmt6.gz --fusion_annot_lib fusion_lib.dat.gz
../softwares/STAR-Fusion_v1.1.0/FusionFilter/util/index_pfam_domain_info.pl --pfam_domains PFAM.domtblout.dat.gz --genome_lib_dir ctat_genome_lib_build_dir
