import chart_studio.plotly as py
import plotly.express as px
import plotly.graph_objects as go
import cufflinks as cf
import matplotlib.pyplot as plt
import pandas as pd



# -----------------------------------------------------------------------------------
# 1. A bar chart to show Customers Distribution By Recency:
# -----------------------------------------------------------------------------------

def plot_customer_distribution_recency_bar_chart(df):
    """
    This function is responsible to plot a bar chart that shows the customer distribution by recency days interval where each bin represents an interval of 50 days:
    """
    customers_per_bins_labeled_df = df
    fig = px.bar(x=customers_per_bins_labeled_df['Days Interval'], y=customers_per_bins_labeled_df['Total Customers'],
             labels={'x': 'Recency Bins (Days)', 'y': 'Number Of Customers'},
             text=customers_per_bins_labeled_df['Total Customers'],
             title = 'Customers Distribution By Recency')
    
    return fig


# -----------------------------------------------------------------------------------
# 2. A bar chart to show Customers Segmentation By Purchase Frequency:
# -----------------------------------------------------------------------------------

def plot_customer_purchase_frequency_bar_chart(df):
    customer_order_frequency_interpretation_counts = df
    fig = px.bar(customer_order_frequency_interpretation_counts,
             x='Interpretation',
             y='Customer Share (%)',
             text='Customer Share (%)',
             hover_data={'Total Counts': True},
             title='Customer Segmentation by Purchase Frequency',
             labels={'Interpretation':'Customer Segment', 'Customer Share (%)':'Customer Share (%)',
                    'Total Counts': 'Total Customers'})

    fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
    fig.update_yaxes(type='log')
    return fig
