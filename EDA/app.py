"""
FastAPI Web Application for MLOPS Data Visualization Dashboard
================================================================

This application provides a web-based dashboard to visualize shopping data analysis results.
It uses Seaborn and Matplotlib for static chart generation.

Author: AI Assistant
Date: 2025-09-30
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pathlib import Path
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64

app = FastAPI(
    title="MLOPS Shopping Data Analytics Dashboard",
    description="Interactive web dashboard for shopping data analysis and visualization using Seaborn",
    version="2.0.0"
)

# Configuration
RESULTS_PATH = Path("results")
sns.set_theme(style="whitegrid") # Set a nice theme for all plots

# Data cache
data_cache = {}

def fig_to_base64(fig):
    """Convert a matplotlib figure to a base64 encoded image."""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    base64_img = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig) # Close the figure to free memory
    return f"data:image/png;base64,{base64_img}"

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
            
            .chart-container img {
                max-width: 100%;
                height: auto;
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
                color: #666;
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
                <div id="profitabilityChart" class="loading">Loading chart...</div>
            </div>
            
            <div class="chart-container">
                <h2>📅 Seasonal & Weekly Trends</h2>
                <div id="seasonalChart" class="loading">Loading chart...</div>
            </div>
            
            <div class="chart-container">
                <h2>💳 Payment Methods Analysis</h2>
                <div id="paymentChart" class="loading">Loading chart...</div>
            </div>
            
            <div class="chart-container">
                <h2>📈 Regional Performance</h2>
                <div id="regionalChart" class="loading">Loading chart...</div>
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
                    document.getElementById('summaryStats').innerHTML = 'Failed to load stats.';
                }
            }
            
            // Generic function to load any chart
            async function loadChart(endpoint, elementId) {
                const chartContainer = document.getElementById(elementId);
                chartContainer.innerHTML = '<div class="loading">Loading chart...</div>';
                try {
                    const response = await fetch(endpoint);
                    const data = await response.json();
                    chartContainer.innerHTML = `<img src="${data.image}" alt="Chart for ${elementId}">`;
                } catch (error) {
                    console.error(`Error loading chart for ${elementId}:`, error);
                    chartContainer.innerHTML = 'Failed to load chart.';
                }
            }

            // Refresh all data
            function refreshData() {
                loadSummaryStats();
                loadChart('/api/charts/profitability', 'profitabilityChart');
                loadChart('/api/charts/seasonal', 'seasonalChart');
                loadChart('/api/charts/payment', 'paymentChart');
                loadChart('/api/charts/regional', 'regionalChart');
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
    
    mall_prof = data_cache['mall_profitability'].sort_values('net_revenue', ascending=False)
    category_prof = data_cache['category_profitability'].sort_values('final_amount', ascending=False)
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    fig.suptitle('Profitability Dashboard', fontsize=18, weight='bold')

    # Mall revenue
    sns.barplot(data=mall_prof, x='net_revenue', y='shopping_mall', ax=axes[0, 0], palette='viridis')
    axes[0, 0].set_title('Net Revenue by Mall')
    axes[0, 0].set_xlabel('Net Revenue ($)')
    axes[0, 0].set_ylabel('Shopping Mall')

    # Discount rates
    sns.barplot(data=mall_prof, x='discount_rate', y='shopping_mall', ax=axes[0, 1], palette='plasma')
    axes[0, 1].set_title('Discount Rate by Mall')
    axes[0, 1].set_xlabel('Average Discount Rate (%)')
    axes[0, 1].set_ylabel('')

    # Category revenue
    sns.barplot(data=category_prof, x='final_amount', y='category', ax=axes[1, 0], palette='magma')
    axes[1, 0].set_title('Revenue by Category')
    axes[1, 0].set_xlabel('Total Revenue ($)')
    axes[1, 0].set_ylabel('Category')

    # Regional distribution
    region_revenue = mall_prof.groupby('Region')['net_revenue'].sum()
    axes[1, 1].pie(region_revenue, labels=region_revenue.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('pastel'))
    axes[1, 1].set_title('Regional Revenue Distribution')
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    return JSONResponse(content={"image": fig_to_base64(fig)})

@app.get("/api/charts/seasonal")
async def get_seasonal_chart():
    """Generate seasonal analysis charts"""
    if not data_cache:
        raise HTTPException(status_code=503, detail="Data not loaded")
    
    seasonal = data_cache['seasonal_trends']
    weekly = data_cache['weekly_patterns']
    monthly = data_cache['monthly_trends']
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    fig.suptitle('Seasonal Analysis Dashboard', fontsize=18, weight='bold')

    # Seasonal revenue
    season_order = ['Spring', 'Summer', 'Fall', 'Winter']
    sns.barplot(data=seasonal, x='total_revenue', y='season', order=season_order, ax=axes[0, 0], palette='coolwarm')
    axes[0, 0].set_title('Revenue by Season')
    axes[0, 0].set_xlabel('Total Revenue ($)')
    axes[0, 0].set_ylabel('Season')

    # Weekly patterns
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    sns.barplot(data=weekly, x='total_revenue', y='weekday_name', order=weekday_order, ax=axes[0, 1], palette='PRGn')
    axes[0, 1].set_title('Revenue by Day of Week')
    axes[0, 1].set_xlabel('Total Revenue ($)')
    axes[0, 1].set_ylabel('')

    # Monthly trends
    sns.lineplot(data=monthly, x='year_month', y='total_revenue', marker='o', ax=axes[1, 0], color='purple')
    axes[1, 0].set_title('Monthly Trends')
    axes[1, 0].set_xlabel('Month')
    axes[1, 0].set_ylabel('Total Revenue ($)')
    axes[1, 0].tick_params(axis='x', rotation=45)

    # Transaction volume
    sns.barplot(data=seasonal, x='total_transactions', y='season', order=season_order, ax=axes[1, 1], palette='cividis')
    axes[1, 1].set_title('Transaction Volume by Season')
    axes[1, 1].set_xlabel('Total Transactions')
    axes[1, 1].set_ylabel('')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    return JSONResponse(content={"image": fig_to_base64(fig)})

@app.get("/api/charts/payment")
async def get_payment_chart():
    """Generate payment method analysis charts"""
    if not data_cache:
        raise HTTPException(status_code=503, detail="Data not loaded")
    
    payment = data_cache['payment_analysis']
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    fig.suptitle('Payment Methods Analysis', fontsize=18, weight='bold')

    # Revenue distribution
    axes[0, 0].pie(payment['total_revenue'], labels=payment['payment_method'], autopct='%1.1f%%', startangle=90, colors=sns.color_palette('Set2'))
    axes[0, 0].set_title('Revenue by Payment Method')

    # Transaction count
    axes[0, 1].pie(payment['transaction_count'], labels=payment['payment_method'], autopct='%1.1f%%', startangle=90, colors=sns.color_palette('Set3'))
    axes[0, 1].set_title('Transaction Count by Payment Method')

    # Average transaction value
    sns.barplot(data=payment, x='avg_transaction_value', y='payment_method', ax=axes[1, 0], palette='rocket')
    axes[1, 0].set_title('Average Transaction Value')
    axes[1, 0].set_xlabel('Average Value ($)')
    axes[1, 0].set_ylabel('Payment Method')

    # Comparison
    payment_melted = payment.melt(id_vars='payment_method', 
                                  value_vars=['revenue_percentage', 'transaction_percentage'],
                                  var_name='percentage_type', value_name='percentage')
    sns.barplot(data=payment_melted, x='percentage', y='payment_method', hue='percentage_type', ax=axes[1, 1], palette='icefire')
    axes[1, 1].set_title('Revenue vs. Transaction Percentage')
    axes[1, 1].set_xlabel('Percentage (%)')
    axes[1, 1].set_ylabel('')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    return JSONResponse(content={"image": fig_to_base64(fig)})

@app.get("/api/charts/regional")
async def get_regional_chart():
    """Generate regional analysis charts"""
    if not data_cache:
        raise HTTPException(status_code=503, detail="Data not loaded")
    
    regional_daily = data_cache['regional_daily_sales']
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    sns.lineplot(data=regional_daily, x='invoice_date', y='total_revenue', hue='Region', ax=ax, palette='tab10')
    
    # Add overall trend
    overall = regional_daily.groupby('invoice_date')['total_revenue'].sum().reset_index()
    sns.lineplot(data=overall, x='invoice_date', y='total_revenue', ax=ax, color='black', linestyle='--', label='Overall')
    
    ax.set_title('Regional Daily Sales Trends', fontsize=16)
    ax.set_xlabel('Date')
    ax.set_ylabel('Revenue ($)')
    ax.legend(title='Region')
    
    plt.tight_layout()
    
    return JSONResponse(content={"image": fig_to_base64(fig)})

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