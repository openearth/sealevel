#!/usr/bin/env python
import pandas as pd

df = pd.read_excel('SLR_database.xlsx')
df.to_json('SLR_database.json', orient='records')
