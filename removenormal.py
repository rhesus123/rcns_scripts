#!/usr/bin/python3

import sys
import os

for i in open(sys.argv[1]):
    fields = i.rstrip().split("\t")
    tcgaid = fields[1]
    sample = int(tcgaid.split("-")[3][:-1])
    if sample < 9:
        print(fields[0])
