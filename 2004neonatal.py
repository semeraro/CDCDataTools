# -*- coding: utf-8 -*-
"""
Created on Fri Oct  5 14:32:26 2018

@author: semeraro
This script uses the CDCDataTools package to read the 2004 births, linked-deaths
file from the CDC. It then gathers some statistics on the data. The script
produces plots and tables. 
"""

from CDCDataTools import IO
import os
import pandas as pd
import matplotlib.pyplot as plt
# Names of files to read. linked deaths, unlinked deaths, total births 2004
#NameOfLinkedDeathFile = os.path.expanduser("~"+"\\Box Sync\\DellMed\\Data\\2004period\\LinkPE04USNum.dat")
#NameOfUnlinkedDeathFile = os.path.expanduser("~"+"\\Box Sync\\DellMed\\Data\\2004period\\LinkPE04USUnl.dat")
#NameOfBirthFile = os.path.expanduser("~"+"\\Box Sync\\DellMed\\Data\\2004period\\LinkPE04USDen.dat")
#
NameOfBirthFile = os.path.expanduser("~"+"\\Box Sync\\DellMed\\Data\\2008cohort\\VS08LKBC.DUSDENOM")
NameOfUnlinkedDeathFile = os.path.expanduser("~"+"\\Box Sync\\DellMed\\Data\\2008cohort\\VS08LKBC.USUNMPUB")
NameOfLinkedDeathFile = os.path.expanduser("~"+"\\Box Sync\\DellMed\\Data\\2008cohort\\VS08LKBC.USNUMPUB")
# vector of fields to read
LinkedDeathColumns = ['RESTATUS','SEX','COMBGEST','ESTGEST','OBGEST_FLG','BRTHWGT','AGED','DOB_YY','DPLURAL','DTHYR']
UnlinkedDeathColumns = ['RESTATUS','SEX','COMBGEST','ESTGEST','OBGEST_FLG','BRTHWGT','AGED','DOB_YY','DPLURAL','DTHYR']
BirthsColumns = ['RESTATUS','SEX','COMBGEST','ESTGEST','OBGEST_FLG','BRTHWGT','AGED','DOB_YY','DPLURAL','DTHYR']
# read data into a pandas dataframe
LinkedDeaths = IO.readCDC(NameOfLinkedDeathFile,LinkedDeathColumns)
UnlinkedDeaths = IO.readCDC(NameOfUnlinkedDeathFile,UnlinkedDeathColumns)
Births = IO.readCDC(NameOfBirthFile,BirthsColumns)
# add a neonatal death boolean column to the death tables
LinkedDeaths['NEONDTH'] = LinkedDeaths.apply(lambda row: int(row.AGED) < 28, axis='columns')
UnlinkedDeaths['NEONDTH'] = UnlinkedDeaths.apply(lambda row: int(row.AGED) < 28, axis='columns')
# print numbers of deaths and neonatal deaths in both linked and unlinked data
total_linked_deaths = len(LinkedDeaths)
total_unlinked_deaths = len(UnlinkedDeaths)
total_deaths = total_linked_deaths + total_unlinked_deaths
total_linked_neonatal_deaths = (LinkedDeaths.NEONDTH == True).sum()
total_unlinked_neonatal_deaths = (UnlinkedDeaths.NEONDTH == True).sum()
total_neonatal_deaths = total_linked_neonatal_deaths + total_unlinked_neonatal_deaths
#
print('Resident and Nonresident Linked and Unlinked Infant Deaths')
print(f'Linked   {total_linked_deaths:6}   deaths, {total_linked_neonatal_deaths:6} neonatal deathes')
print(f'Unlinked {total_unlinked_deaths:6}   deaths, {total_unlinked_neonatal_deaths:6} neonatal deathes')
print(f'All      {total_deaths:6}   deaths, {total_neonatal_deaths:6} neonatal deaths\n')
#
# Remove nonresidents from the data and recalculate the totals numbers
UnlinkedDeaths = UnlinkedDeaths[UnlinkedDeaths.RESTATUS != '4']
LinkedDeaths = LinkedDeaths[LinkedDeaths.RESTATUS != '4']
Births = Births[Births.RESTATUS != '4']
# calculate totals for residents only data
unlinked_resident_deaths = len(UnlinkedDeaths)
unlinked_resident_neonatal_deaths = (UnlinkedDeaths.NEONDTH == True).sum()
linked_resident_deaths  = len(LinkedDeaths)
linked_resident_neonatal_deaths = (LinkedDeaths.NEONDTH == True).sum()
total_resident_deaths = unlinked_resident_deaths + linked_resident_deaths
total_resident_neonatal_deaths = unlinked_resident_neonatal_deaths + linked_resident_neonatal_deaths
resident_births = len(Births)
print('Resident Linked and Unlinked Infant Deaths')
#
print(f'Linked   {linked_resident_deaths:6}   deaths, {linked_resident_neonatal_deaths:6} neonatal deathes')
print(f'Unlinked {unlinked_resident_deaths:6}   deaths, {unlinked_resident_neonatal_deaths:6} neonatal deathes')
print(f'All      {total_resident_deaths:6}   deaths, {total_resident_neonatal_deaths:6} neonatal deaths\n')
# merge the linked and unlinked resident deaths
# call the merged data Deaths which implies All Death records
Deaths = pd.concat([LinkedDeaths,UnlinkedDeaths],ignore_index=False,join='inner')
#
#ResidentBirths = Births[Births.RESTATUS != '4']
# some other foo may need to reside here to "correct" the numbers of records
# to agree with the numbers in some published user guide. 
#
# remove the deaths where combgest is unknown ( COMBGEST == 99 or " ")
# we are going to plot this stuff as a function of gestational age so
# it makes sense to filter it out
KnownGADeaths = Deaths.query("COMBGEST!='  '&COMBGEST!='99'")
# same for births
KnownGABirths = Births.query("COMBGEST!='  '&COMBGEST!='99'")
#df2004Den = df2004Den.query("COMBGEST!='  '&COMBGEST!='99'")
# now grab the neonatal death records. 
ResidentNeonatalDeaths = KnownGADeaths.query("NEONDTH==True")
#df2004neon = df2004deaths.query("NEONDTH==True")
# count the instances of neonatal death by gestational age
NeonatalDeathCount = ResidentNeonatalDeaths['COMBGEST'].value_counts().sort_index()
#neodthcnt = df2004neon['COMBGEST'].value_counts().sort_index()
plt.figure(1)
# Neonatal deaths 
dead = NeonatalDeathCount.plot.bar()
#dead = neodthcnt.plot.bar()
dead.set_title("Neonatal deaths 2004",fontsize=18)
dead.set_xlabel("Gestational Age (COMBGEST)",fontsize=16)
dead.set_ylabel("Deaths",fontsize=16)
# find the number of births at gestational age
BirthCount = KnownGABirths['COMBGEST'].value_counts().sort_index()
#brthcount = df2004Den['COMBGEST'].value_counts().sort_index()
# calculate the probability based on residents birth totals.
NeonatalDeathProbability = NeonatalDeathCount/BirthCount
#neoprob = neodthcnt/brthcount
# Probability of Neonatal Death
plt.figure(2)
probdead = NeonatalDeathProbability.plot.bar()
#probdead = neoprob.plot.bar()
probdead.set_title("Probability of neonatal Death 2004",fontsize=18)
probdead.set_xlabel("Gestational Age (COMBGEST)",fontsize=16)
probdead.set_ylabel("Probability",fontsize=16)
#Total Deaths
TotalDeathCount = KnownGADeaths['COMBGEST'].value_counts().sort_index()
#totaldeadcnt = df2004deaths['COMBGEST'].value_counts().sort_index()
plt.figure(3)
totaldead = TotalDeathCount.plot.bar()
#totaldead = totaldeadcnt.plot.bar()
totaldead.set_title("Infant Death 2004",fontsize=18)
totaldead.set_xlabel("Gestational Age (COMBGEST)",fontsize=16)
totaldead.set_ylabel("Deaths",fontsize=16)
#births
plt.figure(4)
#ResidentBirthsCount = KnownGABirths['COMBGEST'].value_counts().sort_index()
#births = df2004Den['COMBGEST'].value_counts().sort_index()
#birthplot = ResidentBirthsCount.plot.bar()
birthplot = BirthCount.plot.bar()
birthplot.set_title("Births 2004",fontsize=18)
birthplot.set_xlabel("Gestational Age (COMBGEST)",fontsize=16)
birthplot.set_ylabel("Births",fontsize=16)