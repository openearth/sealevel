import datetime
import pathlib

import netCDF4
import numpy as np
import pandas as pd

import windrose
import cmocean
import matplotlib.colors
import matplotlib.pyplot as plt

import slr
import slr.utils


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
    wind_df["year"] = wind_df["t"].dt.year
    wind_df = wind_df.set_index("t")

    # return it
    return wind_df


def make_annual_wind_df(monthly_wind_df):
    """Compute annual averaged wind dataset from monthly wind dataset"""

    # label set to xxxx-01-01 of the current year
    annual_wind_df = monthly_wind_df.groupby(pd.Grouper(freq="1Y", label="left")).mean()
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


def add_u2v2(wind_df):
    """compute and add the u2 and v2 (signed squared wind)"""

    # we now switched to the signed mean (sometimes the wind comes from the north/east)
    wind_df["u2"] = wind_df["u"] ** 2 * np.sign(wind_df["u"])
    wind_df["v2"] = wind_df["v"] ** 2 * np.sign(wind_df["v"])
    wind_df["u2"].fillna(wind_df["u2"].mean(), inplace=True)
    wind_df["v2"].fillna(wind_df["v2"].mean(), inplace=True)

    return wind_df


def compute_coastal_directions(df, wind_df):
    """compute the wind in coastal directions"""
    # convert alpha to radians and from North 0, CW to 0 east, CW
    # x * pi / 180
    alpha_in_rad = np.deg2rad(90 - df["alpha"])
    direction_in_rad = np.arctan2(df["v"], df["u"])
    # these were used in intermediate reports
    df["u2main"] = (wind_df["speed"] ** 2) * np.cos(direction_in_rad - alpha_in_rad)
    df["u2perp"] = (wind_df["speed"] ** 2) * np.sin(direction_in_rad - alpha_in_rad)
    # the squared wind speed components along and perpendicular to the coastline
    df["u2main"].fillna(df["u2main"].mean(), inplace=True)
    df["u2perp"].fillna(df["u2perp"].mean(), inplace=True)

    return df


def get_wind_products(reference_point_wind=None):
    """create a list of all the wind products"""
    if reference_point_wind is None:
        reference_point_wind = {"lat": 53, "lon": 3}

    monthly_wind_products = {}
    monthly_wind_products["NCEP1"] = slr.wind.make_wind_df(
        product="NCEP1",
        lat_i=reference_point_wind["lat"],
        lon_i=reference_point_wind["lon"],
    )
    monthly_wind_products["20CR"] = slr.wind.make_wind_df(
        product="20CR",
        lat_i=reference_point_wind["lat"],
        lon_i=reference_point_wind["lon"],
    )
    monthly_wind_products["Combined"] = slr.wind.combine_linear_scaling(
        monthly_wind_products["20CR"], monthly_wind_products["NCEP1"]
    )
    for product, wind_df in monthly_wind_products.items():
        monthly_wind_products[product] = add_u2v2(wind_df)

    annual_wind_products = {}
    for product, wind_df in monthly_wind_products.items():
        annual_wind_products[product] = slr.wind.make_annual_wind_df(wind_df)
    return monthly_wind_products, annual_wind_products


def get_gtsm_dfs(with_m=False, version="2022"):
    """get the monthly and annual gtsm surge estimates per station"""
    if version == "2022":
        annual_file_name = "gtsm_surge_annual_mean_main_stations.csv"
        monthly_file_name = "gtsm_surge_monthly_mean_main_stations.csv"
    # temporary fix to compare twe datasets
    elif version == "2023":
        annual_file_name = "gtsm_surge_annual_mean_main_stations_2023.csv"
        monthly_file_name = "gtsm_surge_monthly_mean_main_stations_2023.csv"

    src_dir = slr.get_src_dir()
    annual_gtsm_df = pd.read_csv(
        src_dir / "data" / "deltares" / "gtsm" / annual_file_name,
        converters={"t": pd.to_datetime},
    )
    annual_gtsm_df = annual_gtsm_df.drop(columns=["Unnamed: 0"])
    annual_gtsm_df["year"] = annual_gtsm_df.t.dt.year

    monthly_gtsm_df = pd.read_csv(
        src_dir / "data" / "deltares" / "gtsm" / monthly_file_name,
        converters={"t": pd.to_datetime},
    )
    monthly_gtsm_df = monthly_gtsm_df.drop(columns=["Unnamed: 0"])
    # compute year fraction
    monthly_gtsm_df["year"] = [
        slr.utils.datetime2year(dt) for dt in monthly_gtsm_df["t"]
    ]

    # add unit suffix (m -> mm * 1000)
    annual_gtsm_df["surge_mm"] = annual_gtsm_df["surge"] * 1000

    monthly_gtsm_df["surge_mm"] = monthly_gtsm_df["surge"] * 1000

    # explicit use mm
    if not with_m:
        annual_gtsm_df = annual_gtsm_df.drop(columns=["surge"])
        monthly_gtsm_df = monthly_gtsm_df.drop(columns=["surge"])

    if version == "2023":
        # drop date from 1950, due to unexplainable high surge
        monthly_gtsm_df = monthly_gtsm_df[
            monthly_gtsm_df["t"] >= datetime.datetime(1951, 1, 1)
        ]
        annual_gtsm_df = annual_gtsm_df[
            annual_gtsm_df["t"] >= datetime.datetime(1951, 1, 1)
        ]

    return monthly_gtsm_df, annual_gtsm_df


def compute_wind_effect_and_anomaly(fit, names):
    """compute the wind and anomaly effect for the model"""
    u2_index = names.index("Wind $u^2$")
    v2_index = names.index("Wind $v^2$")
    u2_name = fit.model.exog_names[u2_index]
    v2_name = fit.model.exog_names[v2_index]
    u2 = fit.model.exog[:, u2_index]
    v2 = fit.model.exog[:, v2_index]

    wind_effect = fit.params.loc[u2_name] * u2 + fit.params.loc[v2_name] * v2
    wind_anomaly = wind_effect - wind_effect.mean()
    return wind_effect, wind_anomaly
