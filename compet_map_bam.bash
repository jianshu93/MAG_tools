#!/bin/bash
### Jianshu Zhao (jianshu.zhao@gatech.edu)
### competitive mapping and extracing of MAG bam file for recruitment plot.
### dependencies:
### seqtk, samtools and bowtie2， can be installed via conda

threads=$(nproc)
dir_mag=./MAG
reads1=./reads_R1.fastq.gz
reads2=./reads_R2.fastq.gz
output=./output
intleav=./interleave.fastq.gz

while getopts ":d:o:(r1):(r2):T:h" option
do
	case $option in
		d) dir_mag=$OPTARG;;
        r1) reads1=$OPTARG;;
        r2) reads2=$OPTARG;;
        i) intleav=$OPTARG;;
        o) output=$OPTARG;;
        T) threads=$OPTARG;;
        \?) echo "Invalid option: -$OPTARG" >&2
			exit 1
			;;
		:) echo "Option -$OPTARG requires an argument." >&2
		    exit 1
			;;
		h) 
           echo "usage: compet_map_bam.bash -d ./MAGs -r1 ./reads_R1.fastq.gz -r2 ./reads_R2.fastq.gz -T 12 -o ./bam_out
           
           options:
           -d directory contains MAG, can be fasta or fa or fna in the name
           -r1 forward reads to map the the MAG collection
           -r2 reverse reads to map the the MAG collection
           -o output directory to store each bam file for each MAG
           -T number of threas to use for mapping and also format tranformation"
            exit 1
           ;;
	esac
done


if [ -d "$dir_mag" ] 
then
    echo "" 
else
    echo "$dir does not exist, please offer a directory that exists"
    exit 1
fi

if test -f "$reads1"; then
    echo "$reads1 exists."
else
	echo "$reads1 does not exists."
	exit 1
fi

if test -f "$reads2"; then
    echo "$reads2 exists."
else
	echo "$reads2 does not exists."
	exit 1
fi

if test -f "$intleav"; then
    echo "$intleav exists."
else
	echo "$intleav does not exists."
    if test -f "$reads1"; then
        echo "$reads1 exists."
    else
	    echo "$reads1 does not exists."
	    exit 1
    if test -f "$reads2"; then
        echo "$reads2 exists."
    else
	    echo "$reads2 does not exists."
	    exit 1
    fi
fi

if [ -d "$output" ] 
then
    echo "Directory $output already exists. Please offer a new directory"
    exit 1
else
    echo "making directory $output ..."
    $(mkdir $output)
fi


echo "Rename MAG headers and do reads mapping"
dfiles="${dir_mag}/*.fasta"
for F in $dfiles; do
	BASE=${F##*/}
	SAMPLE=${BASE%.*}
    $(seqtk rename $F ${SAMPLE}. > ${dir_mag}/${SAMPLE}.renamed.fasta)
    $(grep -E '^>' ${dir_mag}/${SAMPLE}.renamed.fasta | sed 's/>//' | awk '{print $1}' | tr '\n' ' ' > ${dir_mag}/${SAMPLE}.rename.txt)
    $(cat ${dir_mag}/${SAMPLE}.renamed.fasta >> ${dir_mag}/all_mags_rename.fasta)
    $(rm ${dir_mag}/${SAMPLE}.renamed.fasta)
do

$(bowtie2-build ${dir_mag}/all_mags_rename.fasta ${dir_mag}/all_mags_rename)

if [[ ! -z "$intleav" ]]; then
    $(bowtie2 -x ${dir_mag}/all_mags_rename -q -1 $reads1 -2 $reads2 -S ${output}/all_mags_rename.sam --threads $threads)
else
    $(bowtie2 -x ${dir_mag}/all_mags_rename -q --interleaved $intlev -S ${output}/all_mags_rename.sam --threads $threads)
fi

$(samtools view -bS -@ $threads ${output}/all_mags_rename.sam > ${output}/all_mags_rename.bam)
$(samtools sort -@ $threads -O bam -o ${output}/all_mags_rename_sorted.bam ${output}/all_mags_rename.bam)

dfiles_rename="${dir_mag}/*.rename.txt"

for F in $dfiles_rename; do
    BASE=${F##*/}
	SAMPLE=${BASE%.*}
    $(samtools index ${output}/all_mags_rename_sorted.bam)
    $(satmools view -@ $threads -bS ${output}/all_mags_rename_sorted.bam <(cat $F) > ${output}/${SAMPLE}.sorted.bam)
    $(rm $F)
done

echo "reads mapping and extracting done"