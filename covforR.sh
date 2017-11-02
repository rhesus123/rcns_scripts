#$ -S /bin/bash -t 1-48 -cwd -N cov

cd ../coverage
COV=`ls *.cov | head -n $SGE_TASK_ID | tail -n 1`
cd ../scripts
python avgdepth.py ../hglft_genome_36e9_ade550.bed ../coverage/$COV >${COV%cov}txt
