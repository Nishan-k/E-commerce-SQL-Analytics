import plotly.express as px
import plotly.graph_objects as go
import pandas as pd






# 1. A bar chart for top 10 product categories based on the revenue loss due to the order cancellation:

def plot_top_10_product_categories_by_revenue_loss(top_10_canceled_prod_category:pd.DataFrame):
    """
    This function plots a bar chart for the top 10 products where the revenue was lost due to order cancelation.

    Parameters:
    ------------
    top_10_canceled_prod_category: a pandas dataframe that holds the information required to generate the plot.

    Returns:
    --------
    A bar chart showing the top 10 products where the revenue was lost due to order cancelation.
    """

    fig = px.bar(data_frame=top_10_canceled_prod_category,
                 x='product_category',
                 y='total_amount', 
                     title='Top 10 Product Categories by Revenue Loss',
                     labels={'product_category': 'Product Category',
                             'total_amount': 'Revenue Lost'},
                     text= 'total_amount',
                     color = 'total_amount',
                     color_continuous_scale = 'sunsetdark')
    
    fig.update_traces(texttemplate = "%{text:.2f}", 
                      textposition = "outside")
    fig.write_html("../plot_html/Top_10_Product_Categories_by_Revenue_Loss.html")
    return fig



# 2. A scatter plot to compare cancelation volume Vs cancelation revenue loss:

def plot_cancelation_volume_vs_revenue_loss(cncl_count_and_amount_by_prd_cat: pd.DataFrame):
    """
    This function takes in the dataframe with cancelatoin volume and revenue loss by product category and plots a scatter plot to show their relation
    for our hypothesis.

    Parameters:
    ------------
    cncl_count_and_amount_by_prd_cat: a pandas dataframe that holds the information about cancelation volume and revenue by product category

    Returns:
    --------
    A scatter plot to compare cancelation volume Vs cancelation revenue loss
    """

    fig = px.scatter(data_frame=cncl_count_and_amount_by_prd_cat,
                x='total_n_orders', 
                y='total_amount', 
                size='total_amount',
                color='total_amount',
                color_continuous_scale='OrRd',
                hover_name='product_category',
                hover_data = {
                    'total_n_orders': True,
                    'total_amount': ':.2f'
                },
                title='Category Level Comparison (Cancellation Volume vs Revenue Loss)',
                labels={
                    'total_n_orders': 'Number of cancelled Orders',
                    'total_amount': 'Total Revenue Lost'
                })
    
    fig.update_traces( hovertemplate=
                        "<b>Category:</b> %{hovertext}<br>" +
                        "<b>Cancelled Orders:</b> %{x}<br>" +
                        "<b>Revenue Lost:</b> %{y:.2f}<br>" +
                        "<extra></extra>", 
                    marker=dict(opacity=0.75, 
                    line=dict(width=1, 
                    color='black')))
    
    fig.add_annotation(
        x=16,
        y=15153.48,
        text="High revenue loss despite low cancellations",
        showarrow=True,
        arrowhead=2,
        ax=40,
        ay=-40
    )

    fig.write_html("../plot_html/Cancellation_Volume_vs_Revenue_Loss.html")
    return fig