#!/usr/bin/python3

import sys

individual = dict()
for i in open(sys.argv[1]):
    fields = i.rstrip().split()
    cancerdb = fields[3] + "." + fields[4]
    if cancerdb not in individual:
        individual[cancerdb] = dict()
    individual[cancerdb][fields[0]] = fields[2]

genes = dict()
for i in open(sys.argv[2]):
    fields = i.rstrip().split("\t")
    genes[fields[0]] = fields[1]

for cancerdb in individual:
    expfile = open(sys.argv[3])
    table = dict()
    samples = set()
    for i in expfile:
        fields = i.rstrip().split("\t")
        exp    = fields[1]
        gene   = genes[fields[2]]
        indi   = fields[3]
        if indi in individual[cancerdb]:
            indi = individual[cancerdb][indi]
            samples.add(indi)
            if gene not in table:
                table[gene] = dict()
            table[gene][indi] = exp
    expfile.close()

    outfile = open("exp." + cancerdb + ".tsv", "w")
    samples = list(samples)
    outfile.write("\t".join(samples) + "\n")
    for gene in table:
        out = list()
        out.append(gene)
        for s in samples:
            if s in table[gene]:
                out.append(table[gene][s])
            else:
                out.append("0")
        outfile.write("\t".join(out) + "\n")
    outfile.close()
