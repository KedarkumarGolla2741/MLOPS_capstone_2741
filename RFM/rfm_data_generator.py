import pandas as pd
import datetime as dt

def generate_rfm_data():
    """
    Performs RFM analysis and saves the results to a CSV file with clean data types.
    """
    try:
        df = pd.read_csv('customer_shopping_data.csv')
    except FileNotFoundError:
        print("Error: 'customer_shopping_data.csv' not found.")
        print("Please make sure the data file is in the same directory.")
        return

    df['invoice_date'] = pd.to_datetime(df['invoice_date'], format='%d-%m-%Y')
    df['total_price'] = df['quantity'] * df['price']
    snapshot_date = df['invoice_date'].max() + dt.timedelta(days=1)
    
    rfm = df.groupby('customer_id').agg({
        'invoice_date': lambda date: (snapshot_date - date.max()).days,
        'invoice_no': 'count',
        'total_price': 'sum'
    })
    rfm.rename(columns={'invoice_date': 'Recency',
                        'invoice_no': 'Frequency',
                        'total_price': 'MonetaryValue'}, inplace=True)

    r_labels = range(4, 0, -1)
    f_labels = range(1, 5)
    m_labels = range(1, 5)

    rfm['R_Score'] = pd.qcut(rfm['Recency'], q=4, labels=r_labels)
    rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), q=4, labels=f_labels)
    rfm['M_Score'] = pd.qcut(rfm['MonetaryValue'], q=4, labels=m_labels)
    rfm['RFM_Score'] = rfm[['R_Score', 'F_Score', 'M_Score']].sum(axis=1)

    def assign_segment(score):
        if score >= 11: return 'Champions'
        elif score >= 9: return 'Loyal Customers'
        elif score >= 7: return 'Potential Loyalists'
        elif score >= 5: return 'At-Risk Customers'
        else: return 'Lost Customers'
    rfm['Segment'] = rfm['RFM_Score'].apply(assign_segment)

    # --- FIX APPLIED HERE ---
    # Convert special pandas data types to standard Python types.
    # This prevents serialization errors in the web app.
    rfm['R_Score'] = rfm['R_Score'].astype(int)
    rfm['F_Score'] = rfm['F_Score'].astype(int)
    rfm['M_Score'] = rfm['M_Score'].astype(int)
    rfm['RFM_Score'] = rfm['RFM_Score'].astype(int)
    rfm['Segment'] = rfm['Segment'].astype(str)
    
    rfm.to_csv('rfm_analysis.csv')
    print(f"✅ RFM analysis data for {len(rfm)} customers saved to 'rfm_analysis.csv' with corrected data types.")

if __name__ == "__main__":
    generate_rfm_data()