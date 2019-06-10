# -*- coding: utf-8 -*-
import pandas as pd
# Filter data
#
def remove_nonresidents(table,inplace=False):
    """
    Remove non-residents from data table.
    
    Records for non-resident occurances are removed from the table. 
    
    Parameters:
    table: (pandas dataframe) A pandas dataframe containing CDC Infant Death
    or live birth data. 
        
    inplace: (boolean) Flag controlling filter. If true, non-resident occurances
    are removed from the table and the input table is modified. If False, the
    input table is not altered and a new table is returned.
    
    Returns:
    A pandas dataframe with records removed or nothing.
        """
    if inplace:
        table.drop(table[table.residence_status==4].index,inplace=inplace)
    else:
        return table.drop(table[table.residence_status==4].index,inplace=inplace)
#
# remove records for which no age estimate exists. 
# check for both clinical and obstetric age estimates 
#
def remove_unknown_gestation_age(table,inplace=False):
    """
    find the table entries that have no gestational age estimate.
 
    Records with no clinical and no obstetric age estimate have no 
    estimate at all and are removed. If inplace is true the
    records are removed from the input table. If false, the input table is
    left unchanged and another table is returned that contains only records 
    for which at least one estimate of gestational age exists.
    
    Parameters:
    table: (pandas dataframe) A pandas dataframe containing CDC Infant Death
    or live birth data.
    
    inplace: (boolean) Flag controling filter. If true rows containing no 
    estimate are removed from the table in place. If false a new table is 
    created that has only rows with at least one estimate of gestational age.
    
    Returns:
    A pandas dataframe with records removed or nothing.

    """     
#
    noestimate = table[((table.gestation_in_weeks==99) & (table.clinical_gestation_estimate==99))
    |((table.gestation_in_weeks==99)&(table.clinical_gestation_estimate.isna()))
    |((table.gestation_in_weeks.isna())&(table.clinical_gestation_estimate==99))
    |((table.gestation_in_weeks.isna())&(table.clinical_gestation_estimate.isna()))]
    if inplace:
        table.drop(noestimate.index,inplace=inplace)
    else:
        return table.drop(noestimate.index,inplace=inplace)
            
def split_on_clinical_flag(table):
    """
    split a CDC infant death data table on clinical estimate of gestation used
    
    This function splits the input table into two separate tables. The first 
    contains records for which the flag indicating use of the clinical estimage
    of gestational age is 1 (True). The other table contains records for which
    the clinical estimate flag is != 1 (False). 
    
    Parameters:
    table: (pandas dataframe) A pandas dataframe containing CDC infant death data.
    
    Returns:
    (clinical,obstetric) a tuple of dataframes containing records that use 
    clinical and obstetric estimates of gestational age respectively.
    """
    clinical = table[table.clinical_estimate_of_gestation_used_flag==1]
    obstetric = table[table.clinical_estimate_of_gestation_used_flag!=1]
    return (clinical,obstetric)
# this function splits the table into neonatal deaths and remaining deaths
def extract_neonatal_deaths(table):
    """ 
    returns a tuple of data talbes. The first table is all neonatal deaths, the
    second is other deaths. 
    
    This function splits a data table in two. The result is two tables that
    contain records for which age_at_death_in_days is less than 28 and the 
    other table contains records for which age_at_death_in_days is 28 days and
    up. 
    
    Parameters:
        table(pandas dataframe) a table of CDC infant death records
        
    Returns:
        (neon,other) a tuple of dataframes containing neonatal deaths and other
        non neonatal deaths.
    """
    neon = table[table.age_at_death_in_days<28]
    other = table[table.age_at_death_in_days>=28]
    return (neon,other)
