import pathlib

import netCDF4
import numpy as np
import pandas as pd

import slr


def make_wind_df(lat_i=53, lon_i=3, product="NCEP1", local=True):
    """create a dataset for wind, for 1 latitude/longitude"""

    src_dir = slr.get_src_dir()
    if product == "NCEP1":
        # the following url's are not available during a government shutdown
        u_file = "https://www.esrl.noaa.gov/psd/thredds/dodsC/Datasets/ncep.reanalysis.derived/surface_gauss/uwnd.10m.mon.mean.nc"
        v_file = "https://www.esrl.noaa.gov/psd/thredds/dodsC/Datasets/ncep.reanalysis.derived/surface_gauss/vwnd.10m.mon.mean.nc"

        if local:
            u_file = pathlib.Path(
                src_dir / "data/noaa/uwnd.10m.mon.mean.nc"
            ).expanduser()
            v_file = pathlib.Path(
                src_dir / "data/noaa/vwnd.10m.mon.mean.nc"
            ).expanduser()

    elif product == "20CR":
        if local:
            u_file = pathlib.Path(
                src_dir / "data/noaa/20cr.uwnd.10m.mon.mean.nc"
            ).expanduser()
            v_file = pathlib.Path(
                src_dir / "data/noaa/20cr.vwnd.10m.mon.mean.nc"
            ).expanduser()
        else:
            print(
                f"ERROR: The reanalysis product {product} first needs to be downloaded"
            )

    else:
        print(f"Reanalysis product not available: {product}")

    # open the 2 files
    ds_u = netCDF4.Dataset(u_file)
    ds_v = netCDF4.Dataset(v_file)

    # read lat,lon, time from 1 dataset
    lat, lon, time = (
        ds_u.variables["lat"][:],
        ds_u.variables["lon"][:],
        ds_u.variables["time"][:],
    )

    # check with the others
    lat_v, lon_v, time_v = (
        ds_v.variables["lat"][:],
        ds_v.variables["lon"][:],
        ds_v.variables["time"][:],
    )
    assert (lat == lat_v).all() and (lon == lon_v).all() and (time == time_v).all()

    # convert to datetime
    # Now defaults to return cftime dates https://github.com/Unidata/cftime/issues/136
    # cftime dates are not recognized by pandas
    # in cftime < 1.2.1 there is a bug that this flag doesn't not function properly
    t = netCDF4.num2date(
        time, ds_u.variables["time"].units, only_use_cftime_datetimes=False
    )

    def find_closest(lat, lon, lat_i=lat_i, lon_i=lon_i):
        """lookup the index of the closest lat/lon"""
        Lon, Lat = np.meshgrid(lon, lat)
        idx = np.argmin(((Lat - lat_i) ** 2 + (Lon - lon_i) ** 2))
        Lat.ravel()[idx], Lon.ravel()[idx]
        [i, j] = np.unravel_index(idx, Lat.shape)
        return i, j

    # this is the index where we want our data
    i, j = find_closest(lat, lon)

    # get the u, v variables
    print("found point", lat[i], lon[j])
    u = ds_u.variables["uwnd"][:, i, j]
    v = ds_v.variables["vwnd"][:, i, j]

    # compute derived quantities
    speed = np.sqrt(u**2 + v**2)

    # compute direction in 0-2pi domain
    direction = np.mod(np.angle(u + v * 1j), 2 * np.pi)

    # put everything in a dataframe
    wind_df = pd.DataFrame(data=dict(u=u, v=v, t=t, speed=speed, direction=direction))
    wind_df = wind_df.set_index("t")

    # return it
    return wind_df


def make_annual_wind_df(wind_df):
    """Compute annual averaged wind dataset from monthly wind dataset"""

    # label set to xxxx-01-01 of the current year
    annual_wind_df = wind_df.groupby(pd.Grouper(freq="1Y", label="left")).mean()
    annual_wind_df.index = annual_wind_df.index + datetime.timedelta(days=1)
    annual_wind_df["speed"] = np.sqrt(
        annual_wind_df["u"] ** 2 + annual_wind_df["v"] ** 2
    )
    annual_wind_df["direction"] = np.mod(
        np.angle(annual_wind_df["u"] + annual_wind_df["v"] * 1j), 2 * np.pi
    )

    return annual_wind_df


def combine_linear_scaling(df1, df2):
    """Combine two reanalysis products with a linear scaling using the most
    recent one as reference"""

    date_s = df2.index[0]
    date_e = df1.index[-1]

    df1_cor = df1.copy()

    df1_cor = df1 - df1.loc[date_s:date_e].mean()
    df1_cor = df1_cor * df2.loc[date_s:date_e].std() / df1_cor.loc[date_s:date_e].std()
    df1_cor = df1_cor + df2.loc[date_s:date_e].mean()

    combined_df = pd.concat([df1_cor.loc[:date_s][:-1], df2.loc[date_s:]])

    return combined_df
