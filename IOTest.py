# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 13:29:34 2018

@author: semeraro-la
"""

from CDCDataTools import IO
import os
# test read some data
# the file to read
#filename = os.path.expanduser("~"+"\\Box Sync\\DellMed\\Data\\2004period\\LinkPE04USNum.dat")
filename = os.path.expanduser("~"+"\\Box Sync\\DellMed\\Data\\2005period\\VS05LINK.USNUMPUB")
# vector of fields to read
vrs = ['SEX','COMBGEST','ESTGEST','OBGEST_FLG','BRTHWGT','AGED','DOB_YY','DPLURAL']
# read data into a pandas dataframe
df = IO.readCDC(filename,vrs)
# print out some diagnostics
print(f'dataframe has shape {df.shape}')
print(f'dataframe has {len(df.index)} rows and {len(df.columns)} columns')
print(f'dataframe row 100 is:\n {df.iloc[100]}')
print(f'first 10 elements of birthweight:\n{df.loc[0:9,"BRTHWGT"]}')
# delete the table and try reading some data that doesnt exist
del(df)
vrs2=['SEX','yourmama']
# this should produce a keyerror since 'yourmama' is not in the dataset
try:
    df = IO.readCDC(filename,vrs2)
except KeyError as e:
    print(f'IO error {e} invalid field name')
# now do some searching. Find records with death age < 29 days. 
# add a column called NEONDTH of type boolean to the existing table
# NEONDTH should be true if death age < 29 days
del(vrs2) 
df = IO.readCDC(filename,vrs)
df['NEONDTH'] = df.apply(lambda row: int(row.AGED) < 27, axis='columns')
# now count how many records there are where NEONDTH is true
# this can be done two ways, either query function or selection
# query
print(f'Query Found {len(df.query("NEONDTH==True"))} neonatal deaths')
# selection
print(f'Selection Found {len(df[df.NEONDTH == True])} neonatal deaths')
# print some death records
neon = df.query("NEONDTH==True")
print(f'The first 10 neonatal death records are:\n {neon.iloc[0:9]}')