import chart_studio.plotly as py
import plotly.express as px
import plotly.graph_objects as go
import cufflinks as cf
import matplotlib.pyplot as plt
import numpy as np
import requests



# We are pulling the brazil-states.geojson file for mapping the states in the chart:
url = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"
brazil_geojson = requests.get(url).json()

# -----------------------------------------------------------------------------------
# 1. A choropleth plot to show the revenue distribution per states:
# -----------------------------------------------------------------------------------


def plot_total_rev_per_state(df):
    """
    This function is responsible to plot a choropleth plot that shows the total revenue generated for each state in Brazil.
    """
    total_rev_per_state = df

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
    fig.add_annotation(
                        x=1.45, y="São Paulo",
                        text="High volume, lower AOV",
                        showarrow=True,
                        arrowhead=2
                        )


    return fig




# -----------------------------------------------------------------------------------
# 2. A choropleth plot to show the order volume per states:
# -----------------------------------------------------------------------------------


def plot_total_order_vol_per_state(df):
    """
    This function is responsible to plot a choropleth plot that shows the total orders for each state in Brazil.
    """
    order_volume_per_state = df

    # We are using the quantiles for the color scale where vmin is the 5th percentile and vmax is the 95th percentile:
    vmin = order_volume_per_state["order_volume"].quantile(0.05)
    vmax = order_volume_per_state["order_volume"].quantile(0.95)

    fig = px.choropleth(order_volume_per_state, geojson=brazil_geojson,
                    locations="state",
                    featureidkey="properties.sigla",
                    color="order_volume",
                    color_continuous_scale="Mint",
                    scope="south america",
                    hover_data={
                        "state_names" : True,    
                        "order_volume": True,
                        "order_volume_contribution (%)" : ":.2f",
                        "state": False
                           },
                    range_color=(vmin, vmax),
                    height=750,
                    width=1000
                )
    

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(coloraxis_colorbar = dict(title="Total Orders"),
                 title={
                     "text": "Total Orders Per State",
                     "font": {
                         "size": 23,
                         "color": "black",
                         "family": "Arial"
                     },
                     "x": 0.5,
                     "xanchor": "center"
                 })

    return fig





# -----------------------------------------------------------------------------------
# 3. A lollipop chart to show the AOV with resepect to order volume and revenue by state:
# -----------------------------------------------------------------------------------

def plot_aov_wrt_revenue_and_order_vol(df):
    """
    This function will be responsible to plot a lollipop chart where the line chart represents the AOV,
    the marker size will represent the order volume and the color intensity of the marker will be represented by revenue:
    """

    # Sorting the df  by AOV index in ascending:
    df_sorted = df.sort_values('aov_index', ascending=True).copy()


    fig = go.Figure()

    # Add the line chart:
    fig.add_trace(go.Scatter(
        x=df_sorted['aov_index'],
        y=df_sorted['state_names'],
        mode='lines+markers',
        line=dict(color='gray', width=3),
        marker=dict(
                size=df_sorted['order_volume'],
                sizemode='area',
                sizeref=2.*max(df_sorted['order_volume'])/(40.**2),
                color=-df_sorted['revenue_contribution (%)'],   
                colorscale='greens',
                line = dict(color='dimgray', width=1.5),
                reversescale=True,                              
                showscale=True,
                colorbar=dict(title="Revenue<br>Contribution %",
                            tickvals=[-35, -30, -25, -20, -15, -10, -5, 0],
                            ticktext=['35%', '30%', '25%', '20%', '15%', '10%', '5%', '0%'])
    ),
        hovertemplate="<b>%{y}</b><br>" +
                    "AOV Index: %{x:.2f}x<br>" +
                    "Revenue Contribution: %{customdata[0]:.2f}%<br>" +
                    "Order Volume: %{customdata[1]:,}<br>" +
                    "Total Revenue: R$ %{customdata[2]:,.2f}<br>" +
                    "<extra></extra>",
        customdata=df_sorted[['revenue_contribution (%)', 'order_volume', 'total_revenue']]
    ))


    # Add the reference line at AOV = 1.0:
    fig.add_vline(x=1.0, line_dash="dash", line_color="red",
                annotation_text="Average AOV (1)", annotation_position="top")


    # Add AOV zone annotations:
    fig.add_annotation(
        x=0.85, y=0.95,
        xref="x", yref="paper",
        text="◀ High Order Volume<br>(AOV < 1)",
        showarrow=False,
        bgcolor="rgba(255,255,255,0.7)",
        font=dict(size=11, color="black"),
        xanchor="center"
    )

    fig.add_annotation(
        x=1.20, y=0.95,
        xref="x", yref="paper",
        text="Premium Markets (AOV > 1) ▶",
        showarrow=False,
        font=dict(size=11, color="black"),
        bgcolor="rgba(255,255,255,0.7)",
        xanchor="center"
    )

    fig.update_layout(
        title="<b>State Performance by AOV Index</b><br>" +
            "<span style='font-size: 12px'>Left of red line = Order volume drivers <b>(lower AOV)</b> Right = Premium markets <b>(higher AOV)</b><br></span>",
        xaxis_title="AOV Index (Revenue % ÷ Order Volume %)",
        yaxis_title="States",
        height=700,
        width=1000,
        xaxis=dict(range=[0.7, 1.8]),
        showlegend=False
    )

    fig.update_yaxes(ticklabelstandoff=14)
    return fig