def remove_unknown_clinical_age(table,inplace=False):
    """ 
    returns table with unknown clinical age estimate records removed
    
    This function removes the records in the table which contain unknown or 
    NA values for the clinical estimate of age. Clinical estimate is assumed 
    to be contained in the column, clinical_gestation_estimate.
    
    Parameters:
    table (pandas data frame) A pandas dataframe containing CDC Infant Death
    or live birth data.
    
    inplace (boolean) A flag, if inplace=True the input table is modified. If False
             a new table is returned with the records removed.
    
    Returns:
    A pandas dataframe with records removed or nothing.
    """
    noestimate = table[(table.clinical_gestation_estimate==99)|
            (table.clinical_gestation_estimate.isna())]
    if inplace:
        table.drop(noestimate.index,inplace=inplace)
    else:
        return table.drop(noestimate.index,inplace=inplace)
# this function removes unknown obstetric age records
def remove_unknown_obstetric_age(table,inplace=False):
    """
    return table with unknow obstetric age records removed
    
    This function removes the records in the table which contain unknown or
    NA values for the obstetric age. Obstetric age is assumed to be contained
    in the column gestation_in_weeks. 
    
    Parameters:
    table (pandas data frame)
    inplace (A flag, if inplace=True the input table is modified. If False
             a new table is returned with the records removed.)
    
    Returns:
    A pandas dataframe with records removed or nothing. 
    """
    noestimate = table[(table.gestation_in_weeks==99) | 
                       (table.gestation_in_weeks.isna())]
    if inplace:
        table.drop(noestimate.index,inplace=inplace)
    else:
        return table.drop(noestimate.index,inplace=inplace)
# this method returns a series that contains the number of records corresponding
# to the input column. The series is sorted by value. For example, if the
# column is gestational age then the number of records for each week of age 
# is counted the weeks are then sorted.        
def count_and_sort(table,column):
    """
    Count values in column and sort result.
    
    This method counts the number of distinct occurances of a particular value
    in a column of a table and sorts the result by the index. For example, if
    the column contains gestational ages in weeks the method counts the number 
    of occurances of each gestational age and returns a sorted list of the results.
    
    Parameters:
    table (pandas dataframe)
    column (the column name to count)
    
    Returns:
    A pandas data table with the count of data in the given column.
    """
    return table[column].value_counts(dropna=False).sort_index()
#
def GA(row):
    """
    return a correct gestational age
    
    This function examines the gestational ages and flags and returns
    a usable gestational age based on those values. The input row should 
    contain at least one usable gestational age. 
    
    Parameters:
    row (row of a pandas dataframe) 
    
    returns: 
    a value to be used for gestational age
    """
    # return clinical estimate if clinical used flag is true and a
    # clinical estimage exists. Otherwise return obstetric
    if row['clinical_estimate_of_gestation_used_flag'] == 1:
        if (row['clinical_gestation_estimate']==99) | pd.isna(row['clinical_gestation_estimate']):
            return row['gestation_in_weeks']
        else:
            return row['clinical_gestation_estimate']
    # return obstetric estimate if clinical used flag is false and an obstetric
    # estimate exists. Otherwise return clinical
    else:
        if (row['gestation_in_weeks'] == 99) | pd.isna(row['gestation_in_weeks']):
            return row['clinical_gestation_estimate']
        else:
            return row['gestation_in_weeks']
#
def GATYPE(row):
    """
    return what type of gestational age is used
    
    This function examines the gestational ages and flags in a record
    and returns the type of gestational age used in this record based
    on those values. The possible return types are 'CLN' and 'OBS'. These
    correspond to clinical and obstetric estimates respectively.
    
    Parameters:
    row (row of a pandas dataframe)
    
    returns:
    A string, either 'CLN' or 'OBS'.
    """
    if row['clinical_estimate_of_gestation_used_flag'] == 1:
        if (row['clinical_gestation_estimate']==99) | pd.isna(row['clinical_gestation_estimate']):
            return('OBS')
        else:
            return('CLN')
    else:
        if(row['gestation_in_weeks'] == 99) | pd.isna(row['gestation_in_weeks']):
            return('CLN')
        else:
            return('OBS')
#
def hella():
    print(f'hello from CDCFilters')