#!/usr/bin/python2

import sys
import os

from Bio import SeqIO

#Daniel Elsner
# Check if sequence starts with the start codon ATG


with open(sys.argv[1], "r") as fileA:
    fcontent = list(SeqIO.parse(fileA, "fasta"))
    fileA.close()



count = 0

for i in range(len(fcontent)):
    if str(fcontent[i].seq[:3].strip()) == "ATG" or str(fcontent[i].seq[:3].strip()) == "atg":
        #sys.exit("ATG-Error in " + os.path.realpath(sys.argv[1]) + ": Sequence is missing start codon!")
        count +=1



if count == 6:
    print os.path.realpath(sys.argv[1]) + "ATG-ok"
else:
    print os.path.realpath(sys.argv[1]) + "ATG-ERROR"

