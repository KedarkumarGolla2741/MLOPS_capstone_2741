"""
Startup script for MLOPS Analytics Dashboard
=============================================

This script ensures the data pipeline has been run and starts the FastAPI web server.

Author: AI Assistant
Date: 2025-09-30
"""

import os
import sys
from pathlib import Path
from mlops_data_pipeline import MLOPSDataPipeline

def check_results_exist():
    """Check if analysis results exist"""
    results_path = Path("results")
    required_files = [
        'daily_sales.csv',
        'regional_daily_sales.csv',
        'mall_profitability.csv',
        'category_profitability.csv',
        'seasonal_trends.csv',
        'weekly_patterns.csv',
        'payment_analysis.csv',
        'monthly_trends.csv'
    ]
    
    if not results_path.exists():
        return False
    
    for file in required_files:
        if not (results_path / file).exists():
            return False
    
    return True

def run_pipeline():
    """Run the data pipeline"""
    print("=" * 60)
    print("Running MLOPS Data Pipeline...")
    print("=" * 60)
    
    try:
        pipeline = MLOPSDataPipeline()
        pipeline.run_complete_pipeline()
        print("\n✓ Pipeline completed successfully!")
        return True
    except Exception as e:
        print(f"\n✗ Pipeline failed: {str(e)}")
        return False

def start_dashboard():
    """Start the FastAPI dashboard"""
    print("\n" + "=" * 60)
    print("Starting MLOPS Analytics Dashboard...")
    print("=" * 60)
    print("\n🚀 Dashboard will be available at: http://localhost:8000")
    print("📚 API documentation at: http://localhost:8000/docs")
    print("\nPress CTRL+C to stop the server\n")
    
    import uvicorn
    from app import app
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

def main():
    """Main function"""
    print("\n" + "=" * 60)
    print("MLOPS ANALYTICS DASHBOARD STARTUP")
    print("=" * 60)
    
    # Check if results exist
    if not check_results_exist():
        print("\n⚠️  Analysis results not found.")
        print("Running data pipeline first...\n")
        
        if not run_pipeline():
            print("\n✗ Failed to run pipeline. Please check the error messages above.")
            sys.exit(1)
    else:
        print("\n✓ Analysis results found.")
        response = input("\nDo you want to regenerate the data? (y/n): ")
        if response.lower() == 'y':
            if not run_pipeline():
                print("\n✗ Failed to run pipeline. Please check the error messages above.")
                sys.exit(1)
    
    # Start dashboard
    try:
        start_dashboard()
    except KeyboardInterrupt:
        print("\n\n✓ Dashboard stopped. Goodbye!")
    except Exception as e:
        print(f"\n✗ Error starting dashboard: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()