#!/usr/local/env python
### kmer_counter.py (v1.0) count the kmer occurences for a given fasta(multifasta)
### usage: python kmer_counter.py 6 Name.fasta
###
import sys

k=int(sys.argv[1])
file_fasta=str(sys.argv[2])

row=[]

### remove \n at end of sequence lines and concatenate them before storing it into a list
with open(file_fasta, "r") as file_input:
    block = []
    for line in file_input:
        if line.startswith('>'):
            if block:
                row.append(''.join(block) + '\n')
                block = []
            row.append(line)
        else:
            block.append(line.strip())
    if block:
        row.append(''.join(block))
print(row)
### create empty dictionary for storage of kmer and counts
counts = {}
### Go though each sequence line of fasta file and kmer counting
for i in range(1, len(row)+1,2):
	for j in range(0,len(row[i]) - k + 1):
		kmer = row[i][j:j+k]
		## check whether this kmer exist
		if kmer not in counts:
			counts[kmer] = 0
		# Increment the count for existing kmer
		counts[kmer] += 1
### print to standard output
s=""
for i in counts:
	s = s + str(i) + "\t" + str(counts[i]) + "\n"
print(s)
###write output files
with open("kmer1.txt","w") as fh:
		s=""
		for i in counts:
			s = s + str(i) + "\t" + str(counts[i]) + "\n"
		fh.write(s)
