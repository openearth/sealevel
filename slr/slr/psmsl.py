import io
import datetime
import zipfile
import functools

import numpy as np
import pandas as pd
import requests

import slr
import slr.wind


def missing2nan(value, missing=-99999):
    """convert the value to nan if the float of value equals the missing value"""
    value = float(value)
    if value == missing:
        return np.nan
    return value


def year2date(year_fraction, dtype="datetime64[s]"):
    """convert a fraction of a year + fraction of a year to a date, for example 1993.083 -~> 1993-02-01.
    The dtype should be a valid numpy datetime unit, such as datetime64[s]"""
    startpoints = np.linspace(0, 1, num=12, endpoint=False)
    remainder = np.mod(year_fraction, 1)
    year = np.floor_divide(year_fraction, 1).astype("int")
    month = np.searchsorted(startpoints, remainder)
    if (month == 0).all():
        # if month is set to 0 (for annual data), set to january
        month = np.ones_like(month)
    dates = [
        datetime.datetime(year_i, month_i, 1) for year_i, month_i in zip(year, month)
    ]
    datetime64s = np.asarray(dates, dtype=dtype)
    return datetime64s


def get_data(zf, station, dataset_name):
    """get data for the station (pandas record) from the dataset (url)"""
    info = dict(dataset_name=dataset_name, id=station.name)
    bytes = zf.read("{dataset_name}/data/{id}.rlrdata".format(**info))
    df = pd.read_csv(
        io.BytesIO(bytes),
        sep=";",
        names=("year", "height", "interpolated", "flags"),
        converters={
            "year": lambda x: float(x),
            "height": lambda x: missing2nan(x),
            "interpolated": str.strip,
        },
    )
    df["station"] = station.name
    # store time as t
    df["t"] = year2date(df.year)
    # use time as an index
    df = df.set_index("t")
    return df


def get_data_with_wind(
    station, dataset_name, zipfiles, monthly_wind_df=None, annual_wind_df=None
):
    """get data for the station (pandas record) from the dataset (url)"""
    if "monthly" in dataset_name:
        assert (
            monthly_wind_df is not None
        ), "for monthly dataset, please pass the monthly_wind_df argument"
    if "annual" in dataset_name:
        assert (
            annual_wind_df is not None
        ), "for annual dataset, please pass the annual_wind_df argument"
    info = dict(dataset_name=dataset_name, id=station.name)
    url_names = get_url_names()
    bytes = zipfiles[dataset_name].read(url_names[dataset_name].format(**info))
    df = pd.read_csv(
        io.BytesIO(bytes),
        sep=";",
        names=("year", "height", "interpolated", "flags"),
        converters={
            "height": lambda x: missing2nan(x) - station["nap-rlr"],
            "interpolated": str.strip,
        },
    )
    df["station"] = station.name
    # store time as t
    df["t"] = year2date(df.year, dtype="<M8[ns]")
    df["alpha"] = station["alpha"]
    df = df.set_index("t")

    # merge the wind and water levels
    if "monthly" in dataset_name:
        merged = pd.merge(
            df,
            monthly_wind_df,
            how="left",
            left_index=True,
            right_index=True,
        )
    else:
        merged = pd.merge(
            df,
            annual_wind_df,
            how="left",
            left_index=True,
            right_index=True,
        )

    # fill in missing wind
    merged["u"] = merged["u"].fillna(merged["u"].mean())
    merged["v"] = merged["v"].fillna(merged["v"].mean())
    merged["u2"] = merged["u2"].fillna(merged["u2"].mean())
    merged["v2"] = merged["v2"].fillna(merged["v2"].mean())

    # recompute speed and direction
    merged["speed"] = np.sqrt(merged["u"] ** 2 + merged["v"] ** 2)
    merged["direction"] = np.mod(np.angle(merged["u"] + merged["v"] * 1j), 2 * np.pi)

    return merged


