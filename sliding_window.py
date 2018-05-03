#!/usr/bin/env python2

# Daniel Elsner

# Creates a sliding window of sequence pieces to blast against

# takes two arguments, input file and window size. Only the first record
# in a fasta will be used, the rest ignored.

from Bio import SeqIO  # read sequence files
import sys

# read your sequence file

try:
    with open(sys.argv[1], "rU") as fileA:
        fcontent = list(SeqIO.parse(fileA, "fasta"))
        fileA.close()
except IOError as exc:  # it will complain if you try to open a directory instead of a file
    if exc.errno != errno.EISDIR:
        raise

# the function


def sliding_create(seq_id, seq_str, start_pos, window_size):
    # defines a function that takes the sequence id of the input query, the
    # actual sequence from the fasta seq record, the start position (from the
    # loop, for your sliding window, and the window size, from a command line
    # paramter
    sub_seq = seq_str[start_pos:start_pos + window_size]
    # cut a sub sequence from the full length sequence, from the start
    # position (of this loop iteration) + the window length
    sub_pos_str = str(seq_id + "_POS:_" + str(start_pos) +
                      ":" + str(start_pos + window_size))
    # and create a string with the appropriate name so you know which window
    # you test
    if len(sub_seq) == window_size:
        # only report the sub sequence if it is as long as the window size,
        # otherwise you get shorter pieces at the end
        return ">" + sub_pos_str + "\n" + sub_seq
    else:
        return None

# main loop begins here

with open(sys.argv[1] + "_sliding_window.fa", "w") as writefile:
    # open our output file, same name as the input + the suffix
    # _sliding_window.fa
    for i in range(len(fcontent[0].seq)):
        # for all positions in your sequence
        output = sliding_create(fcontent[0].id, fcontent[
                                0].seq, i, int(sys.argv[2]))
        # get the output of the function, as paramtere give the ID of the
        # fasta record, the sequence of the fasta record, the current
        # iteration of the loop (so we shift the window per one per loop,
        # and how long you want your window to be.
        if output != None:
            # only have output if there is output, otherwise you get lots
            # of empty output from the function when the sub sequence is no
            # longer long enough. Write it into the output file.
            writefile.write(str(output) + "\n")
