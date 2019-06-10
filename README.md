# CDCDataTools
This project contains a python package with tools for reading and processing CDC data related to live birth and infant death. 
The source for the data is the National Vital Statistics System https://www.cdc.gov/nchs/nvss/linked-birth.htm

The raw data, births, linked period infant death, linked cohort infant death can be found here https://www.cdc.gov/nchs/data_access/vitalstatsonline.htm

The Dell women's health group ingested the raw CDC data and populated a database with live birth and infant death data from from the years
2008 through 2016. CSV datasets were created from this database that contain cohort data for infant deaths and live births for each year. 

The Python package has two modules. The IO module has methods to read some of the raw period linked data and all of the data as converted
by the Dell medical school women's health group. The IO module returns a pandas data frame. The CDCFilters module contains useful filters for the data. For example there is a filter 
to remove records which have no gestational age associated with it. CDCFilters methods take pandas data frames as input and return 
data frames or perform filtering in place.

Included in the package are several example python programs that manipulate the data in some way and may produce graphical output. 
In particular the DataToolsDemo.py application demonstrates most of the IO and filter tools in the package. The code is also extensively
documented. Use the python help utility to examine the documentation. 
