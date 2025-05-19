"""
Growth and momentum investing criteria and ratio descriptions.

This module defines the criteria and descriptions used for
growth and momentum-based stock analysis. The criteria represent
ideal ranges for various financial and momentum metrics according
to growth investing principles.
"""

# Growth and momentum investing classification criteria
GROWTH_MOMENTUM_CRITERIA = {
    'revenue_growth': {'great': (0.2, float('inf')), 'good': (0.1, 0.2), 'no_buy': (0, 0.1)},
    'earnings_growth': {'great': (0.2, float('inf')), 'good': (0.1, 0.2), 'no_buy': (0, 0.1)},
    'price_performance_6m': {'great': (0.15, float('inf')), 'good': (0.05, 0.15), 'no_buy': (-float('inf'), 0.05)},
    'price_performance_1y': {'great': (0.25, float('inf')), 'good': (0.1, 0.25), 'no_buy': (-float('inf'), 0.1)},
    'eps_growth': {'great': (0.15, float('inf')), 'good': (0.08, 0.15), 'no_buy': (0, 0.08)},
    'gross_margin': {'great': (0.4, float('inf')), 'good': (0.25, 0.4), 'no_buy': (0, 0.25)},
    'operating_margin': {'great': (0.2, float('inf')), 'good': (0.1, 0.2), 'no_buy': (0, 0.1)},
    'relative_strength': {'great': (0.1, float('inf')), 'good': (0, 0.1), 'no_buy': (-float('inf'), 0)},
    'analyst_recommendation': {'great': (1, 2.5), 'good': (2.5, 3.5), 'no_buy': (3.5, 5)},
    'pe_growth': {'great': (0.8, float('inf')), 'good': (0.5, 0.8), 'no_buy': (0, 0.5)},
}

# Growth and momentum investing ratio descriptions
GROWTH_MOMENTUM_DESCRIPTIONS = {
    'revenue_growth': {
        'name': 'Revenue Growth Rate',
        'description': 'Year-over-year percentage increase in company revenue.',
        'interpretation': 'Higher is better for growth stocks. Strong revenue growth indicates expanding business and market share.',
        'growth_stock_ideal': 'Above 20% annually is excellent, showing rapid expansion.'
    },
    'earnings_growth': {
        'name': 'Earnings Growth Rate',
        'description': 'Year-over-year percentage increase in earnings.',
        'interpretation': 'Higher is better. Accelerating earnings growth is particularly positive.',
        'growth_stock_ideal': 'Above 20% annually shows strong profit expansion.'
    },
    'price_performance_6m': {
        'name': '6-Month Price Performance',
        'description': 'Percentage change in stock price over the last 6 months.',
        'interpretation': 'Higher is better for momentum stocks. Positive price momentum often continues in the short term.',
        'growth_stock_ideal': 'Above 15% in 6 months indicates strong upward momentum.'
    },
    'price_performance_1y': {
        'name': '1-Year Price Performance',
        'description': 'Percentage change in stock price over the last year.',
        'interpretation': 'Higher is better for momentum strategies. Extended price strength often signals market confidence.',
        'growth_stock_ideal': 'Above 25% annually shows sustained price strength.'
    },
    'eps_growth': {
        'name': 'EPS Growth Rate',
        'description': 'Year-over-year percentage increase in earnings per share.',
        'interpretation': 'Higher is better. Consistent EPS growth is a key factor for growth investors.',
        'growth_stock_ideal': 'Above 15% annually indicates strong per-share profit growth.'
    },
    'gross_margin': {
        'name': 'Gross Margin',
        'description': 'Gross profit divided by revenue.',
        'interpretation': 'Higher is better. High margins often indicate competitive advantages and pricing power.',
        'growth_stock_ideal': 'Above 40% suggests strong product margins and pricing power.'
    },
    'operating_margin': {
        'name': 'Operating Margin',
        'description': 'Operating income divided by revenue.',
        'interpretation': 'Higher is better. Improving operating margins suggest operational efficiency.',
        'growth_stock_ideal': 'Above 20% indicates efficient operations and scalable business model.'
    },
    'relative_strength': {
        'name': 'Relative Strength',
        'description': 'Stock\'s performance compared to a benchmark (like S&P 500).',
        'interpretation': 'Higher is better for momentum stocks. Outperformance vs. the market is a positive signal.',
        'growth_stock_ideal': 'Outperforming the market by 10% or more is excellent.'
    },
    'analyst_recommendation': {
        'name': 'Analyst Recommendation',
        'description': 'Average rating from analysts (1=Strong Buy, 5=Strong Sell).',
        'interpretation': 'Lower is better. Strong buy ratings may indicate positive future prospects.',
        'growth_stock_ideal': 'Below 2.5 (between Buy and Strong Buy) suggests analyst confidence.'
    },
    'pe_growth': {
        'name': 'P/E to Growth Score',
        'description': 'Custom score balancing P/E with growth (higher growth justifying higher P/E).',
        'interpretation': 'Higher is better for growth stocks. This metric rewards high growth even with elevated P/E ratios.',
        'growth_stock_ideal': 'Above 0.8 suggests good balance of growth and valuation.'
    }
}
