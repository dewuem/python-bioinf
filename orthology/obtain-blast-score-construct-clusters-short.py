#!/usr/bin/python2

import sys
from collections import OrderedDict

# Daniel Elsner
#Takes a tabular blast results file (outfmt 6), reduced to the the three colums query, hit and score (use "cut", from GNU coreutils, presumably included in most Linux distros), to obtain the score of each relevant pairwise comparison.

# note that because of phylogeny, an outgroup is included ("Outg" in the orthoMCL header format). Remove/change as necessary.

fileA = open(sys.argv[1],"r")
lineacc = []
for lineA in fileA:
    lineacc.append(lineA.split())
lineclean =[]
# Preliminary cleanup
for i in lineacc:
    if i[0] != i[1]:
    
        # Get rid of hits against itself      
          
        a=i[0].split('_')
        b=i[1].split('_')
        # Get rid of the Outgroup (hardcoded, change if necessary). Can be removed if the input files do not contain it.

        if a[0] != "Outg" and b[0] != "Outg":
            lineclean.append(i)

# remove hits against same species
linecleaner = []

for i in lineclean:
    a=i[0].split('|')
    b=i[1].split('|')
        
    if a[0] != b[0]:
        linecleaner.append(i)
# Dynamically create a list of all species - this allows to use the script with other species sets with no modification
los = []
list_of_species = []
for i in linecleaner:
    los.append(i[0].split('|')[0])
    
for i in los:
    if i not in list_of_species:
        list_of_species.append(i)
        # concentrate the first list (which contains duplicates) to a list without duplicates.
      
# transfer the data from one list with the data in a line to three lists. a for query, b for hit, c for score.
cont_check = []
hit_check = []
score_check = []
for i in linecleaner:
    cont_check.append(i[0])
    hit_check.append(i[1])
    score_check.append(i[2])
    
short_list = []
cont_reduced = list(OrderedDict.fromkeys(cont_check))
### Check if there is at least one species with only one sequence 
spec_dup_dict = {}
for spec in list_of_species:
    spec_size = 0
    
    for o in range(len(cont_reduced)):
        contig_id = cont_reduced[o]
        spec_of_interest = contig_id.split('|')[0]
    
        if spec == spec_of_interest:
            spec_size += 1
            
    if spec_size >= 2:
        spec_dup_dict[spec] = True
    else:
        spec_dup_dict[spec] = False
    
if False not in spec_dup_dict.values():
    sys.exit("Error in file " + sys.argv[1] +": All species have two or more sequences. It can not be guaranteed to assemble the correct cluster, two or more clusters may be present.")
    # Make sure there is at least one species with only one represented sequence. If this is not the case, abort and print the above to STDERR
# first part of the analysis. For each sequence, the sequence with the highest blast score in each of the other species is taken and added, so the sequence has an associated sum of the most similar sequence in other species (so called "Top Score"). The goal is to find the sequence cluster that is the most similar, presumably the ortholog cluster.
contig_dict = {}
    
for i in cont_reduced:
    check_list = []
    for o in range(len(cont_check)):
        if i == cont_check[o]:
            check_list.append([cont_check[o], hit_check[o], score_check[o]])

    max_spec_dict = {}
    
    for spec in list_of_species:
        max_spec_list = []
        
        #fuer jede Species
        for hit in range(len(check_list)):
            hit_spec = check_list[hit][1]
        
            if hit_spec.split('|')[0] == spec:
                max_spec_list.append(check_list[hit][2])
                
               
        max_spec_dict[spec] = max_spec_list
    
    
    spec_max_value_dict = {}
    
    
    for spec in list_of_species:
        max_check = max_spec_dict[spec]
    
        if len(max_check) >=2:
            m_value = max(max_check)  # taking the max from 1 creates an error...
        elif len(max_check) == 1:
            m_value = max_check[0]
        else:
            m_value = "NA" # empty = hit against self
    
        spec_max_value_dict[spec] = m_value
    
    # this is the top score per contig against other species
 
    contig_score = 0.0   
       
    for spec in list_of_species:
        if spec_max_value_dict[spec] != "NA":
            contig_score += float(spec_max_value_dict[spec])
        
    contig_dict[i] = contig_score
    
    # contig with the highest score against other species = sum of top scores
# Now the last part: Rank the top score sums, get the highest contig per species.
total_max_value_dict = {}
total_best_contig_dict = {}

for spec in list_of_species:
    max_spec_dict = {}
    
    for o in range(len(contig_dict)):
        contig_id = contig_dict.keys()[o]
        spec_of_interest = contig_id.split('|')[0]
    
        if spec == spec_of_interest:
            max_spec_dict[contig_dict.keys()[o]] = contig_dict.values()[o]
    
    if len(max_spec_dict.keys()) >=2:
        m_key, m_value = max(max_spec_dict.iteritems(), key=lambda x:x[1])
    elif len(max_spec_dict.keys()) == 1:
        m_key, m_value = str(max_spec_dict.keys()).strip("'[]'"), str(max_spec_dict.values()).strip("'[]'")

        
    else:
        m_key, m_value = "NA", "NA" # empty = hit against self
    
    if m_key != "NA":
        total_max_value_dict[spec] = max_spec_dict[m_key]
        total_best_contig_dict[spec] = m_key
        
    else:
        total_max_value_dict[spec] = "NA"
        total_best_contig_dict[spec] = "NA"    
# Now we have the putative cluster.
out_list = ""
for spec in list_of_species:
    out_list += "\t" + str(total_best_contig_dict[spec]).strip("[]")
print sys.argv[1] + ":" + str(out_list)
# This outputs to print, if you loop it in bash and pipe it into a single file, you make a file like the output of OrthoMCL, enabling to redo further analysis steps without modification
# Alternative way to save: Single files, currently not used.
"""
with open(sys.argv[1] + "-new-cluster", 'w') as f:
    for spec in list_of_species:
        f.write(total_best_contig_dict[spec] + "\n")
f.closed  
"""
