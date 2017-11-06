suppressMessages(library(RMySQL))
suppressMessages(library(edgeR))

argv       <- commandArgs(trailing = T)
tmpprefix  <- argv[1]
genes      <- argv[2]
muttype    <- argv[3]
cancerid   <- argv[4]
pvalue     <- argv[5]
foldchange <- argv[6]
genetable  <- argv[7]
plotnum    <- argv[8]
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
proc.time()
print("MESSAGE: Start")
# MySQL connection
con  <- dbConnect(MySQL(), user="XXXX", password="XXXX", dbname="mutarget", host="localhost")

# Expression matrix
query <- paste("select submitid,genename,value from exphelper where cancerid = ",cancerid,";",sep="")
rs    <- dbSendQuery(con, query)
raw   <- fetch(rs, n=-1)
count <- xtabs(value~genename+submitid, data = raw)
count <- as.data.frame.matrix(count)
count <- as.matrix(count)
proc.time()
print("MESSAGE: Expression matrix")

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
query <- paste("select distinct(name) as samples from individual inner join (mutation,genetable) on (individual_patientid = patientid and genetable_geneid = geneid) where cancer_cancerid = ",cancerid," and (",genes,") and muteffect_effectid = '",muttype,"';",sep="")
rs    <- dbSendQuery(con, query)
raw   <- fetch(rs, n=-1)
index <- grep(paste(raw$samples, collapse="|"), rownames(coldata))
coldata$gene[index] <- "Mut"
if(length(coldata[coldata$gene == "Mut",]) == 0){
	print("MESSAGE: Not enough samples with alteration to split into cohorts")
	quit(save="no")

}
proc.time()
print("MESSAGE: Get mutant samples")

# Differential expression using edgeR
edge <- DGEList(counts = count, group = coldata$gene)
keep <- rowSums(cpm(edge) > 1) > 2
edge <- edge[keep, , keep.lib.sizes=FALSE]
edge <- calcNormFactors(edge)
edge <- estimateDisp(edge)
edge <- exactTest(edge)
des  <- as.data.frame(topTags(edge, n = 32000, p.value = pvalue))
des  <- des[abs(des$logFC) > foldchange,]
proc.time()
print("MESSAGE: Differential expression")

# Filtering results
if(genetable != "all"){
	if(genetable == 'action'){
		query <- "select genename from genetable where actionable = 1;"
	} else {
		query <- "select genename from genetable where fda = 1;"
	}
	rs    <- dbSendQuery(con, query)
	raw   <- fetch(rs, n=-1)
	index <- grep(paste(raw$genename, collapse="|"), rownames(des))
	des   <- des[index,]
}

write.table(des, paste(tmpprefix, "exp.tsv", sep = "."), quote = F, sep = "\t")
proc.time()
print("MESSAGE: End of script")
