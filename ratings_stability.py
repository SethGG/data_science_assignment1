from preprocessing import crashes, ratings_overview
from bokeh.models import ColumnDataSource, HoverTool, FixedTicker, DatetimeTickFormatter, PrintfTickFormatter, LabelSet
from bokeh.palettes import YlGn8
from bokeh.io import output_file
from bokeh.plotting import figure, show
from bokeh.layouts import column
from bokeh.transform import linear_cmap
import pandas as pd
import numpy as np


# Ratings vs Stability: Can you come up with some Key Performance Indicators (metrics
# and scores) that help management understand how the app is doing in terms of stability and
# user satisfaction? Visualize them in a nice way. For example, the number of crashes in
# correlation with the daily average rating.


# daily_overview = crashes.set_index("Date").join(ratings_overview.set_index("Date"))
daily_grouper = pd.Grouper(key="Date", freq="W-MON")

daily_crashes = crashes.groupby(daily_grouper).mean("Daily Crashes")
daily_ratings = ratings_overview.groupby(daily_grouper).mean("Daily Average Rating")

daily_overview = daily_crashes.join(daily_ratings)

c = daily_overview["Crashes Norm"] = 1 - daily_overview["Daily Crashes"] / 100
r = daily_overview["Rating Norm"] = daily_overview["Daily Average Rating"] / 5

# (c - (0.5 - r) * (c + r) / (1 + c + r)) * (3 / 4)

daily_overview["Satisfaction Index"] = (c - (0.5 - r) * (c + r) / (1 + c + r)) * (3 / 4)

# colors_idx = [int(x*10) for x in daily_overview["Satisfaction Index"].fillna(0)]
# daily_overview["Colors"] = [Spectral10[i] for i in colors_idx]
cmap = linear_cmap(field_name="Satisfaction Index", palette=YlGn8[::-1], low=0.2, high=1)

daily_overview["Week"] = daily_overview.index.strftime("W%U")

source = ColumnDataSource(daily_overview)

output_file("vis3.html")

fig1 = figure(
    title="Weekly Ratings vs Stability",
    height=500,
    width=800,
    x_axis_label="Average Daily Crashes",
    y_axis_label="Weekly Average Rating",
    background_fill_color="#fafafa"
)

s = fig1.scatter(x="Daily Crashes", y="Daily Average Rating", size=10, source=source, color=cmap)

labels = LabelSet(x="Daily Crashes", y="Daily Average Rating", text="Week", y_offset=8,
                  text_font_size="11px", text_color="#555555",
                  source=source, text_align='center')
fig1.add_layout(labels)

color_bar = s.construct_color_bar(width=10, title="Satisfaction Index")
fig1.add_layout(color_bar, 'right')

fig2 = figure(
    height=300,
    width=800,
)

fig2.scatter(x="Date", y="Rating Norm", source=source, color="green", legend_label="Rating Norm", size=10)
fig2.line(x="Date", y="Crashes Norm", source=source, color="red", legend_label="Crashes Norm")
fig2.scatter(x="Date", y="Satisfaction Index", source=source, color="blue", legend_label="Satisfaction Index", size=10)

grid = column(fig1, fig2)
show(grid)
