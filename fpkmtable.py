#!/usr/bin/python3

import json
import gzip
import sys

def store(matrix, filename):
    f = gzip.open("fpkm/" + filename)
    for i in f:
        gene,value = i.decode("utf-8").rstrip().split()
        gene = gene.split(".")[0]
        if gene not in matrix:
            matrix[gene] = dict()
        matrix[gene][filename] = str(round(float(value),2))
    f.close()

def printmatrix(outname, matrix, genehash, samplehash):
    out = open(outname, "w")
    outline = list()
    header = list(samplehash.keys())

    outline.append("genes")
    for h in header:
        outline.append(samplehash[h])
    out.write("\t".join(outline) + "\n")

    for ensid in matrix:
        outline = list()
        if ensid not in genehash:
            continue
        outline.append(genehash[ensid])
        for sample in header:
            outline.append(matrix[ensid][sample])
        out.write("\t".join(outline) + "\n")
    out.close()

genehash = dict()
for i in open(sys.argv[1]):
    fields = i.rstrip().split("\t")
    genehash[fields[0]] = fields[1]

jfile = open(sys.argv[2]).read()
jdata = json.loads(jfile)

samplehash1  = dict()
samplehash2  = dict()
fpkmmatrix   = dict()
fpkmuqmatrix = dict()

for record in jdata:
    fn = record["file_name"]
    submitterid = record["associated_entities"][0]["entity_submitter_id"]

    if fn.endswith("FPKM.txt.gz"):
        samplehash1[fn] = submitterid
        store(fpkmmatrix, fn)
    else:
        samplehash2[fn] = submitterid
        store(fpkmuqmatrix, fn)

printmatrix("fpkm.tsv", fpkmmatrix, genehash, samplehash1)
printmatrix("fpkmuq.tsv", fpkmuqmatrix, genehash, samplehash2)
