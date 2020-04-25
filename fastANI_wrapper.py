"""
Run pairwise fastANI comaprison bwetten each of the two contig files (draft genome) provided using fastANI_compare_runner() function first,
then classify each contig file according to a reference genome database.

	created by: Jianshu Zhao
	last edited: March 29, 2020 @ 12:50 PM

"""

#!/usr/bin/env python3

import os, subprocess, sys

def fastANI_compare_runner(input_directory_path,output_directory_path):
	### creat contige/geome file list in the
	inputpath = input_directory_path
	wd = input_directory_path + "/temp_directory"
	if not os.path.exists(wd):
    	os.makedirs(wd)

	with open(os.path.join(wd, "output.txt"), "w") as a:
		for path, subdirs, files in os.walk(inputpath):
			for filename in files:
				f = os.path.join(path, filename)
				a.write(str(f) + os.linesep)
	
	input_file = wd + "output.txt"

	num_lines = sum(1 for line in open(input_file))
	if ( num_lines < 1 ):
		print("There is no genome file in the input directory path, please make sure the directory you provided is not empty and contains genome fasta/fna/fa file/files")
		return False
	elif ( num_lines < 2 ):
		print("There are less than 2 genomes in the directory you provided, please do provide more than 2 genoems for compararive analysis of ANI")
		return False
	else:
		output_dir = output_directory_path + "/OUT_compare/"
		try:
			print("fastANI "+ input_file)
			os.system("fastANI --ql " + input_file + " --rL "+ input_file + " --matrix" + " -t 8 -o " + output_dir +"ANI.txt")
	
		except subprocess.CalledProcessError as err:
			print("Error running fastANI compare, check the input files or installation of fastANI package in conda environment")
			print("Error thrown: "+err.output)
			return False
	os.remove(wd)
	print("Completed running fastANI 1.3 comparison")
	return True
	os.remove(wd)

def fastANI_classify_runner(input_file_path,reference_directory_path,output_file_path):
	inputpath = input_directory_path
	inputpath_ref = reference_directory_path

	wd = input_directory_path + "/temp_directory"
	wd_ref = reference_directory_path + "/temp_directory"
	if not os.path.exists(wd):
    	os.makedirs(wd)
    if not os.path.exists(wd_ref):
    	os.makedirs(wd_ref)

	with open(os.path.join(wd, "output.txt"), "w") as a:
		for path, subdirs, files in os.walk(inputpath):
			for filename in files:
				f = os.path.join(path, filename)
				a.write(str(f) + os.linesep)
	
	with open(os.path.join(wd_ref, "output_ref.txt"), "w") as a:
		for path, subdirs, files in os.walk(inputpath_ref):
			for filename in files:
				f = os.path.join(path, filename)
				a.write(str(f) + os.linesep)

	input_file= wd + "output.txt"
	reference_file = wd_ref + "output_ref.txt"

	num_lines = sum(1 for line in open(input_file))
	if ( num_lines < 1 ):
		print("There is no genome file in the input directory path, please make sure the directory you provided is not empty and contains genome fasta/fna/fa file/files")
		return False
	else:
		output_dir = output_directory_path + "/OUT_classify/"

		try:
			print("fastANI "+ input_file)
			os.system("fastANI --ql " + input_file + " --rL "+ reference_file + " -t 8 -o " + output_dir + "classify.txt")
	
		except subprocess.CalledProcessError as err:
			print("Error running fastANI genome classification, check the input files, reference files or installation of fastANI package in conda environment")
			print("Error thrown: "+err.output)
			return False
	print("Completed running fastANI 1.3 classification")
	return True
	os.remove(wd)
	os.remove(wd_ref)

def main():
	inputpath = sys.argv[1] # input directory of files
	outputpath = sys.argv[2] # output directory path
	referpath = sys.argv[3] # 
	fastANI_compare_Run = fastANI_compare_runner(inputpath,outputpath)
	fastANI_classify_Run = fastANI_classify_runner(inputpath,referpath,outputpath)

if __name__ == "__main__":
	main()
