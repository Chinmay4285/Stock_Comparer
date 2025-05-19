"""
Core stock analyzer module containing the main StockAnalyzer class.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from tabulate import tabulate
from IPython.display import display, HTML, Markdown

from stock_analyzer.models.stock_data import StockData
from stock_analyzer.models.report import StockReport
from stock_analyzer.utils.fetch_utils import fetch_stock_data
from stock_analyzer.utils.display_utils import print_report
from stock_analyzer.criteria.value_criteria import VALUE_CRITERIA, VALUE_DESCRIPTIONS
from stock_analyzer.criteria.growth_criteria import GROWTH_MOMENTUM_CRITERIA, GROWTH_MOMENTUM_DESCRIPTIONS


class StockAnalyzer:
    """
    Main analyzer class that evaluates stocks from value and growth perspectives.
    
    This class provides methods for analyzing stocks, generating reports,
    and comparing multiple investment opportunities.
    """
    
    def __init__(self):
        """Initialize the StockAnalyzer with default criteria and descriptions."""
        # Value investing classification criteria
        self.value_criteria = VALUE_CRITERIA
        
        # Growth and momentum investing classification criteria
        self.growth_momentum_criteria = GROWTH_MOMENTUM_CRITERIA
        
        # Set current criteria to value by default
        self.classification_criteria = self.value_criteria.copy()
        
        # Value investing ratio descriptions
        self.value_descriptions = VALUE_DESCRIPTIONS
        
        # Growth and momentum investing ratio descriptions
        self.growth_momentum_descriptions = GROWTH_MOMENTUM_DESCRIPTIONS
        
        # Set current descriptions to value by default
        self.ratio_descriptions = self.value_descriptions.copy()
    
    def test_connection(self):
        """
        Test if stock data API is working properly.
        
        Returns:
            bool: True if connection is successful, False otherwise
        """
        try:
            test_ticker = "AAPL"  # Use a reliable ticker for testing
            stock_data = fetch_stock_data(test_ticker)
            if stock_data and stock_data.info and 'shortName' in stock_data.info:
                print(f"Connection successful! Retrieved data for {stock_data.info.get('shortName', test_ticker)}")
                return True
            else:
                print("Connection issue: Could not retrieve valid data")
                return False
        except Exception as e:
            print(f"Connection error: {str(e)}")
            return False
    
    def calculate_ratios(self, stock_data, analysis_type='value'):
        """
        Calculate all financial ratios based on analysis type.
        
        Args:
            stock_data (StockData): The stock data object
            analysis_type (str): 'value' or 'growth_momentum'
            
        Returns:
            dict: Dictionary of calculated ratios
        """
        if not stock_data or not stock_data.info:
            return None
            
        info = stock_data.info
        income_stmt = stock_data.income_stmt
        balance_sheet = stock_data.balance_sheet
        historical_data = stock_data.historical_data
        market_data = stock_data.market_data
        current_price = stock_data.current_price
        
        # Initialize ratios dictionary
        ratios = {}
        
        # Calculate basic value ratios regardless of analysis type (needed for both)
        ratios['pe_ratio'] = info.get('trailingPE', info.get('forwardPE', None))
        ratios['pb_ratio'] = info.get('priceToBook', None)
        ratios['ps_ratio'] = info.get('priceToSalesTrailing12Months', None)
        ratios['debt_to_equity'] = info.get('debtToEquity', None) / 100 if info.get('debtToEquity') else None
        ratios['roe'] = info.get('returnOnEquity', None)
        ratios['current_ratio'] = info.get('currentRatio', None)
        ratios['dividend_yield'] = info.get('dividendYield', 0)
        ratios['profit_margin'] = info.get('profitMargins', None)
        ratios['peg_ratio'] = info.get('pegRatio', None)
        
        # If analysis type is growth_momentum, calculate additional ratios
        if analysis_type == 'growth_momentum' and historical_data is not None:
            # Calculate price performance metrics
            if not historical_data.empty:
                # 6-month price performance
                six_month_ago_idx = len(historical_data) - min(len(historical_data), 126)  # ~6 months of trading days
                if six_month_ago_idx >= 0 and six_month_ago_idx < len(historical_data):
                    start_price = historical_data['Close'].iloc[six_month_ago_idx]
                    end_price = historical_data['Close'].iloc[-1]
                    ratios['price_performance_6m'] = (end_price - start_price) / start_price if start_price else None
                
                # 1-year price performance
                start_price = historical_data['Close'].iloc[0] if len(historical_data) > 0 else None
                end_price = historical_data['Close'].iloc[-1] if len(historical_data) > 0 else None
                ratios['price_performance_1y'] = (end_price - start_price) / start_price if start_price else None
                
                # Calculate relative strength against the market (S&P 500)
                if market_data is not None and not market_data.empty:
                    stock_return = ratios.get('price_performance_1y')
                    market_start = market_data['Close'].iloc[0] if len(market_data) > 0 else None
                    market_end = market_data['Close'].iloc[-1] if len(market_data) > 0 else None
                    market_return = (market_end - market_start) / market_start if market_start else None
                    
                    if stock_return is not None and market_return is not None:
                        ratios['relative_strength'] = stock_return - market_return
            
            # Calculate other growth metrics
            ratios['revenue_growth'] = info.get('revenueGrowth', None)
            ratios['earnings_growth'] = info.get('earningsGrowth', None)
            ratios['eps_growth'] = info.get('earningsQuarterlyGrowth', None)
            ratios['gross_margin'] = info.get('grossMargins', None)
            ratios['operating_margin'] = info.get('operatingMargins', None)
            ratios['analyst_recommendation'] = info.get('recommendationMean', None)
            
            # Calculate PE to Growth score (custom metric balancing P/E with growth)
            if ratios['pe_ratio'] is not None and ratios['earnings_growth'] is not None and ratios['earnings_growth'] > 0:
                # Higher growth justifies higher P/E
                pe_growth_factor = ratios['earnings_growth'] / ratios['pe_ratio'] if ratios['pe_ratio'] > 0 else 0
                # Normalize to a 0-1 scale (roughly)
                ratios['pe_growth'] = min(1.5, pe_growth_factor * 10)
            
        # Advanced ratios that might need calculation from statements (for value investing)
        if income_stmt is not None and balance_sheet is not None:
            # Get the most recent fiscal year data
            latest_year_income = income_stmt.iloc[:, 0] if not income_stmt.empty else None
            latest_year_balance = balance_sheet.iloc[:, 0] if not balance_sheet.empty else None
            
            # Fill in any missing ratios with calculated values
            if latest_year_income is not None and latest_year_balance is not None:
                # Calculate missing ratios if they weren't in info
                if ratios['current_ratio'] is None and 'TotalCurrentAssets' in latest_year_balance and 'TotalCurrentLiabilities' in latest_year_balance:
                    curr_assets = latest_year_balance['TotalCurrentAssets']
                    curr_liab = latest_year_balance['TotalCurrentLiabilities']
                    ratios['current_ratio'] = curr_assets / curr_liab if curr_liab else None
                    
                # More calculations for missing ratios as needed
                
        return ratios
        
    def get_ratio_explanation(self, ratio_name, ratio_value, rating, analysis_type='value'):
        """
        Generate explanation for a ratio's rating based on analysis type.
        
        Args:
            ratio_name (str): Name of the ratio
            ratio_value (float): Value of the ratio
            rating (str): 'great', 'good', or 'no_buy'
            analysis_type (str): 'value' or 'growth_momentum'
            
        Returns:
            str: Explanation of the ratio's rating
        """
        if analysis_type == 'value':
            descriptions = self.value_descriptions
            ideal_key = 'value_stock_ideal'
        else:  # growth_momentum
            descriptions = self.growth_momentum_descriptions
            ideal_key = 'growth_stock_ideal'
            
        if ratio_name not in descriptions or ratio_value is None:
            return "Insufficient data available."
            
        ratio_info = descriptions[ratio_name]
        
        # Get the appropriate criteria based on analysis type
        if analysis_type == 'value':
            criteria = self.value_criteria[ratio_name]
        else:  # growth_momentum
            if ratio_name in self.growth_momentum_criteria:
                criteria = self.growth_momentum_criteria[ratio_name]
            else:
                return "This metric is not applicable for growth/momentum analysis."
        
        explanation = f"{ratio_info['name']} ({ratio_value:.2f}): "
        
        if rating == 'great':
            explanation += f"EXCELLENT. {ratio_info['interpretation'].split('.')[0]}. "
            explanation += f"For {analysis_type.replace('_', '/')} stocks, {ratio_info.get(ideal_key, '')}"
        elif rating == 'good':
            explanation += f"GOOD. {ratio_info['interpretation'].split('.')[0]}. "
            explanation += f"While not in the ideal range ({criteria['great'][0]:.2f}-{criteria['great'][1] if criteria['great'][1] != float('inf') else 'inf'}), "
            explanation += f"it's still acceptable for {analysis_type.replace('_', '/')} investing."
        else:  # no_buy
            explanation += f"CONCERNING. {ratio_info['interpretation'].split('.')[0]}. "
            explanation += f"For {analysis_type.replace('_', '/')} stocks, this is outside the preferred range. "
            explanation += f"Ideal would be {criteria['great'][0]:.2f}-{criteria['great'][1] if criteria['great'][1] != float('inf') else 'inf'}."
            
        return explanation
        
    def classify_stock(self, ratios, analysis_type='value'):
        """
        Classify stock based on calculated ratios and analysis type.
        
        Args:
            ratios (dict): Dictionary of calculated ratios
            analysis_type (str): 'value' or 'growth_momentum'
            
        Returns:
            tuple: (classification, rating_details)
        """
        if not ratios:
            return "Insufficient data for classification", {}
            
        # Set the appropriate criteria based on analysis type
        if analysis_type == 'value':
            criteria = self.value_criteria
        else:  # growth_momentum
            criteria = self.growth_momentum_criteria
            
        # Count ratings for each category
        rating_counts = {'great': 0, 'good': 0, 'no_buy': 0}
        rating_details = {}
        
        for ratio_name, ratio_value in ratios.items():
            if ratio_value is not None and ratio_name in criteria:
                ratio_criteria = criteria[ratio_name]
                
                # Determine rating for this ratio
                for rating, (min_val, max_val) in ratio_criteria.items():
                    if min_val <= ratio_value < max_val:
                        rating_counts[rating] += 1
                        rating_details[ratio_name] = rating
                        break
        
        # Classification logic
        total_rated = sum(rating_counts.values())
        if total_rated == 0:
            return "Insufficient data for classification", rating_details
            
        # Calculate percentages
        great_percent = rating_counts['great'] / total_rated
        good_percent = rating_counts['good'] / total_rated
        no_buy_percent = rating_counts['no_buy'] / total_rated
        
        # Final classification - adjust thresholds based on analysis type
        if analysis_type == 'value':
            # Value investing classification (stricter)
            if great_percent >= 0.5 and no_buy_percent <= 0.2:
                return "GREAT BUY", rating_details
            elif (great_percent + good_percent) >= 0.6 and no_buy_percent <= 0.3:
                return "GOOD BUY", rating_details
            else:
                return "NO BUY", rating_details
        else:
            # Growth and momentum classification (more generous on growth metrics)
            if great_percent >= 0.4 and no_buy_percent <= 0.3:
                return "GREAT GROWTH OPPORTUNITY", rating_details
            elif (great_percent + good_percent) >= 0.5 and no_buy_percent <= 0.4:
                return "GOOD GROWTH OPPORTUNITY", rating_details
            else:
                return "POOR GROWTH OPPORTUNITY", rating_details
            
    def generate_report(self, ticker, analysis_type='value'):
        """
        Generate comprehensive stock analysis report based on analysis type.
        
        Args:
            ticker (str): Stock ticker symbol
            analysis_type (str): 'value' or 'growth_momentum'
            
        Returns:
            StockReport: Report object or str if error
        """
        # Fetch data
        stock_data = fetch_stock_data(ticker)
        if not stock_data:
            return f"Could not retrieve data for {ticker}"
            
        # Set the appropriate criteria and descriptions based on analysis type
        if analysis_type == 'value':
            self.classification_criteria = self.value_criteria
            self.ratio_descriptions = self.value_descriptions
        else:  # growth_momentum
            self.classification_criteria = self.growth_momentum_criteria
            self.ratio_descriptions = self.growth_momentum_descriptions
            
        # Calculate ratios
        ratios = self.calculate_ratios(stock_data, analysis_type)
        if not ratios:
            return f"Could not calculate ratios for {ticker}"
            
        # Classify stock
        classification, rating_details = self.classify_stock(ratios, analysis_type)
        
        # Generate explanations for each ratio
        ratio_explanations = {}
        for ratio_name, rating in rating_details.items():
            if ratio_name in ratios and ratios[ratio_name] is not None:
                ratio_explanations[ratio_name] = self.get_ratio_explanation(
                    ratio_name, ratios[ratio_name], rating, analysis_type
                )
        
        # Create report
        report = StockReport(
            ticker=ticker,
            company_name=stock_data.info.get('longName', ticker),
            current_price=stock_data.current_price,
            currency=stock_data.info.get('currency', 'USD'),
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            classification=classification,
            ratios=ratios,
            rating_details=rating_details,
            ratio_explanations=ratio_explanations,
            analysis_type=analysis_type
        )
        
        return report
        
    def analyze_multiple_stocks(self, tickers, analysis_type='value'):
        """
        Analyze multiple stocks and categorize them based on analysis type.
        
        Args:
            tickers (list): List of stock ticker symbols
            analysis_type (str): 'value' or 'growth_momentum'
            
        Returns:
            tuple: (results, all_reports)
        """
        results = {}
        
        # Set up result categories based on analysis type
        if analysis_type == 'value':
            results = {
                'GREAT BUY': [],
                'GOOD BUY': [],
                'NO BUY': [],
                'ERROR': []
            }
        else:  # growth_momentum
            results = {
                'GREAT GROWTH OPPORTUNITY': [],
                'GOOD GROWTH OPPORTUNITY': [],
                'POOR GROWTH OPPORTUNITY': [],
                'ERROR': []
            }
        
        all_reports = {}
        
        # Process each ticker
        for ticker in tickers:
            print(f"Analyzing {ticker} ({analysis_type.replace('_', '/')} perspective)...")
            report = self.generate_report(ticker, analysis_type)
            
            if isinstance(report, str):
                # Error occurred
                results['ERROR'].append(ticker)
                all_reports[ticker] = report
            else:
                # Successfully analyzed
                classification = report.classification
                results[classification].append(ticker)
                all_reports[ticker] = report
                
        # Create summary table
        summary_data = []
        for ticker, report in all_reports.items():
            if isinstance(report, str):
                summary_data.append([ticker, "ERROR", report, "-"])
            else:
                # Count great and good indicators
                ratings = report.rating_details.values()
                great_count = list(ratings).count('great')
                good_count = list(ratings).count('good')
                total = len(ratings)
                
                strength = f"{great_count + good_count}/{total} ({(great_count + good_count)/total*100:.1f}%)"
                summary_data.append([ticker, report.classification, report.current_price, strength])
        
        # Display summary
        print("\n" + "="*80)
        print(f"MULTIPLE STOCK ANALYSIS SUMMARY ({analysis_type.replace('_', '/').upper()} PERSPECTIVE)")
        print("="*80)
        print(tabulate(summary_data, headers=["Ticker", "Classification", "Price/Error", "Strength"], tablefmt="grid"))
        print("\n")
        
        # Display categorized results
        for category, tickers in results.items():
            if tickers:
                if category == 'ERROR':
                    print(f"📊 ERRORS ({len(tickers)}): {', '.join(tickers)}")
                elif "GREAT" in category:
                    print(f"🟢 {category} ({len(tickers)}): {', '.join(tickers)}")
                elif "GOOD" in category:
                    print(f"🔵 {category} ({len(tickers)}): {', '.join(tickers)}")
                else:
                    print(f"🔴 {category} ({len(tickers)}): {', '.join(tickers)}")
        
        return results, all_reports
    
    def generate_detailed_comparison(self, all_reports, analysis_type='value'):
        """
        Generate a detailed comparison of all stocks based on analysis type.
        
        Args:
            all_reports (dict): Dictionary of reports
            analysis_type (str): 'value' or 'growth_momentum'
            
        Returns:
            str: Comparison table as markdown
        """
        # Filter out error reports
        valid_reports = {ticker: report for ticker, report in all_reports.items() 
                         if not isinstance(report, str) and report.analysis_type == analysis_type}
        
        if not valid_reports:
            return f"No valid reports for {analysis_type} analysis to compare."
            
        # Prepare comparison data
        comparison_data = []
        
        # Define the metrics to compare based on analysis type
        if analysis_type == 'value':
            metrics = list(self.value_criteria.keys())
        else:  # growth_momentum
            metrics = list(self.growth_momentum_criteria.keys())
        
        # Create header row
        header_row = ["Metric"]
        header_row.extend([f"{report.company_name} ({ticker})" for ticker, report in valid_reports.items()])
        
        # Add data for each metric
        for metric in metrics:
            # Get the appropriate name for the metric based on analysis type
            if analysis_type == 'value':
                metric_name = self.value_descriptions.get(metric, {}).get('name', metric.replace('_', ' ').title())
            else:  # growth_momentum
                metric_name = self.growth_momentum_descriptions.get(metric, {}).get('name', metric.replace('_', ' ').title())
                
            row = [metric_name]
            
            for ticker, report in valid_reports.items():
                value = report.ratios.get(metric)
                rating = report.rating_details.get(metric, 'N/A')
                
                if value is not None:
                    if rating == 'great':
                        formatted_value = f"**{value:.2f}** (Great)"
                    elif rating == 'good':
                        formatted_value = f"*{value:.2f}* (Good)"
                    else:
                        formatted_value = f"{value:.2f} (Poor)"
                else:
                    formatted_value = "N/A"
                    
                row.append(formatted_value)
                
            comparison_data.append(row)
            
        # Add classification row
        classification_row = ["**Classification**"]
        for ticker, report in valid_reports.items():
            classification_row.append(f"**{report.classification}**")
            
        comparison_data.append(classification_row)
        
        # Generate the comparison table
        comparison_table = tabulate(comparison_data, headers=header_row, tablefmt="pipe")
        
        # Display as Markdown
        display(Markdown(f"## {analysis_type.replace('_', ' & ').title()} Stock Comparison"))
        display(Markdown(comparison_table))
        
        return comparison_table


def analyze_stock(ticker, analysis_type='value'):
    """
    Analyze a single stock and display the report.
    
    Args:
        ticker (str): Stock ticker symbol
        analysis_type (str): 'value' or 'growth_momentum'
        
    Returns:
        StockReport: Analysis report
    """
    try:
        analyzer = StockAnalyzer()
        
        # Test connection first
        if not analyzer.test_connection():
            print("Cannot proceed due to connection issues")
            return None
            
        # Get report
        report = analyzer.generate_report(ticker, analysis_type)
        
        if isinstance(report, str):
            print(f"Error: {report}")
            return None
            
        # Display report
        print_report(report)
        return report
    except Exception as e:
        print(f"An error occurred during analysis: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def analyze_multiple(tickers, analysis_type='value'):
    """
    Analyze multiple stocks and display categorized results.
    
    Args:
        tickers (list or str): List of stock ticker symbols or comma-separated string
        analysis_type (str): 'value' or 'growth_momentum'
        
    Returns:
        tuple: (categorized results, full reports)
    """
    if isinstance(tickers, str):
        tickers = [ticker.strip() for ticker in tickers.split(',')]
    
    analyzer = StockAnalyzer()
    results, reports = analyzer.analyze_multiple_stocks(tickers, analysis_type)
    
    # Ask if user wants detailed comparison
    if len(reports) > 1:
        print("\nWould you like to see a detailed comparison? (y/n)")
        response = input()
        if response.lower() == 'y':
            analyzer.generate_detailed_comparison(reports, analysis_type)
    
    return results, reports


def dual_analysis(tickers):
    """
    Analyze stocks from both value and growth+momentum perspectives.
    
    Args:
        tickers (list or str): List of stock ticker symbols or comma-separated string
        
    Returns:
        dict: Reports for both analysis types
    """
    if isinstance(tickers, str):
        tickers = [ticker.strip() for ticker in tickers.split(',')]
    
    analyzer = StockAnalyzer()
    
    # Analyze from value perspective
    print("="*80)
    print("VALUE INVESTING ANALYSIS")
    print("="*80)
    value_results, value_reports = analyzer.analyze_multiple_stocks(tickers, 'value')
    
    # Analyze from growth+momentum perspective
    print("\n" + "="*80)
    print("GROWTH & MOMENTUM INVESTING ANALYSIS")
    print("="*80)
    growth_results, growth_reports = analyzer.analyze_multiple_stocks(tickers, 'growth_momentum')
    
    # Prepare combined report
    dual_report = {
        'value_analysis': {
            'results': value_results,
            'reports': value_reports
        },
        'growth_momentum_analysis': {
            'results': growth_results, 
            'reports': growth_reports
        }
    }
    
    # Ask if user wants detailed comparisons
    if len(tickers) > 1:
        print("\nWould you like to see detailed comparisons? (y/n)")
        response = input()
        if response.lower() == 'y':
            print("\nValue Investing Comparison:")
            analyzer.generate_detailed_comparison(value_reports, 'value')
            print("\nGrowth & Momentum Investing Comparison:")
            analyzer.generate_detailed_comparison(growth_reports, 'growth_momentum')
    
    # Generate a summary of the dual analysis
    print("\n" + "="*80)
    print("DUAL ANALYSIS SUMMARY")
    print("="*80)
    
    summary_data = []
    for ticker in tickers:
        value_report = value_reports.get(ticker)
        growth_report = growth_reports.get(ticker)
        
        # Improved error handling
        value_class = "ERROR"
        growth_class = "ERROR"
        
        if not isinstance(value_report, str):
            try:
                value_class = value_report.classification
            except (KeyError, TypeError, AttributeError):
                value_class = "ERROR (Invalid Report)"
                
        if not isinstance(growth_report, str):
            try:
                growth_class = growth_report.classification
            except (KeyError, TypeError, AttributeError):
                growth_class = "ERROR (Invalid Report)"
        
        if value_class.startswith("ERROR") or growth_class.startswith("ERROR"):
            summary_data.append([ticker, value_class, growth_class, "N/A"])
            continue
            
        # Determine overall recommendation based on both analyses
        value_rating = 2 if "GREAT" in value_class else 1 if "GOOD" in value_class else 0
        growth_rating = 2 if "GREAT" in growth_class else 1 if "GOOD" in growth_class else 0
        
        if value_rating + growth_rating >= 3:
            overall = "⭐⭐⭐ STRONG BUY"
        elif value_rating + growth_rating == 2:
            overall = "⭐⭐ MODERATE BUY"
        elif value_rating + growth_rating == 1:
            overall = "⭐ SPECULATIVE"
        else:
            overall = "❌ AVOID"
            
        summary_data.append([
            ticker, 
            value_class,
            growth_class,
            overall
        ])
    
    print(tabulate(summary_data, headers=["Ticker", "Value Rating", "Growth Rating", "Overall"], tablefmt="grid"))
    
    return dual_report
