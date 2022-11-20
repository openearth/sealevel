import pandas as pd

import ipywidgets
import IPython.display

def fits_to_fits_df(fits):
    """add information to a list of fits and convert it to data frame"""
    for row in fits:
        row['aic'] = row['fit'].aic
        row['F'] = row['fit'].fvalue
        row['df_model'] = row['fit'].df_model
        row['prediction'] = row['fit'].get_prediction()

    for row in fits:
        # does this model have tide included
        has_tide = 'Nodal U' in row['names'] and 'Nodal V' in row['names']
        row['has_tide'] = has_tide

        # does this model have wind included
        has_wind = 'Wind $u^2$' in row['names'] and 'Wind $v^2$' in row['names']
        row['has_wind'] = has_wind


    # add exogenuous table, this column will be added later (dataframe in dataframe should be added as a column)
    exogs = []
    # add prediction with mean wind and tide
    for row in fits:
        # lookup the values that were used for this prediction
        exog_df = pd.DataFrame(
            row['fit'].model.exog,
            columns=row['names']
        )
        exogs.append(exog_df)

        if row['has_tide']:
            exog_mean_tide_df = exog_df.copy()
            exog_mean_tide_df['Nodal U'] = exog_mean_tide_df['Nodal U'].mean()
            exog_mean_tide_df['Nodal V'] = exog_mean_tide_df['Nodal V'].mean()
            row['prediction_mean_tide'] = row['fit'].get_prediction(exog=exog_mean_tide_df)
        if row['has_wind']:
            exog_mean_wind_df = exog_df.copy()
            exog_mean_wind_df['Wind $u^2$'] = exog_mean_wind_df['Wind $u^2$'].mean()
            exog_mean_wind_df['Wind $v^2$'] = exog_mean_wind_df['Wind $v^2$'].mean()
            row['prediction_mean_wind'] = row['fit'].get_prediction(exog=exog_mean_wind_df)
        if row['has_wind'] and row['has_tide']:
            # set both wind and tide to mean/0
            exog_mean_tide_mean_wind_df = exog_df.copy()
            exog_mean_tide_mean_wind_df['Nodal U'] = 0
            exog_mean_tide_mean_wind_df['Nodal V'] = 0
            exog_mean_tide_mean_wind_df['Wind $u^2$'] = exog_mean_tide_mean_wind_df['Wind $u^2$'].mean()
            exog_mean_tide_mean_wind_df['Wind $v^2$'] = exog_mean_tide_mean_wind_df['Wind $v^2$'].mean()
            row['prediction_mean_tide_mean_wind'] = row['fit'].get_prediction(exog=exog_mean_tide_mean_wind_df)


    fits_df = pd.DataFrame(fits)
    fits_df['exog'] = exogs

    return fits_df

def side_by_side_tables(tables):
    """show jupyter notebook tables side by side"""
    widgets = []
    for row in tables:
        widget = ipywidgets.widgets.Output()
        with widget:
            table = row["table"]
            styled = (
                table.style.set_caption(row["title"])
                .format({"height": "{:.1f}", "height - surge": "{:.1f}"})
                .format_index(lambda v: v.strftime("%Y"))
            )
            IPython.display.display(styled)
            # table.info()
        widgets.append(widget)

    # add some CSS styles to distribute free space
    box_layout = ipywidgets.Layout(
        display="flex", flex_flow="row", justify_content="space-around", width="auto"
    )

    # create Horisontal Box container
    hbox = ipywidgets.widgets.HBox(widgets, layout=box_layout)
    return hbox


def top_n_tables(selected_stations, top_n=7):
    """Create a list of tables with top n's"""
    station_tables_waterlevel = []
    station_tables_surge = []
    nl_tables = []
    for _, station in selected_stations.iterrows():
        top_waterlevel = (
            station["rlr_annual"]
            .sort_values("height", ascending=False)
            .reset_index()
            .set_index("t")[["height"]]
            .head(n=top_n)
        )
        row = {
            "title": f"Top {top_n} highest waterlevels ({station['name']})",
            "table": top_waterlevel,
        }
        if "Netherlands" in station["name"]:
            nl_tables.append(row)
        else:
            station_tables_waterlevel.append(row)
    for _, station in selected_stations.iterrows():
        annual_df = station["rlr_annual"]
        top_surge = (
            annual_df.sort_values("height - surge", ascending=False)
            .reset_index()
            .set_index("t")[["height - surge"]]
            .head(n=top_n)
        )
        row = {
            "title": f"Top {top_n} highest waterlevel - surge ({station['name']})",
            "table": top_surge,
        }
        if "Netherlands" in station["name"]:
            nl_tables.append(row)
        else:
            station_tables_surge.append(row)
    IPython.display.display(side_by_side_tables(nl_tables))
    IPython.display.display(side_by_side_tables(station_tables_waterlevel))
    IPython.display.display(side_by_side_tables(station_tables_surge))
