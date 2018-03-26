#!/usr/bin/python3

import sys
import gzip

snv = open(sys.argv[1]) # snv.allcancer.tsv
header = snv.readline().rstrip().split("\t")
snv.close()

files    = dict()
meta     = open(sys.argv[2])
for i in meta:
    fields = i.rstrip().split("\t")
    if fields[5] in header:
        files[fields[5]] = fields[0]
meta.close()

matrix    = list()
get       = set(files.values())
filecount = 0
newheader = list()
for i in header:
    if i not in files:
        sys.stderr.write(i + "\n")
        continue
    newheader.append(i)
    filename  = sys.argv[3] + "/" + files[i]
    htcount   = gzip.open(filename)
    linecount = 0
    for line in htcount:
        fields = line.rstrip().split()
        if fields[0].startswith("_"):
            continue
        if filecount == 0:
            matrix.append([])
            matrix[linecount].append(fields[0])
        matrix[linecount].append(fields[1])
        linecount += 1
    htcount.close()
    filecount += 1

print("\t".join(newheader))
for i in matrix:
    nums = [int(x) for x in i[1:]]
    samplenum = 0
    for n in nums:
        if n > 5:
            samplenum += 1
    if samplenum < 3:
        continue
    print("\t".join(i))
