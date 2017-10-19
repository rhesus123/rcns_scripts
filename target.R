# Script for mutarget target analysis

library(DESeq2)
library(RMySQL)
library(BiocParallel)

# Command line arguments
argv         <- commandArgs(trailing = T)
cancerid     <- argv[1]
effect       <- argv[2]
testgene     <- argv[3]
tmpprefix    <- argv[4]
qvalcutoff   <- argv[5]
foldchcutoff <- argv[6]
filtergene   <- argv[7]
filterout    <- argv[8]

if(is.na(filtergene)){
	# Filter option not set
	print("ok")
} else {
	# Filter option set
	print("not ok")
}

# MySQL connection
con  <- dbConnect(MySQL(), user="XXX", password="XXXX", dbname="mutarget", host="localhost")

# Expression matrix
query.exp <- paste("select submitid,genename,value from expression inner join genetable on genetable_geneid = geneid inner join individual on individual_patientid = patientid where individual_cancerid = ",cancerid,";",sep="")
rs    <- dbSendQuery(con, query.exp)
raw   <- fetch(rs, n=-1)
count <- xtabs(value~genename+submitid, data = raw)
count <- as.data.frame.matrix(count)
count <- as.matrix(count)

# Column data
coldata <- data.frame(gene = rep("WT", ncol(count)))
rownames(coldata) <- colnames(count)

# Normalise raw counts
des <- DESeqDataSetFromMatrix(count, colData = coldata, design =~1)
vsd <- vst(des)
exp <- assay(vsd)

# Select the gene of interest
winp <- data.frame(exp = exp[testgene,], mutant = 0)

# Get all the genes
#TODO Maybe we need to select genes with more than one sample
query <- paste("select distinct(genename) from genetable inner join mutation on geneid = genetable_geneid inner join muteffect on muteffect_effectid = effectid where effectname = '",effect,"' and individual_cancerid = ",cancerid,";",sep="")
rs <- dbSendQuery(con, query)
genes <- fetch(rs, n=-1)

result_table <- data.frame(foldchange = rep(0, nrow(genes)), pvalue = rep(1,nrow(genes)), adj.pval = rep(1,nrow(genes)))
rownames(result_table) <- genes$genename
# Iterate through on genes and calculate Wilcox-test
for(i in 1:nrow(genes)){
	winp$mutant <- 0
	gene  <- genes[i,] # automatic coercion into vector
	query <- paste("select name from mutation inner join (muteffect,cancer,genetable,individual as a) on (muteffect_effectid = effectid and mutation.individual_cancerid = cancerid and genetable_geneid = geneid and patientid = individual_patientid) where cancerid = ",cancerid," and effectname = '",effect,"' and genename = '",gene,"';", sep="")
	rs <- dbSendQuery(con, query)
	samples <- fetch(rs, n=-1)
	index <- grep(paste(samples$name, collapse="|"), rownames(winp))
	winp[index,]$mutant <- 1
	s <- sum(winp$mutant)
	if(s == nrow(winp) || s == 0){
		next
	}
	testres <- wilcox.test(exp~mutant, data = winp)
	result_table[i,]$pvalue <- testres$p.value
	print(gene)
	#TODO Somehow put foldchange into the table
}

# Multiple test correction
result_table$adj.pval <- p.adjust(result_table$pvalue, "BH")
write.table(result_table, "result.tsv", quote=F, sep ="\t")
#Filtering and producing pictures
