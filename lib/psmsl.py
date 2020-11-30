import io
import datetime

import numpy as np
import pandas as pd


def missing2nan(value, missing=-99999):
    """convert the value to nan if the float of value equals the missing value"""
    value = float(value)
    if value == missing:
        return np.nan
    return value

def year2date(year_fraction, dtype='datetime64[s]'):
    """convert a fraction of a year + fraction of a year to a date, for example 1993.083 -~> 1993-02-01.
    The dtype should be a valid numpy datetime unit, such as datetime64[s]"""
    startpoints = np.linspace(0, 1, num=12, endpoint=False)
    remainder = np.mod(year_fraction, 1)
    year = np.floor_divide(year_fraction, 1).astype('int')
    month = np.searchsorted(startpoints, remainder)
    if (month == 0).all():
        # if month is set to 0 (for annual data), set to january
        month = np.ones_like(month)
    dates = [
        datetime.datetime(year_i, month_i, 1)
        for year_i, month_i
        in zip(year, month)
    ]
    datetime64s = np.asarray(dates, dtype=dtype)
    return datetime64s

def get_data(zf, station, dataset_name):
    """get data for the station (pandas record) from the dataset (url)"""
    info = dict(
        dataset_name=dataset_name,
        id=station.name
    )
    bytes = zf.read("{dataset_name}/data/{id}.rlrdata".format(**info))
    df = pd.read_csv(
        io.BytesIO(bytes),
        sep=';',
        names=('year', 'height', 'interpolated', 'flags'),
        converters={
            "year": lambda x: float(x),
            "height": lambda x: missing2nan(x),
            "interpolated": str.strip,
        }
    )
    df['station'] = station.name
    df['t'] = year2date(df.year)
    df = df.set_index('t')
    return df

def compute_u2v2(df, wind_df):
    """compute the u2 and v2 based on the direction and alpha"""

    # convert alpha to radians and from North 0, CW to 0 east, CW
    # x * pi / 180
    alpha_in_rad = np.deg2rad(90 - df['alpha'])
    direction_in_rad = np.arctan2(df['v'], df['u'])
    # these were used in intermediate reports
    df['u2main'] = (wind_df['speed'] ** 2) * np.cos(direction_in_rad - alpha_in_rad)
    df['u2perp'] = (wind_df['speed'] ** 2) * np.sin(direction_in_rad - alpha_in_rad)
    # the squared wind speed components along and perpendicular to the coastline
    df['u2main'].fillna(df['u2main'].mean(), inplace=True)
    df['u2perp'].fillna(df['u2perp'].mean(), inplace=True)
    # we now switched to the signed mean (sometimes the wind comes from the north/east)
    df['u2'] = df['u']**2 * np.sign(df['u'])
    df['v2'] = df['v']**2 * np.sign(df['v'])
    df['u2'].fillna(df['u2'].mean(), inplace=True)
    df['v2'].fillna(df['v2'].mean(), inplace=True)

    return df

def get_data_with_wind(station, dataset_name, wind_df, annual_wind_df, zipfiles, url_names):
    """get data for the station (pandas record) from the dataset (url)"""
    info = dict(
        dataset_name=dataset_name,
        id=station.name
    )
    bytes = zipfiles[dataset_name].read(url_names[dataset_name].format(**info))
    df = pd.read_csv(
        io.BytesIO(bytes),
        sep=';',
        names=('year', 'height', 'interpolated', 'flags'),
        converters={
            "height": lambda x: missing2nan(x) - station['nap-rlr'],
            "interpolated": str.strip,
        }
    )
    df['station'] = station.name
    df['t'] = year2date(df.year, dtype=wind_df.index.dtype)
    df['alpha'] = station['alpha']
    df = df.set_index('t')
    # merge the wind and water levels
    if 'monthly' in dataset_name:
        merged = pd.merge(df, wind_df, how='left', left_index=True, right_index=True)
    else:
        merged = pd.merge(df, annual_wind_df, how='left', left_index=True, right_index=True)
    merged = compute_u2v2(merged, wind_df)


    return merged
