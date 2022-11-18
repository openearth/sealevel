import ipywidgets
import IPython.display


def side_by_side_tables(tables):
    widgets = []
    for row in tables:
        widget = ipywidgets.widgets.Output()
        with widget:
            table = row["table"]
            styled = (
                table.style.set_caption(row["title"])
                .format({"height": "{:.1f}", "height-surge": "{:.1f}"})
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
        annual_df["height-surge"] = annual_df["height"] - (
            (annual_df["surge"] - annual_df["surge"].mean() * 1000)
        )
        top_surge = (
            annual_df.sort_values("height-surge", ascending=False)
            .reset_index()
            .set_index("t")[["height-surge"]]
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