def get_psmsl_urls(local):
    src_dir = slr.get_src_dir()
    psmsl_urls_remote = {
        "met_monthly": "http://www.psmsl.org/data/obtaining/met.monthly.data/met_monthly.zip",
        "rlr_monthly": "http://www.psmsl.org/data/obtaining/rlr.monthly.data/rlr_monthly.zip",
        "rlr_annual": "http://www.psmsl.org/data/obtaining/rlr.annual.data/rlr_annual.zip",
    }
    psmsl_data_dir = src_dir / "data" / "psmsl"
    psmsl_urls_local = {
        "met_monthly": psmsl_data_dir / "met_monthly.zip",
        "rlr_monthly": psmsl_data_dir / "rlr_monthly.zip",
        "rlr_annual": psmsl_data_dir / "rlr_annual.zip",
    }
    if local:
        psmsl_urls = psmsl_urls_local
    else:
        psmsl_urls = psmsl_urls_remote
    return psmsl_urls


def get_url_names():
    url_names = {
        "datum": "{dataset_name}/RLR_info/{id}.txt",
        "diagram": "{dataset_name}/RLR_info/{id}.png",
        "url": "http://www.psmsl.org/data/obtaining/rlr.diagrams/{id}.php",
        "rlr_monthly": "{dataset_name}/data/{id}.rlrdata",
        "rlr_annual": "{dataset_name}/data/{id}.rlrdata",
        "met_monthly": "{dataset_name}/data/{id}.metdata",
        "doc": "{dataset_name}/docu/{id}.txt",
        "contact": "{dataset_name}/docu/{id}_auth.txt",
    }
    return url_names


def get_zipfiles(local=True):

    zipfiles = {}

    psmsl_urls = get_psmsl_urls(local=local)

    for dataset_name, psmsl_url in psmsl_urls.items():
        if local:
            zf = zipfile.ZipFile(psmsl_url)
        else:
            resp = requests.get(psmsl_url)
            # we can read the zipfile
            stream = io.BytesIO(resp.content)
            zf = zipfile.ZipFile(stream)
        zipfiles[dataset_name] = zf
    return zipfiles


def get_station_list(zf, dataset_name="rlr_annual", local=True):
    # this list contains a table of
    # station ID, latitude, longitude, station name, coastline code, station code, and quality flag
    csvtext = zf.read("{}/filelist.txt".format(dataset_name))

    stations = pd.read_csv(
        io.BytesIO(csvtext),
        sep=";",
        names=("id", "lat", "lon", "name", "coastline_code", "station_code", "quality"),
        converters={"name": str.strip, "quality": str.strip},
    )
    stations = stations.set_index("id")

    # each station has a number of files that you can look at.
    # here we define a template for each filename

    # stations that we are using for our computation
    # define the name formats for the relevant files
    url_names = get_url_names()

    # add url's
    def get_url(station, dataset_name):
        """return the url of the station information (diagram and datum)"""
        info = dict(dataset_name=dataset_name, id=station.name)
        url = url_names["url"].format(**info)
        return url

    psmsl_urls = get_psmsl_urls(local)
    for dataset_name in psmsl_urls:
        # fill in the dataset parameter using the global dataset_name
        f = functools.partial(get_url, dataset_name=dataset_name)
        # compute the url for each station
        stations[dataset_name + "_url"] = stations.apply(f, axis=1)

    return stations


def get_main_stations():
    src_dir = slr.get_src_dir()
    main_stations_path = src_dir / "data" / "deltares" / "main_stations.json"
    main_stations = pd.read_json(main_stations_path)
    main_stations = main_stations.set_index("id")
    return main_stations


