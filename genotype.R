library(DESeq2)
library(BiocParallel)
library(RMySQL)

argv       <- commandArgs(trailing = T)
genes      <- argv[1]
muttype    <- argv[2]
cancerid   <- argv[3]
pvalue     <- argv[4]
foldchange <- argv[5]
genetable  <- argv[6]
plotnum    <- argv[7]
cpunum     <- argv[8]
filtergene <- argv[9]
filterout  <- argv[10]

if(is.na(filtergene)){
	# No filter
	query.samples <- paste("select distinct(name) as samples from individual where cancer_cancerid = ",cancerid,";", sep = "")
} else {
	if(filterout == "include"){
		query.samples <- paste("select distinct(name) as samples from individual inner join (mutation,genetable) on (individual_patientid = patientid and genetable_geneid = geneid) where cancer_cancerid = ",cancerid," and genename = '",filtergene,"';",sep="")
	} else {
		query.samples <- paste("select distinct(name) as samples from individual
						where cancer_cancerid = ",cancerid," and 
						name not in (
							     select distinct(name) from individual
							     	inner join (mutation,genetable) on (individual_patientid = patientid and genetable_geneid = geneid) 
							     where cancer_cancerid = ",cancerid," and
							     genename = '",filtergene,"'
							     );",sep="")
	}
}

# Register multicore
register(MulticoreParam(cpunum))

# MySQL connection
con  <- dbConnect(MySQL(), user="XXXX", password="XXXX", dbname="mutarget", host="localhost")

# Expression matrix
query <- paste("select submitid,genename,value from expression inner join genetable on genetable_geneid = geneid inner join individual on individual_patientid = patientid where individual_cancerid = ",cancerid,";",sep="")
rs    <- dbSendQuery(con, query)
raw   <- fetch(rs, n=-1)
count <- xtabs(value~genename+submitid, data = raw)
count <- as.data.frame.matrix(count)
count <- as.matrix(count)

# Column data
coldata <- data.frame(gene = factor(rep("WT", ncol(count)), levels = c("WT","Mut")))
rownames(coldata) <- colnames(count)

# Filtering samples
rs      <- dbSendQuery(con, query.samples)
raw     <- fetch(rs, n=-1)
index   <- grep(paste(raw$samples, collapse="|"), rownames(coldata))
coldata <- coldata[index,,drop=F]
count   <- count[,index]

# Get mutant samples for coldata
genes <- strsplit(genes, ",")
genes <- paste("genename = '",gsub(",","' or genename = '",genes),"'",sep="")
query <- paste("select distinct(name) as samples from individual inner join (mutation,genetable,muteffect) on (individual_patientid = patientid and genetable_geneid = geneid and muteffect_effectid = effectid) where cancer_cancerid = ",cancerid," and (",genes,") and effectname = '",muttype,"';",sep="")
rs    <- dbSendQuery(con, query)
raw   <- fetch(rs, n=-1)
index <- grep(paste(raw$samples, collapse="|"), rownames(coldata))
coldata$gene[index] <- "Mut"

# Differential expression
des <- DESeqDataSetFromMatrix(count, colData = coldata, design =~gene)
des <- DESeq(des, parallel = T)
des <- results(des, contrast = c("gene", "Mut", "WT"), parallel = T)
des <- des[!is.na(des$padj) & des$padj < pvalue & abs(des$log2FoldChange) > foldchange,]

write.table(des, "expresults.tsv", quote = F, sep = "\t")
