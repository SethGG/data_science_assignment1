from preprocessing import crashes, ratings_overview
from bokeh.models import ColumnDataSource, HoverTool, FixedTicker, DatetimeTickFormatter, LabelSet, Title, TapTool
from bokeh.palettes import YlGn8
from bokeh.io import output_file
from bokeh.plotting import figure
from bokeh.transform import linear_cmap
import pandas as pd
import numpy as np


# Ratings vs Stability: Can you come up with some Key Performance Indicators (metrics
# and scores) that help management understand how the app is doing in terms of stability and
# user satisfaction? Visualize them in a nice way. For example, the number of crashes in
# correlation with the daily average rating.


weekly_grouper = pd.Grouper(key="Date", freq="W-MON")

weekly_crashes = crashes.groupby(weekly_grouper).mean("Daily Crashes")
weekly_ratings = ratings_overview.groupby(weekly_grouper).agg(
    {"Daily Average Rating": "mean", "Total Average Rating": "mean"})

weekly_summary = weekly_crashes.join(weekly_ratings)
weekly_summary.index = weekly_summary.index - pd.Timedelta(weeks=1)


c = weekly_summary["Crashes Norm"] = 1 - weekly_summary["Daily Crashes"] / 100
r = weekly_summary["Rating Norm"] = weekly_summary["Daily Average Rating"].fillna(
    weekly_summary["Total Average Rating"]) / 5

# (c - (0.5 - r) * (c + r) / (1 + c + r)) * (3 / 4)

weekly_summary["Satisfaction Index"] = (c - (0.5 - r) * (c + r) / (1 + c + r))*(3/4)
weekly_summary["Daily Average Rating"] = weekly_summary["Daily Average Rating"].fillna(0)

cmap = linear_cmap(field_name="Satisfaction Index", palette=YlGn8[::-1], low=0.2, high=1)

weekly_summary["Week"] = weekly_summary.index.strftime("W%U")

source = ColumnDataSource(weekly_summary)

output_file("vis3.html")

fig1 = figure(
    title="Weekly Ratings and Crashes",
    height=600,
    width=800,
    x_axis_label="Average Daily Crashes",
    y_axis_label="Weekly Average Rating",
    background_fill_color="#fafafa",
    tools=["pan", "wheel_zoom", "reset", "save", "tap"]
)

s = fig1.scatter(x="Daily Crashes", y="Daily Average Rating", size=10, source=source, color=cmap)

labels = LabelSet(x="Daily Crashes", y="Daily Average Rating", text="Week", y_offset=8,
                  text_font_size="11px", text_color="#555555",
                  source=source, text_align='center')
fig1.add_layout(labels)

color_bar = s.construct_color_bar(width=10, title="Satisfaction Index")
fig1.add_layout(color_bar, 'right')

fig1.add_tools(HoverTool(tooltips=[('Date', '@Date{%Y-W%U}'),
                                   ('Total Average Rating', '@{Total Average Rating}'),
                                   ('Daily Average Rating', '@{Daily Average Rating}'),
                                   ('Daily Crashes', '@{Daily Crashes}'),
                                   ('Satisfaction Index', '@{Satisfaction Index}')],
                         formatters={'@Date': 'datetime'}))


fig2 = figure(
    title="Weekly Satisfaction Index",
    height=500,
    width=800,
    x_axis_label="Week",
    y_axis_label="Index Score",
    tools=["pan", "reset"]
)

fig2.add_layout(
    Title(text=r"\[\text{Crash Index}: c = 1 - \frac{\text{Daily Crashes}}{100}\]",
          text_font_style="italic", standoff=5), 'below')
fig2.add_layout(
    Title(text=r"\[\text{Rating Index}: r = \frac{\text{Daily Average Rating*}}{5}\]",
          text_font_style="italic", standoff=5), 'below')
fig2.add_layout(
    Title(text=r"\[\text{* Total Average Rating for weeks without ratings.}\]",
          text_font_style="italic", text_font_size="10px", standoff=0), 'below')
fig2.add_layout(
    Title(text=r"\[\text{Satisfaction Index}: s = \frac{3}{4}(c - \frac{(0.5 - r)(c + r)}{1 + c + r})\]",
          text_font_style="italic", standoff=5), 'below')

fig2.x(x="Date",
       y="Crashes Norm",
       source=source,
       size=10,
       color="red",
       legend_label="Crash Index")
fig2.x(x="Date",
       y="Rating Norm",
       source=source,
       size=10,
       color="blue",
       legend_label="Rating Index")
fig2.line(x="Date",
          y="Satisfaction Index",
          source=source, color="black")
sglyph = fig2.circle(x="Date",
                     y="Satisfaction Index",
                     source=source,
                     color=cmap,
                     size=10)


fig2.xaxis.ticker = FixedTicker(ticks=weekly_summary.index.astype(np.int64) // 10**6)
fig2.xaxis.formatter = DatetimeTickFormatter(days="%U")

tap = TapTool(renderers=[sglyph])
fig2.add_tools(tap)
