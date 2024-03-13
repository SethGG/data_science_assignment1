import sales_vol
import ratings_stability
from bokeh.layouts import column, row
from bokeh.io import output_file
from bokeh.plotting import show
from bokeh.models import Div, ImportedStyleSheet

output_file("index.html")

stylesheet = ImportedStyleSheet(url="https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css")

html = """
<section class="section">
  <h1 class="title">Sales Volume</h1>
  <h2 class="subtitle">
    Here we can view the weekly sales over time in terms of the number of transactions and real money.
  </h2>
</section>
"""
title = Div(text=html, stylesheets=[stylesheet])

sales_layout = column(title, row(sales_vol.fig1, sales_vol.fig2))

html = """
<section class="section">
  <h1 class="title">Ratings vs Stability</h1>
  <h2 class="subtitle">
    Here we can compare the weekly average daily rating against the weekly average daily number of crashes.
  </h2>
</section>
"""
title = Div(text=html, stylesheets=[stylesheet])

rating_layout = column(title, row(ratings_stability.fig1, ratings_stability.fig2))

dashboard = column(sales_layout, rating_layout)
show(dashboard)
