# -*- coding: utf-8 -*-
import os
import pandas as pd
from CDCDataTools import IO
from CDCDataTools import CDCFilters
#
# columns of interest
clinical_age = 'clinical_gestation_estimate'
obstetric_age = 'gestation_in_weeks'
resident = 'residence_status'
clinical_flag = 'clinical_estimate_of_gestation_used_flag'
death_age = 'age_at_death_in_days'
death_year = 'death_year'
delivery_year = 'delivery_year'
#
# where the data is
DataDirectory = os.path.expanduser("~"+"\\Box Sync\\DellMed\\Data\\TUdata\\")
try:
    IO.set_data_directory(DataDirectory)
except RuntimeError:
    pass
#
# create the data frame
columns = [clinical_age,obstetric_age,resident,clinical_flag]
dead = IO.readDWH(2008,columns)
#
# remove non residents
CDCFilters.remove_nonresidents(dead,inplace=True)
#
CDCFilters.remove_unknown_gestation_age(dead,inplace=True)
#
dead['GA']=dead.apply(lambda row: CDCFilters.GA(row),axis=1).astype(int)
dead['GAT']=dead.apply(lambda row: CDCFilters.GATYPE(row),axis=1).astype(str)
#
cobs = CDCFilters.count_and_sort(dead,'GAT')
tbl = pd.DataFrame(data=cobs.values.reshape(1,2),index=[2008],columns=cobs.index)
#messing about with the group object to try to get the output I want. 
grouped_dead = dead.groupby(['GAT','GA'])
clnframe = grouped_dead.size()['CLN'].to_frame()
obsframe = grouped_dead.size()['OBS'].to_frame()
GATypeVsGA = pd.concat([clnframe,obsframe],axis=1).fillna(0).astype(int)
GATypeVsGA.columns = ['CLN','OBS']
GATypeVsGA.plot.bar(rot=0)