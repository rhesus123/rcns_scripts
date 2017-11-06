# Script for mutarget target analysis

suppressMessages(library(edgeR))
suppressMessages(library(RMySQL))

# Command line arguments
argv         <- commandArgs(trailing = T)
tmpprefix    <- argv[1]
cancerid     <- argv[2]
effect       <- argv[3]
testgene     <- argv[4]
qvalcutoff   <- as.numeric(argv[5])
foldchcutoff <- as.numeric(argv[6])
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
print("MESSAGE: Exp matrix")

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
print("MESSAGE: Sample filtering")

# Normalise raw counts
edge <- DGEList(counts = count, group = coldata$gene)
edge <- calcNormFactors(edge)
exp  <- cpm(edge)
proc.time()
print("MESSAGE: Normalisation")

# Select the gene of interest
winp <- data.frame(exp = exp[testgene,], mutant = 0)

# Get all the genes
maxcount <- nrow(coldata) # maximum number of mutation should be less than all the samples (prevent one group syndrome)
mincount <- trunc(nrow(coldata) * mutprev / 100) # minimum number of mutation calculated from mutation prevalence
query.g <- paste("select genename from (select genename,count(name) as patientcount from genetable inner join mutation on geneid = genetable_geneid inner join muteffect on muteffect_effectid = effectid inner join individual on individual_patientid = patientid where effectid = '",effect,"' and individual_cancerid = ",cancerid," group by genename order by genename) as counttable where patientcount > ",mincount," and patientcount < ",maxcount, sep="")
query <- paste("select name,genename from mutation inner join (muteffect,cancer,genetable,individual as a) on (muteffect_effectid = effectid and mutation.individual_cancerid = cancerid and genetable_geneid = geneid and patientid = individual_patientid) where cancerid = 4 and effectid = 12 and genename in (",query.g,");",sep="")
rs <- dbSendQuery(con, query)
mutmatrix <- fetch(rs, n=-1)
mutmatrix <- as.data.frame.matrix(table(mutmatrix$genename, mutmatrix$name))

result_table <- data.frame(foldchange = rep(0, nrow(mutmatrix)), pvalue = rep(1,nrow(mutmatrix)), adj.pval = rep(1,nrow(mutmatrix)))
rownames(result_table) <- rownames(mutmatrix)

# Iterate through genes and calculate Wilcox-test
proc.time()
print("MESSAGE: Start iteration")
for(i in 1:nrow(mutmatrix)){
	winp$mutant <- 0
	samples <- colnames(mutmatrix)[mutmatrix[i,] > 0]
	index <- grep(paste(samples, collapse="|"), rownames(winp))
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
print("MESSAGE: End iteration")

# Multiple test correction
result_table$adj.pval <- p.adjust(result_table$pvalue, "BH")

#Filtering and producing pictures
result_table <- result_table[result_table$adj.pval < qvalcutoff & result_table$foldchange > foldchcutoff,]

write.table(result_table, paste(tmpprefix, "res.tsv",sep="."), quote=F, sep ="\t")
