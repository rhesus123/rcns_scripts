#!/usr/bin/python3

import pysam
import sys

def calcMismatch(read, reference):
    mismatch = 0
    ab = read.get_aligned_pairs()
    for i in ab:
        if i is None:
            continue
        if i[0] is None and i[1] is None:
            query_base = read.query_sequence[i[0]]
            ref_base = reference[i[1]]
            if query_base != ref_base:
                mismatch += 1
    return(mismatch)

def calcIndel(read, reference):
    ct = read.cigartuples
    indelcount = 0
    for i in ct:
        if i[0] == 1 or i[0] == 2:
            indelcount += i[1]
    return(indelcount)

align = pysam.AlignmentFile(sys.argv[1], "rb")
reads = align.fetch(until_eof = True)

# Read reference sequence for mismatch identification
reffile = open(sys.argv[2])
refseq = []
for i in reffile:
    if i.startswith(">"):
        continue
    refseq.append(i.rstrip())
reffile.close()
refseq = "".join(refseq)

# Print header
print("mapped\talignment_len\tmismatchnum\tindelnum\tread_len")

# Parsing reads
for i in reads:
    output = []
    #alignment_len = i.reference_end - i.reference_start
    if i.is_unmapped:
        mapped = "0"
        mismatchnum = 0
        indelnum = 0
    else:
        mapped = "1"
        mismatchnum = calcMismatch(i, refseq)
        indelnum = calcIndel(i, refseq)

    output.append(i.query_name)
    output.append(mapped)
    #output.append(str(alignment_len))
    output.append(str(i.query_alignment_length))
    output.append(str(mismatchnum))
    output.append(str(indelnum))
    output.append(str(i.query_length))

    print("\t".join(output))
