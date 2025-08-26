"""
Storage Module for Phase 2 Implementation
Provides intelligence storage, versioning, and building capabilities.
"""

from .intelligence_storage_manager import (
    IntelligenceStorageManager,
    StorageStatus,
    StorageMetrics,
    StorageOperation
)

from .version_history_manager import (
    VersionHistoryManager,
    VersionStatus,
    Version,
    DiffResult,
    VersionHistory
)

from .intelligence_builder import (
    IntelligenceBuilder,
    IntelligenceType,
    IntelligenceConfidence,
    Pattern,
    TrendAnalysis,
    Connection,
    IntelligenceScore,
    AggregatedIntelligence,
    ValidationResult
)

from .phase2_integration import (
    Phase2Integration,
    create_phase2_integration,
    perform_phase2_search
)

__all__ = [
    # Intelligence Storage Manager
    "IntelligenceStorageManager",
    "StorageStatus", 
    "StorageMetrics",
    "StorageOperation",
    
    # Version History Manager
    "VersionHistoryManager",
    "VersionStatus",
    "Version",
    "DiffResult", 
    "VersionHistory",
    
    # Intelligence Builder
    "IntelligenceBuilder",
    "IntelligenceType",
    "IntelligenceConfidence",
    "Pattern",
    "TrendAnalysis",
    "Connection",
    "IntelligenceScore",
    "AggregatedIntelligence",
    "ValidationResult",
    
    # Phase 2 Integration
    "Phase2Integration",
    "create_phase2_integration",
    "perform_phase2_search"
]
