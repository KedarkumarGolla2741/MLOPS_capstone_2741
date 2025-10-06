# 🌐 Web Dashboard User Guide

## Quick Start

### Windows
1. Double-click `start_dashboard.bat`
2. Open browser to: http://localhost:8000

### Linux/Mac
```bash
chmod +x start_dashboard.sh  # First time only
./start_dashboard.sh
```

### Manual Start
```bash
pip install -r requirements.txt
python run_dashboard.py
```

## Dashboard Overview

### Main Page
When you open http://localhost:8000, you'll see:

1. **Header Section**
   - Dashboard title and description
   - Clean, modern purple gradient design

2. **Summary Statistics Cards**
   - Total Shopping Malls
   - Number of Regions
   - Total Revenue (in millions)
   - Total Transactions

3. **Interactive Charts**
   - Profitability Analysis
   - Seasonal & Weekly Trends
   - Payment Methods Analysis
   - Regional Performance

## Using Interactive Charts

### Navigation
- **Zoom In**: Click and drag to select an area
- **Zoom Out**: Double-click on the chart
- **Pan**: Click and drag after zooming
- **Reset**: Double-click to reset view

### Data Exploration
- **Hover**: Move mouse over data points to see details
- **Legend**: Click legend items to show/hide data series
- **Download**: Click camera icon to save chart as PNG

### Chart Types

#### Profitability Dashboard
- **Bar Charts**: Compare revenue across malls and categories
- **Pie Chart**: See regional revenue distribution
- **Discount Analysis**: Understand discount rates by location

#### Seasonal Analysis
- **Seasonal Trends**: Bar chart showing revenue by season
- **Weekly Patterns**: Line chart showing day-of-week performance
- **Monthly Trends**: Time series showing revenue over time
- **Transaction Volume**: Bar chart of transactions by season

#### Payment Methods
- **Revenue Distribution**: Pie chart by payment method
- **Transaction Count**: Pie chart by transaction volume
- **Average Values**: Bar chart showing average transaction size
- **Comparison**: Side-by-side comparison of payment methods

#### Regional Performance
- **Time Series**: Line chart showing daily sales by region
- **Overall Trend**: Dashed line showing combined performance
- **Regional Comparison**: Compare multiple regions simultaneously

## API Endpoints

### Data Endpoints
Access raw data in JSON format:

```bash
# Summary statistics
curl http://localhost:8000/api/summary

# Mall profitability data
curl http://localhost:8000/api/data/mall_profitability

# Category profitability data
curl http://localhost:8000/api/data/category_profitability

# Payment analysis data
curl http://localhost:8000/api/data/payment_analysis
```

### Chart Endpoints
Get chart configurations:

```bash
# Profitability charts
curl http://localhost:8000/api/charts/profitability

# Seasonal analysis charts
curl http://localhost:8000/api/charts/seasonal

# Payment methods charts
curl http://localhost:8000/api/charts/payment

# Regional performance charts
curl http://localhost:8000/api/charts/regional
```

## API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Using Swagger UI
1. Navigate to http://localhost:8000/docs
2. Click on any endpoint to expand it
3. Click "Try it out" button
4. Click "Execute" to test the endpoint
5. View the response below

## Refreshing Data

### Method 1: Web Interface
Click the "🔄 Refresh Data" button at the bottom of the page

### Method 2: Regenerate Pipeline
```bash
python mlops_data_pipeline.py
```
Then refresh your browser

### Method 3: Restart Dashboard
1. Stop the server (CTRL+C)
2. Run `python run_dashboard.py` again
3. Select 'y' when prompted to regenerate data

## Troubleshooting

### Dashboard won't start
**Error**: `Data not loaded`
- **Solution**: Run the pipeline first: `python mlops_data_pipeline.py`

**Error**: `Port 8000 is already in use`
- **Solution**: Kill the existing process or use a different port:
  ```bash
  uvicorn app:app --port 8001
  ```

### Charts not loading
**Issue**: Charts show "Loading..." indefinitely
- **Solution 1**: Check browser console (F12) for errors
- **Solution 2**: Ensure results folder contains all CSV files
- **Solution 3**: Hard refresh the page (CTRL+F5)

### Data is outdated
**Issue**: Dashboard shows old data
- **Solution**: Regenerate the pipeline and restart the dashboard

### Performance issues
**Issue**: Dashboard is slow
- **Solution 1**: Close other browser tabs
- **Solution 2**: Use a modern browser (Chrome, Firefox, Edge)
- **Solution 3**: Reduce data size or increase server resources

## Browser Compatibility

### Recommended Browsers
- ✅ Google Chrome (latest)
- ✅ Mozilla Firefox (latest)
- ✅ Microsoft Edge (latest)
- ✅ Safari (latest)

### Not Recommended
- ❌ Internet Explorer (any version)
- ❌ Very old browser versions

## Mobile Access

The dashboard is responsive and works on mobile devices:

1. Ensure your mobile device is on the same network
2. Find your computer's IP address:
   - Windows: `ipconfig`
   - Linux/Mac: `ifconfig` or `ip addr`
3. Access: `http://YOUR_IP:8000`

Example: http://192.168.1.100:8000

## Security Considerations

### Local Development
- Dashboard runs on localhost by default (127.0.0.1)
- Only accessible from your computer

### Network Access
To allow network access:
```python
# In app.py or when running uvicorn
uvicorn.run(app, host="0.0.0.0", port=8000)
```

⚠️ **Warning**: This makes the dashboard accessible to anyone on your network

### Production Deployment
For production use:
1. Add authentication middleware
2. Use HTTPS (TLS/SSL certificates)
3. Configure CORS properly
4. Use environment variables for configuration
5. Deploy behind a reverse proxy (nginx, Apache)

## Advanced Usage

### Custom Port
```bash
python -c "import uvicorn; from app import app; uvicorn.run(app, port=8080)"
```

### Development Mode (Auto-reload)
```bash
uvicorn app:app --reload --port 8000
```

### Multiple Workers (Production)
```bash
uvicorn app:app --workers 4 --host 0.0.0.0 --port 8000
```

### Background Process
```bash
# Linux/Mac
nohup python app.py &

# Windows (PowerShell)
Start-Process python -ArgumentList "app.py" -WindowStyle Hidden
```

## Customization

### Changing Colors
Edit the gradient colors in `app.py`:
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Adding New Charts
1. Create a new endpoint in `app.py`:
```python
@app.get("/api/charts/my_chart")
async def get_my_chart():
    # Create Plotly figure
    fig = go.Figure(...)
    return JSONResponse(content=json.loads(fig.to_json()))
```

2. Add to HTML template:
```javascript
async function loadMyChart() {
    const response = await fetch('/api/charts/my_chart');
    const chart = await response.json();
    Plotly.newPlot('myChartDiv', chart.data, chart.layout);
}
```

### Modifying Layout
The HTML template is embedded in `app.py`. Look for the `home()` function and modify the HTML/CSS as needed.

## Support

For issues or questions:
1. Check `pipeline.log` for errors
2. Review this guide
3. Check the browser console (F12)
4. Verify all CSV files exist in `results/` folder

---

**Happy Analyzing! 📊**