"""
Data fetching utilities for stock analyzer.
"""

import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
from typing import Optional, Union, List

from stock_analyzer.models.stock_data import StockData


def fetch_stock_data(ticker: str) -> Optional[StockData]:
    """
    Fetch all necessary stock data from external APIs.
    
    This function retrieves comprehensive stock information including basic info,
    financial statements, historical prices, and market comparison data.
    
    Args:
        ticker (str): Stock ticker symbol (e.g., 'AAPL' for Apple)
        
    Returns:
        StockData: A StockData object containing all fetched information,
                  or None if data couldn't be retrieved
        
    Raises:
        No exceptions are raised, errors are handled internally
    """
    try:
        print(f"Fetching data for {ticker}...")
        
        # Get stock info
        stock = yf.Ticker(ticker)
        
        # Real-time price data
        try:
            stock_info = stock.info
            if not stock_info:
                print(f"Warning: Could not retrieve info for {ticker}")
                return None
        except Exception as e:
            print(f"Error fetching basic info for {ticker}: {str(e)}")
            return None
        
        # Get financial statements
        try:
            income_stmt = stock.income_stmt
            balance_sheet = stock.balance_sheet
            cash_flow = stock.cashflow
        except Exception as e:
            print(f"Warning: Could not retrieve financial statements for {ticker}: {str(e)}")
            income_stmt = pd.DataFrame()
            balance_sheet = pd.DataFrame()
            cash_flow = pd.DataFrame()
        
        # Get historical data for price performance and other momentum metrics
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=365)  # Last year
            historical_data = stock.history(start=start_date, end=end_date, interval="1d")
            
            if historical_data.empty:
                print(f"Warning: No historical data found for {ticker}")
        except Exception as e:
            print(f"Error fetching historical data for {ticker}: {str(e)}")
            historical_data = pd.DataFrame()
        
        # Get market index data for relative strength calculation
        try:
            market_ticker = "^GSPC"  # S&P 500
            market = yf.Ticker(market_ticker)
            market_data = market.history(start=start_date, end=end_date, interval="1d")
            
            if market_data.empty:
                print(f"Warning: No market data found for comparison")
        except Exception as e:
            print(f"Error fetching market data: {str(e)}")
            market_data = pd.DataFrame()
        
        # Create and return StockData object
        return StockData(
            ticker=ticker,
            info=stock_info,
            income_stmt=income_stmt,
            balance_sheet=balance_sheet,
            cash_flow=cash_flow,
            historical_data=historical_data,
            market_data=market_data,
            current_price=stock_info.get('currentPrice', stock_info.get('regularMarketPrice', None))
        )
    except Exception as e:
        print(f"Error fetching data for {ticker}: {str(e)}")
        return None


def fetch_multiple_stocks(tickers: Union[List[str], str]) -> dict:
    """
    Fetch data for multiple stocks.
    
    Args:
        tickers (Union[List[str], str]): List of tickers or comma-separated string
        
    Returns:
        dict: Dictionary of StockData objects, with tickers as keys
    """
    if isinstance(tickers, str):
        tickers = [ticker.strip() for ticker in tickers.split(',')]
        
    result = {}
    for ticker in tickers:
        result[ticker] = fetch_stock_data(ticker)
        
    return result
