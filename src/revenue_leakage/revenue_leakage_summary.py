from IPython.display import display, Markdown, Image, HTML



# ------------------------------------------------------------------------------------
# 1. Baseline Revenue Metrics: Summary
# ------------------------------------------------------------------------------------


def revenue_metrics_summary(revenue_baseline_metrics, revenue_leakage_percentage):
    """
    A function that generates the summary for revenue metrics:
    
    """
    
    total_expected_revenue_in_million = revenue_baseline_metrics.iloc[0,1]
    cancelled_revenue_in_millions = revenue_baseline_metrics.iloc[1, 1]
    rev_frm_comp_orders_in_millions = revenue_baseline_metrics.iloc[2, 1]
    df_html = revenue_baseline_metrics.to_html(index=False)
    display(Markdown(f"""
    
## Baseline Revenue Metrics: Summary
{"--" * 50}

- The headline revenue metrics provide a high-level view of the platform’s overall revenue performance 
and operational efficiency.

- Out of a total market opportunity of **R\${total_expected_revenue_in_million}M**, the business successfully 
realized **R\${rev_frm_comp_orders_in_millions}M** in revenue from `delivered orders`, indicating that the vast 
majority of potential revenue was converted into actual sales.

- Revenue lost due to order cancellations amounts to **R\${cancelled_revenue_in_millions}M**, resulting in an 
overall revenue leakage of just **{revenue_leakage_percentage:.2f}%**. <br>

The metrics and the amounts have been presented in a tabular format below:


"""), HTML(df_html))
        

    display(Markdown(
f"""<br> From a business perspective, this is a strong operational signal:

1. A revenue leakage below 1% (**{revenue_leakage_percentage:.2f}%**) suggests effective order fulfillment and low cancellation impact

2. The gap between expected and realized revenue is minimal, indicating stable customer transactions and reliable logistics

3. Revenue loss from cancellations exists but is not a material risk at the aggregate level.


However, while the overall leakage percentage is low, this aggregate view can mask underlying patterns. 
A small total leakage may still be concentrated within specific order types, customer segments, or specific 
product categories, which could represent optimization opportunities.

This motivates a deeper, granular analysis, starting with a breakdown of orders by status.

#### NEXT SECTION: `Order Status Breakdown`
"""))

  


# ------------------------------------------------------------------------------------
# 2. Order Status Breakdown: Summary
# ------------------------------------------------------------------------------------

def order_status_breakdown_summary(breakdown_of_orders, total_n_orders, cancelled_orders_with_items, cancelled_orders_without_items):
    """
    This function will be responsible to summarize the order_status_breakdown section.
    """
    breakdown_of_orders_html = breakdown_of_orders.to_html(index=False)
    cancelled_orders = breakdown_of_orders[breakdown_of_orders['order_status'] == 'canceled']['total_n_orders'].iloc[0]

    display(Markdown(f""" 
## Order Status Breakdown: Summary

{"--" * 50}
    
The company had a total number of **{total_n_orders}** orders. The table below summarizes the break down of these 
orders.

"""), (HTML(breakdown_of_orders_html)))
    
    display(Markdown(f"""
The company had a total of **{cancelled_orders}** canceled orders. If we further breakdown these canceled orders,
there are two kinds of orders:
1. Canceled orders `with-items`: **{cancelled_orders_with_items.iloc[:, 0].values[0]}**
2. Canceled orders `without-items`: **{cancelled_orders_without_items.iloc[:, 0].values[0]}**

Which results to total canceled orders we have i.e. 

**Total canceled orders** ({cancelled_orders}) = 
**Total canceled orders with items** ({cancelled_orders_with_items.iloc[:, 0].values[0]}) + **Total canceled orders without items** ({cancelled_orders_without_items.iloc[:, 0].values[0]})
"""))
    



# ------------------------------------------------------------------------------------
# 3. Category-Level Revenue Leakage: Summary:
# ------------------------------------------------------------------------------------

