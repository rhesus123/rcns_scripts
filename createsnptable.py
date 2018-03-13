#!/usr/bin/python3

"""
  Create genotype matrix using VCF files from TCGA
  It is made for proper eQTL analysis, where genotype can be 0 1 2
"""

import sys
import gzip
import glob

def addtotable(table, vcfname, chrx, pos, alt, gtype):
    if len(alt) == 1:
        tkey = "%s:%s:%s" % (chrx, pos, alt)
        if tkey not in table:
            table[tkey] = dict()
        table[tkey][vcfname] = gtype

fil2pat = dict()

metainfo = open(sys.argv[1])
for i in metainfo:
    fields   = i.rstrip().split("\t")
    filename = fields[0]
    patient  = fields[1]
    fil2pat[filename] = patient

table = dict()
allnames = list()
for i in glob.glob(sys.argv[2] + "/*.gz"):
    vcfname = i.split("/")[-1]
    if vcfname not in fil2pat:
        continue
    allnames.append(vcfname)
    gz = gzip.open(i)
    for line in gz:
        if line.startswith("#"):
            if "varscan2" in line or "muse" in line or "somaticsniper" in line:
                allnames.pop()
                break
            continue
        fields = line.rstrip().split("\t")
        chrx   = fields[0]
        pos    = fields[1]
        refal  = fields[3]
        if len(refal) != 1:
            continue
        alts   = fields[4].split(",")
        gtypes = fields[10].split(":")[0].split("/")
        ref    = gtypes[0]

        if len(alts) != len(gtypes) - 1:
            alt = alts[int(gtypes[1])-1]
            gtype = "1"
            addtotable(table, vcfname, chrx, pos, alt, gtype)
        else:
            for index in range(len(alts)):
                alt = alts[index]
                gtype = gtypes[index+1]
                if gtype == "0":
                    continue
                if ref == gtype:
                    gtype = "2"
                else:
                    gtype = "1"
                addtotable(table, vcfname, chrx, pos, alt, gtype)
    gz.close()

print("\t".join(allnames))
for tkey in table:
    out = list()
    out.append(tkey)
    for vcfname in allnames:
        if vcfname in table[tkey]:
            out.append(table[tkey][vcfname])
        else:
            out.append("0")
    print("\t".join(out))
