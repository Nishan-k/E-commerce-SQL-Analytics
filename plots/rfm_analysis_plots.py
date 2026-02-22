import chart_studio.plotly as py
import plotly.express as px
import plotly.graph_objects as go
import cufflinks as cf
import matplotlib.pyplot as plt
import numpy as np



# -----------------------------------------------------------------------------------
# 1. A bar chart to show Customers Distribution By Recency:
# -----------------------------------------------------------------------------------

def plot_customer_distribution_recency_bar_chart(df):
    """
    This function is responsible to plot a bar chart that shows the customer distribution by recency days interval where each bin represents an interval of 50 days:
    """
    customers_per_bins_labeled_df = df
    fig = px.bar(
        data_frame=customers_per_bins_labeled_df,
        x= 'Days Interval',
        y= 'Total Customers',
        labels={'x': 'Recency Bins (Days)', 
                'y': 'Number Of Customers'},
        title = 'Customers Distribution By Recency'
        )
    
    fig.update_traces(hovertemplate=
                      "<b>Numer of customers:</b> %{y:,}<br>" +
                      "<b>Recency Bin: </b> %{x}<br>" +
                      "<extra></extra>"
                      )
    
    fig.write_html("../plot_html/Customers_Distribution_By_Recency.html")
    return fig


# -----------------------------------------------------------------------------------
# 2. A bar chart to show Customers Segmentation By Purchase Frequency:
# -----------------------------------------------------------------------------------

def plot_customer_purchase_frequency_bar_chart(df):
    """
    This function will be responsible to plot a bar chart that shows the customers segmentation by purchase frequency:
    """
    customer_order_frequency_interpretation_counts = df
    fig = px.bar(customer_order_frequency_interpretation_counts,
             x='Interpretation',
             y='Customer Share (%)',
             text='Customer Share (%)',
             custom_data='Total Counts',
             title='Customer Segmentation by Purchase Frequency',
             labels={'Interpretation':'Customer Segment', 'Customer Share (%)':'Customer Share (%) Log',
                    'Total Counts': 'Total Customers'})

    fig.update_traces(hovertemplate=
                      "<b>Customer Segment:</b> %{x}<br>" +
                      "<b>Customer Share: </b> %{y:.2f}%<br>" +
                      "<b>Total Customers:</b> %{customdata[0]:,}"+
                      "<extra></extra>"
                      )
    fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
    fig.update_yaxes(type='log')
    fig.write_html("../plot_html/Customer_Segmentation_by_Purchase_Frequency.html")
    return fig



# -----------------------------------------------------------------------------------
# 3. A bar chart to compare the customers by VOLUME V/S VALUE
# -----------------------------------------------------------------------------------

def plot_volume_vs_value_chart(df):
    """
    This function will be responsible to plot a bar chart that represents the total revenue per bin (Customer Buying Behavior Frequency)
    and a line-chart that shows the average amount spent per customer in each bin:    
    """
    segment_monetary_summary_w_customer_share = df
    fig = go.Figure()

    # Adding the Total Revenue:
    fig.add_bar(
        x=segment_monetary_summary_w_customer_share['Interpretation'],
        y=segment_monetary_summary_w_customer_share['Total Revenue'],
        customdata=segment_monetary_summary_w_customer_share[['Total Customers', 'Revenue Contribution (%)']],
        marker=dict(
            color=np.log10(segment_monetary_summary_w_customer_share['Total Revenue']),
            colorscale='Blugrn',
            showscale=True,
            colorbar=dict(x=-0.15,
                          xanchor='left',
                          len=1,
                          thickness=20,
                          tickvals=[])
        ),
        name='Total Revenue',
        text=[f'{val/1000000:.2f}M' if val >= 1000000 
              else f'{val/1000:.0f}K' if val >= 1000 
              else f'{val:.0f}' 
              for val in segment_monetary_summary_w_customer_share['Total Revenue']],
        textposition='outside',
        textfont=dict(size=12, color='black')
    )

    # Adding the Average Revenue Per Person:
    fig.add_scatter(
        x=segment_monetary_summary_w_customer_share['Interpretation'],
        y=segment_monetary_summary_w_customer_share['Average Revenue Per Customer'],
        name='Avg Revenue per Customer',
        text = [f"{avg_rev:.2f}" for avg_rev in segment_monetary_summary_w_customer_share['Average Revenue Per Customer']],
        textposition='top center',
        textfont=dict(size=12, color='black'),
        customdata=segment_monetary_summary_w_customer_share[['Total Customers', 'Revenue Contribution (%)']],
        yaxis='y2',
         marker=dict(
            color=(segment_monetary_summary_w_customer_share['Average Revenue Per Customer']),
            colorscale='OrRd',
            showscale=True,
            colorbar=dict(len=1,
                          xanchor='right',
                          x=1.15,
                          thickness=20,
                          tickvals=[])
        ),
        mode='lines+markers+text'
    )

    fig.update_layout(
        title='Revenue Contribution <b>Volume</b> vs Customer <b>Value</b> by Frequency Segment in Brazilian Real <b>($R)</b>',
        xaxis_title='Customer Segment',
        yaxis=dict(
            title='Total Revenue',
            type='log',
            tickmode='array',
            tickvals=[1000, 10000, 100000, 1000000, 10000000],
            ticktext=['1K', '10K', '100K', '1M', '10M'],
            showgrid=True
        ),
        yaxis2=dict(
            title='Avg Revenue per Customer',
            overlaying='y',
            side='right'
        ),
        legend=dict(
            orientation='h',
            yanchor='top',
            y=-0.25,
            xanchor='center',
            x=0.5
        )
    )
    fig.update_traces(
        selector=dict(type='bar'),
        hoverlabel=dict( bgcolor='white'),
        hovertemplate= 
        "<b>Total Customers:</b> %{customdata[0]:,}<br>"+
        "<b>Total Revenue:</b> %{y:,.2f} $R<br>" +
        "<b>Revenue Contribution (%):</b> %{customdata[1]:,.2f}%<br>"+
        "<extra></extra>"
    )
    fig.update_traces(
        selector=dict(type='scatter'),
        hoverlabel=dict(
        bgcolor='white',
        font_size=14
        ),
        hovertemplate=
        "<b>Total Customers:</b> %{customdata[0]:,}<br>"+
        "<b>Average Revenue Per Customer:</b> %{y:,.2f} $R<br>" +
        "<b>Revenue Contribution (%):</b> %{customdata[1]:,.2f}%<br>"+
        "<extra></extra>"
    )

    fig.write_html("../plot_html/Revenue_contribution_vol_val.html")
    return fig

