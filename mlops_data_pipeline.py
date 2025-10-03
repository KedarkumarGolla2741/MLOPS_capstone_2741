"""
MLOPS Data Pipeline for Shopping Data Analysis
==============================================

This pipeline processes customer shopping data and performs comprehensive analysis including:
1. Daily sales data processing across stores and regions
2. Profitability calculations after discounts
3. Seasonal sales trends identification
4. Payment methods analysis

Author: AI Assistant
Date: 2025-09-25
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
import logging
import os
from pathlib import Path

warnings.filterwarnings('ignore')

class MLOPSDataPipeline:
    """
    A comprehensive data pipeline for MLOPS shopping data analysis
    """
    
    def __init__(self, data_path="D:/GenAI/MLOPS"):
        """
        Initialize the pipeline with data path
        
        Args:
            data_path (str): Path to the directory containing CSV files
        """
        self.data_path = Path(data_path)
        self.customer_file = self.data_path / "customer_shopping_data.csv"
        self.region_file = self.data_path / "Region_detail_table.csv"
        self.df_combined = None
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.data_path / 'pipeline.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def load_and_validate_data(self):
        """
        Load and validate the input data files
        """
        self.logger.info("Loading data files...")
        
        # Check if files exist
        if not self.customer_file.exists():
            raise FileNotFoundError(f"Customer data file not found: {self.customer_file}")
        if not self.region_file.exists():
            raise FileNotFoundError(f"Region data file not found: {self.region_file}")
        
        # Load datasets
        self.df_customer = pd.read_csv(self.customer_file)
        self.df_region = pd.read_csv(self.region_file)
        
        self.logger.info(f"Loaded customer data: {self.df_customer.shape}")
        self.logger.info(f"Loaded region data: {self.df_region.shape}")
        
        # Data validation
        self._validate_data()
        
    def _validate_data(self):
        """
        Perform data validation checks
        """
        self.logger.info("Validating data...")
        
        # Check for required columns
        required_customer_cols = ['invoice_no', 'customer_id', 'gender', 'age', 'category', 
                                'quantity', 'price', 'payment_method', 'invoice_date', 
                                'shopping_mall', 'Discount']
        required_region_cols = ['shopping_mall', 'Region']
        
        missing_customer_cols = set(required_customer_cols) - set(self.df_customer.columns)
        missing_region_cols = set(required_region_cols) - set(self.df_region.columns)
        
        if missing_customer_cols:
            raise ValueError(f"Missing columns in customer data: {missing_customer_cols}")
        if missing_region_cols:
            raise ValueError(f"Missing columns in region data: {missing_region_cols}")
        
        # Check for duplicates
        customer_duplicates = self.df_customer.duplicated().sum()
        if customer_duplicates > 0:
            self.logger.warning(f"Found {customer_duplicates} duplicate rows in customer data")
        
        # Check data types and ranges
        if self.df_customer['age'].min() < 0 or self.df_customer['age'].max() > 120:
            self.logger.warning("Age values seem unrealistic")
        
        if self.df_customer['price'].min() < 0:
            self.logger.warning("Negative price values found")
        
        self.logger.info("Data validation completed")
        
    def join_datasets(self):
        """
        Join customer shopping data with region details based on shopping_mall column
        """
        self.logger.info("Joining datasets on shopping_mall column...")
        
        # Perform inner join to ensure we only get records with matching regions
        self.df_combined = pd.merge(
            self.df_customer, 
            self.df_region, 
            on='shopping_mall', 
            how='inner'
        )
        
        self.logger.info(f"Combined dataset shape: {self.df_combined.shape}")
        
        # Check if any data was lost in join
        lost_records = len(self.df_customer) - len(self.df_combined)
        if lost_records > 0:
            self.logger.warning(f"Lost {lost_records} records during join")
        
        return self.df_combined
    
    def preprocess_data(self):
        """
        Preprocess the combined dataset for analysis
        """
        self.logger.info("Preprocessing data...")
        
        # Convert date column to datetime
        self.df_combined['invoice_date'] = pd.to_datetime(
            self.df_combined['invoice_date'], 
            format='%d-%m-%Y'
        )
        
        # Convert discount percentage to numeric
        self.df_combined['discount_numeric'] = (
            self.df_combined['Discount']
            .str.replace('%', '')
            .astype(float) / 100
        )
        
        # Calculate total amount before discount
        self.df_combined['total_amount'] = (
            self.df_combined['quantity'] * self.df_combined['price']
        )
        
        # Calculate discount amount
        self.df_combined['discount_amount'] = (
            self.df_combined['total_amount'] * self.df_combined['discount_numeric']
        )
        
        # Calculate final amount after discount
        self.df_combined['final_amount'] = (
            self.df_combined['total_amount'] - self.df_combined['discount_amount']
        )
        
        # Extract date components for analysis
        self.df_combined['year'] = self.df_combined['invoice_date'].dt.year
        self.df_combined['month'] = self.df_combined['invoice_date'].dt.month
        self.df_combined['day'] = self.df_combined['invoice_date'].dt.day
        self.df_combined['weekday'] = self.df_combined['invoice_date'].dt.dayofweek
        self.df_combined['quarter'] = self.df_combined['invoice_date'].dt.quarter
        self.df_combined['day_of_year'] = self.df_combined['invoice_date'].dt.dayofyear
        
        # Add season classification
        self.df_combined['season'] = self.df_combined['month'].map({
            12: 'Winter', 1: 'Winter', 2: 'Winter',
            3: 'Spring', 4: 'Spring', 5: 'Spring',
            6: 'Summer', 7: 'Summer', 8: 'Summer',
            9: 'Fall', 10: 'Fall', 11: 'Fall'
        })
        
        self.logger.info("Data preprocessing completed")
        
    def process_daily_sales_data(self):
        """
        Process daily sales data across stores and regions
        """
        self.logger.info("Processing daily sales data...")
        
        # Daily sales aggregation
        daily_sales = self.df_combined.groupby(['invoice_date', 'shopping_mall', 'Region']).agg({
            'final_amount': ['sum', 'count', 'mean'],
            'quantity': 'sum',
            'customer_id': 'nunique'
        }).round(2)
        
        # Flatten column names
        daily_sales.columns = ['total_revenue', 'transaction_count', 'avg_transaction_value', 
                              'total_quantity', 'unique_customers']
        daily_sales = daily_sales.reset_index()
        
        # Calculate additional metrics
        daily_sales['revenue_per_customer'] = (
            daily_sales['total_revenue'] / daily_sales['unique_customers']
        ).round(2)
        
        # Store results
        self.daily_sales = daily_sales
        
        # Regional daily sales
        regional_daily_sales = self.df_combined.groupby(['invoice_date', 'Region']).agg({
            'final_amount': ['sum', 'count', 'mean'],
            'quantity': 'sum',
            'customer_id': 'nunique',
            'shopping_mall': 'nunique'
        }).round(2)
        
        regional_daily_sales.columns = ['total_revenue', 'transaction_count', 'avg_transaction_value',
                                       'total_quantity', 'unique_customers', 'active_malls']
        regional_daily_sales = regional_daily_sales.reset_index()
        
        self.regional_daily_sales = regional_daily_sales
        
        self.logger.info("Daily sales processing completed")
        return daily_sales, regional_daily_sales
    
    def calculate_profitability(self):
        """
        Calculate profitability metrics after discounts
        """
        self.logger.info("Calculating profitability metrics...")
        
        # Mall-level profitability
        mall_profitability = self.df_combined.groupby(['shopping_mall', 'Region']).agg({
            'total_amount': 'sum',
            'discount_amount': 'sum',
            'final_amount': 'sum',
            'quantity': 'sum',
            'invoice_no': 'count'
        }).round(2)
        
        mall_profitability.columns = ['gross_revenue', 'total_discounts', 'net_revenue',
                                     'total_quantity', 'total_transactions']
        
        # Calculate profitability metrics
        mall_profitability['discount_rate'] = (
            mall_profitability['total_discounts'] / mall_profitability['gross_revenue'] * 100
        ).round(2)
        
        mall_profitability['avg_transaction_value'] = (
            mall_profitability['net_revenue'] / mall_profitability['total_transactions']
        ).round(2)
        
        mall_profitability['revenue_per_unit'] = (
            mall_profitability['net_revenue'] / mall_profitability['total_quantity']
        ).round(2)
        
        mall_profitability = mall_profitability.reset_index()
        
        # Category-level profitability
        category_profitability = self.df_combined.groupby('category').agg({
            'total_amount': 'sum',
            'discount_amount': 'sum',
            'final_amount': 'sum',
            'quantity': 'sum'
        }).round(2)
        
        category_profitability['profit_margin'] = (
            (category_profitability['final_amount'] - category_profitability['discount_amount']) /
            category_profitability['final_amount'] * 100
        ).round(2)
        
        category_profitability = category_profitability.reset_index()
        
        self.mall_profitability = mall_profitability
        self.category_profitability = category_profitability
        
        self.logger.info("Profitability calculation completed")
        return mall_profitability, category_profitability
    
    def identify_seasonal_trends(self):
        """
        Identify seasonal sales trends
        """
        self.logger.info("Identifying seasonal trends...")
        
        # Monthly trends
        monthly_trends = self.df_combined.groupby(['year', 'month']).agg({
            'final_amount': 'sum',
            'quantity': 'sum',
            'invoice_no': 'count'
        }).round(2)
        
        monthly_trends.columns = ['total_revenue', 'total_quantity', 'total_transactions']
        monthly_trends = monthly_trends.reset_index()
        monthly_trends['year_month'] = monthly_trends['year'].astype(str) + '-' + monthly_trends['month'].astype(str).str.zfill(2)
        
        # Seasonal trends
        seasonal_trends = self.df_combined.groupby('season').agg({
            'final_amount': ['sum', 'mean'],
            'quantity': 'sum',
            'invoice_no': 'count'
        }).round(2)
        
        seasonal_trends.columns = ['total_revenue', 'avg_revenue', 'total_quantity', 'total_transactions']
        seasonal_trends = seasonal_trends.reset_index()
        
        # Quarterly trends
        quarterly_trends = self.df_combined.groupby(['year', 'quarter']).agg({
            'final_amount': 'sum',
            'quantity': 'sum',
            'invoice_no': 'count'
        }).round(2)
        
        quarterly_trends.columns = ['total_revenue', 'total_quantity', 'total_transactions']
        quarterly_trends = quarterly_trends.reset_index()
        
        # Weekly patterns
        weekly_patterns = self.df_combined.groupby('weekday').agg({
            'final_amount': ['sum', 'mean'],
            'invoice_no': 'count'
        }).round(2)
        
        weekly_patterns.columns = ['total_revenue', 'avg_revenue', 'total_transactions']
        weekly_patterns = weekly_patterns.reset_index()
        
        # Map weekday numbers to names
        weekday_names = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday',
                        4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
        weekly_patterns['weekday_name'] = weekly_patterns['weekday'].map(weekday_names)
        
        self.monthly_trends = monthly_trends
        self.seasonal_trends = seasonal_trends
        self.quarterly_trends = quarterly_trends
        self.weekly_patterns = weekly_patterns
        
        self.logger.info("Seasonal trends identification completed")
        return monthly_trends, seasonal_trends, quarterly_trends, weekly_patterns
    
    def analyze_payment_methods(self):
        """
        Analyze payment methods usage and patterns
        """
        self.logger.info("Analyzing payment methods...")
        
        # Overall payment method analysis
        payment_analysis = self.df_combined.groupby('payment_method').agg({
            'final_amount': ['sum', 'mean', 'count'],
            'quantity': 'sum',
            'customer_id': 'nunique'
        }).round(2)
        
        payment_analysis.columns = ['total_revenue', 'avg_transaction_value', 'transaction_count',
                                   'total_quantity', 'unique_customers']
        payment_analysis = payment_analysis.reset_index()
        
        # Calculate percentages
        total_revenue = payment_analysis['total_revenue'].sum()
        total_transactions = payment_analysis['transaction_count'].sum()
        
        payment_analysis['revenue_percentage'] = (
            payment_analysis['total_revenue'] / total_revenue * 100
        ).round(2)
        
        payment_analysis['transaction_percentage'] = (
            payment_analysis['transaction_count'] / total_transactions * 100
        ).round(2)
        
        # Payment method by region
        payment_by_region = self.df_combined.groupby(['Region', 'payment_method']).agg({
            'final_amount': 'sum',
            'invoice_no': 'count'
        }).round(2)
        
        payment_by_region.columns = ['total_revenue', 'transaction_count']
        payment_by_region = payment_by_region.reset_index()
        
        # Payment method by category
        payment_by_category = self.df_combined.groupby(['category', 'payment_method']).agg({
            'final_amount': 'sum',
            'invoice_no': 'count'
        }).round(2)
        
        payment_by_category.columns = ['total_revenue', 'transaction_count']
        payment_by_category = payment_by_category.reset_index()
        
        # Payment method trends over time
        payment_trends = self.df_combined.groupby(['year', 'month', 'payment_method']).agg({
            'final_amount': 'sum',
            'invoice_no': 'count'
        }).round(2)
        
        payment_trends.columns = ['total_revenue', 'transaction_count']
        payment_trends = payment_trends.reset_index()
        
        self.payment_analysis = payment_analysis
        self.payment_by_region = payment_by_region
        self.payment_by_category = payment_by_category
        self.payment_trends = payment_trends
        
        self.logger.info("Payment methods analysis completed")
        return payment_analysis, payment_by_region, payment_by_category, payment_trends
    
    def generate_summary_report(self):
        """
        Generate a comprehensive summary report
        """
        self.logger.info("Generating summary report...")
        
        report = {
            'data_overview': {
                'total_records': len(self.df_combined),
                'date_range': f"{self.df_combined['invoice_date'].min().date()} to {self.df_combined['invoice_date'].max().date()}",
                'total_revenue': self.df_combined['final_amount'].sum(),
                'total_transactions': len(self.df_combined),
                'unique_customers': self.df_combined['customer_id'].nunique(),
                'unique_malls': self.df_combined['shopping_mall'].nunique(),
                'unique_regions': self.df_combined['Region'].nunique()
            },
            'top_performers': {
                'top_mall_by_revenue': self.mall_profitability.loc[self.mall_profitability['net_revenue'].idxmax(), 'shopping_mall'],
                'top_region_by_revenue': self.mall_profitability.groupby('Region')['net_revenue'].sum().idxmax(),
                'top_category_by_revenue': self.category_profitability.loc[self.category_profitability['final_amount'].idxmax(), 'category'],
                'most_popular_payment_method': self.payment_analysis.loc[self.payment_analysis['transaction_count'].idxmax(), 'payment_method']
            },
            'seasonal_insights': {
                'best_season': self.seasonal_trends.loc[self.seasonal_trends['total_revenue'].idxmax(), 'season'],
                'best_weekday': self.weekly_patterns.loc[self.weekly_patterns['total_revenue'].idxmax(), 'weekday_name'],
                'peak_month': self.monthly_trends.loc[self.monthly_trends['total_revenue'].idxmax(), 'year_month']
            }
        }
        
        self.summary_report = report
        self.logger.info("Summary report generated")
        return report
    
    def save_results(self, output_dir=None):
        """
        Save all analysis results to CSV files
        """
        if output_dir is None:
            output_dir = self.data_path / "results"
        else:
            output_dir = Path(output_dir)
        
        output_dir.mkdir(exist_ok=True)
        
        self.logger.info(f"Saving results to {output_dir}")
        
        # Save all analysis results
        results_to_save = {
            'combined_data.csv': self.df_combined,
            'daily_sales.csv': self.daily_sales,
            'regional_daily_sales.csv': self.regional_daily_sales,
            'mall_profitability.csv': self.mall_profitability,
            'category_profitability.csv': self.category_profitability,
            'monthly_trends.csv': self.monthly_trends,
            'seasonal_trends.csv': self.seasonal_trends,
            'quarterly_trends.csv': self.quarterly_trends,
            'weekly_patterns.csv': self.weekly_patterns,
            'payment_analysis.csv': self.payment_analysis,
            'payment_by_region.csv': self.payment_by_region,
            'payment_by_category.csv': self.payment_by_category,
            'payment_trends.csv': self.payment_trends
        }
        
        for filename, dataframe in results_to_save.items():
            filepath = output_dir / filename
            dataframe.to_csv(filepath, index=False)
            self.logger.info(f"Saved {filename}")
        
        # Save summary report as text
        with open(output_dir / 'summary_report.txt', 'w') as f:
            f.write("MLOPS Data Pipeline Summary Report\n")
            f.write("==================================\n\n")
            for section, data in self.summary_report.items():
                f.write(f"{section.upper()}:\n")
                for key, value in data.items():
                    f.write(f"  {key}: {value}\n")
                f.write("\n")
        
        self.logger.info("All results saved successfully")
    
    def run_complete_pipeline(self):
        """
        Run the complete data pipeline
        """
        self.logger.info("Starting MLOPS Data Pipeline...")
        
        try:
            # Step 1: Load and validate data
            self.load_and_validate_data()
            
            # Step 2: Join datasets
            self.join_datasets()
            
            # Step 3: Preprocess data
            self.preprocess_data()
            
            # Step 4: Process daily sales data
            self.process_daily_sales_data()
            
            # Step 5: Calculate profitability
            self.calculate_profitability()
            
            # Step 6: Identify seasonal trends
            self.identify_seasonal_trends()
            
            # Step 7: Analyze payment methods
            self.analyze_payment_methods()
            
            # Step 8: Generate summary report
            self.generate_summary_report()
            
            # Step 9: Save results
            self.save_results()
            
            self.logger.info("MLOPS Data Pipeline completed successfully!")
            
            return self.summary_report
            
        except Exception as e:
            self.logger.error(f"Pipeline failed: {str(e)}")
            raise


def main():
    """
    Main function to run the pipeline
    """
    # Initialize and run pipeline
    pipeline = MLOPSDataPipeline()
    
    # Run complete pipeline
    summary = pipeline.run_complete_pipeline()
    
    # Print summary
    print("\n" + "="*50)
    print("MLOPS DATA PIPELINE SUMMARY")
    print("="*50)
    
    for section, data in summary.items():
        print(f"\n{section.upper()}:")
        for key, value in data.items():
            print(f"  {key}: {value}")


if __name__ == "__main__":
    main()