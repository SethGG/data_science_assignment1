from preprocessing import sales, crashes, ratings
from bokeh.io import output_file
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource
from bokeh.layouts import row, column, gridplot
import pandas as pd

# print(sales)
# print(crashes)
# print(ratings)

# Sales Volume: Visualize the sales over time (for example, per month or per day) in
# terms of at least two measures. For example: real money (Amount) and transaction count
# (row count).


# Attribute Segmentation and Filtering: Present sales volume (as above) segmented per
# attribute: at least the SKU id (in-app purchase option) attribute should be included, but you
# can also think of the day of the week, time of the day or the country of the customer.

'''fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
counts = [5, 3, 4, 2, 4, 6]
output_file("vis1.html")
p = figure(x_range=fruits, height=350, title="Fruit Counts",
           toolbar_location=None, tools="")

p.vbar(x=fruits, top=counts, width=0.9)

p.xgrid.grid_line_color = None
p.y_range.start = 0

show(p)'''


lenpre = len(sales[sales['Sku Id'] == 'premium'])
lenchar = len(sales[sales['Sku Id'] == 'unlockcharactermanager'])
# lencountry = len(sales[sales['Sku Id']==''])
print(sales["Buyer Country"].unique())
# for col in sales.columns:
#    print(col)
print(lenpre)
print(lenchar)
print(lenpre+lenchar)
x = ['premium', 'unlockcharactermanager']
y = [lenpre, lenchar]

fig = figure(x_range=x, title="SKU ID", toolbar_location=None, tools="")

fig.vbar(x=x, bottom=0, top=y, color='blue', width=0.75, legend_label='SKU ID')
fig.y_range.start = 0
fig.legend.location = 'top_left'


def get_uniques(datfram, column, uniques):
    tmplist = []
    # uniques = datfram[str(column)].unique()
    for x in uniques:
        # tmplist.append((x,len(datfram[datfram[str(column)].dt.day_name()==str(x)])))
        tmplist.append(len(datfram[datfram[str(column)].dt.day_name() == str(x)]))
    return tmplist


countries = []
country_list = sales["Buyer Country"].unique()
for z in country_list:
    countries.append(len(sales[sales['Buyer Country'] == str(z)]))
print(countries)
print(country_list)
select_tools = ['box_select', 'lasso_select', 'poly_select', 'tap', 'reset']
fig1 = figure(x_range=country_list, title="Sales per country", toolbar_location=None, tools=select_tools)

fig1.vbar(x=country_list, bottom=0, top=countries, color='blue', width=0.9, legend_label='Countries')
fig1.y_range.start = 0
fig1.legend.location = 'top_left'

sku_id_countries = gridplot([[fig, fig1]], toolbar_location='right')

time_week = gridplot([[fig, fig1]], toolbar_location='right')

weekday = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

sales_weekday = get_uniques(sales, "Transaction Date", weekday)
print(sales_weekday)
print(sales["Transaction Date"].dt.day_name())
# weekdays=

# for z in sales:
#
#    weekdic[z]=weekdic[z]+1

# "Transaction Date"

dayplot = figure(x_range=weekday, title="Sales per country", toolbar_location=None, tools=select_tools)

dayplot.vbar(x=weekday, bottom=0, top=sales_weekday, color='blue', width=0.9, legend_label='Weekdays')
dayplot.y_range.start = 0
dayplot.legend.location = 'top_left'

show(column(sku_id_countries, dayplot))

# TO-DO

# Ratings vs Stability: Can you come up with some Key Performance Indicators (metrics
# and scores) that help management understand how the app is doing in terms of stability and
# user satisfaction? Visualize them in a nice way. For example, the number of crashes in
# correlation with the daily average rating.

# TO-DO

# Geographical Development: visualize the sales volume (as above) and the average
# rating per country in a geographical setting (using the geopandas package, see more
# information below) , for example the number of customers per country over time. The goal is
# again to give management as much geographic insight as possible.

# TO-DO

# output_file('filename.html', title='Empty Bokeh Figure')

# fig = figure(background_fill_color='gray', background_fill_alpha=0.5, border_fill_color='blue', border_fill_alpha=0.25, #plot_height=300, plot_width=500, x_axis_label='X Label',
# x_axis_type='datetime', x_axis_location='above', x_range=('2018-01-01', '2018-06-30'), y_axis_label='Y Label', y_axis_type='linear', y_axis_location='left',
# y_range=(0, 100), title='Example Figure', title_location='right', toolbar_location='below', tools='save')
# show(fig)
