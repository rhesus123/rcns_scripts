#!/usr/bin/python3

import sys

dbsnpid = set()

for i in open(sys.argv[1]):
    fields = i.rstrip().split("\t")
    if fields[0] in dbsnpid:
        print("Duplicates!", i.rstrip())
    dbsnpid.add(fields[0])
