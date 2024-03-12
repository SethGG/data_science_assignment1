from preprocessing import crashes, ratings_overview
from bokeh.models import ColumnDataSource, HoverTool, FixedTicker, DatetimeTickFormatter, PrintfTickFormatter, LabelSet, Title, TextAnnotation
from bokeh.palettes import YlGn8
from bokeh.io import output_file
from bokeh.plotting import figure, show
from bokeh.layouts import column, row
from bokeh.transform import linear_cmap
import pandas as pd
import numpy as np


# Ratings vs Stability: Can you come up with some Key Performance Indicators (metrics
# and scores) that help management understand how the app is doing in terms of stability and
# user satisfaction? Visualize them in a nice way. For example, the number of crashes in
# correlation with the daily average rating.


daily_grouper = pd.Grouper(key="Date", freq="W-MON")

daily_crashes = crashes.groupby(daily_grouper).mean("Daily Crashes")
daily_ratings = ratings_overview.groupby(daily_grouper).agg(
    {"Daily Average Rating": "mean", "Total Average Rating": "mean"})

daily_overview = daily_crashes.join(daily_ratings)

c = daily_overview["Crashes Norm"] = 1 - daily_overview["Daily Crashes"] / 100
r = daily_overview["Rating Norm"] = daily_overview["Daily Average Rating"].fillna(
    daily_overview["Total Average Rating"]) / 5

# (c - (0.5 - r) * (c + r) / (1 + c + r)) * (3 / 4)

daily_overview["Satisfaction Index"] = (c - (0.5 - r) * (c + r) / (1 + c + r))*(3/4)
daily_overview["Daily Average Rating"] = daily_overview["Daily Average Rating"].fillna(0)

# colors_idx = [int(x*10) for x in daily_overview["Satisfaction Index"].fillna(0)]
# daily_overview["Colors"] = [Spectral10[i] for i in colors_idx]
cmap = linear_cmap(field_name="Satisfaction Index", palette=YlGn8[::-1], low=0.2, high=1)

daily_overview["Week"] = daily_overview.index.strftime("W%U")

source = ColumnDataSource(daily_overview)

output_file("vis3.html")

fig1 = figure(
    title="Weekly Ratings vs Stability",
    height=600,
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
    title="Weekly Satisfaction Index",
    height=500,
    width=800,
    x_axis_label="Week",
    y_axis_label="Index Score"
)

fig2.add_layout(
    Title(text=r"\[\text{Crash Index}: c = 1 - \frac{\text{Daily Crashes}}{100}\]", text_font_style="italic", standoff=0), 'below')
fig2.add_layout(
    Title(text=r"\[\text{Rating Index}: r = \frac{\text{Daily Average Rating}}{5}\]", text_font_style="italic", standoff=0), 'below')
fig2.add_layout(
    Title(text=r"\[\text{Satisfaction Index}: s = \frac{3}{4}(c - \frac{(0.5 - r)(c + r)}{1 + c + r})\]", text_font_style="italic", standoff=0), 'below')

fig2.x(x="Date",
       y="Crashes Norm",
       source=source,
       size=10,
       color="red",
       legend_label="Crash Index")
review_source = ColumnDataSource(daily_overview[daily_overview["Daily Average Rating"] > 0])
fig2.x(x="Date",
       y="Rating Norm",
       source=review_source,
       size=10,
       color="blue",
       legend_label="Rating Index (Using Daily Average)")
review_source_nan = ColumnDataSource(daily_overview[daily_overview["Daily Average Rating"] == 0])
fig2.x(x="Date",
       y="Rating Norm",
       source=review_source_nan,
       size=10,
       color="grey",
       legend_label="Rating Index (Using Total Average)")
fig2.line(x="Date",
          y="Satisfaction Index",
          source=source, color="black")
fig2.circle(x="Date",
            y="Satisfaction Index",
            source=source,
            color=cmap,
            size=10)


fig2.xaxis.ticker = FixedTicker(ticks=daily_overview.index.astype(np.int64) // 10**6)
fig2.xaxis.formatter = DatetimeTickFormatter(days="%U")

grid = row(fig1, fig2)
show(grid)
