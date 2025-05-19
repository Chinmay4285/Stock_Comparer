"""
Criteria package for stock analyzer.
"""

from stock_analyzer.criteria.value_criteria import VALUE_CRITERIA, VALUE_DESCRIPTIONS
from stock_analyzer.criteria.growth_criteria import GROWTH_MOMENTUM_CRITERIA, GROWTH_MOMENTUM_DESCRIPTIONS

__all__ = [
    'VALUE_CRITERIA', 
    'VALUE_DESCRIPTIONS',
    'GROWTH_MOMENTUM_CRITERIA', 
    'GROWTH_MOMENTUM_DESCRIPTIONS'
]
