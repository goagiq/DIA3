"""
Monte Carlo Configuration
Configuration settings for Monte Carlo simulation engine
"""

from typing import List, Dict, Any
from dataclasses import dataclass
from enum import Enum


class DistributionType(Enum):
    """Supported probability distribution types"""
    NORMAL = "normal"
    LOGNORMAL = "lognormal"
    UNIFORM = "uniform"
    EXPONENTIAL = "exponential"
    GAMMA = "gamma"
    BETA = "beta"
    WEIBULL = "weibull"
    POISSON = "poisson"


class SecurityLevel(Enum):
    """Data classification levels"""
    UNCLASSIFIED = "UNCLASSIFIED"
    CONFIDENTIAL = "CONFIDENTIAL"
    SECRET = "SECRET"
    TOP_SECRET = "TOP_SECRET"


@dataclass
class MonteCarloConfig:
    """Configuration for Monte Carlo simulation engine"""
    
    # Performance settings
    max_workers: int = 8
    use_gpu: bool = False
    cache_results: bool = False  # Disable caching by default to avoid Redis dependency
    memory_limit_gb: float = 4.0
    
    # Simulation settings
    default_iterations: int = 10000
    confidence_level: float = 0.95
    seed: int = 42
    
    # Distribution settings
    supported_distributions: List[str] = None
    
    # Security settings (DoD/IC specific)
    enable_encryption: bool = True
    audit_logging: bool = True
    data_classification: str = "UNCLASSIFIED"
    access_control: bool = True
    
    # Time series settings
    time_series_support: bool = True
    max_time_steps: int = 1000
    
    def __post_init__(self):
        if self.supported_distributions is None:
            self.supported_distributions = [
                "normal", "lognormal", "uniform", "exponential", "gamma"
            ]


@dataclass
class DoDICConfig:
    """DoD/IC specific configuration"""
    
    # Security requirements
    encryption_level: str = "AES-256"
    authentication_method: str = "PKI"
    audit_retention_days: int = 365
    
    # Data handling
    data_marking: bool = True
    classification_levels: List[str] = None
    
    # Compliance
    nist_compliance: bool = True
    fisma_compliance: bool = True
    dod_cloud_requirements: bool = True
    
    def __post_init__(self):
        if self.classification_levels is None:
            self.classification_levels = [
                "UNCLASSIFIED", "CONFIDENTIAL", "SECRET", "TOP_SECRET"
            ]


@dataclass
class SimulationConfig:
    """Configuration for individual simulations"""
    
    # Simulation parameters
    num_iterations: int
    confidence_level: float = 0.95
    seed: int = None
    
    # Distribution parameters
    distributions: Dict[str, Dict[str, Any]] = None
    
    # Correlation settings
    correlation_matrix: List[List[float]] = None
    use_copula: bool = False
    copula_type: str = "gaussian"
    
    # Output settings
    include_statistics: bool = True
    include_risk_metrics: bool = True
    include_visualizations: bool = True
    
    def __post_init__(self):
        if self.distributions is None:
            self.distributions = {}
        if self.correlation_matrix is None:
            self.correlation_matrix = []
