from preprocessing import sales
from bokeh.models import ColumnDataSource, HoverTool, FixedTicker, DatetimeTickFormatter, PrintfTickFormatter
from bokeh.io import output_file
from bokeh.plotting import figure, show
from bokeh.layouts import column
import pandas as pd
import numpy as np

# Sales Volume: Visualize the sales over time (for example, per month or per day) in
# terms of at least two measures. For example: real money (Amount) and transaction count
# (row count).

sales_premium = sales[sales["Sku Id"] == "premium"]
sales_unlock = sales[sales["Sku Id"] == "unlockcharactermanager"]

weekly_grouper = pd.Grouper(key="Datetime", freq="w-MON")

weekly_premium = sales_premium.groupby(weekly_grouper).agg(
    {"Sku Id": "count"}).rename(columns={"Sku Id": "premium"})
weekly_unlock = sales_unlock.groupby(weekly_grouper).agg(
    {"Sku Id": "count"}).rename(columns={"Sku Id": "unlockcharactermanager"})
weekly_money = sales.groupby(weekly_grouper).agg({"Amount (Merchant Currency)": "sum"})

weekly_summary = weekly_money.join([weekly_premium, weekly_unlock])
weekly_summary.index = weekly_summary.index - pd.Timedelta(weeks=1)

source = ColumnDataSource(weekly_summary)

output_file("vis1.html")

fig1 = figure(
    title="Weekly Transactions",
    height=400,
    width=800,
    y_range=(0, 100),
    x_axis_label="Week",
    y_axis_label="Transactions",
    tools=["save"],
    background_fill_color="#fafafa"
)
fig1.xaxis.ticker = FixedTicker(ticks=weekly_summary.index.astype(np.int64) // 10**6)
fig1.xaxis.formatter = DatetimeTickFormatter(days="%U")

products = ["premium", "unlockcharactermanager"]
fig1.vbar_stack(stackers=products,
                x="Datetime",
                source=source,
                width=(7*24*60*60*1000)*.9,
                color=["#718dbf", "#e84d60"],
                legend_label=products)

fig1.line(x="Datetime", y="Amount (Merchant Currency)", color="black", source=source)

fig1.legend.location = "top_left"
fig1.legend.orientation = "horizontal"

fig1.add_tools(HoverTool(tooltips=[('Date', '@Datetime{%Y-W%U}'), ('Sku Id', '$name'), ('Transactions', '@$name')],
                         formatters={'@Datetime': 'datetime'}))

fig2 = figure(
    title="Weekly Revenue",
    height=400,
    width=800,
    y_range=(0, 500),
    x_axis_label="Week",
    y_axis_label="Revenue",
    tools=["reset", "save", "ywheel_zoom", "ypan"],
    background_fill_color="#fafafa"
)
fig2.xaxis.ticker = fig1.xaxis.ticker
fig2.xaxis.formatter = fig1.xaxis.formatter

fig2.yaxis.formatter = PrintfTickFormatter(format="€ %s")

fig2.line(x="Datetime", y="Amount (Merchant Currency)", color="black", source=source)

fig2.add_tools(HoverTool(tooltips=[('Date', '@Datetime{%Y-W%U}'), ('Revenue', '@{Amount (Merchant Currency)}')],
                         formatters={'@Datetime': 'datetime'}))
fig1.x_range = fig2.x_range
