# MLOPS Data Pipeline for Shopping Data Analysis

A comprehensive data pipeline for analyzing customer shopping data across multiple stores and regions. This project implements a complete MLOPS workflow for data preprocessing, analysis, and visualization.

## 🚀 Features

### Data Processing
- **Data Integration**: Joins customer shopping data with regional details
- **Data Validation**: Comprehensive data quality checks and validation
- **Data Preprocessing**: Handles date conversions, discount calculations, and feature engineering

### Analytics Capabilities
1. **Daily Sales Processing**: Analyzes sales data across stores and regions on a daily basis
2. **Profitability Analysis**: Calculates profitability metrics after applying discounts
3. **Seasonal Trends**: Identifies seasonal sales patterns and trends
4. **Payment Methods Analysis**: Comprehensive analysis of payment method preferences and patterns

### Visualization
- **Web Dashboard**: FastAPI-based interactive web application
- **Real-time Charts**: Plotly-powered interactive visualizations
- **Static Reports**: Matplotlib/Seaborn generated PNG dashboards
- Heatmaps for pattern identification
- Time series analysis with moving averages
- Comparative charts for performance metrics

## 📁 Project Structure

```
D:\GenAI\MLOPS\
├── customer_shopping_data.csv      # Main shopping data (99,457 records)
├── Region_detail_table.csv         # Regional mapping data
├── mlops_data_pipeline.py          # Main pipeline script
├── visualization_dashboard.py      # Static visualization script
├── app.py                          # FastAPI web application
├── run_dashboard.py                # Dashboard startup script
├── requirements.txt                # Python dependencies
├── README.md                       # This file
└── results/                        # Generated analysis results
    ├── combined_data.csv
    ├── daily_sales.csv
    ├── regional_daily_sales.csv
    ├── mall_profitability.csv
    ├── category_profitability.csv
    ├── seasonal_trends.csv
    ├── weekly_patterns.csv
    ├── payment_analysis.csv
    ├── summary_report.txt
    └── *.png                       # Generated visualizations
```

## 🛠️ Installation

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify Data Files**:
   Ensure the following files are in the project directory:
   - `customer_shopping_data.csv`
   - `Region_detail_table.csv`

## 🏃‍♂️ Usage

### Quick Start - Web Dashboard (Recommended)
Run the interactive web dashboard (automatically runs pipeline if needed):
```bash
python run_dashboard.py
```
Then open your browser to: **http://localhost:8000**

### Run Complete Pipeline Only
```bash
python mlops_data_pipeline.py
```

### Generate Static Visualizations Only
```bash
python visualization_dashboard.py
```

