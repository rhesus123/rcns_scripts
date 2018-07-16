#!/usr/bin/python3

import sys
import glob
import os

class Elements:
    def __init__(self):
        self.TCGAp   = 0 # Number of p < 0.05 in TCGA result
        self.TCGAfdr = 0 # Number of FDR < 0.05 in TCGA result
        self.METAp   = 0 # Number of p < 0.05 in METABRIC result
        self.METAfdr = 0 # Number of FDR < 0.05 in METABRIC result

def parseFile(filename):
    p = 0
    fdr = 0
    f = open(filename)
    f.readline()
    for line in f:
        fields = line.rstrip().split()
        if float(fields[2].replace("<", "")) < 0.05:
            p += 1
        if float(fields[3]) < 0.05:
            fdr += 1
    f.close()
    return p, fdr

tcgafiles = glob.glob(sys.argv[1] + "/*.tcga.tsv")

result = dict()

for filename in tcgafiles:
    gene = ".".join(os.path.basename(filename).split(".")[:-2])
    result[gene] = Elements()
    result[gene].TCGAp, result[gene].TCGAfdr = parseFile(filename)
    result[gene].METAp, result[gene].METAfdr = parseFile(filename.replace("tcga", "meta"))

print("Gene\tTCGA_sigp\tTCGA_sigfdr\tMETA_sigp\tMETA_sigfdr")
for gene in result:
    e = result[gene]
    print("%s\t%d\t%d\t%d\t%d" % (gene, e.TCGAp, e.TCGAfdr, e.METAp, e.METAfdr))
