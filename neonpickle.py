# -*- coding: utf-8 -*-
# this script reads a sequence of infant death and live birth files 
# for each year the script calculates the probability of neonatal death
# for resident births as a function of gestational age. 
# the probability vector is then pickled for later use.
# gestational age is taken to be the value of 'combgest' from the cdc label
# which is 'gestation_in_weeks' in the database.
import pandas as pd
import os
import sys
from CDCDataTools import CDCFilters
# These are the tags or column names I will need. 
clinical_age = 'clinical_gestation_estimate'
obstetric_age = 'gestation_in_weeks'
resident = 'residence_status'
clinical_flag = 'clinical_estimate_of_gestation_used_flag'
death_age = 'age_at_death_in_days'
death_year = 'death_year'
delivery_year = 'delivery_year'
death_columns_used=[death_age,death_year,delivery_year,resident,clinical_age,obstetric_age,clinical_flag]
live_columns_used=[delivery_year,resident,clinical_age,obstetric_age,clinical_flag]
# read some data, create probability numbers for Neonatal Death
# pickle the data 
DataDirectory = os.path.expanduser("~"+"\\Box Sync\\DellMed\\Data\\TUdata\\")
headername = os.path.expanduser("~"+"\\Box Sync\\DellMed\\Data\\TUdata\\headers_infant_deaths.csv")
birthheadername = os.path.expanduser("~"+"\\Box Sync\\DellMed\\Data\\TUdata\\headers_live_births.csv")
deaths_header = pd.read_csv(headername,index_col=False,header=0)
births_header = pd.read_csv(birthheadername,index_col=False,header=0)
col_index_list=list()
for i in range(16,17):
    if (i==9) or (i==10) or (i==12):
        deadfile = DataDirectory + f'infant_deaths_20{i:02}_with_headers.csv'
    else:
        deadfile = DataDirectory + f'infant_deaths_20{i:02}_with_headers.csv'
    if i == 11:
        livefile = DataDirectory + f'live_births_20{i:02}_with_headers.csv'
    else:
        livefile = DataDirectory + f'live_births_20{i:02}.csv'
    probfile = DataDirectory + f'Probability_of_Neonatal_Death_20{i:02}.pkl'
    if(os.path.exists(deadfile) & os.path.exists(livefile)):
        #col_index_list = list()
        col_index_list.clear()
        for name in death_columns_used: # col_index_list contains column numbers
            col_index_list.append(deaths_header.columns.get_loc(name))
        infant_deaths = pd.read_csv(deadfile,index_col=False,header=0,usecols=col_index_list)
        infant_deaths.columns = death_columns_used
        #
        year=2000+i
        ds = CDCFilters.count_and_sort(infant_deaths,death_year)
        first=ds[year]
        if ds.keys().contains(year+1):
            second=ds[year+1]
        else:
            second=0
        print(ds)
        print(f'For infants born in 20{i:02}, {first} died in 20{i:02} and {second} died in 20{i+1:02}')
        #col_index_list=list()
        col_index_list.clear()
        for name in live_columns_used:
            col_index_list.append(births_header.columns.get_loc(name))
        live_births = pd.read_csv(livefile,index_col=False,header=0,usecols=col_index_list)
        live_births.columns = live_columns_used
        CDCFilters.remove_nonresidents(infant_deaths,inplace=True)
        CDCFilters.remove_nonresidents(live_births,inplace=True)
        CDCFilters.remove_unknown_gestation_age(infant_deaths,inplace=True)
        CDCFilters.remove_unknown_gestation_age(live_births,inplace=True)
        #CDCFilters.remove_unknown_obstetric_age(infant_deaths,inplace=True)
        #CDCFilters.remove_unknown_obstetric_age(live_births,inplace=True)
        #CDCFilters.remove_unknown_clinical_age(infant_deaths,inplace=True)
        #CDCFilters.remove_unknown_clinical_age(live_births,inplace=True)
        # construct the total live births table 
        in_year_deaths = infant_deaths[infant_deaths.death_year==year]
        total_births=pd.concat([live_births,in_year_deaths],ignore_index=True,sort=False)
        del in_year_deaths,live_births
        # add GA column to infant_deaths that contains clinical if flag set or 
        # if obstetric missing and obstetric otherwise. 
        infant_deaths['GA'] = infant_deaths.apply(lambda row: CDCFilters.GA(row),axis=1).astype(int)
        # add GA column to live births that contains clinical if flag set or
        # if obstetric missing and obstetric otherwise
        #live_births['GA'] = live_births.apply(lambda row: CDCFilters.GA(row),axis=1).astype(int)
        total_births['GA']=total_births.apply(lambda row: CDCFilters.GA(row),axis=1).astype(int)
        neonatal_deaths = infant_deaths[infant_deaths.age_at_death_in_days < 28]
        #deaths_vs_gestation = CDCFilters.count_and_sort(infant_deaths,'GA')
        #deaths_vs_gestation = infant_deaths['gestation_in_weeks'].value_counts().sort_index()
        total_births_vs_gestation = CDCFilters.count_and_sort(total_births,'GA')
        #births_vs_gestation = CDCFilters.count_and_sort(live_births,'GA')
        #live_births['gestation_in_weeks'].value_counts().sort_index()
        neonatal_deaths_vs_gestation = CDCFilters.count_and_sort(neonatal_deaths,'GA')
        del infant_deaths,neonatal_deaths,total_births
        #neondeath_vs_gestation = neonatal_deaths['gestation_in_weeks'].value_counts().sort_index()
        #del neonatal_deaths
        #births_vs_gestation = live_births['gestation_in_weeks'].value_counts().sort_index()
        #del live_births
        #total_births_vs_gestation = births_vs_gestation.to_frame().add(deaths_vs_gestation.to_frame(),axis=1,fill_value=0)
        #total_births_vs_gestation = deaths_vs_gestation + births_vs_gestation
        #del births_vs_gestation
        #del deaths_vs_gestation
        probability_of_neonatal_death = neonatal_deaths_vs_gestation.to_frame().divide(total_births_vs_gestation.to_frame(),axis=1,fill_value=0)
        del neonatal_deaths_vs_gestation, total_births_vs_gestation
        probability_of_neonatal_death.to_pickle(probfile)
        del probability_of_neonatal_death
        print(f'finished with 20{i:02}')
    else:
        print(f'Missing input file for 20{i:02}')
        sys.exit(0)
