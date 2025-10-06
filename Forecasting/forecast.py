import pandas as pd
from prophet import Prophet
import warnings

# Suppress informational messages from Prophet
import logging
logging.getLogger('cmdstanpy').setLevel(logging.WARNING)

warnings.filterwarnings("ignore")

# Load the datasets
try:
    shopping_data = pd.read_csv('customer_shopping_data.csv')
    region_data = pd.read_csv('Region_detail_table.csv')
except FileNotFoundError:
    print("Make sure 'customer_shopping_data.csv' and 'Region_detail_table.csv' are in the same directory as this script.")
    exit()

# Merge the datasets
df = pd.merge(shopping_data, region_data, on='shopping_mall')

# Data Preprocessing
df['invoice_date'] = pd.to_datetime(df['invoice_date'], dayfirst=True)
df['sales'] = df['price'] * df['quantity']

# Group data and create time series
df_grouped = df.groupby(['shopping_mall', 'Region', 'category', 'invoice_date']).agg({'sales': 'sum'}).reset_index()

# Get all unique combinations of shopping_mall, Region, and category
groups = df_grouped[['shopping_mall', 'Region', 'category']].drop_duplicates().to_dict('records')

all_forecasts = []

# Forecast for the next 90 days (3 months)
forecast_steps = 90

print("Starting forecasting with enhanced Facebook Prophet...")

for group in groups:
    mall = group['shopping_mall']
    region = group['Region']
    category = group['category']

    # Filter data for the current group
    group_df = df_grouped[(df_grouped['shopping_mall'] == mall) &
                          (df_grouped['Region'] == region) &
                          (df_grouped['category'] == category)]

    if group_df.shape[0] < 10: # Increased minimum data points for better modeling
        print(f"Skipping forecast for {mall} - {region} - {category} due to insufficient data.")
        continue

    # Prepare data for Prophet (requires 'ds' and 'y' columns)
    prophet_df = group_df[['invoice_date', 'sales']].rename(columns={
        'invoice_date': 'ds',
        'sales': 'y'
    })

    try:
        # --- NEW: Initialize Prophet with enhanced parameters ---
        model = Prophet(
            seasonality_mode='multiplicative',  # Use multiplicative seasonality for sales data
            changepoint_prior_scale=0.1,        # Increase trend flexibility
            yearly_seasonality=True,
            weekly_seasonality=True
        )

        # Add country-specific holidays (assuming data is from Turkey)
        model.add_country_holidays(country_name='TR')

        # Add a custom monthly seasonality
        model.add_seasonality(name='monthly', period=30.5, fourier_order=5)

        # Fit the model
        model.fit(prophet_df)

        # Create a dataframe for future dates
        future = model.make_future_dataframe(periods=forecast_steps)
        
        # Generate the forecast
        forecast = model.predict(future)
        
        # Extract the forecasted values for the future period
        forecasted_values = forecast['yhat'].iloc[-forecast_steps:].values

        # Get the dates for the forecast period
        max_date = prophet_df['ds'].max()
        forecast_dates = pd.date_range(start=max_date + pd.Timedelta(days=1), periods=forecast_steps)

        # Create a dataframe for the forecast
        forecast_df_out = pd.DataFrame({
            'shopping_mall': mall,
            'Region': region,
            'category': category,
            'forecast_date': forecast_dates,
            'forecasted_sales': forecasted_values
        })
        all_forecasts.append(forecast_df_out)

    except Exception as e:
        print(f"Could not forecast for {mall} - {region} - {category}: {e}")

# Concatenate all forecasts
if all_forecasts:
    final_forecast_df = pd.concat(all_forecasts, ignore_index=True)
    # Ensure forecasted sales are not negative
    final_forecast_df['forecasted_sales'] = final_forecast_df['forecasted_sales'].clip(lower=0)
    # Save forecasts to a CSV file
    final_forecast_df.to_csv('sales_forecast.csv', index=False)
    print("\nForecasting complete. Forecasts saved to sales_forecast.csv")
else:
    print("\nNo forecasts were generated.")