#!/usr/bin/python3

"""
  The script reads a GTF file (which is used with the STAR aligner)
  and add gene symbol to the DESeq2 output. I usually use EnsEMBL
  ids, because those are unique, but other scientists wanted gene symbols.
"""

import sys

gtffile = open(sys.argv[1])
gtf = dict()
for i in gtffile:
    if i.startswith("#"):
        continue
    fields = i.rstrip().split()
    if fields[2] == 'gene':
        ensembl = fields[9].replace('"','')[:-1]
        genesymbol = fields[13].replace('"','')[:-1]
        gtf[ensembl] = genesymbol
gtffile.close()

inp = open(sys.argv[2])
print("genesymbol\tensemblid\t" + inp.readline().rstrip())
for i in inp:
    fields = i.rstrip().split("\t")
    if fields[0] in gtf:
        print(gtf[fields[0]] + "\t" + i.rstrip())
    else:
        print("NA\t" + i.rstrip())
