from preprocessing import sales, crashes, ratings
from bokeh.io import output_file
from bokeh.plotting import figure, show

print(sales)
print(crashes)
print(ratings)

# Sales Volume: Visualize the sales over time (for example, per month or per day) in
# terms of at least two measures. For example: real money (Amount) and transaction count
# (row count).

output_file("vis1.html")
fig = figure()

show(fig)

# Attribute Segmentation and Filtering: Present sales volume (as above) segmented per
# attribute: at least the SKU id (in-app purchase option) attribute should be included, but you
# can also think of the day of the week, time of the day or the country of the customer.

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
