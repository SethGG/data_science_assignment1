from preprocessing import sales, crashes#, ratings
from bokeh.io import output_file
from bokeh.plotting import figure, show, save
from bokeh.models import ColumnDataSource
from bokeh.layouts import row, column, gridplot
from bokeh.palettes import Category20c, viridis, linear_palette
from math import pi
from bokeh.transform import cumsum
import pandas as pd

# Attribute Segmentation and Filtering: Present sales volume (as above) segmented per
# attribute: at least the SKU id (in-app purchase option) attribute should be included, but you
# can also think of the day of the week, time of the day or the country of the customer.

#output_file(filename="test.html")
print(sales)
print(crashes)

lenpre = len(sales[sales['Sku Id'] == 'premium'])
lenchar = len(sales[sales['Sku Id'] == 'unlockcharactermanager'])
# lencountry = len(sales[sales['Sku Id']==''])
x = ['premium', 'unlockcharactermanager']
y = [lenpre, lenchar]

fig = figure(x_range=x, title="Total sales by SKU ID", toolbar_location=None, tools="")

fig.vbar(x=x, bottom=0, top=y, color='blue', width=0.75, legend_label='SKU ID')
fig.y_range.start = 0
fig.legend.location = 'top_left'


def get_uniques(datfram, column, uniques):
    tmplist = []
    for x in uniques:
        tmplist.append(len(datfram[datfram[str(column)].dt.day_name() == str(x)]))
    return tmplist

print(sales)

countries = []
country_list = sales["Buyer Country"].unique()
for z in country_list:
    countries.append(len(sales[sales['Buyer Country'] == str(z)]))
#print(countries)
print(type(countries))
print(type(country_list))
#print(country_list)
country_list1 = country_list.tolist()
country_dic = dict(zip(country_list, countries))
select_tools = ['box_select', 'lasso_select', 'poly_select', 'tap', 'reset']
sorted_countries_sales = sorted(country_list, key=lambda x: countries[country_list1.index(x)])
fig1 = figure(x_range=sorted_countries_sales, title="Sales per country", toolbar_location=None, tools=select_tools)

fig1.vbar(x=country_list, bottom=0, top=countries, color='blue', width=0.9, legend_label='Countries')
fig1.y_range.start = 0
fig1.legend.location = 'top_left'

sku_id_countries = gridplot([[fig, fig1]], toolbar_location='right')

time_week = gridplot([[fig, fig1]], toolbar_location='right')

weekday = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

print(sales)
sales_weekday = get_uniques(sales, "Datetime", weekday)
print(sales_weekday)
print(sales["Datetime"].dt.day_name())


# weekdays=

# for z in sales:
#
#    weekdic[z]=weekdic[z]+1

# "Transaction Date"

dayplot = figure(x_range=weekday, title="Sales per weekday", toolbar_location=None, tools=select_tools)

dayplot.vbar(x=weekday, bottom=0, top=sales_weekday, color='blue', width=0.9, legend_label='Weekdays')
dayplot.y_range.start = 0
dayplot.legend.location = 'top_left'

pie_data=pd.Series(country_dic).reset_index(name='value').rename(columns={'index':'country'})
pie_data['angle'] = pie_data['value']/pie_data['value'].sum() *2*pi
pie_data['color'] = linear_palette(viridis, len(country_dic))

pie = figure(title="Premium vs Unblock character manager", toolbar_location=None, tools="hover", tooltips="@country: @value", x_range=(-0.5, 1.0))

pie.wedge(x=0,y=1, radius=0.4, start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'), line_color="white", fill_color='color', legend_field='country', source=pie_data)


pie.axis.axis_label=None
pie.axis.visible=False
pie.grid.grid_line_color=None

group2 = gridplot([[dayplot, pie]], toolbar_location='right')
fig3 = column(sku_id_countries, group2)
#fig3 = column(sku_id_countries, dayplot)

#save(fig3)
show(fig3)
#show(column(sku_id_countries, dayplot))
