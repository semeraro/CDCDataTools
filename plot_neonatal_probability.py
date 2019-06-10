# -*- coding: utf-8 -*-
import os
import pandas as pd
#import matplotlib.pyplot as plt
#import plotly
#
# This script plots the probability of neonatal death for
# years 2008 through 2016.
#
# The first thing we do is read all of the pickled data and merge
# it to a single pandas data frame. 
#
DataDirectory = os.path.expanduser("~"+"\\Box Sync\\DellMed\\Data\\TUdata\\")
# read in the 2008 data series
neonprob = pd.read_pickle(DataDirectory+f'Probability_of_Neonatal_Death_2008.pkl' )
# create a dataframe
df = pd.DataFrame({'2008':neonprob['GA']})
# append the other years onto the dataframe
for i in range(9,14):
    probfile = DataDirectory + f'Probability_of_Neonatal_Death_20{i:02}.pkl'
    dfi = pd.read_pickle(probfile)
    dfi.columns = [f'20{i:02}']
    df = df.join(dfi)
# Now we have one dataframe with year columns and gestational age in weeks rows.
tix = list(df.index.values[3:38])
lines = df.loc[13:47].plot.line(grid=True,xticks=tix[::2],title='Probability of Neonatal Death') 
lines.set_xlabel("gestation")
lines.set_ylabel("probability")
