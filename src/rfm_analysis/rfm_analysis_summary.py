from IPython.display import display, Markdown, Image, HTML



# ------------------------------------------------------------------------------------
# 1. Recency Analysis: Summary
# ------------------------------------------------------------------------------------


def revenue_analysis_summary(recency_table_full, customers_per_bins_labeled_df, fig):
    """
    This function is responsible to genereate the summary for the R of RFM analysis
    i.e. for revenue analysis and takes positional arguement
    """
    display(Markdown(f"""
## Recency Analysis Conclusion:

Recency measures how long it has been since a customer’s **most recent completed purchase.** 

In this analysis:
- Only orders with `delivered` status were considered to ensure revenue realization.
- **Recency** was calculated as the number of days between a customer's latest purchase timestamp and a threshold set as
`DATE(MAX(order_purchase_timestamp), '+10 days')` .i.e. **{recency_table_full['date_threshold'].iloc[0]}**. This approach was 
chosen because the dataset is historical, and using the current date would distort recency values.

- Each customer is recorded once using a `WINDOW FUNCTION` to capture their most recent purchase.

The resulting table `recency_table_full` holds the entire information at a customer level, leaving space for further
segmentation and drill-down analysis when required, `recency_table_full` holds a data of **{recency_table_full.shape[0]}** rows 
and **{recency_table_full.shape[1]}** features, as a glimpse, here is what it looks like: """))
    display(recency_table_full.head(5))


    display(Markdown(f"""
To improve interpretability, customers were grouped into **50-day recency bins**, allowing the analysis to be performed
at an aggregated level while preserving the underlying customer-level data:
"""))
    display(customers_per_bins_labeled_df)

    display(Markdown("""
The chart below visualizes the distribution of customers across recency bins, highlighting how customer activity
declines as time since last purchase increases:
"""))
    fig.show()
    fig.write_image("../plot_images/Customers_Distribution_By_Recency.png", width=1200, height=600, scale=2)
    display(Image(filename="../plot_images/Customers_Distribution_By_Recency.png"))




# ------------------------------------------------------------------------------------
# 2. Frequency Analysis: Summary
# ------------------------------------------------------------------------------------

def frequency_analysis_summary(customer_order_frequency_interpretation_counts, fig):
    """
    This function is responsible to genereate the summary for the F of RFM analysis
    i.e. for frequency analysis and takes positional arguement
    """

    display(Markdown("""
## Frequency Analysis Conclusion:

Frequency measures **how often a customer makes a complete purchase**.

In this analysis:
- Only orders with `delivered` status were considered to ensure that each counted order represents a 
**completed and revenue-realized transaction**.
- Since a single customer in the OLIST dataset may have multiple `customer_id`s across different orders, 
all frequency calculations were performed at the **`customer_unique_id` level**, which represents a real-world customer.
- The frequency metric was calculated as the **number of distinct orders per customer**.

The resulting table `customer_order_frequency_interpretation` contains **one row per unique customer**, along with:
- `total_orders`: total number of completed purchases
- `Interpretation`: a business-friendly customer segment based on purchase behavior.

To make the results interpretable from a business perspective, customers were segmented as follows:

- **One-Time Buyer**: 1 order  
- **Returning Customer**: 2 orders  
- **Loyal Customer**: 3 orders  
- **Very Loyal Customer**: 4 orders  
- **VIP Customers**: 5 or more orders
"""))

    display(customer_order_frequency_interpretation_counts)


    display(Markdown(f"""
The frequency distribution shows a **strongly right-skewed pattern**, indicating that the majority of 
customers placed only a single order:

- `One-Time Buyer`s dominate the customer base, accounting for **96.947% of all customers**
- Returning and Loyal customers form a much smaller but strategically important segment
- VIP Customers represent a very small fraction but are likely to contribute **disproportionately higher lifetime value**

To properly visualize this imbalance, a **logarithmic scale** was used in the frequency distribution chart. 
This approach prevents one-time buyers from visually overwhelming the chart and allows meaningful comparison 
between smaller yet valuable customer segments."""))

    fig.show()
    fig.write_image("../plot_images/Customer_Segmentation_by_Purchase_Frequency.png", width=1200, height=600, scale=2)
    display(Image(filename="../plot_images/Customer_Segmentation_by_Purchase_Frequency.png"))
        
    display(Markdown("""
Overall, the Frequency analysis reveals that the business is highly dependent on **first-time buyers**, highlighting a significant opportunity for:
- Retention strategies
- Repeat purchase incentives
- Loyalty and CRM programs

These insights will be especially valuable when combined with **Monetary value** in the final RFM segmentation.
"""))