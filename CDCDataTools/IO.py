# -*- coding: utf-8 -*-
"""
Created on Tue Sep  4 13:55:04 2018

@author: semeraro-la
"""
# This module reads the ASCII encoded CDC linked infant birth/death data 
# The format is one record of data per line encoded in ascii format 
# The data is transformed to python types and placed in a dataframe. 
# Initialization
#
infant_death_filenames = {2008:'infant_deaths_2008_with_headers.csv',
                          2009:'infant_deaths_2009_with_headers.csv',
                          2010:'infant_deaths_2010_with_headers.csv',
                          2011:'infant_deaths_2011_with_headers.csv',
                          2012:'infant_deaths_2012_with_headers.csv',
                          2013:'infant_deaths_2013_with_headers.csv',
                          2014:'infant_deaths_2014_with_headers.csv',
                          2015:'infand_deaths_2015_with_headers.csv',
                          2016:'infant_deaths_2016_with_headers.csv'}
import os
import pandas as pd
__data_directory__ = None
#These dictionaries contain maps between column names and column indices in a record. The column
#names are taken from the user guide "Field" designation. See the user guide.
PL04NUM = {'RESTATUS':(137,138),'SEX':(435,436),'COMBGEST':(450,452),'ESTGEST':(445,447),
           'OBGEST_FLG':(455,456),'BRTHWGT':(466,470),'AGED':(871,874),
           'DOB_YY':(14,18),'DPLURAL':(422,423),'DTHYR':(1187,1191)}
PL04DEN = {'RESTATUS':(137,138),'SEX':(435,436),'COMBGEST':(450,452),'ESTGEST':(445,447),
           'OBGEST_FLG':(455,456),'BRTHWGT':(466,470),'AGED':(871,874),
           'DOB_YY':(14,18),'DPLURAL':(422,423),'DTHYR':(1187,1191)}
PL04UNL = {'RESTATUS':(137,138),'RESTATUSD':(1150,1151),'SEX':(435,436),'COMBGEST':(450,452),'ESTGEST':(445,447),
           'OBGEST_FLG':(455,456),'BRTHWGT':(466,470),'AGED':(871,874),
           'DOB_YY':(14,18),'DPLURAL':(422,423),'DTHYR':(1187,1191)}
PL05NUM = {'RESTATUS':(137,138),'SEX':(435,436),'COMBGEST':(450,452),'ESTGEST':(445,447),
           'OBGEST_FLG':(455,456),'BRTHWGT':(466,470),'AGED':(871,874),
           'DOB_YY':(14,18),'DPLURAL':(422,423),'DTHYR':(1187,1191)}
PL08NUM = {'RESTATUS':(137,138),'SEX':(435,436),'COMBGEST':(450,452),'ESTGEST':(445,447),
           'OBGEST_FLG':(455,456),'BRTHWGT':(466,470),'AGED':(871,874),
           'DOB_YY':(14,18),'DPLURAL':(422,423),'DTHYR':(1187,1191),'SEQNUM':(9,14)}
PL08DEN = {'RESTATUS':(137,138),'SEX':(435,436),'COMBGEST':(450,452),'ESTGEST':(445,447),
           'OBGEST_FLG':(455,456),'BRTHWGT':(466,470),'AGED':(871,874),
           'DOB_YY':(14,18),'DPLURAL':(422,423),'DTHYR':(1187,1191),'SEQNUM':(9,14)}
PL08UNL = {'RESTATUS':(137,138),'RESTATUSD':(1150,1151),'SEX':(435,436),'COMBGEST':(450,452),'ESTGEST':(445,447),
           'OBGEST_FLG':(455,456),'BRTHWGT':(466,470),'AGED':(871,874),
           'DOB_YY':(14,18),'DPLURAL':(422,423),'DTHYR':(1187,1191)}
#This variable contains a list of data file names as keys and
#the name of a variable that contains column indices as a value. 
DataFileColumnMaps = {'LinkPE04USNum.dat':PL04NUM,
                  'LinkPE04USUnl.dat':PL04UNL,
                  'VS05LINK.USNUMPUB':PL05NUM,
                  'LinkPE04USDen.dat':PL04DEN,
                  'VS08LKBC.USNUMPUB':PL08NUM,
                  'VS08LKBC.DUSDENOM':PL08DEN,
                  'VS08LKBC.USUNMPUB':PL08UNL}
# IO module for CDC raw datasets
# tries to read a file with a using the varnames
def readCDC(filename, varnames ) :
       fname = filename
       columnindexmap = DataFileColumnMaps[os.path.basename(fname)]
       datadict = {}
       # check to see it the varnames are available
       #if False in map(columnindexmap.haskey(),varnames):
       #    print("unknown variable in varnames")
       with open(fname,'rb') as f:
           count = 0
           for record in f: # parse the strings 
               for var in varnames:
                  start,end = columnindexmap[var]
                  data = record[start:end].decode('utf-8')
                  if var not in datadict:
                      datadict[var] = []
                  datadict[var].append(data)
               count = count + 1
       myframe =  pd.DataFrame(datadict)       
       return myframe
#
def readDWH(year,varnames):
#    if year in infant_death_filenames:
    try:
        filename = infant_death_filenames[year]
        if not (__data_directory__ is None):
            deadfile = os.path.join(__data_directory__,filename)
            if(os.path.exists(deadfile)):
                return pd.read_csv(deadfile,index_col=False,header=0,usecols=varnames)
        else:
            raise RuntimeError("Data directory not initialized")
    except KeyError:
        pass
       # print(f'readDWH: key {year} not present in infant_death_filenames')
#
def set_data_directory(directory):
    global __data_directory__
    if __data_directory__ is None:
        __data_directory__ = directory
    else:
        raise RuntimeError("Data directory name has already been set.")
#def print_datadir():
    #print(__data_directory__)