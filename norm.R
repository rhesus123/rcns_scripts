library(edgeR)

for(i in list.files(pattern = "exp.+tsv")){
	count <- read.table(i, check.names = F, sep="\t", header = T)
	fuck <- data.frame(r = rep(1,ncol(count)))
	edge <- DGEList(count = count, group = fuck$r)
	norm <- cpm(edge)
	#des <- DESeqDataSetFromMatrix(countData = count, colData = fuck, design =~1)
	#norm <- assay(vst(des))
	write.table(norm, file=i, quote = F, sep = "\t")
}
