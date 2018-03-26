#!/usr/bin/python3

import sys

matrix = open(sys.argv[1])
header = matrix.readline().rstrip().split("\t")
print("gene\tsample\tcount")
for i in matrix:
    fields = i.rstrip().split("\t")
    gene   = fields[0]
    for j in range(len(header)):
        print(gene, header[j], fields[j+1], sep = "\t")
