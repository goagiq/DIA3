"""
Progress Tracker

Provides async progress tracking for export operations with detailed status updates.
"""

import asyncio
from datetime import datetime
from typing import Dict, Any, Optional, Callable, List
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class ExportStage(Enum):
    """Export operation stages."""
    INITIALIZING = "initializing"
    PARSING_MARKDOWN = "parsing_markdown"
    CONVERTING_DIAGRAMS = "converting_diagrams"
    PROCESSING_IMAGES = "processing_images"
    GENERATING_PDF = "generating_pdf"
    GENERATING_WORD = "generating_word"
    FINALIZING = "finalizing"
    COMPLETED = "completed"
    FAILED = "failed"


class ProgressTracker:
    """Tracks progress of async export operations."""
    
    def __init__(self, operation_id: str):
        """Initialize progress tracker.
        
        Args:
            operation_id: Unique identifier for the operation
        """
        self.operation_id = operation_id
        self.start_time = datetime.now()
        self.current_stage = ExportStage.INITIALIZING
        self.progress_percentage = 0.0
        self.stage_progress = 0.0
        self.messages: List[str] = []
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.metadata: Dict[str, Any] = {}
        self._cancelled = False
        self._callbacks: List[Callable] = []
        
    def add_callback(self, callback: Callable):
        """Add a progress callback function.
        
        Args:
            callback: Function to call with progress updates
        """
        self._callbacks.append(callback)
    
    def update_progress(self, 
                       stage: ExportStage, 
                       percentage: float, 
                       message: str = "",
                       metadata: Optional[Dict[str, Any]] = None):
        """Update progress for current stage.
        
        Args:
            stage: Current export stage
            percentage: Progress percentage (0-100)
            message: Status message
            metadata: Additional metadata
        """
        if self._cancelled:
            return
            
        self.current_stage = stage
        self.stage_progress = max(0.0, min(100.0, percentage))
        
        # Calculate overall progress based on stage weights
        stage_weights = {
            ExportStage.INITIALIZING: 5,
            ExportStage.PARSING_MARKDOWN: 15,
            ExportStage.CONVERTING_DIAGRAMS: 20,
            ExportStage.PROCESSING_IMAGES: 15,
            ExportStage.GENERATING_PDF: 25,
            ExportStage.GENERATING_WORD: 25,
            ExportStage.FINALIZING: 10,
            ExportStage.COMPLETED: 100,
            ExportStage.FAILED: 100
        }
        
        # Calculate overall progress
        total_weight = sum(stage_weights.values())
        completed_weight = 0
        
        for s in ExportStage:
            if s == stage:
                completed_weight += stage_weights[s] * (percentage / 100.0)
                break
            elif s != ExportStage.COMPLETED and s != ExportStage.FAILED:
                completed_weight += stage_weights[s]
        
        self.progress_percentage = (completed_weight / total_weight) * 100
        
        if message:
            # Handle both enum and numeric stage values
            stage_name = stage.value if hasattr(stage, 'value') else str(stage)
            self.messages.append(f"[{stage_name}] {message}")
            logger.info(f"Progress {self.operation_id}: {message}")
        
        if metadata:
            self.metadata.update(metadata)
        
        # Notify callbacks
        self._notify_callbacks()
    
    def add_error(self, error: str):
        """Add an error message.
        
        Args:
            error: Error message
        """
        self.errors.append(error)
        logger.error(f"Export error {self.operation_id}: {error}")
        self._notify_callbacks()
    
    def add_warning(self, warning: str):
        """Add a warning message.
        
        Args:
            warning: Warning message
        """
        self.warnings.append(warning)
        logger.warning(f"Export warning {self.operation_id}: {warning}")
        self._notify_callbacks()
    
    def complete(self, success: bool = True):
        """Mark operation as completed.
        
        Args:
            success: Whether operation was successful
        """
        if success:
            self.current_stage = ExportStage.COMPLETED
            self.progress_percentage = 100.0
            self.update_progress(ExportStage.COMPLETED, 100, "Export completed successfully")
        else:
            self.current_stage = ExportStage.FAILED
            self.update_progress(ExportStage.FAILED, 100, "Export failed")
    
    def cancel(self):
        """Cancel the operation."""
        self._cancelled = True
        logger.info(f"Export cancelled {self.operation_id}")
        self._notify_callbacks()
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status.
        
        Returns:
            Status dictionary
        """
        return {
            "operation_id": self.operation_id,
            "current_stage": self.current_stage.value if hasattr(self.current_stage, 'value') else str(self.current_stage),
            "progress_percentage": self.progress_percentage,
            "stage_progress": self.stage_progress,
            "start_time": self.start_time.isoformat(),
            "elapsed_time": (datetime.now() - self.start_time).total_seconds(),
            "messages": self.messages[-10:],  # Last 10 messages
            "errors": self.errors,
            "warnings": self.warnings,
            "metadata": self.metadata,
            "cancelled": self._cancelled
        }
    
    def _notify_callbacks(self):
        """Notify all registered callbacks."""
        status = self.get_status()
        for callback in self._callbacks:
            try:
                callback(status)
            except Exception as e:
                logger.error(f"Error in progress callback: {e}")


class ProgressManager:
    """Manages multiple progress trackers."""
    
    def __init__(self):
        """Initialize progress manager."""
        self.trackers: Dict[str, ProgressTracker] = {}
    
    def create_tracker(self, operation_id: str) -> ProgressTracker:
        """Create a new progress tracker.
        
        Args:
            operation_id: Unique operation identifier
            
        Returns:
            Progress tracker instance
        """
        tracker = ProgressTracker(operation_id)
        self.trackers[operation_id] = tracker
        return tracker
    
    def get_tracker(self, operation_id: str) -> Optional[ProgressTracker]:
        """Get a progress tracker by ID.
        
        Args:
            operation_id: Operation identifier
            
        Returns:
            Progress tracker or None if not found
        """
        return self.trackers.get(operation_id)
    
    def remove_tracker(self, operation_id: str):
        """Remove a progress tracker.
        
        Args:
            operation_id: Operation identifier
        """
        if operation_id in self.trackers:
            del self.trackers[operation_id]
    
    def get_all_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all trackers.
        
        Returns:
            Dictionary of tracker statuses
        """
        return {
            op_id: tracker.get_status() 
            for op_id, tracker in self.trackers.items()
        }
