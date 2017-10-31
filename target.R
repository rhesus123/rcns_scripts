# Script for mutarget target analysis

suppressMessages(library(DESeq2))
suppressMessages(library(RMySQL))

# Command line arguments
argv         <- commandArgs(trailing = T)
cancerid     <- argv[1]
effect       <- argv[2]
testgene     <- argv[3]
tmpprefix    <- argv[4]
qvalcutoff   <- argv[5]
foldchcutoff <- argv[6]
mutprev      <- as.numeric(argv[7])
filtergene   <- argv[8]
filterout    <- argv[9]
print(getwd())
proc.time()
print("Start")
# MySQL connection
con  <- dbConnect(MySQL(), user="XXXX", password="XXXX", dbname="mutarget", host="localhost")

# Expression matrix
query.exp <- paste("select submitid,genename,value from exphelper where cancerid = ",cancerid,";",sep="")
rs    <- dbSendQuery(con, query.exp)
raw   <- fetch(rs, n=-1)
count <- xtabs(value~genename+submitid, data = raw)
count <- as.data.frame.matrix(count)
count <- as.matrix(count)
proc.time()
print("Exp matrix")

# Column data
coldata <- data.frame(gene = rep("WT", ncol(count)))
rownames(coldata) <- colnames(count)

# Sample filtering TODO Maybe it is worth to put it into the query.exp?
if(!is.na(filtergene)){
	if(filterout == 'include'){
		query <- paste("select distinct(name) as samples from individual inner join (mutation,genetable) on (individual_patientid = patientid and genetable_geneid = geneid) where cancer_cancerid = ",cancerid," and genename = '",filtergene,"';",sep="")
	} else {
		query <- paste("select distinct(name) as samples from individual where cancer_cancerid = ",cancerid," and name not in ( select distinct(name) from individual inner join (mutation,genetable) on (individual_patientid = patientid and genetable_geneid = geneid) where cancer_cancerid = ",cancerid," and genename = '",filtergene,"' );",sep="")
	}
	rs      <- dbSendQuery(con, query)
	raw     <- fetch(rs, n=-1)
	index   <- grep(paste(raw$samples, collapse="|"), rownames(coldata))
	coldata <- coldata[index,,drop=F]
	count   <- count[,index]
}
proc.time()
print("Sample filtering")

# Normalise raw counts
des <- DESeqDataSetFromMatrix(count, colData = coldata, design =~1)
vsd <- vst(des)
exp <- assay(vsd)
proc.time()
print("Normalisation")

# Select the gene of interest
winp <- data.frame(exp = exp[testgene,], mutant = 0)

# Get all the genes
maxcount <- nrow(coldata) # maximum number of mutation should be less than all the samples (prevent one group syndrome)
mincount <- trunc(nrow(coldata) * mutprev / 100) # minimum number of mutation calculated from mutation prevalence
query <- paste("select * from (select genename,count(name) as patientcount from genetable inner join mutation on geneid = genetable_geneid inner join muteffect on muteffect_effectid = effectid inner join individual on individual_patientid = patientid where effectname = '",effect,"' and individual_cancerid = ",cancerid," group by genename order by genename) as counttable where patientcount > ",mincount," and patientcount < ",maxcount,";", sep="")
rs <- dbSendQuery(con, query)
genes <- fetch(rs, n=-1)
proc.time()
print("Get all genes")

result_table <- data.frame(foldchange = rep(0, nrow(genes)), pvalue = rep(1,nrow(genes)), adj.pval = rep(1,nrow(genes)))
rownames(result_table) <- genes$genename
# Iterate through genes and calculate Wilcox-test
proc.time()
print("Start iteration")
for(i in 1:nrow(genes)){
	winp$mutant <- 0
	gene  <- genes[i,1] # automatic coercion into vector
	query <- paste("select name from mutation inner join (muteffect,cancer,genetable,individual as a) on (muteffect_effectid = effectid and mutation.individual_cancerid = cancerid and genetable_geneid = geneid and patientid = individual_patientid) where cancerid = ",cancerid," and effectname = '",effect,"' and genename = '",gene,"';", sep="")
	rs <- dbSendQuery(con, query)
	samples <- fetch(rs, n=-1)
	index <- grep(paste(samples$name, collapse="|"), rownames(winp))
	winp[index,]$mutant <- 1
	# Check how many samples we have
	s <- sum(winp$mutant)
	if(s == nrow(winp) || s == 0){ # if there is no two groups
		print(paste(gene, "will cause problem"))
		next
	}
	testres <- wilcox.test(exp~mutant, data = winp)
	result_table[i,]$pvalue <- testres$p.value

	#The original script use the ratio of the medians
	expmu <- median(winp[winp$mutant == 1,1])
	expwt <- median(winp[winp$mutant == 0,1])
	result_table[i,]$foldchange <- max(expmu, expwt) / min(expmu, expwt)
}
proc.time()
print("End iteration")

# Multiple test correction
result_table$adj.pval <- p.adjust(result_table$pvalue, "BH")

#Filtering and producing pictures
result_table <- result_table[result_table$adj.pval < qvalcutoff & result_table$foldchange > foldchcutoff,]

write.table(result_table, "result.tsv", quote=F, sep ="\t")
