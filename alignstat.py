#!/usr/bin/python3

import pysam
import sys

def calcMismatch(read, reference):
    ab = read.get_aligned_pairs()
    for i in ab:
        print(i)

def calcIndel(read, reference):
    ct = read.cigartuples
    indelcount = 0
    for i in ct:
        if i[0] == 1 or i[0] == 2:
            indelcount += i[1]
    return(indelcount)

align = pysam.AlignmentFile(sys.argv[1], "rb")
reads = align.fetch()

# Read reference sequence for mismatch identification
reffile = open(sys.argv[2])
refseq = []
for i in reffile:
    if i.startswith(">"):
        continue
    refseq.append(i.rstrip())
reffile.close()
refseq = "".join(refseq)

# Parsing reads
for i in reads:
    output = []
    alignment_len = i.reference_end - i.reference_start
    if i.is_unmapped:
        mapped = "0"
    else:
        mapped = "1"
    mismatchnum = calcMismatch(i, reference)
    indelnum = calcIndel(i, reference)

    output.append(i.query_name)
    output.append(mapped)
    output.append(str(alignment_len))
    output.append(str(i.query_alignment_length))
    output.append(str(i.query_length))
    output.append(i.cigarstring)

    print("\t".join(output))
