#!/usr/bin/python3

"""
   Read Cosmis Census (https://cancer.sanger.ac.uk/cosmic/census?tier=1) list
   and NCBI's gene2pubmed (ftp://ftp.ncbi.nlm.nih.gov/gene/DATA/) 
   table and create a list a gene how many times cited in publications
"""

import sys

censusfile = open(sys.argv[1])
censusfile.readline()
census = dict()
for i in censusfile:
    fields = i.rstrip().split("\t")
    symbol = fields[0]
    entrez = fields[2]
    census[entrez] = symbol

gene2pub = open(sys.argv[2])
gene2pub.readline()
hist = dict()
for i in gene2pub:
    fields = i.rstrip().split("\t")
    if fields[1] in census:
        if fields[1] not in hist:
            hist[fields[1]] = 0
        hist[fields[1]] += 1

for h in hist:
    print("%s\t%d" % (census[h], hist[h]))
