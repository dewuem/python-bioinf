#!/usr/bin/python2

import sys
import errno
import glob

from Bio import SeqIO

# Daniel Elsner
# This script concatenates single alignments. Make sure there are no spelling errors in the sequence names. Only the alignment files to combine may be in the directory.

# Possibility to improve this, if necessary: Give also the IDs and the position for each sequence.

fcontent = []


species_dict = {}

for filename in sorted(glob.glob(sys.argv[1])):
    
    

    try:
        with open(filename, "rU") as fileA:
            fcontent = list(SeqIO.parse(fileA, "fasta"))
            fileA.close()
    except IOError as exc: # now with error handling, so if there happens to be a directory in the folder, it doesn't matter.
        if exc.errno != errno.EISDIR:
            raise
    
    for i in range(len(fcontent)):
        #print fcontent[i].id
        
        if not fcontent[i].id in species_dict:
            species_dict[fcontent[i].id] = str(fcontent[i].seq)
        else:
            oldseq = species_dict[fcontent[i].id]
            newseq = oldseq + str(fcontent[i].seq)
            species_dict[fcontent[i].id] = newseq



    # get the sequence for each species, according to their place in the file (with Biopython). Transform to strin, add to Species string. Second list as an intermediate step is not necessary.

    
# Write to the output file, in the same directory as the script was started from
try:
    with open("combi-test.fa", "w") as writefile:
        
        for i in range(len(species_dict)):
            writefile.write(">" + species_dict.keys()[i] + "\n")
            writefile.write(species_dict.values()[i] + "\n")

      

except IOError as exc:
        if exc.errno != errno.EISDIR:
            raise # now with error handling