def add_series_to_stations(
    selected_stations, local=True, wind_product="NCEP1", reference_point_wind=None
):
    zipfiles = get_zipfiles(local=local)

    monthly_wind_products, annual_wind_products = slr.wind.get_wind_products(
        reference_point_wind=reference_point_wind
    )

    annual_wind_df = annual_wind_products[wind_product]
    monthly_wind_df = monthly_wind_products[wind_product]
    monthly_gtsm_df, annual_gtsm_df = slr.wind.get_gtsm_dfs()

    # get data for all stations
    for dataset_name in get_psmsl_urls(local=local):
        f = functools.partial(
            # this  function  fills in missing wind with nan
            slr.psmsl.get_data_with_wind,
            dataset_name=dataset_name,
            # don't include year otherwise we get year_x and year_y
            monthly_wind_df=monthly_wind_df.drop(columns=["year"]),
            annual_wind_df=annual_wind_df.drop(columns=["year"]),
            zipfiles=zipfiles,
        )
        # look up the data for each station
        selected_stations[dataset_name] = [
            f(station) for _, station in selected_stations.iterrows()
        ]

    # add surge to stations annual data
    rlr_annual_dfs = []
    rlr_monthly_dfs = []
    met_monthly_dfs = []
    for idx, station in selected_stations.iterrows():
        annual_df = station["rlr_annual"]
        assert (
            station.ddl_id in annual_gtsm_df["ddl_id"].values
        ), f"ddl_id ({station.ddl_id}) of station: {station.name} not in gtsm"
        # add gtsm
        annual_df = pd.merge(
            annual_df,
            annual_gtsm_df[annual_gtsm_df.ddl_id == station["ddl_id"]].set_index(
                "year"
            )[["surge"]],
            left_on="year",
            right_index=True,
            how="left",
        )
        annual_df["surge"] = annual_df["surge"].fillna(annual_df["surge"].mean())
        rlr_annual_dfs.append(annual_df)

        # Add gtsm to monthly data
        rlr_monthly_df = station["rlr_monthly"]
        monthly_gtsm_df_i = monthly_gtsm_df[
            monthly_gtsm_df["ddl_id"] == station["ddl_id"]
        ]
        rlr_monthly_df = pd.merge(
            rlr_monthly_df,
            monthly_gtsm_df_i[["t", "surge"]],
            left_index=True,
            right_on="t",
            how="left",
        )
        rlr_monthly_df = rlr_monthly_df.set_index("t")
        rlr_monthly_df["surge"] = rlr_monthly_df["surge"].fillna(
            rlr_monthly_df["surge"].mean()
        )
        rlr_monthly_dfs.append(rlr_monthly_df)

        # also for the metric data

        met_monthly_df = station["met_monthly"]
        monthly_gtsm_df_i = monthly_gtsm_df[
            monthly_gtsm_df["ddl_id"] == station["ddl_id"]
        ]
        met_monthly_df = pd.merge(
            met_monthly_df,
            monthly_gtsm_df_i[["t", "surge"]],
            left_index=True,
            right_on="t",
            how="left",
        )
        met_monthly_df = met_monthly_df.set_index("t")
        met_monthly_df["surge"] = met_monthly_df["surge"].fillna(
            met_monthly_df["surge"].mean()
        )
        met_monthly_dfs.append(met_monthly_df)

    selected_stations["rlr_annual"] = rlr_annual_dfs
    selected_stations["rlr_monthly"] = rlr_monthly_dfs
    selected_stations["met_monthly"] = met_monthly_dfs

    return selected_stations


def add_aggregated_stations(selected_stations):
    """add the aggregated stations to the list, note that the psmsl_ids are hard coded."""
    aggregated_stations = [
        {
            "ddl_id": "NL",
            "name": "Netherlands",
            "psmsl_id": 10000,
            "idx": [20, 22, 23, 24, 25, 32],
        },
        {
            "ddl_id": "NL-DELFZL",
            "name": "Netherlands (without Delfzijl)",
            "psmsl_id": 10001,
            "idx": [20, 22, 23, 25, 32],
        },
    ]

    frames = [selected_stations]
    for aggregated_station in aggregated_stations:
        sub_selection = selected_stations.loc[aggregated_station["idx"]]
        row = {
            "name_rws": aggregated_station["name"],
            "name": aggregated_station["name"],
            "ddl_id": aggregated_station["ddl_id"],
            "location": aggregated_station["name"],
            "id": aggregated_station["psmsl_id"],
        }
        for dataset_name in ["rlr_annual", "rlr_monthly", "met_monthly"]:
            data_per_station = pd.concat(sub_selection[dataset_name].tolist())
            grouped = data_per_station[["year", "height", "u2", "v2", "surge"]].groupby(
                "t"
            )
            mean_df = grouped.mean().reset_index()
            # # filter out non-trusted part (before NAP, also with some missing stations)
            mean_df = mean_df[mean_df["year"] >= 1890].copy()
            row[dataset_name] = mean_df

        frames.append(pd.DataFrame([pd.Series(row, name=row["id"])]))
    selected_stations = pd.concat(frames)
    return selected_stations
