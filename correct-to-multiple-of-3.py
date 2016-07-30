#!/usr/bin/python2

import sys
import errno

from Bio import SeqIO

# Daniel Elsner

# This script serves to take all sequences in a fasta and fills them up in a multiple of three. Some bioinformatics programs require this. Filling up is done with "-" as gaps.

def length_correct(in_string):
    #check if the string is divisible by three (codeml fails if that is not the case, and the only way to make it do the analysis anyway is to edit the sequence)
    # if it is not, add either one or two dashes as appropriate
    
    in_length = len(in_string)
    
    if in_length % 3 == 0:
        return in_string
    elif (in_length + 1) % 3 == 0:
        return in_string + "-"
    elif (in_length + 2) % 3 == 0:
        return in_string + "--"
    

try:
    with open(sys.argv[1], "r") as fileA:
        fcontent = list(SeqIO.parse(fileA, "fasta"))
        fileA.close()
except IOError as exc: # now with error handling, so if there happens to be a directory in the folder, it doesn't matter.
    if exc.errno != errno.EISDIR:
        raise

    

# use the lengt_correct function on all sequences.
for check in range(len(fcontent)):
    fcontent[check].seq = length_correct(fcontent[check].seq)


# write to file - when it is working, allow it to overwrite the input file.
seq_output = open(sys.argv[1], "w")
SeqIO.write(fcontent, seq_output, "fasta")
seq_output.close()



