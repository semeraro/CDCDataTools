# -*- coding: utf-8 -*-
#  Analysis of 2008 preterm infant deaths from Tomaslav Urban's data
#
# Dave Semeraro - Janurary 2019
import pandas as pd
import sys
import os
from CDCDataTools import CDCFilters
import matplotlib.pyplot as plt
# These are the tags or column names I will need. 
clinical_age = 'clinical_gestation_estimate'
obstetric_age = 'gestation_in_weeks'
resident = 'residence_status'
clinical_flag = 'clinical_estimate_of_gestation_used_flag'
death_age = 'age_at_death_in_days'
death_year = 'death_year'
delivery_year = 'delivery_year'
# read the infant death data
# the data contains no column headers so we have to add them later
# read_csv will use the first column of the data as the index.
# turn this off with index_col=False
death_columns_used=[death_age,death_year,delivery_year,resident,clinical_age,obstetric_age,clinical_flag]
filename = os.path.expanduser("~"+"\\Box Sync\\DellMed\\Data\\TUdata\\infant_deaths_2008.csv")
headername = os.path.expanduser("~"+"\\Box Sync\\DellMed\\Data\\TUdata\\headers_infant_deaths.csv")
col_index_list = list()
deaths_header = pd.read_csv(headername,index_col=False,header=0)
for name in death_columns_used: # col_index_list contains column numbers
    col_index_list.append(deaths_header.columns.get_loc(name))
infant_deaths = pd.read_csv(filename,index_col=False,header=0,usecols=col_index_list)
infant_deaths.columns = death_columns_used
# read the birth data. 
# the column header situation is the same for live births as for infant death
# add the headers after the read
live_columns_used=[delivery_year,resident,clinical_age,obstetric_age,clinical_flag]
filename = os.path.expanduser("~"+"\\Box Sync\\DellMed\\Data\\TUdata\\live_births_2008.csv")
headername = os.path.expanduser("~"+"\\Box Sync\\DellMed\\Data\\TUdata\\headers_live_births.csv")
col_index_list=list()
births_header = pd.read_csv(headername,index_col=False,header=0)
for name in live_columns_used:
    col_index_list.append(births_header.columns.get_loc(name))
