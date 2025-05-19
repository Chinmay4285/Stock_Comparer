#!/usr/bin/env python3
"""
Dual analysis example script.

This script demonstrates how to perform dual analysis (both value and growth/momentum)
on multiple stocks using the StockAnalyzer.
"""

import sys
import argparse
from stock_analyzer.analyzer import dual_analysis

def main():
    """Run a dual analysis based on command line arguments."""
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Perform dual analysis on stocks')
    parser.add_argument('tickers', type=str, nargs='+', help='Stock ticker symbols (e.g., AAPL MSFT GOOGL)')
    parser.add_argument('--no-interactive', action='store_true', help='Skip interactive prompts')
    parser.add_argument('--save-reports', action='store_true', help='Save HTML reports for each stock')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Convert tickers list to comma-separated string if multiple tickers were provided
    if len(args.tickers) == 1 and ',' in args.tickers[0]:
        tickers = args.tickers[0]  # Already comma-separated
    else:
        tickers = args.tickers  # List of tickers
    
    # Set whether to use interactive mode
    interactive_mode = not args.no_interactive
    
    # Perform dual analysis
    print(f"Performing dual analysis on {tickers}...")
    dual_report = dual_analysis(tickers)
    
    # Save reports if requested
    if args.save_reports:
        from stock_analyzer.utils.display_utils import save_report_html
        
        print("\nSaving HTML reports...")
        for analysis_type, data in dual_report.items():
            for ticker, report in data['reports'].items():
                if not isinstance(report, str):  # Skip error reports
                    filename = f"{ticker}_{analysis_type}.html"
                    save_report_html(report, filename)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
