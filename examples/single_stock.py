#!/usr/bin/env python3
"""
Single stock analysis example script.

This script demonstrates how to analyze a single stock using the StockAnalyzer.
"""

import sys
import argparse
from stock_analyzer.analyzer import analyze_stock

def main():
    """Run a single stock analysis based on command line arguments."""
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Analyze a single stock')
    parser.add_argument('ticker', type=str, help='Stock ticker symbol (e.g., AAPL)')
    parser.add_argument('--analysis-type', type=str, choices=['value', 'growth_momentum'], 
                        default='value', help='Type of analysis to perform')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Analyze the stock
    print(f"Analyzing {args.ticker} from {args.analysis_type.replace('_', '/')} perspective...")
    report = analyze_stock(args.ticker, args.analysis_type)
    
    if report is None:
        print(f"Error analyzing {args.ticker}")
        return 1
    
    print(f"\nAnalysis completed: {report.classification}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
