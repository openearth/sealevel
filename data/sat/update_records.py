#!/usr/bin/env python
import os
import re
import datetime

import netCDF4

name_re = re.compile(r'.*_y(?P<year>\d+)_m(?P<month>\d+).nc')
unit = "seconds since 1970-01-01z00:00"

files = [f for f in os.listdir(".") if f.startswith('record_') and f.endswith('.nc')]
for filename in files:
    match = name_re.search(filename).groupdict()
    ds = netCDF4.Dataset(filename, "a")
    var = ds.createVariable("time", "double", dimensions=("record",))
    var.units = unit
    date = datetime.datetime(int(match["year"]), int(match["month"]), 1)
    datenum = netCDF4.date2num([date], unit)
    var[0] = datenum
    ds.close()

