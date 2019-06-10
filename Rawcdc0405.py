# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 10:34:16 2018

@author: semeraro-la
"""
from CDCDataTools import IO
import os
import pandas as pd
#This program creates a concatinated file from the raw 2004-2005 data
#This file should be comparable to the csv file that was pulled from 
#some Stata data elsewhere. 
#Once the file is created we can do some analysis on it to compare with
#analysis done on the csv data previously. In particular we can get 
#the number of neonatal deaths from this data and compare it with the
#other data. 
file2004 = os.path.expanduser("~"+"\\Box Sync\\DellMed\\Data\\2004period\\LinkPE04USNum.dat")
file2005 = os.path.expanduser("~"+"\\Box Sync\\DellMed\\Data\\2005period\\VS05LINK.USNUMPUB")
#
# vector of fields to read
vrs = ['SEX','COMBGEST','ESTGEST','OBGEST_FLG','BRTHWGT','AGED','DOB_YY','DPLURAL','DTHYR']
# read data into a pandas dataframe
df2004 = IO.readCDC(file2004,vrs)
df2005 = IO.readCDC(file2005,vrs)
# find the neonatal deaths in the two datasets.
# now add a neonatal death boolean column to the merged data
df2004['NEONDTH'] = df2004.apply(lambda row: int(row.AGED) < 28, axis='columns')
df2005['NEONDTH'] = df2005.apply(lambda row: int(row.AGED) < 28, axis='columns')
print(f'{len(df2004.query("NEONDTH==True"))} neonatal deathes in 2004')
print(f'{len(df2005.query("NEONDTH==True"))} neonatal deathes in 2005')
print(f'concatinating 2004, 2005 {df2004.shape}, {df2005.shape}')
# concatinate these two files into a single file
# ignoring the index means that the row index has no meaning. Simply concat
# the rows. Join = inner means intersect the columns rather than adding the 
# union of the columns. Intersecting only includes columns that appear in
# both dataframes. Union includes all columns from both datasets. 
df0405 = pd.concat([df2004,df2005],ignore_index=True,join='inner')
print(f'dataframe has shape {df0405.shape}')
# and I can ditch the two input datasets. 
del(df2004)
del(df2005)
#Now count up the number of Neonatal deaths. 
print(f'{len(df0405.query("NEONDTH==True"))} neonatal deaths in 2004-2005')
#now map neonatal deaths as a function of gestational age. 
dfgdlt20 = df0405.loc[df0405['COMBGEST'].astype(int) <= 20]
dfgdlt20.shape
