"""
Display utilities for stock analyzer.
"""

from IPython.display import display, HTML, Markdown
from typing import Union, Dict
from datetime import datetime

from stock_analyzer.models.report import StockReport
from stock_analyzer.criteria.value_criteria import VALUE_DESCRIPTIONS, VALUE_CRITERIA
from stock_analyzer.criteria.growth_criteria import GROWTH_MOMENTUM_DESCRIPTIONS, GROWTH_MOMENTUM_CRITERIA


def print_report(report: Union[StockReport, str]) -> str:
    """
    Pretty print the stock analysis report with enhanced visuals.
    
    This function takes a StockReport object and generates a rich HTML
    visualization of the report, with color-coding, formatted tables,
    and detailed explanations.
    
    Args:
        report (Union[StockReport, str]): Report object or error message
        
    Returns:
        str: HTML content of the report
    """
    if isinstance(report, str):
        print(report)
        return report
            
    # Determine analysis type
    analysis_type = report.analysis_type
    
    # Create a colorful header - blue for value, purple for growth+momentum
    header_color = "#0066cc" if analysis_type == 'value' else "#8A2BE2"
    
    header = f"""
<div style="background-color:{header_color}; color:white; padding:15px; border-radius:10px; margin:10px 0;">
    <h1 style="text-align:center;">{report.company_name} ({report.ticker})</h1>
    <h2 style="text-align:center;">{analysis_type.replace('_', ' & ').title()} Analysis</h2>
    <h3 style="text-align:center;">Current Price: {report.current_price} {report.currency}</h3>
    <h3 style="text-align:center;">Analysis Time: {report.timestamp}</h3>
</div>
"""
    
    # Classification section with appropriate color
    if "GREAT" in report.classification:
        bgcolor = "#4CAF50"  # Green
    elif "GOOD" in report.classification:
        bgcolor = "#2196F3"  # Blue
    else:
        bgcolor = "#F44336"  # Red
        
    classification_html = f"""
<div style="background-color:{bgcolor}; color:white; padding:10px; border-radius:10px; margin:10px 0; text-align:center;">
    <h2>INVESTMENT CLASSIFICATION: {report.classification}</h2>
</div>
"""
    
    # Ratios table
    ratios_data = []
    
    # Get the appropriate criteria dictionaries based on analysis type
    from stock_analyzer.criteria.value_criteria import VALUE_DESCRIPTIONS
    from stock_analyzer.criteria.growth_criteria import GROWTH_MOMENTUM_DESCRIPTIONS
    
    value_descriptions = VALUE_DESCRIPTIONS
    growth_momentum_descriptions = GROWTH_MOMENTUM_DESCRIPTIONS
    
    for ratio_name, ratio_value in report.ratios.items():
        if ratio_value is not None and ratio_name in report.rating_details:
            rating = report.rating_details.get(ratio_name, 'N/A')
            
            # Color for rating
            if rating == 'great':
                color = 'green'
            elif rating == 'good':
                color = 'blue'
            else:  # no_buy
                color = 'red'
            
            # Get ratio info from the appropriate description dictionary
            if analysis_type == 'value':
                ratio_info = value_descriptions.get(ratio_name, {'name': ratio_name.replace('_', ' ').title()})
            else:  # growth_momentum
                ratio_info = growth_momentum_descriptions.get(ratio_name, {'name': ratio_name.replace('_', ' ').title()})
            
            ratios_data.append([
                ratio_info.get('name', ratio_name.replace('_', ' ').title()), 
                f"{ratio_value:.2f}" if isinstance(ratio_value, (int, float)) else ratio_value,
                f"<span style='color:{color};'>{rating.upper()}</span>"
            ])
            
    # Create ratios table HTML
    table_html = f"<h2>{analysis_type.replace('_', ' & ').upper()} FINANCIAL RATIOS:</h2>"
    table_html += "<table border='1' style='width:100%; border-collapse:collapse;'>"
    table_html += "<tr style='background-color:#f2f2f2;'><th>Ratio</th><th>Value</th><th>Rating</th></tr>"
    
    for row in ratios_data:
        table_html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td></tr>"
        
    table_html += "</table>"
    
    # Summary statistics
    great_count = report.great_count
    good_count = report.good_count
    no_buy_count = report.no_buy_count
    total = report.total_rated
    
    summary_html = "<h2>SUMMARY:</h2>"
    summary_html += "<div style='padding:10px; background-color:#f9f9f9; border-radius:5px;'>"
    
    if total > 0:
        summary_html += f"<p>• <span style='color:green;'>Great indicators</span>: {great_count}/{total} ({great_count/total*100:.1f}%)</p>"
        summary_html += f"<p>• <span style='color:blue;'>Good indicators</span>: {good_count}/{total} ({good_count/total*100:.1f}%)</p>"
        summary_html += f"<p>• <span style='color:red;'>Poor indicators</span>: {no_buy_count}/{total} ({no_buy_count/total*100:.1f}%)</p>"
    
    summary_html += f"<p><b>{report.summary}</b></p>"
    summary_html += "</div>"
    
    # Ratio explanations section
    explanations_html = "<h2>RATIO ANALYSIS:</h2>"
    explanations_html += "<div style='padding:10px; background-color:#f9f9f9; border-radius:5px;'>"
    
    for ratio_name, explanation in report.ratio_explanations.items():
        rating = report.rating_details.get(ratio_name, 'N/A')
        if rating == 'great':
            color = 'green'
        elif rating == 'good':
            color = 'blue' 
        else:
            color = 'red'
            
        # Get detailed information about the ratio
        ratio_info = None
        if analysis_type == 'value':
            ratio_info = value_descriptions.get(ratio_name, {})
        else:  # growth_momentum
            ratio_info = growth_momentum_descriptions.get(ratio_name, {})
            
        # Create a more detailed explanation with ratio information
        if ratio_info:
            # Start with the colored rating explanation
            explanations_html += f"<div style='margin-bottom:15px; border-left:4px solid {color}; padding-left:10px;'>"
            explanations_html += f"<p style='color:{color}; font-weight:bold;'>• {explanation}</p>"
            
            # Add more educational content
            explanations_html += f"<div style='margin-left:20px; font-size:0.9em;'>"
            explanations_html += f"<p><strong>What it means:</strong> {ratio_info.get('description', 'No description available.')}</p>"
            
            explanations_html += f"<p><strong>How to interpret:</strong> {ratio_info.get('interpretation', 'No interpretation available.')}</p>"
            
            # Add ideal range information
            ideal_key = 'value_stock_ideal' if analysis_type == 'value' else 'growth_stock_ideal'
            explanations_html += f"<p><strong>Ideal range for {analysis_type.replace('_', '/')} investing:</strong> {ratio_info.get(ideal_key, 'No ideal range specified.')}</p>"
            
            # Add criteria information
            criteria = None
            if analysis_type == 'value' and ratio_name in VALUE_CRITERIA:
                criteria = VALUE_CRITERIA[ratio_name]
            elif analysis_type == 'growth_momentum' and ratio_name in GROWTH_MOMENTUM_CRITERIA:
                criteria = GROWTH_MOMENTUM_CRITERIA[ratio_name]
            
            if criteria:
                explanations_html += "<p><strong>Rating criteria:</strong></p>"
                explanations_html += "<ul>"
                for rating_name, (min_val, max_val) in criteria.items():
                    min_str = f"{min_val:.2f}" if min_val != float('-inf') else "-∞"
                    max_str = f"{max_val:.2f}" if max_val != float('inf') else "∞"
                    rating_color = "green" if rating_name == "great" else "blue" if rating_name == "good" else "red"
                    explanations_html += f"<li><span style='color:{rating_color};'>{rating_name.upper()}</span>: {min_str} to {max_str}</li>"
                explanations_html += "</ul>"
            
            explanations_html += "</div></div>"
        else:
            # Fallback if no detailed info is available
            explanations_html += f"<p><span style='color:{color};'>• {explanation}</span></p>"
            
    explanations_html += "</div>"
    
    # Combine all HTML sections
    full_html = header + classification_html + table_html + summary_html + explanations_html
    
    # Display in Jupyter
    display(HTML(full_html))
    
    # Return HTML for potential saving
    return full_html


def save_report_html(report: StockReport, filename: str = None) -> str:
    """
    Save a report as an HTML file.
    
    Args:
        report (StockReport): Report to save
        filename (str, optional): Filename to save to. If None, one will be generated.
        
    Returns:
        str: Path to the saved file
    """
    if filename is None:
        filename = f"{report.ticker}_{report.analysis_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        
    if not filename.endswith('.html'):
        filename += '.html'
        
    html_content = print_report(report)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Stock Analysis: {report.ticker} - {report.analysis_type.title()}</title>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """)
    
    print(f"Report saved to {filename}")
    return filename


def generate_comparison_markdown(comparison_data: Dict, title: str) -> str:
    """
    Generate a markdown-formatted comparison table.
    
    Args:
        comparison_data (Dict): Comparison data
        title (str): Title for the comparison
        
    Returns:
        str: Markdown-formatted comparison
    """
    markdown_text = f"## {title}\n\n"
    
    # Add comparison table
    if 'table' in comparison_data:
        markdown_text += comparison_data['table']
        markdown_text += "\n\n"
    
    # Display as Markdown
    display(Markdown(markdown_text))
    
    return markdown_text
