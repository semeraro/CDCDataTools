"""
A short script to test the CDCDataTools package.
Read the data for 2008. Filter it. Create a plot.
"""
from CDCDataTools import IO
from CDCDataTools import CDCFilters
import os
import pandas as pd 
import matplotlib.pyplot as plt 
#
# These string variables contain the field names we want to extract
# from the data. This is done for convenience in notation as the 
# column headers are verbose.
clinical_age  = 'clinical_gestation_estimate'
obstetric_age = 'gestation_in_weeks'
resident      = 'residence_status'
clinical_flag = 'clinical_estimate_of_gestation_used_flag'
death_age     = 'age_at_death_in_days'
death_year    = 'death_year'
delivery_year = 'delivery_year'
#
# string variable containing the full path to the data (csv file)
# The double back slash is the proper escape sequence for windows.
DataDirectory = os.path.expanduser("~"+"\\Desktop\\")
try:
    IO.set_data_directory(DataDirectory)
except RuntimeError:
    pass
#
# Create the pandas dataframe
columns = [clinical_age,obstetric_age,resident,clinical_flag]
dead = IO.readDWH(2008,columns)
#
# remove non residents
CDCFilters.remove_nonresidents(dead,inplace=True)
#
# remove records with unknown gestational age 
# missing both clinical and obsetric estimates
CDCFilters.remove_unknown_gestation_age(dead,inplace=True)
#
# add a column to the table called GA which contains the "correct"
# gestational age. See the documentation for CDCFilters.GA
dead['GA'] = dead.apply(lambda row: CDCFilters.GA(row),axis=1).astype(int)
#
# add a column to the table called GAT that contains the type of 
# gestational age estimate for this record. Either CLN or OBS for
# clinical or obstetric respectively
dead['GAT'] = dead.apply(lambda row: CDCFilters.GATYPE(row),axis=1).astype(str)
#
# group the data by gestational age type
grouped_dead = dead.groupby(['GAT','GA'])
clinicalDead = grouped_dead.size()['CLN'].to_frame()
obstetricDead = grouped_dead.size()['OBS'].to_frame()
GATypeVsGA = pd.concat([clinicalDead,obstetricDead],axis=1).fillna(0).astype(int)
GATypeVsGA.columns = ['CLN','OBS']
GATypeVsGA.plot.bar(rot=0)
plt.show()