live_births = pd.read_csv(filename,index_col=False,header=0,usecols=col_index_list)
live_births.columns = live_columns_used
# do a little clean up
del filename, headername, deaths_header, births_header
# remove non residents
# use the CDCFilters module
CDCFilters.remove_nonresidents(infant_deaths,inplace=True)
CDCFilters.remove_nonresidents(live_births,inplace=True)
# remove unknown gestational age. 
CDCFilters.remove_unknown_gestation_age(infant_deaths,inplace=True)
CDCFilters.remove_unknown_gestation_age(live_births,inplace=True)
# split the tables into records that use clinical estimate and those that dont.
clindeath,obsdeath = CDCFilters.split_on_clinical_flag(infant_deaths)
clinlive,obslive = CDCFilters.split_on_clinical_flag(live_births)
# count total deaths vs gestational age for clin
clindvsage = CDCFilters.count_and_sort(clindeath,clinical_age)
plt.figure(1)
clindeadplot = clindvsage.plot.bar()
clindeadplot.set_title("Clinical Estimate Used",fontsize=18)
clindeadplot.set_xlabel("Gestational Age",fontsize=16)
clindeadplot.set_ylabel("Deaths",fontsize=16)
# count total births vs ga for clinical estimate. 
clinbvsage = CDCFilters.count_and_sort(clinlive,clinical_age)
plt.figure(2)
clinbirthplot = clinbvsage.plot.bar()
clinbirthplot.set_title("Clinical Estimate Used",fontsize=18)
clinbirthplot.set_xlabel("Gestational Age",fontsize=16)
clinbirthplot.set_ylabel("Births",fontsize=16)
# plot just the preterm data
plt.figure(3)
clinbirthplot = clinbvsage[0:6].plot.bar()
clinbirthplot.set_title("Clinical Estimate Used",fontsize=18)
clinbirthplot.set_xlabel("Gestational Age",fontsize=16)
clinbirthplot.set_ylabel("Births",fontsize=16)
# count deaths vs gestational age for obstetric estimate
obsdvsage = CDCFilters.count_and_sort(obsdeath,obstetric_age)
plt.figure(4)
obsdeadplot = obsdvsage.plot.bar()
obsdeadplot.set_title("Clinical Estimate Not Used",fontsize=18)
obsdeadplot.set_xlabel("Gestational Age",fontsize=16)
obsdeadplot.set_ylabel("Deaths",fontsize=16)
# count births vs gestational age fo obstetric estimates
obsbvsage = CDCFilters.count_and_sort(obslive,obstetric_age)
plt.figure(5)
obsliveplot = obsbvsage.plot.bar()
obsliveplot.set_title("Clinical Estimate Not Used",fontsize=18)
obsliveplot.set_xlabel("Gestational Age",fontsize=16)
obsliveplot.set_ylabel("Births",fontsize=16)
# just the preterm. 
plt.figure(6)
obsliveplot = obsbvsage[0:6].plot.bar()
obsliveplot.set_title("Clinical Estimate Not Used",fontsize=18)
obsliveplot.set_xlabel("Gestational Age",fontsize=16)
obsliveplot.set_ylabel("Births",fontsize=16)
# look at clinical estimate in obstetric records with unknown obs age
unknowndead = obsdeath[obsdeath.gestation_in_weeks==99]
unknowndeadvsclinga = CDCFilters.count_and_sort(unknowndead,clinical_age)
plt.figure(7)
ukdvclinplot = unknowndeadvsclinga.plot.bar()
ukdvclinplot.set_title("Unknown Obstetric Deaths",fontsize=18)
ukdvclinplot.set_xlabel("Gestational Age",fontsize=16)
ukdvclinplot.set_ylabel("Deaths",fontsize=16)
# live
unknownlive = obslive[obslive.gestation_in_weeks==99]
unknownlivevsclinga = CDCFilters.count_and_sort(unknownlive,clinical_age)
plt.figure(8)
uklvclinplot=unknownlivevsclinga.plot.bar()
uklvclinplot.set_title("Unknown Obstetric Births",fontsize=18)
uklvclinplot.set_xlabel("Gestational Age",fontsize=16)
uklvclinplot.set_ylabel("Births")
# clean up
del clinbvsage, clindeath, clindvsage, clinlive
del obsbvsage, obsdeath, obsdvsage, obslive
# add GA column to infant_deaths that contains clinical if flag set or 
# obstetric missing and obstetric otherwise. 
infant_deaths['GA'] = infant_deaths.apply(lambda row: CDCFilters.GA(row),axis=1).astype(int)
# add GA column to live births that contains clinical if flag set or
# obstetric missing and obstetric otherwise
live_births['GA'] = live_births.apply(lambda row: CDCFilters.GA(row),axis=1).astype(int)
infantdeathsvsga = CDCFilters.count_and_sort(infant_deaths,'GA')
plt.figure(9)
idgaplt = infantdeathsvsga.plot.bar()
idgaplt.set_title("Deaths VS GA",fontsize=18)
idgaplt.set_xlabel("Gestational Age",fontsize=16)
idgaplt.set_ylabel("Deaths",fontsize=16)
#
live_birthsvsga = CDCFilters.count_and_sort(live_births,'GA')
plt.figure(10)
lbgaplt = live_birthsvsga.plot.bar()
lbgaplt.set_title("Surviving Births VS GA",fontsize=18)
lbgaplt.set_xlabel("Gestational Age",fontsize=16)
lbgaplt.set_ylabel("Births",fontsize=16)
# get the total
birthvsga = live_birthsvsga.to_frame()
deathvsga = infantdeathsvsga.to_frame()
totalbirthvsga = birthvsga.add(deathvsga,axis=1,fill_value=0)
# calculate neonatal death
neonatal_deaths = infant_deaths[infant_deaths.age_at_death_in_days < 28]
neonvsga = CDCFilters.count_and_sort(neonatal_deaths,'GA')
plt.figure(11)
ndgaplt = neonvsga.plot.bar()
ndgaplt.set_title("Neonatal Deaths VS GA",fontsize=18)
ndgaplt.set_xlabel("Gestational Age",fontsize=16)
ndgaplt.set_ylabel("Deaths",fontsize=16)
prob = neonvsga.to_frame().divide(totalbirthvsga,fill_value=0)
# split tables by gestational estimate type
#clinical_deaths,obstetric_deaths = CDCFilters.split_on_clinical_flag(infant_deaths)
#clinical_neonatal,obstetric_neonatal = CDCFilters.split_on_clinical_flag(neonatal_deaths)
#delete records with missing obstetric age in obstetric data
#CDCFilters.remove_unknown_obstetric_age(obstetric_deaths,inplace=True)
#CDCFilters.remove_unknown_obstetric_age(obstetric_neonatal,inplace=True)
#calculate death counts vs gestational age
#clinical_deaths_vs_gestation = CDCFilters.count_and_sort(clinical_deaths,clinical_age)
# count births and deaths vs gestational age. 
#totaldeaths_vs_gestation = infant_deaths['gestation_in_weeks'].value_counts().sort_index()
#neondeath_vs_gestation = neonatal_deaths['gestation_in_weeks'].value_counts().sort_index()
#births_vs_gestation = live_births['gestation_in_weeks'].value_counts().sort_index()
#total_births_vs_gestation = totaldeaths_vs_gestation + births_vs_gestation
#probability_of_neonatal_death = neondeath_vs_gestation/total_births_vs_gestation
# plot it
#plt.figure(1)
#dead = neondeath_vs_gestation.plot.bar()
#dead.set_title("Neonatal deaths infants born in 2008",fontsize=18)
#dead.set_xlabel("Gestation age (weeks)",fontsize=16)
#dead.set_ylabel("Deaths",fontsize=16)
#plt.figure(2)
#prob = probability_of_neonatal_death.plot.bar()
#prob.set_title("Probability of Neonatal Death 2008",fontsize=18)
#prob.set_xlabel("Gestation age (weeks)",fontsize=16)
#prob.set_ylabel("Probability",fontsize=16)