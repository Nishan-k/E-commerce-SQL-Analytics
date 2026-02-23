from IPython.display import display, Markdown, Image, HTML



# ------------------------------------------------------------------------------------
# 1. Recency Analysis: Summary
# ------------------------------------------------------------------------------------


def get_recency_analysis_summary(recency_table_full, customers_per_bins_labeled_df, fig):

    """
    This function is responsible to generate the summary for the R of RFM analysis
    i.e. for recency analysis and takes positional arguement
    """

    display(Markdown(
  
f""" ## Summary: Recency Analysis Per Customer:
<hr>

### Objective:<br>
This analysis measures customer recency by calculating the number of days since a customer’s most recent delivered purchase. Since the dataset is 
historical and not up to date, `a fixed reference date of 2018-09-08` (**10 days** after the last recorded purchase) was used instead of the current date to avoid 
misleading recency values. Each customer is included only once by selecting their latest completed order using a `window function`.                
                                          
### Key Insights:<br>                     

- On average, customers take approximately **248 days** to place their `second purchase`, indicating a long repurchase cycle.

- Out of **96,478 customers**, only **18,741** return within **1–100 days**, while the majority **(45,240 customers)** make a second 
purchase between **100–300 days.**

- A significant portion of customers show very long gaps between purchases, with **25,406 customers** returning after **300–500 days**, and 
**7,091** customers taking more than **500 days.**

- Overall, repeat purchasing behavior is heavily concentrated in the **100–300 day window,** suggesting low short-term retention and 
a slow repeat-purchase cycle.


<hr>
                                          
> The bar chart below visualizes customer counts across 50-day recency bins, highlighting the delayed repurchase behavior.             
                                                                              
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

    display(Markdown(
f""" ## Summary: Frequency Analysis

<hr>

### Objective:                                                               
This analysis examines customer buying frequency by counting the number of `distinct orders` per customer. The `goal is to identify repeat 
customers, highlight high-value segments, and understand potential churn risk from one-time buyers.` For better business interpretation, customers 
are grouped into `five frequency-based segments`.

                     
**Customer Segments:**
- `One-Time Buyer:` 1 order
- `Returning Customer:` 2 orders
- `Loyal Customer:` 3 orders
- `Very Loyal Customer:` 4 orders
- `VIP Customers:` 5 or more orders                     

### Key Insights:
- The frequency distribution is `heavily right-skewed`, with `One-Time Buyers` dominating the customer base at **97.00% (90,557 customers).**
- Returning (**2.756% or 2,573 customers**) and Loyal (**0.194% or 181 customers**) egments are much smaller but represent the early stages of repeat purchasing.              
- Very Loyal (**0.030% or 28 customers**)  and VIP (**0.020% or 19 customers**)  makeup a very small fraction but are likely to generate higher lifetime value.           
- Overall, the business relies strongly on `One-Time Buyers`, while repeat purchase behavior is limited across. 
- A logarithmic scale was used in the frequency distribution chart to prevent one-time buyers from visually dominating the 
chart and to allow clearer comparison across smaller but more valuable customer segments.

<hr>
> ### Business Implications:
The strong dependence on one-time buyers suggests a high risk of customer churn after the first purchase. 
While high-frequency customers are few, they represent an opportunity for long-term value creation. The business could 
benefit from retention-focused strategies such as `repeat-purchase incentives, targeted communication for returning customers, and basic loyalty or CRM programs`
to encourage customers to move into higher-frequency segments.

> The bar chart below visualizes the customer purchase frequency in % in 5 different segments:                                                                                           
"""))
    
    fig.show()
    
    




# ------------------------------------------------------------------------------------
# 3. Monetary Analysis: Summary
# ------------------------------------------------------------------------------------

def get_monetary_analysis_summary(segment_monetary_summary_w_customer_share, fig):
    """
    This function is responsible to generate the summary for the M of RFM analysis
    i.e. for monetary analysis and takes positional arguement
    """

    display(Markdown(
f""" ## Summary: Monetary Analysis
<hr>

### Objective:
Analyze the `total revenue, the average revenue per customer, and the revenue contribution(%)` of the customers, based on the **5-Segments** 
defined in the `frequency analysis`. Only `delivered` orders are considered to ensure that the revenue analyzed was actually realized by the business. 
The goal is to identify `which customer segments contribute the most value and understand the drivers of revenue generation.`                   

### Key Insights:
-Revenue is heavily concentrated among `One-Time Buyers`, who account for **90,557** customers, generate **$\R 14.55 M** in total revenue, and 
contribute **97.0%** of overall revenue, despite having a relatively low average revenue of **$\R 160.73** per customer. 
- As purchase frequency increases, average revenue per customer rises sharply, even though the number of customers decreases. 
Across repeat customer segments, the average revenue per customer ranges from **$\R 291.02** to **$\R 787.14**.
- Although repeat customer segments contribute less than **2.7%** of total revenue combined, they are significantly more valuable on 
a per-customer basis compared to `One-Time Buyers`.
- Overall, the results show that `transaction volume, rather than customer value, is the primary driver of total revenue.`

<hr>

> ### Business Implication:
The company’s current revenue model is `strongly volume-driven and depends heavily on `One-Time Buyers`. While repeat customers generate higher 
revenue per customer, their small numbers limit their overall impact. This indicates `an opportunity to improve long-term revenue by increasing 
repeat purchase rates through retention-focused strategies, such as post-purchase engagement, targeted offers for returning customers, or simple loyalty programs.`


> The chart below displays the comparison between the <b>Volume</b> and <b>Value</b>, where the bar chart represent the **volume**, while the line chart represents the
**value**:
            
 """))
    
    fig.show()
    
    





def get_key_findings_and_interp():
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