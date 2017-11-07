#!/usr/bin/python

import sys

class Gene:
    def __init__(self, numcov):
        self.length = 0
        self.minpos = 0
        self.maxpos = 0
        self.chrx   = ""
        self.covsum = [0] * numcov

def findLowIndex(pos, array, lowindex, hiindex):


covfiles = sys.argv[2:]

genes = dict()
for i in open(sys.argv[1]):
    fields = i.rstrip().split("\t")
    chrx   = fields[0]
    start  = int(fields[1])
    end    = int(fields[2])
    annot  = fields[3]
    if annot == "-":
        continue
    for j in annot.split(","):
        k,v = j.split("|")
        if k == "ref" and not v.startswith("NM_") and not v.startswith("NR_") and not v.startswith("LOC") and not v.startswith("ORF"):
            if v not in genes:
                genes[v] = Gene(len(covfiles))
            # Assume there is no overlap between regions
            genes[v].length += (end - start)
            genes[v].start = min(start, genes[v].start)
            genes[v].end   = max(end, genes[v].end)
            genes[v].chrx  = chrx

lookup = dict()
for g in genes:
    if g.chrx not in lookup:
        lookup[g.chrx] = list()
    lookup[g.chrx].append([g.start, g.end, g])

for chrx in lookup:
    lookup[chrx] = sorted(lookup[chrx], key = lambda x:x[0])

count = 0
for c in covfiles:
    for i in open(c):
        fields = i.rstrip().split()
        chrx   = fields[0]
        pos    = int(fields[1])
        cov    = int(fields[2])
        lowestindex = findLowIndex(pos, lookup[chrx], 0, len(lookup[chrx])-1)
    count += 1
