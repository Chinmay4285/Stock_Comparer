#!/usr/bin/env python3
"""
Multiple stocks analysis example script.

This script demonstrates how to analyze multiple stocks using the StockAnalyzer.
"""

import sys
import argparse
from stock_analyzer.analyzer import analyze_multiple

def main():
    """Run a multiple stock analysis based on command line arguments."""
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Analyze multiple stocks')
    parser.add_argument('tickers', type=str, nargs='+', help='Stock ticker symbols (e.g., AAPL MSFT GOOGL)')
    parser.add_argument('--analysis-type', type=str, choices=['value', 'growth_momentum'], 
                        default='value', help='Type of analysis to perform')
    parser.add_argument('--no-interactive', action='store_true', help='Skip interactive prompts')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Convert tickers list to comma-separated string if multiple tickers were provided
    if len(args.tickers) == 1 and ',' in args.tickers[0]:
        tickers = args.tickers[0]  # Already comma-separated
    else:
        tickers = args.tickers  # List of tickers
    
    # Set whether to use interactive mode
    interactive_mode = not args.no_interactive
    
    # Analyze the stocks
    print(f"Analyzing {tickers} from {args.analysis_type.replace('_', '/')} perspective...")
    results, reports = analyze_multiple(tickers, args.analysis_type)
    
    # In non-interactive mode, we can still display a detailed comparison
    if not interactive_mode and len(reports) > 1:
        from stock_analyzer.analyzer import StockAnalyzer
        analyzer = StockAnalyzer()
        analyzer.generate_detailed_comparison(reports, args.analysis_type)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
