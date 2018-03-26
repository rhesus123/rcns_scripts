library("MatrixEQTL", lib.loc="/home/other/tnagy/R/x86_64-redhat-linux-gnu-library/3.3")

snps <- SlicedData$new()
snps$fileDelimiter <- "\t"
snps$fileSkipRows <- 1
snps$fileSkipColumns <- 1
snps$fileSliceSize <- 4000
snps$LoadFile("snv.allcancer.tsv")

exp <- SlicedData$new()
exp$fileDelimiter <- "\t"
exp$fileSkipRows <- 1
exp$fileSkipColumns <- 1
exp$fileSliceSize <- 4000
exp$LoadFile("rnaseq.norm.tsv")

cvrt <- SlicedData$new()
cvrt$fileDelimiter <- "\t"
cvrt$fileOmitCharacters <- "NA"
cvrt$fileSkipRows <- 1
cvrt$fileSkipColumns <- 1
cvrt$LoadFile("covariates.tsv")

snpspos <- read.table("snv.location.tsv", header = T, stringsAsFactors = F)
genepos <- read.table("genes.location.tsv", header = T, stringsAsFactors = F)

eqtl <- Matrix_eQTL_main(snps = snps, cvrt = cvrt, min.pv.by.genesnp = F, noFDRsaveMemory = F, gene = exp, output_file_name = "result", pvOutputThreshold = 1e-2, useModel = modelLINEAR, errorCovariance = numeric(), verbose = T, pvalue.hist = T, snpspos = snpspos, genepos = genepos, cisDist = 1e6)

save.image("session.RData")
