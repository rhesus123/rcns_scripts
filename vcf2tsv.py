#!/usr/bin/python3

# Usage: python3 vcf2tsv.py input.vcf.gz output.tsv
# output is a tab delimited file 0: reference 1: heterozygous 2: homozygous

import gzip
import sys

vcf = gzip.open(sys.argv[1], "r")
outfile = open(sys.argv[2], "w")

for i in vcf:
    line = i.decode("utf-8").rstrip()
    if line.startswith("#"):
        if line.startswith("#CHR"):
            outfile.write("\t".join(line.split("\t")[9:]) + "\n")
        continue
    fields = line.split("\t")
    if fields[6] != "PASS":
        continue
    key = "_".join([fields[0], fields[1], fields[3], fields[4]])
    output = [key]
    for gt in range(9,len(fields)):
        tag = fields[gt].split(":")[0]
        # I know in my case the number of genotypes cannot be larger than 6
        a = tag[0]
        b = tag[2]
        if (a == "." or a == "0") and a == b:
            output.append("0")
        elif a == b:
            output.append("2")
        else:
            output.append("1")
    outfile.write("\t".join(output) + "\n")
outfile.close()
