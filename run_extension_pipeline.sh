#!/bin/bash
#
# @author  Kumar Saurabh Singh
# @update  16th June 2017
# @license GNU GPL -v 3.0
#
if [[ ! $2 || ! $3 ]] ; then
   echo "
.DESCRIPTION
   This program tries to extend the partial or misassembled
   sequence in either direction using an iterative process
   utilizing raw reads information.
.USAGE
   $0 <reads> <prefix> <gene_length> 
   reads	reads fasta file.
   prefix	prefix for the extended sequence.
   gene_length	expected gene length	
";
   exit 1;
fi

if [[ ! -r $1 ]]; then
   echo "Cannot open file: $1";
   exit 1;
fi

reads="$1"
prefix="$2"
length="$3"
i=0
ex=0
until [ $ex -gt $length ]
do
#
echo "Running iteration $i"
#
lastz "${prefix}${i}.fasta" $reads[nameparse=full] --format=general:name2 --ambiguous=iupac | sed 's/>//g' - | sed '1d' > "lastz${i}.out"
#
seqtk subseq $reads "lastz${i}.out" > "lastz${i}.fasta"
#
temp=`grep -c ">" "lastz${i}.fasta"`
#
j=$(($temp - 1))
#
python read_merge.py -r "${prefix}${i}.fasta" -f "lastz${i}.fasta" #&> /dev/null
#
rm record_0.merger record_0.seq
#
i=$(($i + 1))
#
mv "record_${j}.fasta" "$prefix${i}.fasta"
#
ex=`perl FastA.length.pl cyp${i}.fasta | cut -f2`
#
done
