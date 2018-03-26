#!/usr/bin/python3

import sys

noneed = set()
for i in open(sys.argv[1]):
    noneed.add(i.rstrip())

snv = open(sys.argv[2])
header = snv.readline().rstrip().split("\t")
newheader = list()
keep = set()
for i in range(len(header)):
    if header[i] in noneed:
        continue
    newheader.append(header[i])
    keep.add(i+1)

print("\t".join(newheader))
for i in snv:
    fields = i.rstrip().split("\t")
    out = list()
    s   = 0
    out.append(fields[0])
    for index in range(1,len(fields)):
        if index in keep:
            out.append(fields[index])
            s += int(fields[index])
    if s > 5:
        print("\t".join(out))
