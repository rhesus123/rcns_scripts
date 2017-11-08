#$ -S /bin/bash -t 1-48 -cwd -N cov

cd ../coverage
COV=`ls *.grch37.cov | head -n $SGE_TASK_ID | tail -n 1`
cd ../scripts
python depthmatrix.py ../ki.bed ../coverage/$COV >${COV%cov}txt
