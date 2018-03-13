#!/usr/bin/python

"""
  select variation set from person with the larges number of SNP
"""

import sys

metadata = dict()
for i in open(sys.argv[1]):
    fields = i.rstrip().split("\t")
    person = fields[5]
    filen  = fields[0]
    if person not in metadata:
        metadata[person] = set()
    metadata[person].add(filen)

snv    = open(sys.argv[2])
header = snv.readline().rstrip().split("\t")
count = dict()

for i in header:
    count[i] = 0

for i in snv:
    fields = i.rstrip().split("\t")
    for j in range(1, len(fields)):
        if fields[j] != "0":
            count[header[j-1]] += 1

snv.close()

winner = dict()
for person in metadata:
    m = 0
    s = ""
    for sample in metadata[person]:
        if sample not in count:
            continue
        if count[sample] > m:
            m = count[sample]
            s = sample
    winner[s] = person

snv = open(sys.argv[2])
header = snv.readline().rstrip().split("\t")
newheader = list()
keep = set()
for i in range(len(header)):
    if header[i] in winner:
        newheader.append(winner[header[i]])
        keep.add(i+1)


print("\t".join(newheader))

for i in snv:
    fields = i.rstrip().split("\t")
    out = list()
    out.append(fields[0])
    s = 0
    for j in range(1,len(fields)):
        if j in keep:
            out.append(fields[j])
            s += int(fields[j])
    if s > 0:
        print("\t".join(out))
