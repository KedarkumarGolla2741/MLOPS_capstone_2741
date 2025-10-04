import pandas as pd
import plotly.express as px
import plotly.io as pio
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

# Use a modern, clean Plotly theme
pio.templates.default = "plotly_white"

# Create the main FastAPI application object
app = FastAPI()

# This is a "lifespan event". It runs the code inside once, when the app starts.
@app.on_event("startup")
async def startup_event():
    """
    Loads the RFM data from the CSV file into the app's state when the server starts.
    This is efficient because it's only done once.
    """
    try:
        # Load the pre-calculated RFM data
        rfm_df = pd.read_csv("rfm_analysis.csv")
        # Store the dataframe in the app's state, so all requests can access it
        app.state.rfm_df = rfm_df
        print("✅ RFM data loaded successfully at startup.")
    except FileNotFoundError:
        print("❌ Error: 'rfm_analysis.csv' not found.")
        print("👉 Please run 'rfm_data_generator.py' first to create the data file.")
        app.state.rfm_df = None


@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serves the main HTML page for the dashboard."""
    with open("index.html") as f:
        return f.read()

# --- Chart Endpoints ---

@app.get("/api/charts/segments")
async def get_segment_chart(request: Request):
    """Creates and returns the customer segmentation bar chart."""
    rfm_df = request.app.state.rfm_df
    if rfm_df is None:
        return {"error": "Data not loaded"}
    
    segment_counts = rfm_df['Segment'].value_counts().reset_index()
    fig = px.bar(
        segment_counts,
        x='Segment',
        y='count',
        title="Customer Segmentation",
        color='Segment',
        text_auto=True,
        labels={'count': 'Number of Customers', 'Segment': 'Customer Segment'}
    )
    fig.update_layout(xaxis={'categoryorder':'total descending'}, showlegend=False)
    return fig.to_dict()


@app.get("/api/charts/recency")
async def get_recency_chart(request: Request):
    """Creates and returns the Recency histogram."""
    rfm_df = request.app.state.rfm_df
    if rfm_df is None:
        return {"error": "Data not loaded"}

    fig = px.histogram(rfm_df, x="Recency", title="Recency (Days) Distribution", nbins=40)
    return fig.to_dict()


@app.get("/api/charts/frequency")
async def get_frequency_chart(request: Request):
    """Creates and returns the Frequency histogram."""
    rfm_df = request.app.state.rfm_df
    if rfm_df is None:
        return {"error": "Data not loaded"}

    fig = px.histogram(rfm_df, x="Frequency", title="Frequency (Purchases) Distribution", nbins=40)
    return fig.to_dict()


@app.get("/api/charts/monetary")
async def get_monetary_chart(request: Request):
    """Creates and returns the Monetary Value histogram."""
    rfm_df = request.app.state.rfm_df
    if rfm_df is None:
        return {"error": "Data not loaded"}
        
    fig = px.histogram(rfm_df, x="MonetaryValue", title="Monetary Value Distribution", nbins=40)
    return fig.to_dict()