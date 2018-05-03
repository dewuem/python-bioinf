#!/usr/bin/python3
import sys 

# Daniel Elsner
# Takes the output of an OrthologousGroups_single_copies file, keeps only the IDs and strips the (SPEC) tag (not needed) to produce nice columns for list comparison

for i in sys.stdin:
    null,a = i.split("\t") # keep only IDs
    a=a.strip() # clean the string up
    a=a.split(" ") # separate on space
    a=sorted(a) # sort list alphabetically
    for o in range(len(a)):
        a[o], null = a[o].split("(") # we don't want the bracket
    
    a=', '.join(a) # make list a string again
    print(a, end="\n") # print
