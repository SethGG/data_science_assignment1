from preprocessing import sales
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Range1d, Plot, AnnularWedge, Legend, LegendItem, HoverTool, TapTool
from math import pi

# Attribute Segmentation and Filtering: Present sales volume (as above) segmented per
# attribute: at least the SKU id (in-app purchase option) attribute should be included, but you
# can also think of the day of the week, time of the day or the country of the customer.


def get_uniques(datfram, column, uniques):
    tmplist = []
    for x in uniques:
        tmplist.append(len(datfram[datfram[str(column)].dt.day_name() == str(x)]))
    return tmplist


select_tools = ['tap', 'box_select', 'reset', 'save']
lenpre = len(sales[sales['Sku Id'] == 'premium'])
lenchar = len(sales[sales['Sku Id'] == 'unlockcharactermanager'])
x = ['premium', 'unlockcharactermanager']
y = [lenpre, lenchar]

fig = figure(x_range=x, title="Total sales by SKU ID", toolbar_location=None, tools=select_tools, x_axis_label="SKU ID",
             y_axis_label="Transactions", background_fill_color="#fafafa", height=500, width=400)

fig.vbar(x=x, bottom=0, top=y, width=0.75, color=["#718dbf", "#e84d60"])
fig.y_range.start = 0

fig.add_tools(HoverTool(tooltips=[('Sku Id', '@x'), ('Sales', '@top')]))

colors = {
    'premium': "#718dbf",
    'unlockcharactermanager': "#e84d60"
}

xdr = Range1d(start=-2, end=2)
ydr = Range1d(start=-2, end=2)

donut = Plot(x_range=xdr, y_range=ydr, background_fill_color="#fafafa", height=500, width=500)
donut.title.text = "Total sales by SKU ID"
aggregated = sales.groupby("Sku Id").size().to_frame("count1")
aggregated['proportion'] = aggregated['count1']/aggregated['count1'].sum()
selected = aggregated[aggregated.proportion >= 0].copy()
sku_id = selected.index.tolist()
angles = selected.proportion.map(lambda x: 2*pi*(x)).cumsum().tolist()

skuid_source = ColumnDataSource(dict(
    start=[0] + angles[:-1],
    end=angles,
    colors=[colors[skuid] for skuid in x],
    proportion=aggregated['proportion'],
    count1=aggregated['count1'],
    skuid=aggregated.index
))

glyph = AnnularWedge(x=0, y=0, inner_radius=0.9, outer_radius=1.7,
                     start_angle="start", end_angle="end",
                     line_color="white", line_width=3, fill_color="colors")
r = donut.add_glyph(skuid_source, glyph)

legend = Legend(location="center")
for i, name in enumerate(colors):
    legend.items.append(LegendItem(label=name, renderers=[r], index=i))
donut.add_layout(legend, "center")
donut.add_tools(HoverTool(tooltips=[('Sku ID', '@skuid'), ('Sales', '@count1'), ('Proportion', '@proportion{00.0%}')]))
donut.add_tools(TapTool())

weekday = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

sales_weekday = get_uniques(sales, "Datetime", weekday)


dayplot = figure(x_range=weekday, title="Sales per weekday", toolbar_location=None,
                 tools=select_tools, x_axis_label="Weekday",
                 y_axis_label="Transactions", background_fill_color="#fafafa", height=500, width=500)

dayplot.vbar(x=weekday, bottom=0, top=sales_weekday, color='grey', width=0.9)
dayplot.y_range.start = 0
dayplot.add_tools(HoverTool(tooltips=[('Weekday', '@x'), ('Sales', '@top')]))
