#!/usr/bin/python3

import sys
import glob
import gzip


fq = gzip.open(sys.argv[1])
count = 0
found = 0
for line in fq:
    if count % 4 == 1:
        if "TGGAATTCT" in line.decode('utf-8'):
            found += 1
    count += 1
fq.close()
print(sys.argv[1], found / (count / 4))
