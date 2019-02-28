#!/usr/bin/python3

import sys
import gzip

#Allele|Consequence|IMPACT|SYMBOL|Gene|Feature_type|Feature|BIOTYPE|EXON|INTRON|HGVSc|HGVSp|cDNA_position|CDS_position|Protein_position|Amino_acids|Codons|Existing_variation|DISTANCE|STRAND|FLAGS|VARIANT_CLASS|SYMBOL_SOURCE|HGNC_ID|CANONICAL|TSL|APPRIS|CCDS|ENSP|SWISSPROT|TREMBL|UNIPARC|REFSEQ_MATCH|SOURCE|GIVEN_REF|USED_REF|BAM_EDIT|GENE_PHENO|SIFT|PolyPhen|DOMAINS|miRNA|HGVS_OFFSET|AF|AFR_AF|AMR_AF|EAS_AF|EUR_AF|SAS_AF|AA_AF|EA_AF|gnomAD_AF|gnomAD_AFR_AF|gnomAD_AMR_AF|gnomAD_ASJ_AF|gnomAD_EAS_AF|gnomAD_FIN_AF|gnomAD_NFE_AF|gnomAD_OTH_AF|gnomAD_SAS_AF|MAX_AF|MAX_AF_POPS|CLIN_SIG|SOMATIC|PHENO|PUBMED|MOTIF_NAME|MOTIF_POS|HIGH_INF_POS|MOTIF_SCORE_CHANGE|PHENOTYPES

def vepparser(vepannot):
    keep = False
    for annot in vepannot.split(","):
        fields = annot.split("|")
        try:
            max_af = float(fields[60])
        except ValueError:
            keep = True
            max_af = 0
        consequences = fields[1].split('&')
        impact = fields[2]
        phenotypes = fields[70]
        print(fields[64], phenotypes)
        for consequence in consequences:
            if max_af > 0.01 and (impact == 'HIGH' or consequence == 'coding_sequence_variant' or impact == 'MODERATE'):
                keep = True
    return keep

for i in gzip.open(sys.argv[1]):
    line = i.decode('utf-8').rstrip()
    if line.startswith("#"):
        #print(line)
        continue
    fields = line.split("\t")
    if fields[6] != "PASS":
        continue
    info = fields[7].split(";")
    for tag in info:
        if "=" not in tag:
            continue
        key, value = tag.split("=")
        if key == "CSQ":
            keep = vepparser(value)
            if keep:
                #print(line)
                pass
            break
