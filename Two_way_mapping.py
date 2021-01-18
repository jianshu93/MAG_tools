#!/usr/bin/env python


##### for extract mapping annotation from diamond output (query name and subject name) acoording to a column of 
##### gene/contig name predicted from prdigal, second column may be the abundance of each gene
#### usage: python Twq_way_mapping.py gene_name_abundance.txt annotation.txt > new.txt


import sys
file1=str(sys.argv[1])
file2=str(sys.argv[2])

## read gene RPKM file, first column gene name (k127_21231242_1, from prodigal output), Second column RPKM vales
m=0
rows=""
dict1 = {}
with open(file1, "r") as f:
	for line in f:
		line = line.strip()
		rows = line.split("\t")
		dict1[rows[0]] = rows[1]
		m=m+1
##print(m)
### read gene annotation file, first colulm gene name(k127_21231242_1, from prodigal output), second column entry for Swiss-Prot reference sequence ‘sp|Q89XJ6|NOSZ_BRADU’(uniprot_sprot.data)
n=0
rows1=""
dict2 = {}
with open(file2, "r") as f:
	for line in f:
		line = line.strip()
		rows1 = line.split("\t")
		dict2[rows1[0]] = rows1[1]
		n=n+1
## print(n)

dict3={}

for key in dict2:
	if key in dict1:
		dict3[key] = [dict2[key],dict1[key]]
	
for j in dict3:
	print(f"{str(dict3[j][0])}\t{str(dict3[j][1])}")
