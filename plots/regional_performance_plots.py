import chart_studio.plotly as py
import plotly.express as px
import plotly.graph_objects as go
import cufflinks as cf
import matplotlib.pyplot as plt
import numpy as np
import requests


# -----------------------------------------------------------------------------------
# 1. A choropleth plot to show the revenue distribution per states:
# -----------------------------------------------------------------------------------


def plot_total_rev_per_state(df):
    """
    This function is responsible to plot a choropleth plot that shows the total revenue generated for each state in Brazil.
    """
    total_rev_per_state = df

    # We are pulling the brazil-states.geojson file for mapping the states in the chart:
    url = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"
    brazil_geojson = requests.get(url).json()

    # We are using the quantiles for the color scale where vmin is the 5th percentile and vmax is the 95th percentile:
    vmin = total_rev_per_state["total_revenue"].quantile(0.05)
    vmax = total_rev_per_state["total_revenue"].quantile(0.95)

    fig = px.choropleth(total_rev_per_state, geojson=brazil_geojson,
                    locations="state",
                    featureidkey="properties.sigla",
                    color="total_revenue",
                    color_continuous_scale="Mint",
                    scope="south america",
                    hover_data={
                        "state_names" : True,    
                        "total_revenue": ":,.3~s",
                        "revenue_contribution (%)" : ":.2f",
                        "state": False
                           },
                    range_color=(vmin, vmax),
                    height=750,
                    width=1000
                )
    

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(coloraxis_colorbar = dict(title="Total Revenue"),
                 title={
                     "text": "Revenue Realization Per State",
                     "font": {
                         "size": 23,
                         "color": "black",
                         "family": "Arial"
                     },
                     "x": 0.5,
                     "xanchor": "center"
                 })

    return fig