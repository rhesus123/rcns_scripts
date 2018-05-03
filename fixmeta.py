#!/usr/bin/python3

"""
   There is a problem with the metatable generation.
   The new JSON files from TCGA do not contain old tags, so
   my old script (metaread.py) not working. I use it to fix
   this behaviour
"""

import sys

cancer = dict()
for i in open(sys.argv[1]):
    fields = i.rstrip().split("\t")
    cancer[fields[3]] = [fields[2], fields[1]]

for i in open(sys.argv[2]):
    fields = i.rstrip().split("\t")
    fields[3] = cancer[fields[2]][0]
    fields[4] = cancer[fields[2]][1]
    print("\t".join(fields))
