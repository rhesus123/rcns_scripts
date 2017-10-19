#!/usr/bin/python3

"""
   Check EnsID/Gene symbol from two different tables
"""

import sys

frommart = dict()
for i in open(sys.argv[1]):
    fields = i.rstrip().split("\t")
    frommart[fields[0]] = fields[1]

for i in open(sys.argv[2]):
    fields = i.rstrip().split("\t")
    if len(fields) < 4:
        continue
    ensid  = fields[3]
    symbol = fields[2]
    if ensid not in frommart:
        print("Ivalid EnsID:", ensid)
        continue
    if frommart[ensid] != symbol:
        print(ensid, symbol, frommart[ensid], sep = "\t")
