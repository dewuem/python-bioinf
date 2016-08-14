#!/usr/bin/python2

import sys
from scipy.stats import chisqprob
# Daniel Elsner
# calculates the likelihood ratio test
with open(sys.argv[1], "r") as fileA:
    fcontent = list(fileA)
    fileA.close()
    
switch = False
mem_0 = 0
df_0 = 0
mem_1 = 0
df_1 = 0
df = 0
p_value = 0

for lineA in fcontent:
    if switch == False:
        mem_0 = float(lineA.split()[10])
        df_0 = int(lineA.split()[9])
        switch = True
        
    else:
        mem_1 = float(lineA.split()[10])
        df_1 = int(lineA.split()[9])
        df = df_1-df_0
        memdiff = 2*(mem_1 - mem_0)
        
        p_value = chisqprob(memdiff, df)
        
        print lineA.split()[0] + "\t" + lineA.split()[1] + "\t" + "df:" + "\t" + str(df) + "\t" + "p_value:" + "\t" + str(p_value)
        switch = False
