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

daily_grouper = pd.Grouper(key="Datetime", freq="w-MON")

daily_premium = sales_premium.groupby(daily_grouper).agg(
    {"Sku Id": "count"}).rename(columns={"Sku Id": "premium"})
daily_unlock = sales_unlock.groupby(daily_grouper).agg(
    {"Sku Id": "count"}).rename(columns={"Sku Id": "unlockcharactermanager"})
daily_money = sales.groupby(daily_grouper).agg({"Amount (Merchant Currency)": "sum"})

daily_summary = daily_money.join([daily_premium, daily_unlock])
daily_summary.index = daily_summary.index - pd.Timedelta(weeks=1)
print(daily_summary)

source = ColumnDataSource(daily_summary)

output_file("vis1.html")

fig1 = figure(
    title="Weekly Transactions",
    height=300,
    width=800,
    y_range=(0, 100),
    x_axis_label="Week",
    y_axis_label="Transactions",
    tools=["xpan", "reset", "save", "xwheel_zoom"],
    background_fill_color="#fafafa"
)
fig1.xaxis.ticker = FixedTicker(ticks=daily_summary.index.astype(np.int64) // 10**6)
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
    height=300,
    width=800,
    y_range=(0, 500),
    x_axis_label="Week",
    y_axis_label="Revenue",
    tools=["xpan", "reset", "save", "xwheel_zoom"],
    background_fill_color="#fafafa"
)
fig2.xaxis.ticker = fig1.xaxis.ticker
fig2.xaxis.formatter = fig1.xaxis.formatter

fig2.yaxis.formatter = PrintfTickFormatter(format="€ %s")

fig2.line(x="Datetime", y="Amount (Merchant Currency)", color="black", source=source)

fig2.add_tools(HoverTool(tooltips=[('Date', '@Datetime{%Y-W%U}'), ('Revenue', '@{Amount (Merchant Currency)}')],
                         formatters={'@Datetime': 'datetime'}))

grid = column(fig1, fig2)
fig1.x_range = fig2.x_range

show(grid)
