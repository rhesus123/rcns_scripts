#!/usr/bin/python3

"""
   Selector: A simple parser to extract some interesting genes for Excel
   Excel cannot load a 7GB XML, so I create this script to extract a subset
"""

import sys

def isSelected(record, need):
    for r in record:
        if r.strip().startswith("<name"):
            for n in need:
                genename = "<name>" + n + "</name>"
                if genename in r:
                    return True
    return False

entrymode = False
record    = list()
need      = ["BRCA1", "TP53", "NOTCH1"]

for i in open(sys.argv[1]):
    if i.startswith("<?xml") or i.startswith("<proteinAtlas") or i.startswith("</proteinAtlas"):
        print(i.rstrip())
    if i.strip().startswith("<entry"):
        entrymode = True
        record    = list()
    if entrymode:
        record.append(i)
    if i.strip().startswith("</entry"):
        if isSelected(record, need):
            print("".join(record))
        entrymode = False
