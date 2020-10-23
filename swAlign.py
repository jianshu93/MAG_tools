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

def smith_waterman(seq_a, seq_b):
	m, n = len(seq_a), len(seq_b)  
	
	##Initial scoring matrix
	score = make_matrix(m+1, n+1)
	pointer = make_matrix(m+1, n+1)
	# initial maximum score in DP table
	max_score = 0
	max_i = 0
	max_j = 0

	# Calculate DP table and mark pointers, pay attention to lines and columns!!!!!!!!!
	for j in range(1, m + 1):
		for i in range(1, n + 1):
			score[i][j] = max(0,score[i][j-1] + gap,
				score[i-1][j] + gap, 
				score[i-1][j-1] + match_score(seq_a[j-1], seq_b[i-1]))
			if score[i][j] == 0:
				pointer[i][j] = 0
			if score[i][j] == score[i-1][j] + gap:
				pointer[i][j] = "L"
			if score[i][j] == score[i][j-1] + gap:
				pointer[i][j] = "U"
			if score[i][j] == score[i-1][j-1] + match_score(seq_a[j-1], seq_b[i-1]):
				pointer[i][j] = "D"
			if score[i][j] >= max_score:
				max_i = i
				max_j = j
				max_score = score[i][j];
	
	align_seq_a, align_seq_b = '', ''
	i,j = max_i,max_j
	#traceback according to poiners
	while pointer[i][j] != 0:
		if pointer[i][j] == "D":
			align_seq_a += seq_a[j-1]
			align_seq_b += seq_b[i-1]
			i -= 1
			j -= 1
		elif pointer[i][j] == "U":
			align_seq_b += '-'
			align_seq_a += seq_a[j-1]
			j -= 1
		elif pointer[i][j] == "L":
			align_seq_b += seq_b[i-1]
			align_seq_a += '-'
			i -= 1
		align_seq_a_1 = align_seq_a[::-1]
		align_seq_b_1 = align_seq_b[::-1]
	return score, pointer, max_i, max_j, max_score, align_seq_a_1, align_seq_b_1

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

	score, pointer, max_i, max_j, max_score, align_seq_a, align_seq_b = smith_waterman(seq_a,seq_b)
	print_matrix(score)
	print("max score is: " + str(max_score))
	print("max score position is: " + str(max_i+1) + ", " + str(max_j+1))
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



