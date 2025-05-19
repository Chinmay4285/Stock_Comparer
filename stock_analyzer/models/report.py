"""
Report model class for stock analyzer.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class StockReport:
    """
    Data class that holds stock analysis report.
    
    Attributes:
        ticker (str): Stock ticker symbol
        company_name (str): Company name
        current_price (float): Current stock price
        currency (str): Currency code (e.g., USD)
        timestamp (str): Timestamp of the analysis
        classification (str): Investment classification
        ratios (Dict[str, float]): Calculated financial ratios
        rating_details (Dict[str, str]): Rating details for each ratio
        ratio_explanations (Dict[str, str]): Explanations for each ratio
        analysis_type (str): Type of analysis ('value' or 'growth_momentum')
    """
    ticker: str
    company_name: str
    current_price: float
    currency: str
    timestamp: str
    classification: str
    ratios: Dict[str, Any]
    rating_details: Dict[str, str]
    ratio_explanations: Dict[str, str]
    analysis_type: str = 'value'
    
    @property
    def great_count(self) -> int:
        """Count of 'great' ratings in the report."""
        return list(self.rating_details.values()).count('great')
    
    @property
    def good_count(self) -> int:
        """Count of 'good' ratings in the report."""
        return list(self.rating_details.values()).count('good')
    
    @property
    def no_buy_count(self) -> int:
        """Count of 'no_buy' ratings in the report."""
        return list(self.rating_details.values()).count('no_buy')
    
    @property
    def total_rated(self) -> int:
        """Total number of rated metrics."""
        return len(self.rating_details)
    
    @property
    def strength_percentage(self) -> float:
        """Percentage of great and good ratings."""
        if self.total_rated == 0:
            return 0.0
        return (self.great_count + self.good_count) / self.total_rated * 100
    
    @property
    def summary(self) -> str:
        """Generate a summary of the report."""
        if "GREAT" in self.classification:
            if self.analysis_type == 'value':
                return "This stock shows strong fundamentals across multiple metrics and may be undervalued."
            else:
                return "This stock shows strong growth and momentum across multiple metrics and may be poised for continued outperformance."
        elif "GOOD" in self.classification:
            if self.analysis_type == 'value':
                return "This stock shows decent fundamentals with some strengths, suggesting a reasonable investment."
            else:
                return "This stock shows decent growth and momentum characteristics, suggesting potential for continued performance."
        else:
            if self.analysis_type == 'value':
                return "This stock has several concerning indicators and may not be a good value investment at current prices."
            else:
                return "This stock lacks sufficient growth and momentum characteristics to be considered a strong growth investment."
