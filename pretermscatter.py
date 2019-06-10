# -*- coding: utf-8 -*-
# preterm scatter plot 
# generate a 3D scatter plot with the age at death, gestational age, and birth 
# year on the x, y, and z axes respectively. Only do this for preterm births
# that 
#
import plotly.plotly as py
import plotly
import plotly.graph_objs as go
#plotly.tools.set_credentials_file(username='semeraro',api_key='bd3y0GP3EhnWYioxtUMT')
import os
import pandas as pd
from CDCDataTools import CDCFilters
#
clinical_age = 'clinical_gestation_estimate'
obstetric_age = 'gestation_in_weeks'
resident = 'residence_status'
clinical_flag = 'clinical_estimate_of_gestation_used_flag'
death_age = 'age_at_death_in_days'
death_year = 'death_year'
delivery_year = 'delivery_year'
neoncolor = 'rgb(55,226,84)'
othercolor = 'rgb(128,55,55)'
#
col_list=[clinical_age,obstetric_age,resident,clinical_flag,death_age,death_year,delivery_year]
DataDirectory = os.path.expanduser("~"+"\\Box Sync\\DellMed\\Data\\TUdata\\")
death_columns_used=[death_age,death_year,delivery_year,resident,clinical_age,obstetric_age,clinical_flag]
allyears = pd.DataFrame(columns=col_list)
for i in range(8,17):
    deadfile = DataDirectory + f'infant_deaths_20{i:02}_with_headers.csv'
    if(os.path.exists(deadfile)):
        infant_deaths = pd.read_csv(deadfile,index_col=False,header=0,usecols=col_list)
# remove the non residents and no ga. 
        CDCFilters.remove_nonresidents(infant_deaths,inplace=True)
        CDCFilters.remove_unknown_gestation_age(infant_deaths,inplace=True)
# calculate a gestational age based on the clinical and obstetric ages. 
        infant_deaths['GA'] = infant_deaths.apply(lambda row: CDCFilters.GA(row),axis=1).astype(int)
        infant_deaths['GATYPE'] = infant_deaths.apply(lambda row:CDCFilters.GATYPE(row),axis=1)
# select preterm births only. GA < 24 weeks. drop other records
        infant_deaths.drop(infant_deaths[infant_deaths.GA>=24].index,inplace=True)
        # for some reason appending the GA column imports it as a float64 rather than 
        # an int which it is in the infant_deaths data
        allyears = allyears.append(infant_deaths,ignore_index=True,sort=True).astype({'GA':int})
# at this point we have a DataFrame called allyears with all of the data we need. Now its time
# to plot the data. 
# extract neonatal deaths
neon,other = CDCFilters.extract_neonatal_deaths(allyears)
traceneon = go.Scatter3d(
        x = neon[delivery_year],
        y = neon['GA'],
        z = neon[death_age],
        mode = 'markers',
        marker = dict(
                size = 3,
                color=neoncolor,
                line = dict(
                        width=0)))
traceother = go.Scatter3d(
        x = other[delivery_year],
        y = other['GA'],
        z = other[death_age],
        mode = 'markers',
        marker = dict(
                size = 3,
                color=othercolor,
                line = dict(
                        width=0)))
data = [traceneon,traceother]
layout = dict(
        width=1024,
        height=768,
        autosize=False,
        title='2008 - 2016 Preterm Deaths',
        scene=dict(
                xaxis=dict(
                        gridcolor='rgb(255,255,255)',
                        zerolinecolor='rgb(255, 255, 255)',
                        showbackground=True,
                        backgroundcolor='rgb(230, 230,230)',
                        title='Birth Year'
                ),
                yaxis=dict(
                        gridcolor='rgb(255, 255, 255)',
                        zerolinecolor='rgb(255, 255, 255)',
                        showbackground=True,
                        backgroundcolor='rgb(230, 230,230)',
                        title='Weeks Gestation'
                ),
                zaxis=dict(
                        gridcolor='rgb(255, 255, 255)',
                        zerolinecolor='rgb(255, 255, 255)',
                        showbackground=True,
                        backgroundcolor='rgb(230, 230,230)',
                        title='Death Age'
                ),
                aspectratio=dict(x=1,y=1,z=0.7),
                aspectmode='manual'
        ),
)
# uncomment for offline plot
#fig=dict(data=data,layout=layout)
#plotly.offline.plot(fig,filename="GAPreterm.html")
# uncomment for online plot
py.plot(data,layout,auto_open=True,filename="scatter")
               