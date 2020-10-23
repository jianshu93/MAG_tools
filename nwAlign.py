#!/usr/loca/env python3

import sys
match = 1
mismatch = -1
gap = -1 

def make_matrix(num_n, num_m):
	### Create an n*m matrix filled with zeros
	return [[0]*num_n for i in range(num_m)]

def match_score(alpha, beta):
	if alpha == beta:
		return match
	else:
		return mismatch

def print_matrix(matrix):
	for i in range(len(matrix)):
		s=''
		for j in range(len(matrix[i])):
			s = s + str(matrix[i][j]) + " "
		print(s)

def needleman_wunsch(seq_a, seq_b):
	m, n = len(seq_a), len(seq_b)
	# Generate DP table and traceback path pointer matrix
	score = make_matrix(m+1, n+1)
	pointer = make_matrix(m+1, n+1)
	# Intializing DP table
	for i in range(0, n + 1):
		score[i][0] = gap * i
	for j in range(0, m + 1):
		score[0][j] = gap * j
	### filling the matrix according to maximizing rule and remember where the max value come from
	for j in range(1, m + 1):
		for i in range(1, n + 1):
			score[i][j] = max(score[i - 1][j - 1] + match_score(seq_a[j-1], seq_b[i-1]), 
				score[i - 1][j] + gap, 
				score[i][j - 1] + gap)
			
			if score[i][j] == score[i - 1][j] + gap:
				pointer[i][j] = "U"
			if score[i][j] == score[i][j-1] + gap:
				pointer[i][j] = "L"
			if score[i][j] == score[i - 1][j - 1] + match_score(seq_a[j-1], seq_b[i-1]):
				pointer[i][j] = "D"
	#### trace back according to point table
	score_final = score[m][n]
	align_seq_a, align_seq_b = '', ''
	i,j = m,n 
	while i > 0 and j > 0: 
		label_current = pointer[i][j]
		if label_current == "D":
			align_seq_a += seq_a[j-1]
			align_seq_b += seq_b[i-1]
			i -= 1
			j -= 1
		elif label_current == "L":
			align_seq_a += seq_a[j-1]
			align_seq_b += '-'
			j -= 1
		elif label_current == "U":
			align_seq_a += '-'
			align_seq_b += seq_b[i-1]
			i -= 1

	###### for those score j=0
	while i > 0:
		align_seq_b += seq_b[i-1]
		align_seq_a += '-'
		i -= 1
	###### for those score i=0
	while j > 0:
		align_seq_b += '-'
		align_seq_a += seq_a[j-1]
		j -= 1
	align_seq_a_1 = align_seq_a[::-1]
	align_seq_b_1 = align_seq_b[::-1]
	return score, pointer, score_final, align_seq_a_1, align_seq_b_1

def main():

	file1=str(sys.argv[1])
	file2=str(sys.argv[2])
	with open(file1, 'r') as f1:
		for line in f1:
			line = line.strip()
			if not line.startswith('>'):
				seq_a = line.strip()

	with open(file2, 'r') as f2:
		for line in f2:
			line = line.strip()
			if not line.startswith('>'):
				seq_b = line.strip()

	score, pointer, score_final, align_seq_a, align_seq_b = needleman_wunsch(seq_a,seq_b)
	print_matrix(score)
	print("Final score is: " + str(score_final))
	print("The original sequence is: ")
	print(seq_a)
	print(seq_b)
	print("The aligned sequence is: ")
	print(align_seq_a)
	s=''
	for i in range(0,len(align_seq_a)):
		if align_seq_a[i] == align_seq_b[i]:
			s = s + "|"
		elif align_seq_a[i] == "-" or align_seq_b[i] == "-":
			s = s + " "
		else:
			s = s + "*"
	print(s)
	print(align_seq_b)

if __name__ == "__main__":
	main()

