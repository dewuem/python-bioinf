#!/usr/bin/python2


import sys
import errno

from Bio import SeqIO

# Daniel Elsner

# Check if the input sequence is a multiple of 3, that is the codons add up


def length_check(in_string):
    #check if the string is divisible by three
    
    in_length = len(in_string.strip())
    
    if in_length % 3 != 0 and in_length != 0:
        return True
    else:
        return False
    

try:
    with open(sys.argv[1], "r") as fileA:
        fcontent = list(SeqIO.parse(fileA, "fasta"))
        fileA.close()
except IOError as exc: # now with error handling, so if there happens to be a directory in the folder, it doesn't matter.
    if exc.errno != errno.EISDIR:
        raise

Stats = False
    


if length_check(fcontent[0].seq) == True:
    Stats = True
elif length_check(fcontent[0].seq) == False:
    pass
else:
    print "ERROR"





if Stats == True:
    print "Error in " + sys.argv[1] + " - sequence not a multiple of 3!"
