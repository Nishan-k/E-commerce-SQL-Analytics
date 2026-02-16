from IPython.display import display, Markdown, Image, HTML




# ------------------------------------------------------------------------------------
# 1. Revenue Realization Per State: Summary
# ------------------------------------------------------------------------------------

def get_revenue_real_per_state_summary(highest_rev_generating_state, lowest_rev_generating_state, plt_total_rev_by_state, total_states):
    """
    Returns a summary for the Revenue Realization Per State section:
    """

    display(Markdown(f""" ## Summary: Revenue Realization Per State:   
                     
<hr>                   

### Objective:<br>
Analyze the total **realized revenue** across **{total_states}** Brazilian states (based on *delivered orders only*) and 
visualize the geographic revenue distribution using a choropleth map, where color intensity represents revenue magnitude.


### Key Insights:<br>
- **{highest_rev_generating_state['state_names'].iloc[0]}** is the **highest revenue-generating state**, contributing **R$ 
{highest_rev_generating_state['total_revenue'].iloc[0]:,.2f}**  (**{highest_rev_generating_state['revenue_contribution (%)'].iloc[0]:.2f}%** of total revenue).

- **{lowest_rev_generating_state['state_names'].iloc[0]}** is the **lowest revenue-generating state**, contributing **R$ 
{lowest_rev_generating_state['total_revenue'].iloc[0]:,.2f}** (**{lowest_rev_generating_state['revenue_contribution (%)'].iloc[0]:.2f}%** of total revenue.


<hr>

> The choropleth visualization highlights strong geographic revenue concentration, enabling quick identification of high-value and underperforming regions.
"""))
    
    plt_total_rev_by_state.show()



# ------------------------------------------------------------------------------------
# 1. Order-Volume Per State: Summary
# ------------------------------------------------------------------------------------
def get_order_volume_per_state_summary(total_states, highest_order_volume, lowest_order_volume, plot):
     
     """
        Returns a summary for the Order-Volume Per State section:
     """
     display(Markdown(f""" ## Summary: Order Volume Per State:

<hr>

### Objective:<br>
Analyze the **total volume of orders** across the **{total_states}** Brazilian states based on delivered orders and visualize the
geographic order volume distribution via choropleth map, where the color intensity represents the magnitude of
the volume of orders made.
<br>

## Key Insights:
- `{highest_order_volume['state_names'].iloc[0]}` has **the highest volume for orders** and is also **the highest
revenue generating state**.

- `{lowest_order_volume['state_names'].iloc[0]}` has **the lowest volume for orders** and is also **the lowest 
revenue generating state**.
- The `Volume of Order` and `Revenue Generation` has **a linear relationship for these two states**, this relationship
will be analyzed for other states in the later stage.


> The choropleth visualization below highlights strong geographic order-volume concentration, enabling quick 
identification of states where the most of the revenue for the company lies in:

"""))
     

     plot.show()

     
