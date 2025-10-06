# 🚀 Quick Start Guide - MLOPS Web Dashboard

## What's New? 🎉

You now have a **modern, interactive web dashboard** for your shopping data analytics!

### ✨ Features
- 📊 **Interactive Charts**: Zoom, pan, and explore data with Plotly
- 🎨 **Beautiful UI**: Modern purple gradient design with responsive layout
- 🔄 **Real-time Updates**: Refresh data without reloading
- 📱 **Mobile Friendly**: Works on desktop, tablet, and mobile
- 🌐 **REST API**: Access data programmatically
- 📚 **Auto-generated Docs**: Interactive API documentation

## 🏃 Getting Started (3 Steps)

### Step 1: Install Dependencies (First Time Only)
```bash
pip install -r requirements.txt
```

### Step 2: Start the Dashboard
**Option A - Easy (Recommended):**
```bash
python run_dashboard.py
```

**Option B - Windows Quick Start:**
- Double-click `start_dashboard.bat`

**Option C - Linux/Mac:**
```bash
chmod +x start_dashboard.sh
./start_dashboard.sh
```

### Step 3: Open Your Browser
Navigate to: **http://localhost:8000**

That's it! 🎉

## 📁 New Files Added

```
MLOPS/
├── app.py                      # FastAPI web application (main)
├── run_dashboard.py            # Startup script with pipeline check
├── start_dashboard.bat         # Windows batch launcher
├── start_dashboard.sh          # Linux/Mac bash launcher
├── DASHBOARD_GUIDE.md          # Detailed user guide
├── QUICKSTART.md              # This file
├── .gitignore                 # Git ignore patterns
└── requirements.txt           # Updated with FastAPI & Plotly
```

## 🎯 What You'll See

### Dashboard Sections

1. **📊 Summary Overview** (Top Cards)
   - Total Shopping Malls: 10
   - Regions: Multiple regions
   - Total Revenue: $XX.XXM
   - Transactions: 99,457+

2. **💰 Profitability Analysis**
   - Revenue by mall (horizontal bar chart)
   - Discount rates by mall (bar chart)
   - Revenue by category (horizontal bar chart)
   - Regional revenue distribution (pie chart)

3. **📅 Seasonal & Weekly Trends**
   - Revenue by season (bar chart)
   - Revenue by day of week (line chart)
   - Monthly trends over time (line chart)
   - Transaction volume by season (bar chart)

4. **💳 Payment Methods Analysis**
   - Revenue distribution (pie chart)
   - Transaction count (pie chart)
   - Average transaction value (bar chart)
   - Payment method comparison (grouped bars)

5. **📈 Regional Performance**
   - Daily sales trends by region (multi-line chart)
   - Overall trend (dashed line)

## 🔗 Available URLs

Once started, you can access:

- **Main Dashboard**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **API Docs (ReDoc)**: http://localhost:8000/redoc
- **Summary Stats**: http://localhost:8000/api/summary
- **Mall Data**: http://localhost:8000/api/data/mall_profitability
- **Category Data**: http://localhost:8000/api/data/category_profitability
- **Payment Data**: http://localhost:8000/api/data/payment_analysis

## 💡 Interactive Features

### On Every Chart:
- 🖱️ **Hover**: See detailed values
- 🔍 **Zoom**: Click and drag to zoom in
- 🔄 **Reset**: Double-click to reset view
- 👆 **Pan**: Drag to pan after zooming
- 📷 **Save**: Click camera icon to download PNG
- 👁️ **Toggle**: Click legend to show/hide series

## 🔄 Updating Data

### If You Add New Data:
```bash
# Option 1: Use the startup script (prompts you)
python run_dashboard.py

# Option 2: Run pipeline manually, then restart
python mlops_data_pipeline.py
python app.py
```

### Refresh in Browser:
Click the "🔄 Refresh Data" button at the bottom of the dashboard

## 🛠️ Troubleshooting

### Problem: "Data not loaded"
**Solution**: Run the pipeline first
```bash
python mlops_data_pipeline.py
```

### Problem: "Port already in use"
**Solution**: Kill the existing process or use different port
```bash
# Find and kill process on port 8000 (Windows)
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or use different port
uvicorn app:app --port 8001
```

### Problem: Charts not showing
**Solution**: 
1. Hard refresh: Press `Ctrl + F5`
2. Check browser console: Press `F12`
3. Ensure `results/` folder has all CSV files

## 📚 Need More Help?

- **Detailed Guide**: See `DASHBOARD_GUIDE.md`
- **API Documentation**: Visit http://localhost:8000/docs
- **Original README**: See `README.md`

## 🎨 Customization

### Change Port
```bash
uvicorn app:app --port 8080
```

### Enable Network Access
```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```
Then access from other devices: `http://YOUR_IP:8000`

### Development Mode (Auto-reload on changes)
```bash
uvicorn app:app --reload
```

## 📊 Using the API

### Example: Get Summary Stats
```bash
curl http://localhost:8000/api/summary
```

### Example: Get Mall Profitability
```bash
curl http://localhost:8000/api/data/mall_profitability > mall_data.json
```

### Example: Python Script
```python
import requests

# Get summary
response = requests.get('http://localhost:8000/api/summary')
data = response.json()
print(f"Total Revenue: ${data['total_revenue']:,.2f}")

# Get mall profitability
malls = requests.get('http://localhost:8000/api/data/mall_profitability')
print(malls.json())
```

## ✅ Next Steps

1. ✅ Install dependencies
2. ✅ Start the dashboard
3. ✅ Open http://localhost:8000
4. 📊 Explore your data interactively!
5. 🔍 Check out the API at http://localhost:8000/docs
6. 📖 Read DASHBOARD_GUIDE.md for advanced features

## 🌟 Pro Tips

- **Keyboard Shortcuts in Charts**: 
  - Double-click: Reset zoom
  - Shift + drag: Pan
  
- **Mobile Access**: Access from phone/tablet on same WiFi network

- **Share Charts**: Use camera icon to download charts as PNG

- **API Integration**: Use the REST API to integrate with other tools

- **Multiple Dashboards**: Run on different ports for different datasets

---

**Enjoy your new interactive dashboard! 🎉**

Questions? Check `DASHBOARD_GUIDE.md` or the API docs at `/docs`