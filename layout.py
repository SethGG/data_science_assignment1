import sales_vol
import attribute_seg
import ratings_stability
import geographical_dev
from bokeh.layouts import column, row
from bokeh.io import output_file
from bokeh.plotting import show
from bokeh.models import Div, ImportedStyleSheet

output_file("index.html")

stylesheet = ImportedStyleSheet(url="https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css")

html = """
<section class="section">
  <h1 class="title is-2">Emerald-IT: Complete Reference for Dungeons and Dragons 5</h1>
  <h2 class="subtitle">
    Interactive dashboard used to understand and interpret the data of the app.
  </h2>
  <h2 class="subtitle is-6 is-italic">
    Data Science 2023-2024<br>
    Assignment 1: visual analytics<br>
    Daniël Zee (s2063131) & Marts Niewandt (s2624893)
</section>
<section class="section">
  <h1 class="title is-4">Sales Volume</h1>
  <h2 class="subtitle">
    Here we can view the weekly sales over time in terms of the number of transactions and real money.
  </h2>
</section>
"""
title = Div(text=html, stylesheets=[stylesheet])

sales_layout = column(title, row(sales_vol.fig1, sales_vol.fig2))

html = """
<section class="section">
  <h1 class="title is-4">Attribute Segmentation and Filtering</h1>
  <h2 class="subtitle">
    Here we can view the sales volume segmented per SKU id and day of the week.
  </h2>
</section>
"""
title = Div(text=html, stylesheets=[stylesheet])

seg_layout = column(title, row(attribute_seg.donut, attribute_seg.fig, attribute_seg.dayplot))

html = """
<section class="section">
  <h1 class="title is-4">Ratings vs Stability</h1>
  <h2 class="subtitle">
    Here we can compare the weekly average daily rating against the weekly average daily number of crashes.
  </h2>
</section>
"""
title = Div(text=html, stylesheets=[stylesheet])

rating_layout = column(title, row(ratings_stability.fig1, ratings_stability.fig2))

html = """
<section class="section">
  <h1 class="title is-4">Geographical Development</h1>
  <h2 class="subtitle">
    Here we can view the sales volume and ratings per country in a geographical setting.
  </h2>
</section>
"""
title = Div(text=html, stylesheets=[stylesheet])

geo_layout = column(title, geographical_dev.fig)

dashboard = column(sales_layout, seg_layout, rating_layout, geo_layout)
show(dashboard)
