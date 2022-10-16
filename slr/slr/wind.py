import pathlib

import netCDF4
import numpy as np
import pandas as pd

import slr


def make_wind_df(lat_i=53, lon_i=3, local=True):
    """create a dataset for wind, for 1 latitude/longitude"""
    # the following url's are not available during a government shutdown
    u_file = "http://www.esrl.noaa.gov/psd/thredds/dodsC/Datasets/ncep.reanalysis.derived/surface_gauss/uwnd.10m.mon.mean.nc"
    v_file = "http://www.esrl.noaa.gov/psd/thredds/dodsC/Datasets/ncep.reanalysis.derived/surface_gauss/vwnd.10m.mon.mean.nc"

    src_dir = slr.get_src_dir()

    if local:
        u_file = pathlib.Path(src_dir / "data/noaa/uwnd.10m.mon.mean.nc").expanduser()
        v_file = pathlib.Path(src_dir / "data/noaa/vwnd.10m.mon.mean.nc").expanduser()

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
