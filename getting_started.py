#!/usr/bin/env python3
"""
Stock Analyzer - Getting Started Script

This script demonstrates the key functionality of the Stock Analyzer package.
It walks through analyzing stocks from value and growth perspectives,
comparing multiple companies, and performing dual analysis.

To run:
    python getting_started.py

Requirements:
    - stock_analyzer package installed
    - dependencies from requirements.txt installed
"""

import os
import time
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Import the main analysis functions
from stock_analyzer.analyzer import analyze_stock, analyze_multiple, dual_analysis
from stock_analyzer.utils.display_utils import save_report_html
from stock_analyzer.criteria.value_criteria import VALUE_CRITERIA, VALUE_DESCRIPTIONS
from stock_analyzer.criteria.growth_criteria import GROWTH_MOMENTUM_CRITERIA, GROWTH_MOMENTUM_DESCRIPTIONS

def print_section_header(title):
    """Print a formatted section header to make output more readable"""
    print("\n" + "="*80)
    print(f" {title} ".center(80, "="))
    print("="*80 + "\n")

def print_ratio_info(criteria_dict, descriptions_dict):
    """Print detailed information about financial ratios"""
    for ratio_name, description in descriptions_dict.items():
        criteria = criteria_dict.get(ratio_name, {})
        
        print(f"\n{description.get('name', ratio_name.upper())}:")
        print(f"  What it means: {description.get('description', 'No description available')}")
        print(f"  How to interpret: {description.get('interpretation', 'No interpretation available')}")
        
        if 'value_stock_ideal' in description:
            print(f"  Ideal for value investing: {description.get('value_stock_ideal')}")
        elif 'growth_stock_ideal' in description:
            print(f"  Ideal for growth investing: {description.get('growth_stock_ideal')}")
        
        if criteria:
            print("  Rating criteria:")
            for rating, (min_val, max_val) in criteria.items():
                min_str = f"{min_val:.2f}" if min_val != float('-inf') else "-infinity"
                max_str = f"{max_val:.2f}" if max_val != float('inf') else "infinity"
                print(f"    - {rating.upper()}: {min_str} to {max_str}")
        
        print("-" * 50)

