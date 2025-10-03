"""
FastAPI Web Application for MLOPS Data Visualization Dashboard
================================================================

This application provides a web-based dashboard to visualize shopping data analysis results.

Author: AI Assistant
Date: 2025-09-30
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json

app = FastAPI(
    title="MLOPS Shopping Data Analytics Dashboard",
    description="Interactive web dashboard for shopping data analysis and visualization",
    version="1.0.0"
)

# Configuration
RESULTS_PATH = Path("results")

# Data cache
data_cache = {}

def load_data():
    """Load all analysis results into memory"""
    global data_cache
    
    try:
        data_cache = {
            'daily_sales': pd.read_csv(RESULTS_PATH / "daily_sales.csv"),
            'regional_daily_sales': pd.read_csv(RESULTS_PATH / "regional_daily_sales.csv"),
            'mall_profitability': pd.read_csv(RESULTS_PATH / "mall_profitability.csv"),
            'category_profitability': pd.read_csv(RESULTS_PATH / "category_profitability.csv"),
            'seasonal_trends': pd.read_csv(RESULTS_PATH / "seasonal_trends.csv"),
            'weekly_patterns': pd.read_csv(RESULTS_PATH / "weekly_patterns.csv"),
            'payment_analysis': pd.read_csv(RESULTS_PATH / "payment_analysis.csv"),
            'monthly_trends': pd.read_csv(RESULTS_PATH / "monthly_trends.csv"),
            'payment_by_region': pd.read_csv(RESULTS_PATH / "payment_by_region.csv"),
            'payment_by_category': pd.read_csv(RESULTS_PATH / "payment_by_category.csv"),
        }
        
        # Convert date columns
        data_cache['daily_sales']['invoice_date'] = pd.to_datetime(data_cache['daily_sales']['invoice_date'])
        data_cache['regional_daily_sales']['invoice_date'] = pd.to_datetime(data_cache['regional_daily_sales']['invoice_date'])
        
        return True
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        return False

@app.on_event("startup")
async def startup_event():
    """Load data on application startup"""
    success = load_data()
    if success:
        print("✓ Data loaded successfully!")
    else:
        print("✗ Failed to load data. Make sure to run the pipeline first.")

@app.get("/", response_class=HTMLResponse)
async def home():
    """Main dashboard page"""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>MLOPS Shopping Analytics Dashboard</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            
            .container {
                max-width: 1400px;
                margin: 0 auto;
            }
            
            .header {
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                margin-bottom: 30px;
                text-align: center;
            }
            
            .header h1 {
                color: #667eea;
                font-size: 2.5em;
                margin-bottom: 10px;
            }
            
            .header p {
                color: #666;
                font-size: 1.1em;
            }
            
            .dashboard-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            
            .card {
                background: white;
                border-radius: 15px;
                padding: 25px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }
            
            .card:hover {
                transform: translateY(-5px);
                box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            }
            
            .card h2 {
                color: #667eea;
                margin-bottom: 15px;
                font-size: 1.5em;
                border-bottom: 2px solid #667eea;
                padding-bottom: 10px;
            }
            
            .chart-container {
                background: white;
                border-radius: 15px;
                padding: 25px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                margin-bottom: 30px;
            }
            
            .nav-buttons {
                display: flex;
                gap: 15px;
                flex-wrap: wrap;
                justify-content: center;
                margin-top: 20px;
            }
            
            .nav-button {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 12px 24px;
                border: none;
                border-radius: 25px;
                cursor: pointer;
                font-size: 1em;
                transition: all 0.3s ease;
                text-decoration: none;
                display: inline-block;
            }
            
            .nav-button:hover {
                transform: scale(1.05);
                box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
            }
            
            .loading {
                text-align: center;
                padding: 40px;
                color: white;
                font-size: 1.2em;
            }
            
            #summaryStats {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
            }
            
            .stat-card {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
            }
            
            .stat-value {
                font-size: 2em;
                font-weight: bold;
                margin-bottom: 5px;
            }
            
            .stat-label {
                font-size: 0.9em;
                opacity: 0.9;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🛍️ MLOPS Shopping Analytics Dashboard</h1>
                <p>Interactive Data Visualization & Business Intelligence</p>
            </div>
            
            <div class="dashboard-grid">
                <div class="card">
                    <h2>📊 Overview</h2>
                    <div id="summaryStats" class="loading">Loading statistics...</div>
                </div>
            </div>
            
            <div class="chart-container">
                <h2>💰 Profitability Analysis</h2>
                <div id="profitabilityChart"></div>
            </div>
            
            <div class="chart-container">
                <h2>📅 Seasonal & Weekly Trends</h2>
                <div id="seasonalChart"></div>
            </div>
            
            <div class="chart-container">
                <h2>💳 Payment Methods Analysis</h2>
                <div id="paymentChart"></div>
            </div>
            
            <div class="chart-container">
                <h2>📈 Regional Performance</h2>
                <div id="regionalChart"></div>
            </div>
            
            <div class="nav-buttons">
                <a href="/docs" class="nav-button">📚 API Documentation</a>
                <button onclick="refreshData()" class="nav-button">🔄 Refresh Data</button>
            </div>
        </div>
        
        <script>
            // Load summary statistics
            async function loadSummaryStats() {
                try {
                    const response = await fetch('/api/summary');
                    const data = await response.json();
                    
                    const statsHtml = `
                        <div class="stat-card">
                            <div class="stat-value">${data.total_malls}</div>
                            <div class="stat-label">Shopping Malls</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">${data.total_regions}</div>
                            <div class="stat-label">Regions</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">$${(data.total_revenue / 1000000).toFixed(2)}M</div>
                            <div class="stat-label">Total Revenue</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">${data.total_transactions.toLocaleString()}</div>
                            <div class="stat-label">Transactions</div>
                        </div>
                    `;
                    
                    document.getElementById('summaryStats').innerHTML = statsHtml;
                } catch (error) {
                    console.error('Error loading summary:', error);
                }
            }
            
            // Load profitability chart
            async function loadProfitabilityChart() {
                try {
                    const response = await fetch('/api/charts/profitability');
                    const chart = await response.json();
                    Plotly.newPlot('profitabilityChart', chart.data, chart.layout, {responsive: true});
                } catch (error) {
                    console.error('Error loading profitability chart:', error);
                }
            }
            
            // Load seasonal chart
            async function loadSeasonalChart() {
                try {
                    const response = await fetch('/api/charts/seasonal');
                    const chart = await response.json();
                    Plotly.newPlot('seasonalChart', chart.data, chart.layout, {responsive: true});
                } catch (error) {
                    console.error('Error loading seasonal chart:', error);
                }
            }
            
            // Load payment chart
            async function loadPaymentChart() {
                try {
                    const response = await fetch('/api/charts/payment');
                    const chart = await response.json();
                    Plotly.newPlot('paymentChart', chart.data, chart.layout, {responsive: true});
                } catch (error) {
                    console.error('Error loading payment chart:', error);
                }
            }
            
            // Load regional chart
            async function loadRegionalChart() {
                try {
                    const response = await fetch('/api/charts/regional');
                    const chart = await response.json();
                    Plotly.newPlot('regionalChart', chart.data, chart.layout, {responsive: true});
                } catch (error) {
                    console.error('Error loading regional chart:', error);
                }
            }
            
            // Refresh all data
            function refreshData() {
                loadSummaryStats();
                loadProfitabilityChart();
                loadSeasonalChart();
                loadPaymentChart();
                loadRegionalChart();
            }
            
            // Initial load
            window.onload = refreshData;
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/api/summary")
async def get_summary():
    """Get summary statistics"""
    if not data_cache:
        raise HTTPException(status_code=503, detail="Data not loaded")
    
    mall_prof = data_cache['mall_profitability']
    
    return {
        "total_malls": len(mall_prof),
        "total_regions": mall_prof['Region'].nunique(),
        "total_revenue": float(mall_prof['net_revenue'].sum()),
        "total_transactions": int(mall_prof['total_transactions'].sum()),
        "avg_discount_rate": float(mall_prof['discount_rate'].mean())
    }

@app.get("/api/charts/profitability")
async def get_profitability_chart():
    """Generate profitability charts"""
    if not data_cache:
        raise HTTPException(status_code=503, detail="Data not loaded")
    
    mall_prof = data_cache['mall_profitability'].sort_values('net_revenue', ascending=True)
    category_prof = data_cache['category_profitability'].sort_values('final_amount', ascending=True)
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Net Revenue by Mall', 'Discount Rate by Mall',
                       'Revenue by Category', 'Regional Revenue Distribution'),
        specs=[[{"type": "bar"}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "pie"}]]
    )
    
    # Mall revenue
    fig.add_trace(
        go.Bar(x=mall_prof['net_revenue']/1000000, y=mall_prof['shopping_mall'],
               orientation='h', name='Revenue', marker_color='#667eea'),
        row=1, col=1
    )
    
    # Discount rates
    fig.add_trace(
        go.Bar(x=mall_prof['discount_rate'], y=mall_prof['shopping_mall'],
               orientation='h',name='Discount Rate', marker_color='#f093fb'),
        row=1, col=2
    )
    
    # Category revenue
    fig.add_trace(
        go.Bar(x=category_prof['final_amount']/1000000, y=category_prof['category'],
               orientation='h', name='Category Revenue', marker_color='#4facfe'),
        row=2, col=1
    )
    
    # Regional distribution
    region_revenue = mall_prof.groupby('Region')['net_revenue'].sum()
    fig.add_trace(
        go.Pie(labels=region_revenue.index, values=region_revenue.values,
               marker_colors=['#667eea', '#764ba2', '#f093fb', '#4facfe']),
        row=2, col=2
    )
    
    fig.update_xaxes(title_text="Revenue (Millions)", row=1, col=1)
    fig.update_xaxes(title_text="Discount Rate (%)", row=1, col=2)
    fig.update_xaxes(title_text="Revenue (Millions)", row=2, col=1)
    
    fig.update_layout(height=800, showlegend=False, title_text="Profitability Dashboard")
    
    return JSONResponse(content=json.loads(fig.to_json()))

@app.get("/api/charts/seasonal")
async def get_seasonal_chart():
    """Generate seasonal analysis charts"""
    if not data_cache:
        raise HTTPException(status_code=503, detail="Data not loaded")
    
    seasonal = data_cache['seasonal_trends']
    weekly = data_cache['weekly_patterns']
    monthly = data_cache['monthly_trends']
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Revenue by Season', 'Revenue by Day of Week',
                       'Monthly Trends', 'Transaction Volume by Season'),
        specs=[[{"type": "bar"}, {"type": "bar"}],
               [{"type": "scatter"}, {"type": "bar"}]]
    )
    
    # Seasonal revenue
    season_order = ['Spring', 'Summer', 'Fall', 'Winter']
    seasonal_ordered = seasonal.set_index('season').reindex(season_order).reset_index()
    
    fig.add_trace(
        go.Bar(x=seasonal_ordered['total_revenue']/1000000, y=seasonal_ordered['season'], 
               orientation='h', marker_color='#667eea', name='Seasonal Revenue'),
        row=1, col=1
    )
    
    # Weekly patterns
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekly_ordered = weekly.set_index('weekday_name').reindex(weekday_order).reset_index()
    
    fig.add_trace(
        go.Bar(x=weekly_ordered['total_revenue']/1000000, y=weekly_ordered['weekday_name'], 
               orientation='h', marker_color='#764ba2', name='Weekly Revenue'),
        row=1, col=2
    )
    
    # Monthly trends
    fig.add_trace(
        go.Scatter(x=monthly['year_month'], y=monthly['total_revenue']/1000000,
                  mode='lines+markers', marker_color='#f093fb', 
                  line=dict(width=2), name='Monthly Trends'),
        row=2, col=1
    )
    
    # Transaction volume
    fig.add_trace(
        go.Bar(x=seasonal_ordered['total_transactions']/1000, y=seasonal_ordered['season'], 
               orientation='h', marker_color='#4facfe', name='Transactions'),
        row=2, col=2
    )
    
    fig.update_xaxes(title_text="Revenue (Millions)", row=1, col=1)
    fig.update_xaxes(title_text="Revenue (Millions)", row=1, col=2)
    fig.update_xaxes(title_text="Year-Month", row=2, col=1)
    fig.update_yaxes(title_text="Revenue (Millions)", row=2, col=1)
    fig.update_xaxes(title_text="Transactions (Thousands)", row=2, col=2)
    
    fig.update_layout(height=800, showlegend=False, title_text="Seasonal Analysis Dashboard")
    
    return JSONResponse(content=json.loads(fig.to_json()))

@app.get("/api/charts/payment")
async def get_payment_chart():
    """Generate payment method analysis charts"""
    if not data_cache:
        raise HTTPException(status_code=503, detail="Data not loaded")
    
    payment = data_cache['payment_analysis']
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Revenue by Payment Method', 'Transaction Count by Payment Method',
                       'Average Transaction Value', 'Payment Method Comparison'),
        specs=[[{"type": "pie"}, {"type": "pie"}],
               [{"type": "bar"}, {"type": "bar"}]]
    )
    
    colors = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe']
    
    # Revenue distribution
    fig.add_trace(
        go.Pie(labels=payment['payment_method'], values=payment['total_revenue'],
               marker_colors=colors),
        row=1, col=1
    )
    
    # Transaction count
    fig.add_trace(
        go.Pie(labels=payment['payment_method'], values=payment['transaction_count'],
               marker_colors=colors),
        row=1, col=2
    )
    
    # Average transaction value
    fig.add_trace(
        go.Bar(x=payment['avg_transaction_value'], y=payment['payment_method'], 
               orientation='h', marker_color=colors, name='Avg Value'),
        row=2, col=1
    )
    
    # Comparison - Revenue percentage
    fig.add_trace(
        go.Bar(x=payment['revenue_percentage'], y=payment['payment_method'], 
               orientation='h', name='Revenue %', marker_color='#667eea'),
        row=2, col=2
    )
    # Comparison - Transaction percentage
    fig.add_trace(
        go.Bar(x=payment['transaction_percentage'], y=payment['payment_method'], 
               orientation='h', name='Transactions %', marker_color='#764ba2'),
        row=2, col=2
    )
    
    fig.update_xaxes(title_text="Average Value ($)", row=2, col=1)
    fig.update_xaxes(title_text="Percentage (%)", row=2, col=2)
    
    fig.update_layout(height=800, title_text="Payment Methods Analysis")
    
    return JSONResponse(content=json.loads(fig.to_json()))

@app.get("/api/charts/regional")
async def get_regional_chart():
    """Generate regional analysis charts"""
    if not data_cache:
        raise HTTPException(status_code=503, detail="Data not loaded")
    
    regional_daily = data_cache['regional_daily_sales']
    
    # Create line chart for regional trends
    fig = go.Figure()
    
    for region in regional_daily['Region'].unique():
        region_data = regional_daily[regional_daily['Region'] == region]
        fig.add_trace(go.Scatter(
            x=region_data['invoice_date'],
            y=region_data['total_revenue']/1000,
            mode='lines',
            name=region,
            line=dict(width=2)
        ))
    
    # Add overall trend
    overall = regional_daily.groupby('invoice_date')['total_revenue'].sum()/1000
    fig.add_trace(go.Scatter(
        x=overall.index,
        y=overall.values,
        mode='lines',
        name='Overall',
        line=dict(width=3, dash='dash', color='black')
    ))
    
    fig.update_layout(
        title='Regional Daily Sales Trends',
        xaxis_title='Date',
        yaxis_title='Revenue (Thousands)',
        height=600,
        hovermode='x unified'
    )
    
    return JSONResponse(content=json.loads(fig.to_json()))

@app.get("/api/data/mall_profitability")
async def get_mall_profitability():
    """Get mall profitability data"""
    if not data_cache:
        raise HTTPException(status_code=503, detail="Data not loaded")
    
    return JSONResponse(content=data_cache['mall_profitability'].to_dict(orient='records'))

@app.get("/api/data/category_profitability")
async def get_category_profitability():
    """Get category profitability data"""
    if not data_cache:
        raise HTTPException(status_code=503, detail="Data not loaded")
    
    return JSONResponse(content=data_cache['category_profitability'].to_dict(orient='records'))

@app.get("/api/data/payment_analysis")
async def get_payment_analysis():
    """Get payment analysis data"""
    if not data_cache:
        raise HTTPException(status_code=503, detail="Data not loaded")
    
    return JSONResponse(content=data_cache['payment_analysis'].to_dict(orient='records'))

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting MLOPS Analytics Dashboard...")
    print("📊 Dashboard will be available at: http://localhost:8000")
    print("📚 API documentation at: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)