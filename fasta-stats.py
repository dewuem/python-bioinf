#!/usr/bin/python2

#Daniel Elsner

# Python 2.7

# This script calculates stats for fasta files.

# While there have been other scripts to do similar things, this was done out of curiosity and as a scripting exercise. Additionally, it can be modified easily to show additional values of interest, and I understand what it does, instead of relying that somebody else did it right.

# Note: Some of the functions have been added just to see how it is done. Not necessarily useful. 

import sys
import math
from itertools import repeat

numlengths = []
lineA_length = 0
gcnumber = 0


def length_of_sequence(numlengths):
    
    # Function for sequence length
    
    total = 0
    for contiglength in numlengths: 
        total += contiglength
    return total
    
def average_seq_length(numlengths):
    
    # Function for average sequence length
    
    sum_of_numlengths = length_of_sequence(numlengths)
    average = sum_of_numlengths / float(len(numlengths))
    return average

# Functions for variance and std. 



def length_var(cont_lengths):
    average=average_seq_length(cont_lengths)
    variance=0.0
    for score in cont_lengths:
        variance += (average - score) ** 2
        
    variance /= len(cont_lengths)
    return variance
    
def numlengths_std_deviation(variance):
    
    
    return variance ** 0.5

    

def median(input):

    #Function for median sequence length
    
    if len(input) == 1:
        return 1
    else:
            
        if len(input) % 2 == 0:
            input = sorted(input)
            #even
            middle=len(input) / 2
            midavg=(input[middle-1]+input[middle]) / 2.0
            
            if midavg.is_integer() == True:
                
                # if the two most middle values are the same and their quotient is an integer, I don't want .0 to show up.
                
                return int(midavg)
            else:
                return midavg
        
        else:
            input = sorted(input)
            #odd:
            return input[len(input) / 2]



"""
def n50(input):
    
    # covered by the percentile function, left as reference. The median is also the 50 percentile
    
    ninput = []
    for element in input:
        for elemt in range(1,(element+1)):
            ninput.append(element)
    
    return int(median(sorted(ninput)))
"""    





def percentile(input):

    # Partial Function for N25, N50, N75
    ## Here: Percentile of a list containing n elements of each value n = NXY: N75 is the 25 percentile, N50 is the 50 percentile/median, N25 is the 75 percentile.

    N = sorted(input)
    ninput = []
    for element in N:
   #     ninput.extend(element*[element]) # faster but still not ideal

        ninput.extend(repeat(element, element)) #supposedly fastest (maybe not noticable because of hdd), but seems not much faster than second solution
        
        #extend is a built in function that takes each element and copies it the specified amount. Found in Python online documentation.

        
        # old and slow; loop within a loop. Works but is inefficient, would have been my first choice.
        # for elemt in range(1,(element+1)):
        #     ninput.append(element)
    
    return sorted(ninput)


def NXY(ninput, P):


    # Partial Function for N25, N50, N75    
    # Splitting up the functions so the time consuming step (making a list in wich each value n occurs n times) run only once instead of three times
    
    
    n = int(round(P * len(ninput) + 0.5))
    return ninput[n-1]


def GC(gclen, totallen):
    
    # Function for GC percentage
    
    return (float(gclen) / length_of_sequence(totallen)) * 100
    

    

fileA = open(sys.argv[1],"r")

# Use the file as an argument for the script in terminal.




for lineA in fileA:
    if lineA.startswith(">") == True:
        
        # The > char is used to determine when a conding sequence stops in the file.
        # Sequence length is added line by line, until > is encountered, since fasta files can have coding parts over multiple lines.
        
        if lineA_length !=0:
            numlengths.append(lineA_length)
        
        
        lineA_length = 0
        
    else:
        lineA=lineA.strip()
        
        # strip the line of whitespace characters
        
        lineA_length += len(lineA)
        
        for char in lineA:
            if char == "G" or char == "C" or char == "g" or char == "c":
                gcnumber += 1
                
                #count occurences of GC. Probably not very efficient to do a loop within a loop.
        
        # each line is stripped of whitespace characters, split up according to tabulators and added to a list.

if lineA_length !=0:
    numlengths.append(lineA_length)
    # also append the last length, because there won't be another > encountered.

# variance=length_var(numlengths)

# calculates variance, commented out since it is not used currently.

nxinput = percentile(numlengths)

# calculates base input for percentiles/N25/N50/N75 once.


# Output is tab delimited, so it can be easily cut by columns.

print "File:\t%s" % (sys.argv[1]) # if desired, print file path
print "Number of contigs:\t" + str(len(numlengths))
print "Mean contig length:\t" + str(round(average_seq_length(numlengths),2)) + "\tbp, rounded to two decimal points."
print "Median:\t" + str(median(numlengths)) + "\tbp"
print "N10:\t" + str(NXY(nxinput, 0.9)) + "\tbp - 10 % of the contigs are this long or longer"
print "N25:\t" + str(NXY(nxinput, 0.75)) + "\tbp - 25 % of the contigs are this long or longer"
print "N50:\t" + str(NXY(nxinput, 0.5)) + "\tbp - 50 % of the contigs are this long or longer"
print "N75:\t" + str(NXY(nxinput, 0.25)) + "\tbp - 75 % of the contigs are this long or longer"
print "N90:\t" + str(NXY(nxinput, 0.1)) + "\tbp - 90 % of the contigs are this long or longer"
print "Total sequence lengths:\t" + str(length_of_sequence(numlengths)) + "\tbp"
print "GC count:\t" + str(gcnumber) + "\tbp"
print "GC percent:\t" + str(round(GC(gcnumber, numlengths),2)) + "\t%, rounded to two decimal points."
print "Variance:\t" + str(variance)
print "Stamdard Deviation:\t" + str(numlengths_std_deviation(variance))
