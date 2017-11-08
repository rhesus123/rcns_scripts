#!/usr/bin/python

import sys

class Gene:
    def __init__(self, numcov):
        self.length = 0
        self.start  = 0
        self.end    = 0
        self.chrx   = ""
        self.covsum = [0] * numcov

def findLowIndex(pos, array, lowindex, hiindex):
    midindex = lowindex + (hiindex - lowindex) / 2
    lowpos   = array[lowindex][0]
    midpos   = array[midindex][0]
    hiend    = array[hiindex][1]

    if hiindex - lowindex < 3:
        return lowindex

    if pos < lowpos or pos > hiend:
        return -1
    if pos > lowpos and pos < midpos:
        return findLowIndex(pos, array, lowindex, midindex)
    if pos > midpos and pos < hiend:
        return findLowIndex(pos, array, midindex, hiindex)
    return -1

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
                genes[v].start = start
                genes[v].end   = end
            genes[v].length += (end - start)
            genes[v].start = min(start, genes[v].start)
            genes[v].end   = max(end, genes[v].end)
            genes[v].chrx  = chrx

lookup = dict()
for g in genes:
    if genes[g].chrx not in lookup:
        lookup[genes[g].chrx] = list()
    lookup[genes[g].chrx].append([genes[g].start, genes[g].end, g])

for chrx in lookup:
    lookup[chrx] = sorted(lookup[chrx], key = lambda x:x[0])

count = 0
for c in covfiles:
    sys.stderr.write(c+"\n")
    for i in open(c):
        fields = i.rstrip().split()
        chrx   = fields[0]
        pos    = int(fields[1])
        cov    = int(fields[2])
        lowestindex = findLowIndex(pos, lookup[chrx], 0, len(lookup[chrx])-1)
        for index in range(lowestindex, len(lookup[chrx])):
            if lookup[chrx][index][0] < pos and lookup[chrx][index][1] > pos:
                g = lookup[chrx][index][2]
                genes[g].covsum[count] += cov
    count += 1

print "\t".join(covfiles)
for g in genes:
    line = list()
    line.append(g)
    for i in range(len(covfiles)):
        ratio = float(genes[g].covsum[i]) / float(genes[g].length)
        line.append(str(ratio))
    print "\t".join(line)
