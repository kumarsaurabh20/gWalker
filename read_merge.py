#!/usr/bin/env python2
"""
Usage:: reads_merge.py -r <reference sequence> -f <reads file>
The script merges all the reads in reads file to the reference sequence.
"""
from __future__ import (print_function, division)
from Bio import SeqIO
import sys, os, getopt

__author__ = 'Kumar'

reference = ''
reads = ''

try:
	myopts, args = getopt.getopt(sys.argv[1:],"r:f:")
	for o, a in myopts:
		if o == '-r':
			reference = str(a)
		elif o == '-f':
			reads = str(a)
			
except getopt.GetoptError as e:
	print(str(e))
	print("Usage:: %s -r <reference sequence> -f <reads file>" %sys.argv[0])
	sys.exit(2)
#
try:
	records = list(SeqIO.parse(reads, "fasta"))
	for i in range(len(records)):
		SeqIO.write(records[i], "record_%d.fasta"%(i), "fasta")
		if i == 0:
			ref = "%s"% (reference)
			input2 = "record_%d.fasta" % (i)
			merger = "record_%d.merger" % (i)
			out = "record_%d.seq" % (i) 
			cmd="merge -asequence %s -bsequence %s -outfile %s -outseq %s" % (ref,input2,merger,out)
			os.system(cmd)
			cmd="tr 'a-z' 'A-Z' < %s > record_%d.fasta"% (out,i)
			os.system(cmd)
		else:
			j = i - 1
			ref = "record_%d.fasta"% (j)
                        input2 = "record_%d.fasta" % (i)
                        merger = "record_%d.merger" % (i)
                        out = "record_%d.seq" % (i)
                        cmd="merge -asequence %s -bsequence %s -outfile %s -outseq %s" % (ref,input2,merger,out)
                        os.system(cmd)
                        cmd="tr 'a-z' 'A-Z' < %s > record_%d.fasta"% (out,i)
                        os.system(cmd)
except IOError:
	print("Oops..you missed something. Try again!!")
	print("Usage:: python read_merge.py -r <reference sequence> -f <reads file>")
	sys.exit(2)
