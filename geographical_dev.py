# Geographical Development: visualize the sales volume (as above) and the average
# rating per country in a geographical setting (using the geopandas package, see more
# information below) , for example the number of customers per country over time. The goal is
# again to give management as much geographic insight as possible.

import pandas as pd
import geopandas as gpd
import pycountry
import json
from preprocessing import ratings_country
from bokeh.io import output_file, show
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar, TabPanel, Tabs
from bokeh.plotting import figure
from bokeh.palettes import Iridescent23


shapefile = "geo/ne_110m_admin_0_countries.shp"
gdf = gpd.read_file(shapefile)[["ADMIN", "ADM0_A3", "geometry"]]
gdf.columns = ["country", "country_code", "geometry"]
gdf = gdf.drop(gdf.index[159])


def convert_country_name(code):
    return pycountry.countries.get(alpha_2=code).alpha_3


monthly_grouper = pd.Grouper(key="Date", freq="ME")
ratings_country["Country"] = ratings_country["Country"].apply(convert_country_name)
monthly_summary = ratings_country.groupby([monthly_grouper, "Country"]).agg(
    {"Daily Average Rating": "mean", "Total Average Rating": "last"})


def monthly_figure(title, month, attribute, palette, low, high):
    month_data = monthly_summary.loc[month,]
    merged = gdf.merge(month_data, left_on="country_code", right_on="Country", how="left")

    geosource = GeoJSONDataSource(geojson=json.dumps(json.loads(merged.to_json())))

    color_mapper = LinearColorMapper(palette=palette, low=low, high=high, nan_color="silver")
    color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8, width=500,
                         height=20, location=(0, 0), orientation="horizontal")

    fig = figure(
        title=title,
        height=500,
        width=1000,
        toolbar_location="right",
        tools=["wheel_zoom", "pan", "reset"]
    )

    fig.xgrid.grid_line_color = None
    fig.ygrid.grid_line_color = None

    fig.patches('xs', 'ys', source=geosource, fill_alpha=1, line_width=0.5, line_color="black",
                fill_color={"field": attribute, "transform": color_mapper})
    fig.add_layout(color_bar, "below")

    return fig


tabs = []
figs = []

for month in monthly_summary.index.get_level_values("Date").unique():
    fig = monthly_figure("Geographical Total Average Rating",
                         month=month, attribute="Total Average Rating", palette=Iridescent23, low=0, high=5)
    figs.append(fig)
    tabs.append(TabPanel(child=fig, title=month.strftime("%b %Y")))

for fig in figs:
    fig.x_range = figs[0].x_range
    fig.y_range = figs[0].y_range
    fig.tools = figs[0].tools


output_file("vis4.html")
show(Tabs(tabs=tabs))
