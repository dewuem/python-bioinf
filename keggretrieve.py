#!/usr/bin/python2

# coding: utf-8

# Daniel Elsner
# Get the amino acid sequence from the correct url for a kegg entry...
# Use best with GNU parallel (Tange 2011a) and an input list containing all the gene IDs from a kegg pathway.

import sys
from bs4 import BeautifulSoup
import requests


url = sys.argv[1]


r  = requests.get(url)
data = r.text


soup = BeautifulSoup(data, 'html.parser')


print soup.pre.get_text()