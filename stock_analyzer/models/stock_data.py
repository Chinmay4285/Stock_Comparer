"""
Stock data model classes for the stock analyzer.
"""

import pandas as pd
from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class StockData:
    """
    Data class that holds all stock information.
    
    Attributes:
        ticker (str): Stock ticker symbol
        info (Dict[str, Any]): Stock information from API
        income_stmt (pd.DataFrame): Income statement data
        balance_sheet (pd.DataFrame): Balance sheet data
        cash_flow (pd.DataFrame): Cash flow statement data
        historical_data (pd.DataFrame): Historical price data
        market_data (pd.DataFrame): Market benchmark data
        current_price (float): Current stock price
    """
    ticker: str
    info: Dict[str, Any]
    income_stmt: Optional[pd.DataFrame] = None
    balance_sheet: Optional[pd.DataFrame] = None
    cash_flow: Optional[pd.DataFrame] = None
    historical_data: Optional[pd.DataFrame] = None
    market_data: Optional[pd.DataFrame] = None
    current_price: Optional[float] = None
    
    def __post_init__(self):
        """Additional initialization after data class is created."""
        if self.current_price is None and self.info:
            self.current_price = self.info.get('currentPrice', self.info.get('regularMarketPrice', None))
