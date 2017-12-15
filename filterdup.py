#!/usr/bin/python3

"""
  Filter duplicated gene fusions
  We use the duplicated gene database
"""

import sys

genes = dict()
dgd = open(sys.argv[1])
dgd.readline()
for i in dgd:
    fields = i.rstrip().split("\t")
    if fields[7] in genes and fields[1] != genes[fields[7]]:
        print("Oh no!")
        exit(1)
    genes[fields[7]] = fields[1]

fusion = open(sys.argv[2])
print(fusion.readline().rstrip())
for i in fusion:
    fields = i.rstrip().split()
    geneA, geneB = fields[0].split("--")
    if geneA not in genes or geneB not in genes or genes[geneA] != genes[geneB]:
        print(i.rstrip())
