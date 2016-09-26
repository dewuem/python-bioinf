#!/usr/bin/env python2

# Daniel Elsner

# 16.06.2016

# download the go-basic.obo from the GO consortium

# cut the Interproscan output file for columns with ID and GO-ID (usually 1,14), then grep for all entries with GO terms, reduce reduncancy by using a dictionary and sets.

# should give a table (pipe with > into an output file) with one identifier and all the GO terms for that identifier.

import sys
import goatools

pwd = '' # enter your working directory


# LOAD THE GO TERMS
p = goatools.obo_parser.GODag(pwd + 'go-basic.obo')


with open(sys.argv[1], 'r') as readfile:
    id_list_content = list(readfile)
    
outdict={}
out_id_dict={}
    
for i in range(len(id_list_content)):
    
    u, j = id_list_content[i].split('\t')
    
    outdict[u] = set()
    out_id_dict[u] = set()
    
for i in range(len(id_list_content)):
    
    u, j = id_list_content[i].split('\t')
    
    if '|' in str(j):
        for n in str(j).split('|'):
            outdict[u].add(n.strip())
            out_id_dict[u].add(str(p[n.strip()].name))
    else:
        outdict[u].add(str(j.strip()))
        try:
            out_id_dict[u].add(str(p[str(j.strip())].name))
        except:
            pass

for i in range(len(outdict)):
    print str(outdict.keys()[i]) + "\t" + ', '.join(outdict.values()[i]) + "\t" + ', '.join(out_id_dict.values()[i])
