from preprocessing import sales
from bokeh.models import ColumnDataSource
from bokeh.io import output_file
from bokeh.plotting import figure
import pandas as pd

# Sales Volume: Visualize the sales over time (for example, per month or per day) in
# terms of at least two measures. For example: real money (Amount) and transaction count
# (row count).

daily_summary = sales.groupby(pd.Grouper(key="Datetime", freq="D"))

# daily_summary = sales.groupby("Transaction Date").agg(
#    {"Amount (Merchant Currency)": "sum", "Transaction Date": "count"})
# daily_summary.rename(columns={"Amount (Merchant Currency)": "Real Money",
#                     "Transaction Date": "Transaction Count"}, inplace=True)
# print(daily_summary)

# source = ColumnDataSource(daily_summary)

# start_date = daily_summary.index[0]
# end_date = start_date + pd.DateOffset(days=30)

# output_file("vis1.html")
# fig = figure(
#    x_axis_type="datetime",
#    height=300,
#    width=800,
#    x_range=(start_date, end_date),
#    x_axis_label="Date",
#    y_axis_label="Amount"
# )
# fig.vbar(x="Transaction Date", top="Transaction Count", source=source, width=(24*60*60*1000)*.9, color="red")
