#$ -S /bin/bash -t 1-869 -cwd -N cutalign 


export PATH="~/.local/bin:/bigdisk/programs/bin/bwa:/bigdisk/programs/bin/samtools:$PATH"

cd /home/other/tnagy/bigdisk/goel2018/rawfastq/

FQ=`ls *fastq.gz | head -n $SGE_TASK_ID | tail -n 1`

cutadapt -a TGGAATTCTCGGGTGC -e 0.13 -q 25,25 -m 18 -o /home/other/tnagy/bigdisk/goel2018/trimmed/$FQ $FQ
