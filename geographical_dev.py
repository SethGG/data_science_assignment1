# Geographical Development: visualize the sales volume (as above) and the average
# rating per country in a geographical setting (using the geopandas package, see more
# information below) , for example the number of customers per country over time. The goal is
# again to give management as much geographic insight as possible.

import pandas as pd
import geopandas as gpd
import pycountry
import json
from preprocessing import ratings_country, sales
from bokeh.io import output_file
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar, TabPanel, Tabs, HoverTool
from bokeh.plotting import figure
from bokeh.palettes import Iridescent23, TolYlOrBr9, RdYlGn8


shapefile = "geo/ne_110m_admin_0_countries.shp"
gdf = gpd.read_file(shapefile)[["ADMIN", "ADM0_A3", "geometry"]]
gdf.columns = ["country", "country_code", "geometry"]
gdf = gdf.drop(gdf.index[159])


def convert_country_name(code):
    return pycountry.countries.get(alpha_2=code).alpha_3


monthly_grouper = pd.Grouper(key="Date", freq="ME")
ratings_country["Country"] = ratings_country["Country"].apply(convert_country_name)
monthly_summary_ratings = ratings_country.groupby([monthly_grouper, "Country"]).agg(
    {"Daily Average Rating": "mean", "Total Average Rating": "last"})

monthly_grouper = pd.Grouper(key="Datetime", freq="ME")
sales["Country"] = sales["Buyer Country"].apply(convert_country_name)
monthly_summary_sales = sales.groupby([monthly_grouper, "Country"]).size().to_frame("Sales")
monthly_summary_sales["Sales Change"] = monthly_summary_sales.groupby(level=1)["Sales"].diff()


def monthly_figure(title, monthly_summary, month, attribute, palette, low, high, color_title):
    month_data = monthly_summary.loc[month,]
    merged = gdf.merge(month_data, left_on="country_code", right_on="Country", how="left")

    geosource = GeoJSONDataSource(geojson=json.dumps(json.loads(merged.to_json())))

    color_mapper = LinearColorMapper(palette=palette, low=low, high=high, nan_color="silver")
    color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8, width=500,
                         height=20, location=(0, 0), orientation="horizontal", title=color_title)

    fig = figure(
        title=title,
        height=600,
        width=1200,
        toolbar_location="right",
        tools=["wheel_zoom", "pan", "reset"],
        background_fill_color="#fafafa"
    )

    fig.xgrid.grid_line_color = None
    fig.ygrid.grid_line_color = None

    fig.patches('xs', 'ys', source=geosource, fill_alpha=1, line_width=0.5, line_color="black",
                fill_color={"field": attribute, "transform": color_mapper})
    fig.add_layout(color_bar, "below")

    return fig


ratings_tabs = []
ratings_figs = []
ratings_daily_tabs = []
ratings_daily_figs = []
for month in monthly_summary_ratings.index.get_level_values("Date").unique():
    fig = monthly_figure("Geographical Total Average Rating", monthly_summary=monthly_summary_ratings,
                         month=month, attribute="Total Average Rating", palette=Iridescent23, low=0, high=5,
                         color_title="Rating Score")
    fig.add_tools(HoverTool(tooltips=[('Country', '@country'), ('Total Average Rating', '@{Total Average Rating}')]))
    ratings_figs.append(fig)
    ratings_tabs.append(TabPanel(child=fig, title=month.strftime("%b %Y")))

    fig = monthly_figure("Geographical Daily Average Rating", monthly_summary=monthly_summary_ratings,
                         month=month, attribute="Daily Average Rating", palette=Iridescent23, low=0, high=5,
                         color_title="Rating Score")
    fig.add_tools(HoverTool(tooltips=[('Country', '@country'), ('Daily Average Rating', '@{Daily Average Rating}')]))
    ratings_daily_figs.append(fig)
    ratings_daily_tabs.append(TabPanel(child=fig, title=month.strftime("%b %Y")))
ratings_panel = TabPanel(child=Tabs(tabs=ratings_tabs), title="Geographical Total Average Rating")
ratings_daily_panel = TabPanel(child=Tabs(tabs=ratings_daily_tabs), title="Geographical Daily Average Rating")


sales_tabs = []
sales_figs = []
sales_dif_tabs = []
sales_dif_figs = []
for month in monthly_summary_sales.index.get_level_values("Datetime").unique():
    fig = monthly_figure("Geographical Sales (Volume)", monthly_summary=monthly_summary_sales,
                         month=month, attribute="Sales", palette=TolYlOrBr9, low=0, high=45,
                         color_title="Sales Volume")
    fig.add_tools(HoverTool(tooltips=[('Country', '@country'), ('Sales Volume', '@Sales')]))
    sales_figs.append(fig)
    sales_tabs.append(TabPanel(child=fig, title=month.strftime("%b %Y")))

    fig = monthly_figure("Geographical Sales (Difference from Previous Month)", monthly_summary=monthly_summary_sales,
                         month=month, attribute="Sales Change", palette=RdYlGn8[::-1], low=-30, high=30,
                         color_title="Sales Difference")
    fig.add_tools(HoverTool(tooltips=[('Country', '@country'), ('Sales Difference', '@{Sales Change}')]))
    sales_dif_figs.append(fig)
    sales_dif_tabs.append(TabPanel(child=fig, title=month.strftime("%b %Y")))
sales_panel = TabPanel(child=Tabs(tabs=sales_tabs), title="Geographical Sales Volume")
sales_dif_panel = TabPanel(child=Tabs(tabs=sales_dif_tabs), title="Geographical Sales Difference")


for fig in ratings_figs:
    fig.x_range = ratings_figs[0].x_range
    fig.y_range = ratings_figs[0].y_range
    fig.tools = ratings_figs[0].tools

for fig in ratings_daily_figs:
    fig.x_range = ratings_daily_figs[0].x_range
    fig.y_range = ratings_daily_figs[0].y_range
    fig.tools = ratings_daily_figs[0].tools

for fig in sales_figs:
    fig.x_range = sales_figs[0].x_range
    fig.y_range = sales_figs[0].y_range
    fig.tools = sales_figs[0].tools

for fig in sales_dif_figs:
    fig.x_range = sales_dif_figs[0].x_range
    fig.y_range = sales_dif_figs[0].y_range
    fig.tools = sales_dif_figs[0].tools

output_file("vis4.html")

fig = Tabs(tabs=[ratings_panel, ratings_daily_panel, sales_panel, sales_dif_panel])
# show(fig)
