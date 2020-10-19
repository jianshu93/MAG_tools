#!/usr/bin/env python3
### find orthology in pairwise genomes or a directory of genomes
### jianshu.zhao@gatech.edu
### usage: ./find_orthologs.py -i1 <Input file 1> -i2 <Input file 2>
### -o <Output file name> –t <Sequence type – n/p>

import sys
import os
import argparse
import subprocess

def pairwise_comparison(in1, in2):
	current_dir = os.getcwd()
	file1 = in1
	file2 = in2
	file2_db = "file2_db"
	file1_db = "file1_db"
	best_hit12 = os.path.join(current_dir, "best_hit12.txt")
	best_hit21 = os.path.join(current_dir, "best_hit21.txt")

	### make database for searching
	if seq_type == "n":
		subprocess.call('makeblastdb -in ' + file2 + ' -dbtype nucl -out ' + file2_db, shell=True)
		subprocess.call('blastn -db ' + file2_db + ' -query ' + file1 + '-max_target_seqs 1 -out ' + best_hit12 + ' -outfmt 6', shell=True)
		subprocess.call('makeblastdb -in ' + file1 + ' -dbtype nucl -out ' + file1_db, shell=True)
		subprocess.call('blastn -db ' + file1_db + ' -query ' + file2 + ' -max_target_seqs 1 -out ' + best_hit21 + ' -outfmt 6', shell=True)

	elif seq_type == "p":
		subprocess.call('makeblastdb -in ' + file2 + ' -dbtype prot -out ' + file2_db, shell=True)
		subprocess.call('blastp -db ' + file2_db + ' -query ' + file1 + '-max_target_seqs 1 -out ' + best_hit12 + ' -outfmt 6', shell=True)
		subprocess.call('makeblastdb -in ' + file1 + ' -dbtype prot -out ' + file1_db, shell=True)
		subprocess.call('blastp -db ' + file1_db + ' -query ' + file2 + ' -max_target_seqs 1 -out ' + best_hit21 + ' -outfmt 6', shell=True)
	else:
		print("not supported")

def find_rbh(blast_output1, blast_output2, output_rbh):
	file_hit1 = blast_output1
	file_hit2 = blast_output2
	outputfile = output_rbh

	table1 = []
	with open(file_hit1, 'r'):
		for line in f:
		line = line.strip()
		rows = line.split("\t")
		table1.append(rows)
	table2 = []
	with open(file_hit2, 'r'):
		for line in f:
		line = line.strip()
		rows = line.split("\t")
		table2.append(rows)

	table_new=[]
	for i in table1:
		for j in table2:
			if i[0] = j[1] and i[1] = j[0]:
				table_new.append(j)

	with open(os.path.join(current_dir,outputfile), 'w'):
		for 


def main():
	parser = argparse.ArgumentParser(description="This script find reciprocal best hits of two genome")
	parser.add_argument("-i1", "--input1", help= "This is sequence gene file 1", required=True)
	parser.add_argument("-i2", "--input2", help= "This is sequence gene file 2", required=True)
	parser.add_argument("-o", "--output", help= "output file name by default in current directory")
	parser.add_argument("-t", "--type", help= "sequence type, n or p")

	args=parser.parse_args()

	seq1 = args.input1
	seq2 = args.input2
	output = args.output
	seq_type = args.type

	pairwise_comparison(seq1, seq2)
	find_rbh(best_hit12, best_hit21, output)
if __name__ == "__main__":
    main()