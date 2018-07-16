#!/usr/bin/python3

"""
  Read two tables and create a joint table with both values.
  If a row is missing from the tables, it contains a -
"""

import sys

class Record:
    def __init__(self):
        self.tables = list()
        self.tables.append([])
        self.tables.append([])
    def both(self):
        if len(self.tables[0]) > 0 and len(self.tables[1]) > 0:
            return True
        return False

def parse(filename, store, count):
    f = open(filename)
    f.readline() # read header
    for i in f:
        fields = i.rstrip().split("\t")
        if fields[0] not in store:
            store[fields[0]] = Record()
        store[fields[0]].tables[count] = fields[1:]
    f.close()
    return len(fields)

store = dict()
fnum1 = parse(sys.argv[1], store, 0) - 1
fnum2 = parse(sys.argv[2], store, 1) - 1

print("gene\ttcga fold change\ttcga p value\ttcga FDR\tmeta fold change\tmeta p value\tmeta FDR") #FIXME the header can be wrong if you use results from Target
for gene in store:
    if store[gene].both() == True:
        print(gene, "\t".join(store[gene].tables[0]), "\t".join(store[gene].tables[1]), sep = "\t")
for gene in store:
    if len(store[gene].tables[0]) > 0 and len(store[gene].tables[1]) == 0:
        print(gene, "\t".join(store[gene].tables[0]), "\t".join(["-"] * fnum2), sep = "\t")
for gene in store:
    if len(store[gene].tables[0]) == 0 and len(store[gene].tables[1]) > 0:
        print(gene, "\t".join(["-"] * fnum1), "\t".join(store[gene].tables[1]), sep = "\t")
