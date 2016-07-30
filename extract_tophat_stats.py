#!/usr/bin/python

# Daniel Elsner

# Extract tophat align_summary.txt into a nice csv for comparison. Be careful, if there are no unmapped reads, that part will be omitted and replaced with "NA". May not always work right under some circumstances, verify your own results!

import sys
import os

with open(sys.argv[1], "r") as fileA:
    fcontent = list(fileA)
    fileA.close()
    
out_list = []

head, tail = os.path.split(os.path.dirname(sys.argv[1]))

out_list.append(tail)

#Left reads:

#Input
out_list += [int(s) for s in fcontent[1].split() if s.isdigit()]

#Mapped
out_list += [int(s) for s in fcontent[2].split() if s.isdigit()]

#Mapped %
out_list += [str(word).strip('(') for word in fcontent[2].split() if word.startswith('(') or word.endswith('%)')]

#Multiple    
out_list += [int(s) for s in fcontent[3].split() if s.isdigit()]

#Multiple % and > 20
out_list += [str(word).strip('(').strip(')') for word in fcontent[3].split() if word.startswith('(') or word.endswith('%)')]


#Right reads:

#Input
out_list += [int(s) for s in fcontent[5].split() if s.isdigit()]

#Mapped
out_list += [int(s) for s in fcontent[6].split() if s.isdigit()]

#Mapped %
out_list += [str(word).strip('(') for word in fcontent[6].split() if word.startswith('(') or word.endswith('%)')]

#Multiple    
out_list += [int(s) for s in fcontent[7].split() if s.isdigit()]

#Multiple % and > 20
out_list += [str(word).strip('(').strip(')') for word in fcontent[7].split() if word.startswith('(') or word.endswith('%)')]


if fcontent[8].startswith('Unpaired'):
    #Unpaired reads:

    #Input
    out_list += [int(s) for s in fcontent[9].split() if s.isdigit()]

    #Mapped
    out_list += [int(s) for s in fcontent[10].split() if s.isdigit()]

    #Mapped %
    out_list += [str(word).strip('(') for word in fcontent[10].split() if word.startswith('(') or word.endswith('%)')]

    #Multiple    
    out_list += [int(s) for s in fcontent[11].split() if s.isdigit()]

    #Multiple % and > 20
    out_list += [str(word).strip('(').strip(')') for word in fcontent[11].split() if word.startswith('(') or word.endswith('%)')]
    
    #Overall read mapping
    out_list += [str(word) for word in fcontent[12].split() if word.endswith('%')]


    #Aligned pairs
    out_list += [int(s) for s in fcontent[14].split() if s.isdigit()]

    #Multiple
    out_list += [int(s) for s in fcontent[15].split() if s.isdigit()]

    #Multiple %
    out_list += [str(word).strip('(').strip(')') for word in fcontent[15].split() if word.startswith('(') or word.endswith('%)')]

    #Discordant
    out_list += [int(s) for s in fcontent[16].split() if s.isdigit()]

    #Discordant %
    out_list += [str(word).strip('(').strip(')') for word in fcontent[16].split() if word.startswith('(') or word.endswith('%)')]


    #Concordant
    out_list += [str(word) for word in fcontent[17].split() if word.endswith('%')]


else:
    
    out_list.append("NA")
    out_list.append("NA")   
    out_list.append("NA")
    out_list.append("NA")
    out_list.append("NA")
    out_list.append("NA")   

    #Overall read mapping
    out_list += [str(word) for word in fcontent[8].split() if word.endswith('%')]

    #Aligned pairs
    out_list += [int(s) for s in fcontent[10].split() if s.isdigit()]

    #Multiple
    out_list += [int(s) for s in fcontent[11].split() if s.isdigit()]

    #Multiple %
    out_list += [str(word).strip('(').strip(')') for word in fcontent[11].split() if word.startswith('(') or word.endswith('%)')]

    #Discordant
    out_list += [int(s) for s in fcontent[12].split() if s.isdigit()]

    #Discordant %
    out_list += [str(word).strip('(').strip(')') for word in fcontent[12].split() if word.startswith('(') or word.endswith('%)')]

    #Concordant
    out_list += [str(word) for word in fcontent[13].split() if word.endswith('%')]

out_list = filter(None, out_list)

print ",".join([str(x) for x in out_list] )