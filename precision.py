#!/usr/bin/python3

"""
   Round a matrix to a specific digit
"""

import sys

f = open(sys.argv[1])
print(f.readline().rstrip())

for i in f:
    fields = i.rstrip().split("\t")
    for index in range(1,len(fields)):
        fields[index] = str(round(float(fields[index]),2))
    print("\t".join(fields))
