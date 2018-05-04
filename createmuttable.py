#!/usr/bin/python3

import sys

individual = dict()
for i in open(sys.argv[1]):
    fields = i.rstrip().split()
    cancerdb = fields[3] + "." + fields[4]
    if cancerdb not in individual:
        individual[cancerdb] = dict()
    if not fields[2].startswith("TCGA"):
        continue
    individual[cancerdb][fields[0]] = "-".join(fields[2].split("-")[0:4])

genes = dict()
for i in open(sys.argv[2]):
    fields = i.rstrip().split("\t")
    genes[fields[0]] = fields[1]

for cancerdb in individual:
    for mut in ["3", "6", "9", "10", "12", "14", "18", "26", "27"]: # mutation types
        mutfile = open(sys.argv[3])
        table   = dict()
        samples = set()
        for i in mutfile:
            fields = i.rstrip().split("\t")
            gene   = genes[fields[1]]
            indi   = fields[2]
            if fields[3] != mut:
                continue
            if indi in individual[cancerdb]:
                indi = individual[cancerdb][indi]
                samples.add(indi)
                if gene not in table:
                    table[gene] = set()
                table[gene].add(indi)
        mutfile.close()

        outfile = open("mut." + cancerdb + "." + mut + ".tsv", "w")
        samples = ["genes"] + list(samples)
        outfile.write("\t".join(samples) + "\n")
        for gene in table:
            out = list()
            out.append(gene)
            for s in samples:
                if s in table[gene]:
                    out.append("1")
                else:
                    out.append("0")
            outfile.write("\t".join(out) + "\n")
        outfile.close()
