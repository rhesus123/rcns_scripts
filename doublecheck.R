suppressMessages(library(DESeq2))
suppressMessages(library(pheatmap))
suppressMessages(library(repr))
suppressMessages(library(BiocParallel))
suppressMessages(library(clusterProfiler))
suppressMessages(library(org.Hs.eg.db))

register(MulticoreParam(4))

count <- as.matrix(read.table("../tables/allcounts.tsv", sep = "\t", check.names = F))
coldata <- read.table("../tables/allcoldata.tsv", sep = "\t", check.names = F)
count <- count[,rownames(coldata)]

mcol <- coldata[coldata$primary == "MELANOMA",]
mcol$class <- droplevels(mcol$class)
mcount <- count[,rownames(mcol)]
mdes <- DESeqDataSetFromMatrix(countData = mcount, colData = mcol, design =~class)
mdes <- mdes[rowSums(counts(mdes)) > 1,]
mdes <- DESeq(mdes, parallel = T)
mres <- results(mdes, contrast = c("class", "metastatic", "primary"), parallel = T)
mres.new <- mres[!is.na(mres$padj) & mres$padj < 0.001,]

count <- as.matrix(read.table("../tables/allcounts.tsv.bak", sep = "\t", check.names = F))
coldata <- read.table("../tables/allcoldata.tsv.bak", sep = "\t", check.names = F)
count <- count[,rownames(coldata)]

mcol <- coldata[coldata$primary == "MELANOMA",]
mcol$class <- droplevels(mcol$class)
mcount <- count[,rownames(mcol)]
mdes <- DESeqDataSetFromMatrix(countData = mcount, colData = mcol, design =~class)
mdes <- mdes[rowSums(counts(mdes)) > 1,]
mdes <- DESeq(mdes, parallel = T)
mres <- results(mdes, contrast = c("class", "metastatic", "primary"), parallel = T)
mres.old <- mres[!is.na(mres$padj) & mres$padj < 0.001,]
