import pyproj
import numpy as np
import pandas as pd

import bokeh
import bokeh.plotting
import bokeh.tile_providers

import windrose

import cmocean
import matplotlib.colors
import matplotlib.pyplot as plt
import seaborn as sns


WEBMERCATOR = pyproj.Proj("epsg:3857")
WGS84 = pyproj.Proj("epsg:4326")


def stations_map(stations, selected_stations):
    """show all the stations on a map"""

    # compute the bounds of the plot
    sw = (50, -5)
    ne = (55, 10)
    # transform to web mercator
    wgs2web = pyproj.Transformer.from_proj(WGS84, WEBMERCATOR, always_xy=True)
    sw_wm = wgs2web.transform(sw[1], sw[0])
    ne_wm = wgs2web.transform(ne[1], ne[0])
    # create a plot
    fig = bokeh.plotting.figure(
        tools="pan, wheel_zoom",
        plot_width=600,
        plot_height=200,
        x_range=(sw_wm[0], ne_wm[0]),
        y_range=(sw_wm[1], ne_wm[1]),
    )
    fig.axis.visible = False
    # add some background tiles

    fig.add_tile(bokeh.tile_providers.get_provider("STAMEN_TERRAIN"))
    # add the stations
    x, y = wgs2web.transform(np.array(stations.lon), np.array(stations.lat))
    fig.circle(x, y)
    x, y = wgs2web.transform(
        np.array(selected_stations.lon), np.array(selected_stations.lat)
    )
    _ = fig.circle(x, y, color="red")
    return fig


def wind_plot(wind_df):
    """Create a plot with wind data"""
    # create a wide figure, showing 2 wind roses with some extra info
    fig = plt.figure(figsize=(13, 6))
    # we're creating 2 windroses, one boxplot
    ax = fig.add_subplot(1, 2, 1, projection="windrose")
    ax = windrose.WindroseAxes.from_ax(ax=ax)
    # from radians 0 east, ccw to 0 north cw, use meteo convention of "wind from" (270 - math degrees)
    # see for example: http://colaweb.gmu.edu/dev/clim301/lectures/wind/wind-uv.html
    wind_direction_meteo = np.mod(270 - (360.0 * wind_df.direction / (2 * np.pi)), 360)
    # create a box plot
    ax.box(
        wind_direction_meteo,
        wind_df.speed,
        bins=np.arange(0, 8, 1),
        cmap=cmocean.cm.speed,
    )
    ax.legend(loc="best")

    # and a scatter showing the seasonal pattern (colored by month)
    ax = fig.add_subplot(
        1, 2, 2, projection="polar", theta_direction=-1, theta_offset=np.pi / 2.0
    )
    N = matplotlib.colors.Normalize(1, 12)
    months = [x.month for x in wind_df.index]
    sc = ax.scatter(
        # here we need radians, but again use math -> meteo conversion
        (np.pi + np.pi / 2) - wind_df.direction,
        wind_df.speed,
        c=months,
        cmap=cmocean.cm.phase,
        vmin=0,
        vmax=12,
        alpha=0.5,
        s=10,
        edgecolor="none",
    )
    _ = plt.colorbar(sc, ax=ax)
    _ = fig.suptitle("wind from, average/month\nspeed [m/s] and direction [deg]")


def surge_vs_wind(gtsm_df, annual_wind_df):
    """create a plot of surge height versus wind"""

    annual_wind_df["year"] = [x.year for x in annual_wind_df.index]
    gtsm_df["year"] = [x.year for x in gtsm_df["t"]]

    fig, axes = plt.subplots(ncols=2, figsize=(13, 6))
    wind_gtsm_df = pd.merge(
        annual_wind_df,
        gtsm_df.query('name =="NL"').drop(columns=["year"]),
        left_index=True,
        right_on="t",
        how="right",
    )
    wind_gtsm_stations_df = pd.merge(
        annual_wind_df,
        gtsm_df.query('name != "NL"'),
        left_index=True,
        right_on="t",
        how="right",
    )
    wind_gtsm_df.plot.scatter(
        "u",
        "v",
        c=wind_gtsm_df["surge"],
        cmap=matplotlib.cm.RdYlBu,
        ax=axes[0],
        vmin=-0.1,
        vmax=0.1,
    )

    axes[0].grid(True)
    axes[0].set_title(f"Surge height as a function of u,v")
    axes[0].set_ylim(-1, 4)
    axes[0].set_xlim(-1, 4)
    axes[1].plot(
        wind_gtsm_stations_df["speed"],
        wind_gtsm_stations_df["surge"],
        "g.",
        alpha=0.5,
        label="stations",
    )
    axes[1].plot(
        wind_gtsm_df["speed"], wind_gtsm_df["surge"], "ko", label="NL", alpha=0.5
    )
    axes[1].set_xlim(-1, 4)
    axes[1].set_ylim(-0.05, 0.15)
    axes[1].set_xlabel(f"Wind speed [m/s]")
    axes[1].set_ylabel("Surge height [m]")
    axes[1].set_title("Surge height as a function of windspeed")
    axes[1].legend()
    return fig


def wind_trends(annual_wind_products, gtsm_df):
    """show a figure with wind trends for all products"""
    fig, axes = plt.subplots(figsize=(13, 8), nrows=2, sharex=True)
    lowess = False
    for product, annual_wind_df in annual_wind_products.items():
        g = sns.regplot(
            x="year",
            y="speed",
            data=annual_wind_df,
            lowess=lowess,
            ax=axes[0],
            label=f"{product}",
            scatter_kws=dict(alpha=0.3),
        )
    g = sns.regplot(
        x="year", y="surge", data=gtsm_df.query('name=="NL"'), ax=axes[1], lowess=lowess
    )
    axes[0].set_xlabel("")
    axes[0].set_ylabel("Wind speed [m/s]")
    axes[0].legend(loc="best")
    axes[1].set_ylabel("Surge height [m]")
    axes[1].set_xlabel("Year")
    return fig
