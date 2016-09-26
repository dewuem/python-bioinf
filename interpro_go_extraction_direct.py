#!/usr/bin/env python2

# Daniel Elsner

# 26.09.2016

# ake the GO ID directly from Interproscan, without the need of previous cutting and grepping.

# Input: The interproscan-output.tsv file

import sys

with open(sys.argv[1], 'r') as readfile:
    id_list_content = list(readfile)
    
outdict={}

# make a dict, this prevents duplicate entries and makes access easy
    
for i in range(len(id_list_content)):
    
    if "GO" in id_list_content[i]:
        # only if there is a GO entry, otherwise there is nothing to split
            
        inputs = id_list_content[i].split('\t')
        p, j = inputs[0], inputs[13]
        #from the entry line, get the Gene Name and the GO IDs
        
        outdict[p] = set()
        # create a set, this spares us from checking for duplicates and just keeps everything once
    
    else:
        pass
        #if there is no GO entry, pass the line
    
    
for i in range(len(id_list_content)):
        
    if "GO" in id_list_content[i]:
        
        # only if there is a GO entry, otherwise there is nothing to split
    
        inputs = id_list_content[i].split('\t')
        p, j = inputs[0], inputs[13]
        #from the entry line, get the Gene Name and the GO IDs
        
        if '|' in str(j):
            for n in str(j).split('|'):
                outdict[p].add(n.strip())
                
                # individual GOs are separated by "|", for each of them add them to the set, automatically checking if it is already there.
                
        else:
            outdict[p].add(str(j.strip()))
            # create a set, this spares us from checking for duplicates and just keeps everything once
    else:
        pass
        #if there is no GO entry, pass the line

for i in range(len(outdict)):
    print str(outdict.keys()[i]) + "\t" + ', '.join(outdict.values()[i])