def main():
    """Main function demonstrating Stock Analyzer functionality"""
    # Welcome message
    print_section_header("STOCK ANALYZER TUTORIAL")
    print("Welcome to the Stock Analyzer tutorial! This script will walk you through")
    print("using the Stock Analyzer package to evaluate stocks from both value investing")
    print("and growth/momentum perspectives.\n")
    
    # Print information about financial ratios
    print_section_header("VALUE INVESTING RATIOS")
    print("Value investing focuses on finding companies trading below their intrinsic value.")
    print("Here are the key ratios used in value analysis:\n")
    print_ratio_info(VALUE_CRITERIA, VALUE_DESCRIPTIONS)
    
    print_section_header("GROWTH & MOMENTUM INVESTING RATIOS")
    print("Growth investing focuses on companies with strong growth potential.")
    print("Momentum investing focuses on stocks with strong price trends.")
    print("Here are the key metrics used in growth and momentum analysis:\n")
    print_ratio_info(GROWTH_MOMENTUM_CRITERIA, GROWTH_MOMENTUM_DESCRIPTIONS)
    
    # Single Stock Analysis
    print_section_header("SINGLE STOCK ANALYSIS: APPLE (AAPL)")
    print("Let's analyze Apple (AAPL) from both value and growth perspectives.\n")
    
    print("Analyzing Apple from a value investing perspective...")
    apple_value_report = analyze_stock("AAPL", analysis_type="value")
    
    # Wait for user to review
    input("\nPress Enter to continue to Apple's growth analysis...\n")
    
    print("Analyzing Apple from a growth/momentum perspective...")
    apple_growth_report = analyze_stock("AAPL", analysis_type="growth_momentum")
    
    # Wait for user to review
    input("\nPress Enter to continue to multiple stock analysis...\n")
    
    # Multiple Stock Analysis
    print_section_header("COMPARING MULTIPLE TECH STOCKS")
    print("Now let's compare several major tech companies:\n")
    
    # Define list of tech stocks to analyze
    tech_stocks = ["AAPL", "MSFT", "GOOGL", "AMZN", "META"]
    print(f"Stocks to analyze: {', '.join(tech_stocks)}")
    
    print("\nAnalyzing from a value investing perspective...")
    value_results, value_reports = analyze_multiple(tech_stocks, analysis_type="value")
    
    # Wait for user to review
    input("\nPress Enter to continue to growth comparison...\n")
    
    print("Analyzing from a growth/momentum perspective...")
    growth_results, growth_reports = analyze_multiple(tech_stocks, analysis_type="growth_momentum")
    
    # Wait for user to review
    input("\nPress Enter to continue to dual analysis...\n")
    
    # Dual Analysis
    print_section_header("COMPREHENSIVE DUAL ANALYSIS")
    print("Finally, let's perform a dual analysis which examines stocks from both")
    print("value and growth perspectives simultaneously:\n")
    
    dual_report = dual_analysis(tech_stocks)
    
    # Generate visualizations if matplotlib is available
    try:
        print_section_header("VISUALIZATIONS")
        print("Creating visualizations of key metrics for comparison...\n")
        
        # Extract key value metrics for comparison
        value_metrics = ['pe_ratio', 'pb_ratio', 'roe', 'debt_to_equity']
        value_data = []
        
        for ticker in tech_stocks:
            report = value_reports.get(ticker)
            if not isinstance(report, str) and hasattr(report, 'ratios'):
                row = {'Ticker': ticker}
                for metric in value_metrics:
                    row[VALUE_DESCRIPTIONS[metric]['name']] = report.ratios.get(metric, np.nan)
                value_data.append(row)
        
        # Create DataFrame for visualization
        value_df = pd.DataFrame(value_data)
        
        # Create the visualization
        if not value_df.empty and len(value_df) > 1:
            fig, axes = plt.subplots(2, 2, figsize=(15, 10))
            axes = axes.flatten()
            
            for i, metric in enumerate(value_metrics):
                metric_name = VALUE_DESCRIPTIONS[metric]['name']
                ax = axes[i]
                value_df.plot(x='Ticker', y=metric_name, kind='bar', ax=ax, color='skyblue')
                ax.set_title(metric_name)
                ax.set_ylabel(metric_name)
                
                # Add horizontal lines for 'great' thresholds
                criteria = VALUE_CRITERIA[metric]
                if criteria['great'][1] != float('inf'):
                    ax.axhline(y=criteria['great'][1], color='green', linestyle='--', alpha=0.7, label='Great threshold')
                if criteria['great'][0] > 0:
                    ax.axhline(y=criteria['great'][0], color='green', linestyle='--', alpha=0.7)
                
                # Add annotations
                for j, v in enumerate(value_df[metric_name]):
                    if not np.isnan(v):
                        ax.text(j, v + 0.05, f"{v:.2f}", ha='center')
            
            plt.tight_layout()
            plt.savefig('value_metrics_comparison.png')
            print("Value metrics visualization saved as 'value_metrics_comparison.png'")
            
            # Growth metrics visualization
            growth_metrics = ['revenue_growth', 'earnings_growth', 'price_performance_1y', 'relative_strength']
            growth_data = []
            
            for ticker in tech_stocks:
                report = growth_reports.get(ticker)
                if not isinstance(report, str) and hasattr(report, 'ratios'):
                    row = {'Ticker': ticker}
                    for metric in growth_metrics:
                        if metric in GROWTH_MOMENTUM_DESCRIPTIONS:
                            row[GROWTH_MOMENTUM_DESCRIPTIONS[metric]['name']] = report.ratios.get(metric, np.nan)
                    growth_data.append(row)
            
            # Create DataFrame for visualization
            growth_df = pd.DataFrame(growth_data)
            
            if not growth_df.empty and len(growth_df) > 1:
                fig, axes = plt.subplots(2, 2, figsize=(15, 10))
                axes = axes.flatten()
                
                for i, metric in enumerate(growth_metrics):
                    if metric in GROWTH_MOMENTUM_DESCRIPTIONS:
                        metric_name = GROWTH_MOMENTUM_DESCRIPTIONS[metric]['name']
                        ax = axes[i]
                        growth_df.plot(x='Ticker', y=metric_name, kind='bar', ax=ax, color='purple')
                        ax.set_title(metric_name)
                        ax.set_ylabel(metric_name)
                        
                        # Add horizontal lines for 'great' thresholds
                        criteria = GROWTH_MOMENTUM_CRITERIA[metric]
                        ax.axhline(y=criteria['great'][0], color='green', linestyle='--', alpha=0.7, label='Great threshold')
                        
                        # Add annotations
                        for j, v in enumerate(growth_df[metric_name]):
                            if not np.isnan(v):
                                ax.text(j, v + 0.01, f"{v:.2f}", ha='center')
                
                plt.tight_layout()
                plt.savefig('growth_metrics_comparison.png')
                print("Growth metrics visualization saved as 'growth_metrics_comparison.png'")
        else:
            print("Not enough valid data for visualization")
    except Exception as e:
        print(f"Could not create visualizations: {str(e)}")
    
    # Save reports
    print_section_header("SAVING REPORTS")
    print("The Stock Analyzer can save analysis reports as HTML files.\n")
    
    # Save Apple's value report
    if apple_value_report is not None and not isinstance(apple_value_report, str):
        html_file = save_report_html(apple_value_report, "AAPL_value_analysis.html")
        print(f"Apple value analysis report saved to {html_file}")
    
    # Save Apple's growth report
    if apple_growth_report is not None and not isinstance(apple_growth_report, str):
        html_file = save_report_html(apple_growth_report, "AAPL_growth_analysis.html")
        print(f"Apple growth analysis report saved to {html_file}")
    
    # Conclusion
    print_section_header("CONCLUSION")
    print("This tutorial has demonstrated the key functionality of the Stock Analyzer package:")
    print("  1. Analyzing individual stocks from value and growth perspectives")
    print("  2. Comparing multiple companies within an industry")
    print("  3. Performing comprehensive dual analysis")
    print("  4. Saving reports for future reference")
    print("  5. Understanding financial ratios and their significance\n")
    print("Remember that these analyses are tools to aid your judgment, not replace it.")
    print("The best investment decisions combine quantitative analysis with qualitative")
    print("research, industry knowledge, and a clear investment strategy.\n")
    print("For more information, refer to the README.md file and documentation.")
    print("Happy investing!")

if __name__ == "__main__":
    main()
