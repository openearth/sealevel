#!/usr/bin/env python
import pathlib
import sys

import pandas as pd

path = pathlib.Path(sys.argv[1])
new_filename = path.with_suffix('.json').name
df = pd.read_csv(path)
df.to_json(new_filename, orient='records')
