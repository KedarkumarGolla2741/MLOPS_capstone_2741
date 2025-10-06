import pandas as pd
from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse
import matplotlib
import seaborn as sns
import matplotlib.pyplot as plt
import io
import uvicorn

# Set the Matplotlib backend
matplotlib.use('Agg')

app = FastAPI()

# Load original data to populate filters and for plotting
try:
    shopping_data = pd.read_csv('customer_shopping_data.csv')
    # --- CHANGE: Convert date column on load ---
    shopping_data['invoice_date'] = pd.to_datetime(shopping_data['invoice_date'], dayfirst=True)
    region_data = pd.read_csv('Region_detail_table.csv')
    original_df = pd.merge(shopping_data, region_data, on='shopping_mall')
    # --- CHANGE: Calculate sales column on load ---
    original_df['sales'] = original_df['price'] * original_df['quantity']
except FileNotFoundError:
    original_df = pd.DataFrame()
    print("Warning: Original data files not found. Filter dropdowns may be empty.")

# Load the forecasted data
try:
    forecast_df = pd.read_csv('sales_forecast.csv')
    forecast_df['forecast_date'] = pd.to_datetime(forecast_df['forecast_date'])
except FileNotFoundError:
    forecast_df = pd.DataFrame()

@app.get("/dashboard", response_class=HTMLResponse)
async def read_dashboard():
    try:
        with open("index.html") as f:
            return HTMLResponse(content=f.read(), status_code=200)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Error: index.html not found in the same directory.</h1>", status_code=404)

@app.get("/filters")
def get_filters():
    if original_df.empty:
        return {"error": "Original data not found, cannot populate filters."}
    
    filters = {
        "shopping_malls": sorted(original_df['shopping_mall'].unique().tolist()),
        "regions": sorted(original_df['Region'].unique().tolist()),
        "categories": sorted(original_df['category'].unique().tolist())
    }
    return filters

@app.get("/")
def read_root():
    return {"message": "Sales Forecasting API. Go to /dashboard to see the UI."}

@app.get("/forecast/plot")
def get_forecast_plot(shopping_mall: str, region: str, category: str):
    if forecast_df.empty or original_df.empty:
        return Response(content="Data not found. Please run the forecasting script first.", status_code=404)

    # --- NEW LOGIC TO GET BOTH ACTUAL AND FORECAST DATA ---

    # 1. Get forecast data
    forecast_data = forecast_df[
        (forecast_df['shopping_mall'] == shopping_mall) &
        (forecast_df['Region'] == region) &
        (forecast_df['category'] == category)
    ]

    # 2. Get and prepare actual data
    actual_data_filtered = original_df[
        (original_df['shopping_mall'] == shopping_mall) &
        (original_df['Region'] == region) &
        (original_df['category'] == category)
    ]
    
    # Aggregate actual data to get daily sales totals
    actual_daily_sales = actual_data_filtered.groupby('invoice_date')['sales'].sum().reset_index()

    if forecast_data.empty or actual_daily_sales.empty:
        return Response(content="No data available for the selected criteria.", status_code=404)

    # 3. Determine the date range for the last year of actual data
    last_actual_date = actual_daily_sales['invoice_date'].max()
    one_year_prior = last_actual_date - pd.Timedelta(days=365)
    
    actual_data_last_year = actual_daily_sales[
        actual_daily_sales['invoice_date'] >= one_year_prior
    ]

    # 4. Create the combined plot
    plt.figure(figsize=(15, 7))

    # Plot last 1 year of actual data
    sns.lineplot(data=actual_data_last_year, x='invoice_date', y='sales', label='Actual Sales (Last 1 Year)')

    # Plot next 90 days of forecast data
    sns.lineplot(data=forecast_data, x='forecast_date', y='forecasted_sales', label='Forecasted Sales (Next 90 Days)', linestyle='--')

    plt.title(f'Sales History & Forecast for {category} in {shopping_mall} ({region})')
    plt.xlabel('Date')
    plt.ylabel('Sales')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()

    # Save plot to buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    return Response(content=buf.getvalue(), media_type="image/png")

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8090)