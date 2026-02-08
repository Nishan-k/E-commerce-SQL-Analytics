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
