#!/usr/bin/python3

import sys
import glob
import gzip

fastqz = glob.glob("*/*/*.fastq.gz")

for i in fastqz:
    fq = gzip.open(i)
    count = 0
    found = 0
    for line in fq:
        if count % 4 == 1:
            if "TGGAATTCT" in line.decode('utf-8'):
                found += 1
        count += 1
    fq.close()
    print(i, found / (count / 4))
