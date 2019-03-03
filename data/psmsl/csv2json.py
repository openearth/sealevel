#!/usr/bin/env python
import pandas as pd
filename = 'gslGPChange2014.txt'
columns = ['time', 'gsl_rate (mm)', 'gsl_rate_error (mm)', 'gsl (mm)', 'gsl_error(mm)']
df = pd.read_csv(filename, names=columns, sep='\t', comment='%')
df.to_json('gsl.json', orient='records')
