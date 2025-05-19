"""
Value investing criteria and ratio descriptions.

This module defines the criteria and descriptions used for
value-based stock analysis. The criteria represent ideal ranges
for various financial ratios according to value investing principles.
"""

# Value investing classification criteria
VALUE_CRITERIA = {
    'pe_ratio': {'great': (0, 15), 'good': (15, 25), 'no_buy': (25, float('inf'))},
    'pb_ratio': {'great': (0, 1.5), 'good': (1.5, 3), 'no_buy': (3, float('inf'))},
    'ps_ratio': {'great': (0, 2), 'good': (2, 4), 'no_buy': (4, float('inf'))},
    'debt_to_equity': {'great': (0, 0.5), 'good': (0.5, 1.5), 'no_buy': (1.5, float('inf'))},
    'roe': {'great': (0.15, float('inf')), 'good': (0.1, 0.15), 'no_buy': (0, 0.1)},
    'current_ratio': {'great': (1.5, 3), 'good': (1, 1.5), 'no_buy': (0, 1)},
    'dividend_yield': {'great': (0.03, float('inf')), 'good': (0.01, 0.03), 'no_buy': (0, 0.01)},
    'profit_margin': {'great': (0.15, float('inf')), 'good': (0.08, 0.15), 'no_buy': (0, 0.08)},
    'peg_ratio': {'great': (0, 1), 'good': (1, 2), 'no_buy': (2, float('inf'))},
}

# Value investing ratio descriptions
VALUE_DESCRIPTIONS = {
    'pe_ratio': {
        'name': 'Price-to-Earnings Ratio',
        'description': 'Compares a company\'s share price to its earnings per share.',
        'interpretation': 'Lower is better for value stocks. A low P/E may indicate an undervalued stock, while a high P/E might suggest overvaluation or high growth expectations.',
        'value_stock_ideal': 'Below 15 is excellent for value investing, suggesting potential undervaluation.'
    },
    'pb_ratio': {
        'name': 'Price-to-Book Ratio',
        'description': 'Compares a company\'s market value to its book value.',
        'interpretation': 'Lower is better for value stocks. A P/B ratio under 1.5 may indicate an undervalued stock relative to its assets.',
        'value_stock_ideal': 'Below 1.5 is considered excellent for value investing.'
    },
    'ps_ratio': {
        'name': 'Price-to-Sales Ratio',
        'description': 'Compares a company\'s market cap to its revenue.',
        'interpretation': 'Lower is better. A low P/S ratio may indicate an undervalued stock based on its sales performance.',
        'value_stock_ideal': 'Below 2 is excellent for value investing, particularly in established industries.'
    },
    'debt_to_equity': {
        'name': 'Debt-to-Equity Ratio',
        'description': 'Measures a company\'s financial leverage by comparing total liabilities to shareholders\' equity.',
        'interpretation': 'Lower is generally better. High leverage can increase financial risk and volatility.',
        'value_stock_ideal': 'Below 0.5 is excellent, indicating conservative financial management.'
    },
    'roe': {
        'name': 'Return on Equity',
        'description': 'Measures how efficiently a company generates profit from its equity.',
        'interpretation': 'Higher is better. Strong ROE indicates efficient use of shareholders\' capital.',
        'value_stock_ideal': 'Above 15% shows excellent profitability and efficiency.'
    },
    'current_ratio': {
        'name': 'Current Ratio',
        'description': 'Measures a company\'s ability to pay short-term obligations.',
        'interpretation': 'Higher is generally better. A ratio above 1.5 suggests good short-term financial health.',
        'value_stock_ideal': 'Between 1.5 and 3.0 is ideal, showing good liquidity without excessive idle capital.'
    },
    'dividend_yield': {
        'name': 'Dividend Yield',
        'description': 'Annual dividend payment relative to share price.',
        'interpretation': 'Higher is generally better for income investors. Shows how much cash flow you\'re receiving per dollar invested.',
        'value_stock_ideal': 'Above 3% is excellent for value and income investing.'
    },
    'profit_margin': {
        'name': 'Profit Margin',
        'description': 'Percentage of revenue that translates into profit.',
        'interpretation': 'Higher is better. Shows how efficiently a company converts sales into profits.',
        'value_stock_ideal': 'Above 15% indicates strong profitability and competitive advantages.'
    },
    'peg_ratio': {
        'name': 'Price/Earnings to Growth Ratio',
        'description': 'P/E ratio divided by earnings growth rate.',
        'interpretation': 'Lower is better. Takes into account growth expectations to give context to the P/E ratio.',
        'value_stock_ideal': 'Below 1.0 suggests the stock may be undervalued relative to its growth rate.'
    }
}
