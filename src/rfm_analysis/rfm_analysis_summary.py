from IPython.display import display, Markdown, Image, HTML



# ------------------------------------------------------------------------------------
# 1. Recency Analysis: Summary
# ------------------------------------------------------------------------------------


def get_revenue_analysis_summary(recency_table_full, customers_per_bins_labeled_df, fig):
    """
    This function is responsible to generate the summary for the R of RFM analysis
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
    




# ------------------------------------------------------------------------------------
# 2. Frequency Analysis: Summary
# ------------------------------------------------------------------------------------

def get_frequency_analysis_summary(customer_order_frequency_interpretation_counts, fig):
    """
    This function is responsible to generate the summary for the F of RFM analysis
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
    
        
    display(Markdown("""
Overall, the Frequency analysis reveals that the business is highly dependent on **first-time buyers**, highlighting a significant opportunity for:
- Retention strategies
- Repeat purchase incentives
- Loyalty and CRM programs

These insights will be especially valuable when combined with **Monetary value** in the final RFM segmentation.
"""))
    




# ------------------------------------------------------------------------------------
# 3. Monetary Analysis: Summary
# ------------------------------------------------------------------------------------

def get_monetary_analysis_summary(segment_monetary_summary_w_customer_share, fig):
    """
    This function is responsible to generate the summary for the M of RFM analysis
    i.e. for monetary analysis and takes positional arguement
    """

    display(Markdown(f"""
## Monetary Analysis Conclusion:

Monetary analysis focuses on understanding **how much revenue customers generate**, not just how often they purchase.
While Frequency identifies repeat behavior, **Monetary highlights customer value**.

In this analysis:
- Only **delivered orders** were considered to ensure that revenue reflects completed transactions.
- Monetary value was calculated at the **order item level** to capture the true transaction amount, then aggregated to the
  `customer_unique_id` level.
- The monetary data was joined with the previously defined **Frequency-based customer segments**, allowing revenue
  contribution and customer value to be analyzed together."""))
        
    display(segment_monetary_summary_w_customer_share)
        
    display(Markdown("The chart below displays the comparison between the <b>Volume</b> and <b>Value</b>"))
    fig.show()
    





def get_key_findings_and_intrerp():
    display(Markdown("""
### Key Findings:

- **One-Time Buyers** generate the **highest total revenue** overall, primarily due to their overwhelming volume
  (≈97% of the customer base), despite having the **lowest average revenue per customer**.
- **Returning, Loyal, and Very Loyal customers**, although significantly fewer in number, contribute **progressively higher
  average revenue per customer**, indicating stronger individual customer value.
- **VIP Customers** represent the smallest segment but show **one of the highest average revenues per customer**,
  highlighting their importance from a long-term value perspective rather than volume.
- The contrast between **total revenue (volume-driven)** and **average revenue per customer (value-driven)** reveals that
  revenue concentration alone can be misleading without considering customer quality.

### Business Interpretation:

- Revenue is currently **volume-driven**, dominated by One-Time Buyers.
- However, **high-frequency segments deliver disproportionately higher value per customer**, making them ideal targets
  for:
  - Retention strategies
  - Personalized marketing
  - Loyalty and reward programs

The final visualization effectively demonstrates this dual perspective by:
- Using **Log₁₀ scaled total revenue** to highlight revenue concentration.
- Overlaying **average revenue per customer** to reveal customer value across segments.

This analysis reinforces the importance of balancing **customer acquisition** with **customer retention and value growth**
to build a sustainable revenue strategy.
"""))