from preprocessing import sales
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.io import output_file
from bokeh.plotting import figure, show
from bokeh.layouts import column
import pandas as pd

# Sales Volume: Visualize the sales over time (for example, per month or per day) in
# terms of at least two measures. For example: real money (Amount) and transaction count
# (row count).

sales_premium = sales[sales["Sku Id"] == "premium"]
sales_unlock = sales[sales["Sku Id"] == "unlockcharactermanager"]

daily_grouper = pd.Grouper(key="Datetime", freq="D")

daily_premium = sales_premium.groupby(daily_grouper).agg(
    {"Sku Id": "count"}).rename(columns={"Sku Id": "premium"})
daily_unlock = sales_unlock.groupby(daily_grouper).agg(
    {"Sku Id": "count"}).rename(columns={"Sku Id": "unlockcharactermanager"})
daily_money = sales.groupby(daily_grouper).agg({"Amount (Merchant Currency)": "sum"})

daily_summary = daily_money.join([daily_premium, daily_unlock])
print(daily_summary)

source = ColumnDataSource(daily_summary)

start_date = daily_summary.index[0]
end_date = start_date + pd.DateOffset(days=30)

output_file("vis1.html")

fig1 = figure(
    x_axis_type="datetime",
    height=300,
    width=800,
    x_range=(start_date, end_date),
    y_range=(0, 25),
    x_axis_label="Date",
    y_axis_label="Transactions",
    tools=["xpan", "reset", "save", "xwheel_zoom"]
)

products = ["premium", "unlockcharactermanager"]
fig1.vbar_stack(stackers=products,
                x="Datetime",
                source=source,
                width=(24*60*60*1000)*.9,
                color=["#718dbf", "#e84d60"],
                legend_label=products)
fig1.legend.location = "top_left"
fig1.legend.orientation = "horizontal"

fig1.add_tools(HoverTool(tooltips=[('Date', '@Datetime{%F}'), ('Sku Id', '$name'), ('Transactions', '@$name')],
                         formatters={'@Datetime': 'datetime'}))

fig2 = figure(
    x_axis_type="datetime",
    height=300,
    width=800,
    x_range=(start_date, end_date),
    y_range=(0, 120),
    x_axis_label="Date",
    y_axis_label="Amount",
    tools=["xpan", "reset", "save", "xwheel_zoom"]
)
fig2.line(x="Datetime", y="Amount (Merchant Currency)", color="black", source=source)

fig2.add_tools(HoverTool(tooltips=[('Date', '@Datetime{%F}'), ('Amount', '@{Amount (Merchant Currency)}')],
                         formatters={'@Datetime': 'datetime'}))

grid = column(fig1, fig2)
fig1.x_range = fig2.x_range

show(grid)
