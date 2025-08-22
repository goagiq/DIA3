#!/usr/bin/env python3
"""
Source Tracking Module

This module provides comprehensive source tracking capabilities for data points,
calculations, and analysis results. It includes data structures for tracking
source references, calculation steps, and generating tooltips.
"""

import json
import os
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Any, Union
from pathlib import Path


@dataclass
class SourceReference:
    """Represents a source reference for data or calculations."""
    source_type: str  # 'file', 'api', 'calculation', 'model', 'external'
    source_path: str  # File path, API endpoint, or identifier
    line_number: Optional[int] = None  # Line number in file
    function_name: Optional[str] = None  # Function or method name
    timestamp: Optional[str] = None  # When the source was accessed
    confidence: Optional[float] = None  # Confidence score (0-1)
    metadata: Optional[Dict[str, Any]] = None  # Additional metadata


@dataclass
class CalculationStep:
    """Represents a step in a calculation or analysis."""
    step_name: str
    formula: Optional[str] = None  # Mathematical formula or algorithm
    input_data: Optional[Dict[str, Any]] = None  # Input data for this step
    output_data: Optional[Dict[str, Any]] = None  # Output data from this step
    parameters: Optional[Dict[str, Any]] = None  # Parameters used
    timestamp: Optional[str] = None  # When calculation was performed
    execution_time: Optional[float] = None  # Execution time in seconds


@dataclass
class DataPoint:
    """Represents a data point with source tracking and tooltip information."""
    value: Any
    label: str
    description: Optional[str] = None
    source_references: List[SourceReference] = None
    calculation_steps: List[CalculationStep] = None
    confidence: Optional[float] = None
    uncertainty: Optional[float] = None
    timestamp: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.source_references is None:
            self.source_references = []
        if self.calculation_steps is None:
            self.calculation_steps = []
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()


class SourceTracker:
    """Main class for tracking sources and generating tooltips."""
    
    def __init__(self, session_id: Optional[str] = None):
        self.session_id = session_id or f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.source_references: List[SourceReference] = []
        self.calculation_steps: List[CalculationStep] = []
        self.data_points: List[DataPoint] = []
        self.session_data: Dict[str, Any] = {
            "session_id": self.session_id,
            "start_time": datetime.now().isoformat(),
            "source_references": [],
            "calculation_steps": [],
            "data_points": []
        }
    
    def add_source_reference(self, source_ref: SourceReference) -> str:
        """Add a source reference and return its ID."""
        self.source_references.append(source_ref)
        self.session_data["source_references"].append(asdict(source_ref))
        return f"src_{len(self.source_references)}"
    
    def add_calculation_step(self, calc_step: CalculationStep) -> str:
        """Add a calculation step and return its ID."""
        self.calculation_steps.append(calc_step)
        self.session_data["calculation_steps"].append(asdict(calc_step))
        return f"calc_{len(self.calculation_steps)}"
    
    def create_data_point(self, value: Any, label: str, **kwargs) -> DataPoint:
        """Create a data point with tracking information."""
        data_point = DataPoint(value=value, label=label, **kwargs)
        self.data_points.append(data_point)
        self.session_data["data_points"].append(asdict(data_point))
        return data_point
    
    def _generate_tooltip_content(self, data_point: DataPoint) -> str:
        """Generate tooltip content for a data point."""
        tooltip_parts = []
        
        # Add description
        if data_point.description:
            tooltip_parts.append(f"<strong>Description:</strong> {data_point.description}")
        
        # Add source references
        if data_point.source_references:
            tooltip_parts.append("<strong>Sources:</strong>")
            for i, ref in enumerate(data_point.source_references, 1):
                source_info = f"  {i}. {ref.source_type}: {ref.source_path}"
                if ref.line_number:
                    source_info += f" (line {ref.line_number})"
                if ref.confidence:
                    source_info += f" (confidence: {ref.confidence:.2f})"
                tooltip_parts.append(source_info)
        
        # Add calculation steps
        if data_point.calculation_steps:
            tooltip_parts.append("<strong>Calculations:</strong>")
            for i, step in enumerate(data_point.calculation_steps, 1):
                calc_info = f"  {i}. {step.step_name}"
                if step.formula:
                    calc_info += f" (formula: {step.formula})"
                tooltip_parts.append(calc_info)
        
        # Add confidence and uncertainty
        if data_point.confidence is not None:
            tooltip_parts.append(f"<strong>Confidence:</strong> {data_point.confidence:.2f}")
        if data_point.uncertainty is not None:
            tooltip_parts.append(f"<strong>Uncertainty:</strong> {data_point.uncertainty:.2f}")
        
        # Add timestamp
        if data_point.timestamp:
            tooltip_parts.append(f"<strong>Generated:</strong> {data_point.timestamp}")
        
        return "<br>".join(tooltip_parts)
    
    def generate_source_report(self) -> Dict[str, Any]:
        """Generate a comprehensive source report."""
        return {
            "session_id": self.session_id,
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_sources": len(self.source_references),
                "total_calculations": len(self.calculation_steps),
                "total_data_points": len(self.data_points)
            },
            "source_references": [asdict(ref) for ref in self.source_references],
            "calculation_steps": [asdict(step) for step in self.calculation_steps],
            "data_points": [asdict(dp) for dp in self.data_points]
        }
    
    def save_session_data(self, filepath: Optional[str] = None) -> str:
        """Save session data to a JSON file."""
        if filepath is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filepath = f"Results/source_tracking_{self.session_id}_{timestamp}.json"
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.session_data, f, indent=2, default=str)
        
        return filepath
    
    def export_tooltip_data(self) -> Dict[str, str]:
        """Export tooltip data for all data points."""
        tooltip_data = {}
        for dp in self.data_points:
            tooltip_data[dp.label] = self._generate_tooltip_content(dp)
        return tooltip_data


# Global source tracker instance
_global_source_tracker: Optional[SourceTracker] = None


def get_source_tracker() -> SourceTracker:
    """Get or create the global source tracker instance."""
    global _global_source_tracker
    if _global_source_tracker is None:
        _global_source_tracker = SourceTracker()
    return _global_source_tracker


def track_source(source_type: str, source_path: str, **kwargs) -> SourceReference:
    """Track a source reference."""
    tracker = get_source_tracker()
    source_ref = SourceReference(
        source_type=source_type,
        source_path=source_path,
        timestamp=datetime.now().isoformat(),
        **kwargs
    )
    tracker.add_source_reference(source_ref)
    return source_ref


def track_calculation(step_name: str, **kwargs) -> CalculationStep:
    """Track a calculation step."""
    tracker = get_source_tracker()
    calc_step = CalculationStep(
        step_name=step_name,
        timestamp=datetime.now().isoformat(),
        **kwargs
    )
    tracker.add_calculation_step(calc_step)
    return calc_step


def create_tracked_data_point(value: Any, label: str, **kwargs) -> DataPoint:
    """Create a data point with automatic tracking."""
    tracker = get_source_tracker()
    return tracker.create_data_point(value, label, **kwargs)


def reset_source_tracker():
    """Reset the global source tracker."""
    global _global_source_tracker
    _global_source_tracker = None
