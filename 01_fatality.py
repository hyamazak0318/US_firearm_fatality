#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 19:36:38 2023

@author: yamahi0318
"""

# construct a data set of firearm fatality rate

import pandas as pd

y_list = [2016,2015,2014,2013,2012,2011,2010,2009,2008,2007,2006,2005,2004,2003,2002]

# prepare the columns
row_list = [['STATE', 'FIP', 'deaths', 'pop', 'fat_rate', 'Year']]

# convert the input text file into the list
for y in y_list:
    file = f"fatality-data/{y}.txt"
    fh = open(file)
    mid_list = []
    for line in fh:
        # tidy up the names of column
        row = line.replace('"','')
        row = row.replace("Notes","")
        # remove the unnecessary spaces
        row = row.strip()
        row = row.split('	')
        # add the year variable to the original data
        row.append(f"{y}")
        # add the rows onto the list
        mid_list.append(row)
    # accumulate the single year data onto the list
    row_list.extend(mid_list[1:52])
        
#%%

# convert the list into the Pandas dataframe
colnames = row_list[0]
datarows = row_list[1:]
fat = pd.DataFrame(columns=colnames, data=datarows)

# convert the strings into numbers
fat[["deaths","pop"]] = fat[["deaths","pop"]].astype(int)
fat["fat_rate"] = fat["fat_rate"].astype(float)

fat.to_csv("fatality.csv", index=False)
