library(DESeq2)

for(i in list.files(pattern = "exp.+tsv")){
	count <- read.table(i, check.names = F)
	fuck <- data.frame(r = rep(1,ncol(count)))
	des <- DESeqDataSetFromMatrix(countData = count, colData = fuck, design =~1)
	norm <- assay(vst(des))
	write.table(norm, file=i, quote = F)
}
