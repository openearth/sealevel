"""
This is a minimal example on how to retrieve data from water info.
Make sure to set up a path to store the resulting dataframe.
"""

from ddlpy import ddlpy
import datetime
import matplotlib
import pandas as pd
import numpy as np
import os

path = '../data/ddl/raw/'
# get all locations
locations = ddlpy.locations()

#select a set of parameters
# and a set of stations
code= 'WATHTE'
unit= 'NAP'
station= ['DNHV', 'HARLGN', 'HARL', 'HOEKVHLD', 'HOEK', 'HOEKVHLNDDM','VLIS', 'VLISSGN']

# Filter the locations dataframe with the desired parameters and stations.
selected= locations[locations.index.isin(station)]

selected = selected[(selected['Grootheid.Code'] == code) &
                      (selected['Hoedanigheid.Code'] == unit) ].reset_index()

# Obtain measurements per parameter row
#index= 0
for index in range(len(station)):
    print('station:', station[index])
    location= selected.loc[index]

    # This is parallel as ddlpy.measurements
    for year in np.arange(2000, 2020):
        start_date = datetime.datetime(year, 1, 1)
        end_date = datetime.datetime(year, 12, 31)
        print('Starting collecting info for year %d...'%year)

        try:
            measurements = ddlpy.measurements(location, start_date=start_date, end_date=end_date)
            if (len(measurements)>0):
                print('Data was found in Waterbase. Saving data in csv.')
                measurements.to_csv(path+"%s_%s_%s_%d.csv"%(location.Code, code, unit, year), index= False)
            else:
                print('Measurements returned table with 0 elements.')
        except:
            print('Data could not be collected.')
            continue