### Start Web Dashboard Only (requires pre-run pipeline)
```bash
python app.py
```
Or using uvicorn directly:
```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

## 🌐 Web Dashboard Features

The FastAPI web dashboard provides an interactive, modern interface for exploring your data:

### Available Dashboards
1. **Summary Overview**: Key metrics at a glance (total revenue, malls, regions, transactions)
2. **Profitability Analysis**: 
   - Net revenue by shopping mall
   - Discount rates comparison
   - Revenue by product category
   - Regional revenue distribution
3. **Seasonal & Weekly Trends**:
   - Revenue by season
   - Day-of-week patterns
   - Monthly trends over time
   - Transaction volume analysis
4. **Payment Methods Analysis**:
   - Revenue distribution by payment method
   - Transaction count breakdown
   - Average transaction values
   - Comparative metrics
5. **Regional Performance**:
   - Daily sales trends by region
   - Regional comparisons
   - Overall trend analysis

### Interactive Features
- **Zoom & Pan**: All charts support interactive zoom and pan
- **Hover Details**: Hover over data points for detailed information
- **Legend Toggle**: Click legend items to show/hide data series
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Real-time Updates**: Refresh data without reloading the page

### API Endpoints
Access data programmatically through REST API:
- `GET /`: Main dashboard (HTML)
- `GET /api/summary`: Summary statistics (JSON)
- `GET /api/charts/profitability`: Profitability charts data
- `GET /api/charts/seasonal`: Seasonal analysis charts data
- `GET /api/charts/payment`: Payment methods charts data
- `GET /api/charts/regional`: Regional performance charts data
- `GET /api/data/mall_profitability`: Raw mall profitability data
- `GET /api/data/category_profitability`: Raw category profitability data
- `GET /api/data/payment_analysis`: Raw payment analysis data
- `GET /docs`: Interactive API documentation (Swagger UI)

## 📊 Data Overview

### Dataset Statistics
- **Total Records**: 99,457 transactions
- **Date Range**: January 1, 2021 to March 8, 2023
- **Shopping Malls**: 10 unique locations
- **Regions**: 7 distinct regions
- **Categories**: 8 product categories
- **Payment Methods**: 3 types (Cash, Credit Card, Debit Card)

### Key Insights
- **Top Performing Mall**: Mall of Istanbul
- **Top Region by Revenue**: Levent
- **Most Popular Category**: Clothing
- **Preferred Payment Method**: Cash
- **Best Season**: Winter
- **Peak Day**: Monday

## 🔍 Analysis Components

### 1. Daily Sales Processing
- Aggregates sales data by date, store, and region
- Calculates daily metrics:
  - Total revenue
  - Transaction count
  - Average transaction value
  - Unique customers
  - Revenue per customer

### 2. Profitability Analysis
- **Mall-level Profitability**:
  - Gross revenue vs net revenue
  - Discount rates and impact
  - Average transaction values
  - Revenue per unit sold

- **Category-level Profitability**:
  - Profit margins by category
  - Discount impact analysis
  - Performance comparisons

### 3. Seasonal Trends Analysis
- **Monthly Trends**: Revenue patterns over time
- **Seasonal Analysis**: Performance by season
- **Weekly Patterns**: Day-of-week preferences
- **Quarterly Trends**: Quarterly performance metrics

### 4. Payment Methods Analysis
- **Usage Patterns**: Distribution of payment methods
- **Regional Preferences**: Payment method preferences by region
- **Category Preferences**: Payment method usage by product category
- **Trend Analysis**: Payment method trends over time

## 📈 Output Files

### Analysis Results (CSV)
- `combined_data.csv`: Complete joined dataset with calculated fields
- `daily_sales.csv`: Daily sales metrics by store
- `regional_daily_sales.csv`: Daily sales metrics by region
- `mall_profitability.csv`: Profitability analysis by shopping mall
- `category_profitability.csv`: Profitability analysis by product category
- `seasonal_trends.csv`: Seasonal analysis results
- `weekly_patterns.csv`: Weekly pattern analysis
- `payment_analysis.csv`: Payment method analysis results

### Visualizations (PNG)
- `profitability_dashboard.png`: Comprehensive profitability charts
- `seasonal_analysis_dashboard.png`: Seasonal trends visualization
- `payment_analysis_dashboard.png`: Payment methods analysis
- `daily_sales_trends.png`: Time series analysis
- `heatmap_analysis.png`: Pattern identification heatmaps

### Reports
- `summary_report.txt`: Executive summary with key findings
- `pipeline.log`: Detailed execution log

## 🔧 Technical Details

### Pipeline Architecture
```
Data Loading → Validation → Joining → Preprocessing → Analysis → Visualization → Export
```

### Key Classes
- **MLOPSDataPipeline**: Main pipeline orchestrator
- **MLOPSVisualizationDashboard**: Visualization generator

### Error Handling
- Comprehensive logging system
- Data validation checks
- Graceful error handling and reporting

### Performance
- Efficient pandas operations
- Memory-optimized processing
- Parallel processing where applicable

## 📋 Requirements

### Python Version
- Python 3.8+

### Dependencies
- pandas >= 1.5.0
- numpy >= 1.24.0
- matplotlib >= 3.6.0
- seaborn >= 0.12.0
- pathlib2 >= 2.3.0
- fastapi >= 0.104.0
- uvicorn[standard] >= 0.24.0
- plotly >= 5.17.0
- python-multipart >= 0.0.6

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 📞 Support

For questions or issues, please check the pipeline logs in `results/pipeline.log` for detailed error information.

---

**Note**: This pipeline is designed for MLOPS best practices and can be easily integrated into automated workflows and CI/CD pipelines.