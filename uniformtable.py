#/usr/bin/python3

"""
   In Mutarget the SNV file contains less samples, because not all samples has both genotype and expression file
   Using this script expression matrix and SNV matrix will contain the same number of samples in the same order
"""

import sys

exp = open(sys.argv[1]).readline().rstrip().split("\t")
mutfile = open(sys.argv[2])
convert = dict()
header = mutfile.readline().rstrip().split("\t")
for i in range(len(header)):
    for j in range(len(exp)):
        if header[i] in exp[j]:
            convert[j] = i
            break

print("\t".join(exp))
for i in mutfile:
    fields = i.rstrip().split("\t")
    out = ["0"] * len(exp)
    for j in convert:
        out[j] = fields[convert[j]]
    print("\t".join(out))
