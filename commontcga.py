#!/usr/bin/python3

"""
   Read RNA-seq and SNV metadata and choose only samples where the individual can be found in both list
"""

import sys

def getpatient(filecontent):
    pat = dict()
    for i in filecontent:
        fields  = i.rstrip().split("\t")[1].split("-")
        patient = fields[0] + "-" + fields[1] + "-" + fields[2]
        if patient not in pat:
            pat[patient] = list()
        pat[patient].append(i)
    return(pat)

rna = dict()
snv = dict()

rnastuff = open(sys.argv[1])
snvstuff = open(sys.argv[2])

rna = getpatient(rnastuff)
snv = getpatient(snvstuff)

common = rna.keys() & snv.keys()

outrna = open(sys.argv[3], "w")
outsnv = open(sys.argv[4], "w")

for i in common:
    for rec in rna[i]:
        outrna.write(rec)
    for rec in snv[i]:
        outsnv.write(rec)

outrna.close()
outsnv.close()
rnastuff.close()
snvstuff.close()
