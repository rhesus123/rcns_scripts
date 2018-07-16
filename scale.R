
for(i in list.files(pattern = "exp.+tsv")){
	data <- read.table(i, header = T, check.names = F, sep = "\t")
	keep <- grep("-", data[,1], invert = T)
	data <- data[keep,]
	for(col in 2:ncol(data)){
		data[, col] <- floor(data[, col] / mean(data[, col]) * 1000)
	}
	data <- data[rowSums(data[,2:ncol(data)]) > 50,]
	write.table(data, paste("../scaled/", i, sep = ""), quote = F, sep = "\t", row.names = F)
	cat(i,sep="\n")
}
