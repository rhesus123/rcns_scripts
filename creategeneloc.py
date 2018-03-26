#!/usr/bin/python3

import sys

gff = open(sys.argv[1])
genes = dict()
for i in gff:
    if i.startswith("#"):
        continue
    fields = i.rstrip().split("\t")
    if fields[2] != "gene":
        continue
    chrx  = "chr" + fields[0]
    start = fields[3]
    end   = fields[4]
    gid   = fields[8].split()[1][:-1].replace('"', '')
    genes[gid] = [chrx, start, end]

newexp = open(sys.argv[3], "w")
out    = open(sys.argv[4], "w")
exp    = open(sys.argv[2])
newexp.write(exp.readline())
out.write("geneid\tchr\ts1\ts2\n")
for i in exp:
    geneid = i.rstrip().split()[0]
    key    = geneid.split(".")[0]
    if key not in genes:
        continue
    newexp.write(i)
    out.write(geneid + "\t" + "\t".join(genes[key]) + "\n")
