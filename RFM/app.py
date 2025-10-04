import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
import datetime as dt
import traceback
import io

# --- App Configuration ---
app = FastAPI()
sns.set_theme(style="whitegrid")

# --- RFM Analysis Logic (Robust Version) ---
def perform_rfm_analysis(file_path: str):
    try:
        df = pd.read_csv(file_path)
        df['invoice_date'] = pd.to_datetime(df['invoice_date'], format='%d-%m-%Y', errors='coerce')
        df.dropna(subset=['invoice_date'], inplace=True)
        df['total_price'] = df['quantity'] * df['price']
        
        snapshot_date = df['invoice_date'].max() + dt.timedelta(days=1)
        rfm = df.groupby('customer_id').agg({
            'invoice_date': lambda date: (snapshot_date - date.max()).days,
            'invoice_no': 'count',
            'total_price': 'sum'
        }).rename(columns={
            'invoice_date': 'Recency', 'invoice_no': 'Frequency', 'total_price': 'MonetaryValue'
        })

        r_labels, f_labels, m_labels = range(4, 0, -1), range(1, 5), range(1, 5)
        
        rfm['R_Score'] = pd.qcut(rfm['Recency'], q=4, labels=r_labels, duplicates='drop')
        rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), q=4, labels=f_labels, duplicates='drop')
        rfm['M_Score'] = pd.qcut(rfm['MonetaryValue'], q=4, labels=m_labels, duplicates='drop')

        rfm['R_Score'] = rfm['R_Score'].astype(int)
        rfm['F_Score'] = rfm['F_Score'].astype(int)
        rfm['M_Score'] = rfm['M_Score'].astype(int)
        rfm['RFM_Score'] = rfm[['R_Score', 'F_Score', 'M_Score']].sum(axis=1)

        def assign_segment(score):
            if score >= 11: return 'Champions'
            elif score >= 9: return 'Loyal Customers'
            elif score >= 7: return 'Potential Loyalists'
            elif score >= 5: return 'At-Risk Customers'
            else: return 'Lost Customers'
        rfm['Segment'] = rfm['RFM_Score'].apply(assign_segment)

        return rfm.reset_index()
    except Exception:
        print(f"💥 An error occurred during RFM analysis:")
        print(traceback.format_exc())
        return None

# --- Server Startup ---
@app.on_event("startup")
async def startup_event():
    print("🚀 Server starting up... Performing RFM analysis.")
    app.state.rfm_df = perform_rfm_analysis("customer_shopping_data.csv")
    if app.state.rfm_df is not None:
        print(f"✅ RFM analysis complete. {len(app.state.rfm_df)} customers loaded.")
    else:
        print("❌ RFM analysis failed. Please check the error message above.")


# --- HTML and API Endpoints ---
@app.get("/", response_class=HTMLResponse)
async def serve_dashboard():
    with open("index.html") as f:
        return f.read()

def plot_to_png_response(fig):
    """Saves a matplotlib figure to a PNG in memory and returns a StreamingResponse."""
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight')
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")

@app.get("/api/charts/segments")
async def chart_segments(request: Request):
    rfm_df = request.app.state.rfm_df
    if rfm_df is None: return HTMLResponse("Data not available", status_code=500)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(ax=ax, data=rfm_df, x='Segment', order=rfm_df['Segment'].value_counts().index, palette='viridis')
    ax.set_title('Customer Segmentation', fontsize=16)
    ax.tick_params(axis='x', rotation=45)
    return plot_to_png_response(fig)

@app.get("/api/charts/distributions")
async def chart_distributions(request: Request):
    rfm_df = request.app.state.rfm_df
    if rfm_df is None: return HTMLResponse("Data not available", status_code=500)
    
    fig, axes = plt.subplots(3, 1, figsize=(10, 15))
    fig.suptitle('RFM Distributions', fontsize=20)
    
    sns.histplot(ax=axes[0], data=rfm_df, x='Recency', kde=True).set_title('Recency (Days)')
    sns.histplot(ax=axes[1], data=rfm_df, x='Frequency', kde=True).set_title('Frequency (Purchases)')
    sns.histplot(ax=axes[2], data=rfm_df, x='MonetaryValue', kde=True).set_title('Monetary Value')
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    return plot_to_png_response(fig)