def category_level_revenue_leakage_summary(revenue_lost_per_prodct_cat, prod_cat_w_max_amount, prod_cat_w_min_amount,
                                           cancelled_orders, revenue_leakage_percentage, cancelled_orders_with_items_val,
                                           cancelled_orders_without_items_val,
                                           fig):
    
    revenue_lost_per_prodct_cat_html = revenue_lost_per_prodct_cat.to_html(index=False)
    prod_cat_w_max_amount_html = prod_cat_w_max_amount.to_html(index=False)
    prod_cat_w_min_amount_html = prod_cat_w_min_amount.to_html(index=False)
    
    display(Markdown(f""" 
## Category-Level Revenue Leakage: Summary:
                     
{"--" * 50}
    
We found out that there is a total of: **{cancelled_orders} cancelled orders** and a
revenue leakage of: **{revenue_leakage_percentage:.2f} %**, if we drill down, there are two categories of order cancellations:

1. **Total canceled orders with items ({cancelled_orders_with_items_val}):**
These are the orders where a customer placed an order, the items were ready to be shipped but customer canceled the orders
at the end moment before the shipment started resulting to the creation of `order_id` in the `order_items` table. 

2. **Total canceled orders without items ({cancelled_orders_without_items_val}):** These are the orders where a customer 
placed an order but due to certain scenarios like **payment failure or app crash**, the orders never reached the item level
`order_id` resulting in the creation of `order_id` in the `orders` table only.


The table below lists the **product categories** whose orders were canceled and are displayed in
descending order w.r.t `total_amount`, where, the table consists
of `product_category`, `total_amount`, and `revenue_leak_percentage`"""), HTML(revenue_lost_per_prodct_cat_html))
    
    
    display(Markdown(f""" Where, the **maxiumum** values was: """), HTML(prod_cat_w_max_amount_html))
    display(Markdown(f""" and the the **minimum** values was: """), HTML(prod_cat_w_min_amount_html))
    
    
    display(Markdown(f"""To get the better idea, the chart below plots the top 10 `product_categories`, based
    on their contribution in the total revenue leakage:"""))
    display(fig)
    fig.write_image("../plot_images/Top_10_Product_Categories_by_Revenue_Loss.png", width=1200, height=600, scale=2)
    display(Image(filename="../plot_images/Top_10_Product_Categories_by_Revenue_Loss.png"))






# ------------------------------------------------------------------------------------
# 4. Category Level Comparison Analysis (Canceled Volume vs Revenue Loss): Summary
# ------------------------------------------------------------------------------------


def category_lvl_vol_vs_rvn_summary(fig, cncl_count_and_amount_by_prd_cat):
    
    display(Markdown(f"""
## Category Level Comparison Analysis (Canceled Volume vs Revenue Loss) - Summary: 

{"--" * 50}

To further understand the drivers of revenue leakage, a category-level comparison was conducted
between the **number of cancelled orders** and the **total revenue lost** per product category.

The scatter plot below visualizes this relationship:
- Each point represents a product category
- The x-axis shows the number of cancelled orders
- The y-axis shows the total revenue lost
- Color intensity (red scale) represents the magnitude of revenue loss
"""))

    display(fig)

    fig.write_image("../plot_images/High_revenue_loss_despite_low_cancellations.png", scale=2, width=1200, height=600)
    display(Image(filename="../plot_images/High_revenue_loss_despite_low_cancellations.png"))

    display(Markdown(f"""
## Hypothesis Evaluation:

**Hypothesis 1:**  
*High-priced or logistics-heavy categories will show disproportionately high revenue loss, even if cancellation volume is low.*

**Supported:**  
- The visualization reveals at least one category with a relatively **low number of cancellations**
but **exceptionally high revenue loss**, indicating that high item value or logistics costs
can amplify financial impact even when cancellation volume is moderate.

---

**Hypothesis 2:**  
*Some categories may have high cancellation rates but low revenue impact, indicating operational inefficiencies rather than financial risk.*

**Supported:**  
- Several categories follow a near-linear relationship where higher cancellation volume
results in proportionally higher revenue loss. However, some categories exhibit
**high cancellation counts with comparatively lower revenue loss**, suggesting
process inefficiencies rather than major financial exposure.


There was just one outlier or a product category that is marked in the scatter plot above, where the number of cancellations
was low but the financial impact it had was high compared to all the products displayed below:
"""))
    display(cncl_count_and_amount_by_prd_cat[cncl_count_and_amount_by_prd_cat['product_category'] == 'cool_stuff'])

    display(Markdown("""
## Key Takeaways:

- Revenue leakage is **not solely driven by cancellation volume**
- Certain categories pose **higher financial risk per cancellation**
- Category-level analysis enables **prioritized intervention**:
  - High revenue loss categories → pricing, logistics, supplier review
  - High cancellation volume but low loss → operational and process improvements

This analysis highlights the importance of evaluating **both frequency and financial impact**
when addressing revenue leakage.
"""))
