# Stock Analyzer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![yfinance](https://img.shields.io/badge/powered%20by-yfinance-brightgreen.svg)](https://github.com/ranaroussi/yfinance)

A comprehensive Python tool for analyzing stocks from both value investing and growth/momentum perspectives. Stock Analyzer helps you make more informed investment decisions by evaluating key financial metrics, comparing companies, and identifying promising opportunities based on your investment philosophy.

![Example Analysis](docs/images/example_analysis.png)
*Note: Replace with an actual screenshot of the analysis output when available*

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Examples](#usage-examples)
- [Understanding Results](#understanding-results)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Features

- **Dual Investment Philosophies**: Analyze stocks through both value investing (Graham/Buffett) and growth/momentum lenses
- **Comprehensive Metrics**: Evaluate 9+ financial ratios for value analysis and 10+ metrics for growth analysis
- **Automated Classification**: Stocks are automatically classified as "GREAT BUY", "GOOD BUY", or "NO BUY" based on multiple criteria
- **Multiple Stock Comparison**: Compare and rank stocks within an industry or portfolio
- **Educational Explanations**: Learn what each financial ratio means and how to interpret it
- **Beautiful Reports**: Generate rich HTML reports with color-coded results and detailed explanations
- **Data Visualization**: Create visual comparisons of key metrics across companies
- **Flexible Analysis**: Analyze single stocks, multiple companies, or perform dual perspective analysis

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/stock-analyzer.git
cd stock-analyzer
```

2. Create a virtual environment (recommended):
```bash
# Using venv
python -m venv venv

# Activate the environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt

# Install the package in development mode
pip install -e .
```

## Quick Start

The fastest way to get started is to run the included demo script:

```bash
python getting_started.py
```

This interactive script will:
- Explain the financial ratios used in analysis
- Demonstrate single stock analysis using Apple (AAPL)
- Show how to compare multiple tech stocks
- Perform dual analysis from both value and growth perspectives
- Create visualizations of key metrics
- Save HTML reports for reference

## Usage Examples

### Analyzing a Single Stock

```python
from stock_analyzer.analyzer import analyze_stock

# Analyze from a value investing perspective (default)
value_report = analyze_stock("MSFT")

# Analyze from a growth/momentum perspective
growth_report = analyze_stock("MSFT", analysis_type="growth_momentum")
```

### Comparing Multiple Stocks

```python
from stock_analyzer.analyzer import analyze_multiple

# Define stocks to analyze
stocks = ["AAPL", "MSFT", "GOOGL", "AMZN"]

# Analyze from a value perspective
value_results, value_reports = analyze_multiple(stocks)

# Analyze from a growth perspective
growth_results, growth_reports = analyze_multiple(stocks, analysis_type="growth_momentum")
```

### Performing Dual Analysis

```python
from stock_analyzer.analyzer import dual_analysis

# Analyze stocks from both perspectives
dual_report = dual_analysis(["AAPL", "MSFT", "GOOGL"])
```

### Command-Line Usage

You can also use the provided example scripts directly from the command line:

```bash
# Analyze a single stock
python -m examples.single_stock AAPL

# Analyze a single stock from growth perspective
python -m examples.single_stock AAPL --analysis-type growth_momentum

# Analyze multiple stocks
python -m examples.multiple_stocks AAPL MSFT GOOGL AMZN

# Perform dual analysis
python -m examples.dual_analysis AAPL MSFT GOOGL AMZN
```

### Saving Reports

```python
from stock_analyzer.utils.display_utils import save_report_html

# Save a report to an HTML file
html_file = save_report_html(report, "AAPL_analysis.html")
```

## Understanding Results

The analysis provides several key outputs:

### Classification System

- **Value Analysis Classifications**:
  - "GREAT BUY": Strong fundamentals across multiple metrics, potentially undervalued
  - "GOOD BUY": Decent fundamentals with some strengths, reasonable investment
  - "NO BUY": Several concerning indicators, not recommended at current prices

- **Growth Analysis Classifications**:
  - "GREAT GROWTH OPPORTUNITY": Strong growth and momentum metrics
  - "GOOD GROWTH OPPORTUNITY": Decent growth characteristics 
  - "POOR GROWTH OPPORTUNITY": Insufficient growth metrics

- **Dual Analysis Overall Rating**:
  - "⭐⭐⭐ STRONG BUY": Excellent in both value and growth dimensions
  - "⭐⭐ MODERATE BUY": Strong in one dimension, decent in the other
  - "⭐ SPECULATIVE": Good in one dimension, poor in the other
  - "❌ AVOID": Poor in both dimensions

### Key Metrics Evaluated

#### Value Investing Metrics:
- Price-to-Earnings (P/E) Ratio
- Price-to-Book (P/B) Ratio
- Price-to-Sales (P/S) Ratio
- Debt-to-Equity Ratio
- Return on Equity (ROE)
- Current Ratio
- Dividend Yield
- Profit Margin
- PEG Ratio

#### Growth & Momentum Metrics:
- Revenue Growth Rate
- Earnings Growth Rate
- 6-Month Price Performance
- 1-Year Price Performance
- EPS Growth Rate
- Gross Margin
- Operating Margin
- Relative Strength vs. Market
- Analyst Recommendations
- P/E to Growth Score

Each metric includes detailed explanations of what it means, how to interpret it, and what ranges are considered ideal for different investment approaches.

## Project Structure

```
stock_analyzer/
│
├── stock_analyzer/            # Main package
│   ├── analyzer.py            # Core analyzer class
│   ├── models/                # Data models
│   │   ├── stock_data.py      # Stock data models
│   │   └── report.py          # Report models
│   ├── utils/                 # Utility functions
│   │   ├── fetch_utils.py     # Data fetching utilities
│   │   └── display_utils.py   # Display utilities
│   └── criteria/              # Investment criteria
│       ├── value_criteria.py  # Value investing criteria
│       └── growth_criteria.py # Growth investing criteria
│
├── examples/                  # Example usage scripts
│   ├── single_stock.py        # Single stock analysis example
│   ├── multiple_stocks.py     # Multiple stocks analysis
│   └── dual_analysis.py       # Dual analysis example
│
├── notebooks/                 # Jupyter notebooks
│   └── getting_started.ipynb  # Getting started notebook
│
├── getting_started.py         # Interactive tutorial script
├── setup.py                   # Package setup file
├── requirements.txt           # Dependencies
└── README.md                  # This file
```

## Troubleshooting

If you encounter issues:

1. **Data Retrieval Problems**: 
   The package relies on yfinance for data, which occasionally has connectivity issues. Try running the analysis again after a few minutes.

2. **ImportError**: 
   Make sure all dependencies are installed with `pip install -r requirements.txt`

3. **Stock Not Found**: 
   Verify the ticker symbol is correct and the stock is publicly traded.

4. **Missing Ratios**: 
   Some companies may not have all financial data available, resulting in N/A values for certain ratios.

5. **Visualization Issues**:
   Ensure matplotlib and pandas are properly installed. Run `pip install matplotlib pandas` if needed.

## Contributing

Contributions are welcome! Here's how you can contribute:

1. **Fork the repository**
2. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Commit your changes**:
   ```bash
   git commit -m 'Add some feature'
   ```
4. **Push to the branch**:
   ```bash
   git push origin feature/your-feature-name
   ```
5. **Open a pull request**

Please make sure your code follows the existing style and includes appropriate tests.

### Areas for Contribution
- Additional financial metrics or ratios
- Enhanced visualization capabilities
- Integration with additional data sources
- Industry-specific analysis modules
- Backtesting capabilities
- Improved documentation and examples

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [yfinance](https://github.com/ranaroussi/yfinance) for providing stock data
- Inspired by value investing principles from Benjamin Graham and Warren Buffett
- Growth and momentum concepts from William O'Neil's CANSLIM methodology

---

If you find Stock Analyzer useful, please give it a star on GitHub! For questions, issues, or suggestions, please open an issue on the GitHub repository.
