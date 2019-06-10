# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 10:24:49 2018

@author: semeraro-la
"""
# Import stuff
import os
import pandas as pd
import plotly
# the data file names
theDead=os.path.expanduser("~"+"\\Box Sync\\DellMed\\Data\\2004period\\death.pkl")
theLive=os.path.expanduser("~"+"\\Box Sync\\DellMed\\Data\\2004period\\birth.pkl")
# import the data
Deaths = pd.read_pickle(theDead)
Births = pd.read_pickle(theLive)
# prepare the plot data
# The three axis will be birth weight, death age (days), and gestational age
# Create a table with preterm infants only. gestational age < 23 weeks
GALimit = str(23) # have to convert to string because Combgest is string.
# querystring - Note reference to GALimit with '@' operator. The '@' operator 
# lets you reference python variables inside of a query string. 
querystring = "COMBGEST!='99'&COMBGEST!='  '&COMBGEST<=@GALimit"
PretermDeaths = Deaths.query(querystring)
# extract some sequences
data = []
dotcolor = 'rgb(55,126,184)'
x = PretermDeaths['BRTHWGT']
y = PretermDeaths['AGED']
z = PretermDeaths['COMBGEST']

color = dotcolor
trace = dict(
    name = 'instance',
    x = x,
    y = y,
    z = z,
    type = "scatter3d",
    mode = 'markers',
    marker = dict(size=3,color=color,line=dict(width=0)))
data.append(trace)

layout = dict(
        width=1024,
        height=768,
        autosize=False,
        title='2004 Preterm Deaths',
        scene=dict(
                xaxis=dict(
                        gridcolor='rgb(255,255,255)',
                        zerolinecolor='rgb(255, 255, 255)',
                        showbackground=True,
                        backgroundcolor='rgb(230, 230,230)',
                        title='WT'
                ),
                yaxis=dict(
                        gridcolor='rgb(255, 255, 255)',
                        zerolinecolor='rgb(255, 255, 255)',
                        showbackground=True,
                        backgroundcolor='rgb(230, 230,230)',
                        title='Death Day'
                ),
                zaxis=dict(
                        gridcolor='rgb(255, 255, 255)',
                        zerolinecolor='rgb(255, 255, 255)',
                        showbackground=True,
                        backgroundcolor='rgb(230, 230,230)',
                        title='Gestation'
                ),
                aspectratio=dict(x=1,y=1,z=0.7),
                aspectmode='manual'
        ),
)
fig=dict(data=data,layout=layout)            
#from plotly.graph_objs import Scatter, Layout
#plotly.offline.plot(fig,image='png',image_filename='deadscatter')
plotly.offline.plot(fig)
#py.offline.plot({"data":[Scatter(x=[1,2,3,4],y=[4,1,3,7])],
#                            "layout":Layout(title="hello world")})
