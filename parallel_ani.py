### parallel ani using mummer 4. Jianshu Zhao

import os
import multiprocessing as mp
import sys
import re
import argparse
from shutil import which
import subprocess

def dnadiff(list):
	output = list[2]
	file1 = list[0]
	file2 = list[1]
	command = 'dnadiff ' + '-p ' + output + ' ' + file1 + ' ' + file2 + ' ' + '2>1'
	subprocess.call(command, shell = True)
	return output

def add_distance(distances, cluster_1, cluster_2, distance):
	# If this is the first time we've seen this pair, then we just add it to the dictionary.
	if (cluster_1, cluster_2) not in distances:
		distances[(cluster_1, cluster_2)] = distance
	# If we've seen this pair before (the other way around), then we make sure the distances are
	# close (sanity check) and then save the mean distance.
	else:
		assert abs(distance - distances[(cluster_1, cluster_2)]) < 0.1
		distances[(cluster_1, cluster_2)] = (distances[(cluster_1, cluster_2)] + distance) / 2.0



def main():
	#### parse arguments
	parser = argparse.ArgumentParser(description='parallel average nucleutide identity')
	parser.add_argument("-o","--output",required=True,help="output file path")
	parser.add_argument("-t", "--threads", nargs="?", type=int, default=1, help="number of threads")
	parser.add_argument("file", nargs="+", help="file help")

	args = parser.parse_args()
	thread_num = args.threads
	files = args.file
	output_file = args.output

	if thread_num and thread_num < 1:
		raise ValueError

	if which("dnadiff") is None:
		raise ValueError("Mummer not found! Please install it first: conda install -c bioconda mummer")
	pool = mp.Pool(processes = thread_num)
	list_input =[]
	for f in files:
		for h in files:
			list_input.append([str(f),str(h),str(f) + "_" + str(h)])
	# print(list_input)
	results = list(pool.map(dnadiff,list_input))
	pool.close()
	pool.join()

	### extract ani value from dnadiff output

	for f in results:
		ani_report = str(f) + ".report"
		tmp_output = []
		f_new = str(f).split('_')
		with open(ani_report, "r") as fh:
			line_num = 0
			for line in fh:
				line_num += 1
				line = line.strip()
				if line.startswith('AvgIdentity') and line_num <= 20:
					rows = re.split('\s+', line)
					with open(output_file + '_tmp',"a") as fw:
						fw.write(str(f_new[0]) + '\t' + str(f_new[1]) + '\t' + str(rows[1]) + '\n')

	### transform 3 column to symmetric matrix and print to file
	with open(output_file + '_tmp', 'rt') as dnadiff_output:
		clusters = set()
		distances = {}
		for line in dnadiff_output:
			parts = line.strip().split('\t')
			cluster_1 = parts[0]
			cluster_2 = parts[1]
			ani = float(parts[2])
			if cluster_1 == cluster_2:
				distance = 100
			else:
				distance = ani
			clusters.add(cluster_1)
			clusters.add(cluster_2)
			add_distance(distances, cluster_1, cluster_2, distance)
			add_distance(distances, cluster_2, cluster_1, distance)
	
	clusters = sorted(clusters)
	original_stdout = sys.stdout
	with open(output_file, 'w') as f:
		sys.stdout = f

		s='\t'
		for k in clusters:
			s = s + k + '\t'
		print(s)
		for i in clusters:
			print(i, end='')
			for j in clusters:
				print('\t', end='')
				distance = distances[(i, j)]
				print('%.2f' % distance, end='')
			print()
		sys.stdout = original_stdout

if __name__ == "__main__":
	main()

