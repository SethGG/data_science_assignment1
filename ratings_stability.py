from preprocessing import crashes, ratings_overview

# Ratings vs Stability: Can you come up with some Key Performance Indicators (metrics
# and scores) that help management understand how the app is doing in terms of stability and
# user satisfaction? Visualize them in a nice way. For example, the number of crashes in
# correlation with the daily average rating.

print(crashes)
print(ratings_overview)

source = ColumnDataSource(daily_summary)
