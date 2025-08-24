"""
Modular Report System

This package contains modular components for generating enhanced reports.
Each module is independent and configurable, allowing for flexible report generation.
"""

from .base_module import BaseModule
from .strategic_recommendations_module import StrategicRecommendationsModule
from .executive_summary_module import ExecutiveSummaryModule

__all__ = [
    'BaseModule',
    'StrategicRecommendationsModule',
    'ExecutiveSummaryModule'
]
