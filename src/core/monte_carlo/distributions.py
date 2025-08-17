"""
Distribution Library
Common probability distributions for Monte Carlo simulations
"""

import numpy as np
from typing import Dict, Any, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class DistributionLibrary:
    """Library of probability distributions for Monte Carlo simulations"""
    
    def __init__(self):
        self.supported_distributions = {
            "normal": self._normal_distribution,
            "lognormal": self._lognormal_distribution,
            "uniform": self._uniform_distribution,
            "exponential": self._exponential_distribution,
            "gamma": self._gamma_distribution,
            "beta": self._beta_distribution,
            "weibull": self._weibull_distribution,
            "poisson": self._poisson_distribution
        }
    
    def sample(self, distribution_type: str, params: Dict[str, Any], 
               size: int = 1) -> np.ndarray:
        """Sample from a probability distribution"""
        if distribution_type not in self.supported_distributions:
            raise ValueError(f"Unsupported distribution: {distribution_type}")
        
        try:
            return self.supported_distributions[distribution_type](params, size)
        except Exception as e:
            logger.error(f"Error sampling from {distribution_type}: {e}")
            raise
    
    def validate_params(self, distribution_type: str, params: Dict[str, Any]) -> bool:
        """Validate distribution parameters"""
        if distribution_type not in self.supported_distributions:
            return False
        
        try:
            # Test sampling with minimal size to validate parameters
            self.supported_distributions[distribution_type](params, 1)
            return True
        except Exception:
            return False
    
    def _normal_distribution(self, params: Dict[str, Any], size: int) -> np.ndarray:
        """Normal distribution sampling"""
        mean = params.get("mean", 0.0)
        std = params.get("std", 1.0)
        
        if std <= 0:
            raise ValueError("Standard deviation must be positive")
        
        return np.random.normal(mean, std, size)
    
    def _lognormal_distribution(self, params: Dict[str, Any], size: int) -> np.ndarray:
        """Log-normal distribution sampling"""
        mean = params.get("mean", 0.0)
        std = params.get("std", 1.0)
        
        if std <= 0:
            raise ValueError("Standard deviation must be positive")
        
        return np.random.lognormal(mean, std, size)
    
    def _uniform_distribution(self, params: Dict[str, Any], size: int) -> np.ndarray:
        """Uniform distribution sampling"""
        low = params.get("low", 0.0)
        high = params.get("high", 1.0)
        
        if low >= high:
            raise ValueError("Low must be less than high")
        
        return np.random.uniform(low, high, size)
    
    def _exponential_distribution(self, params: Dict[str, Any], size: int) -> np.ndarray:
        """Exponential distribution sampling"""
        scale = params.get("scale", 1.0)
        
        if scale <= 0:
            raise ValueError("Scale must be positive")
        
        return np.random.exponential(scale, size)
    
    def _gamma_distribution(self, params: Dict[str, Any], size: int) -> np.ndarray:
        """Gamma distribution sampling"""
        shape = params.get("shape", 1.0)
        scale = params.get("scale", 1.0)
        
        if shape <= 0 or scale <= 0:
            raise ValueError("Shape and scale must be positive")
        
        return np.random.gamma(shape, scale, size)
    
    def _beta_distribution(self, params: Dict[str, Any], size: int) -> np.ndarray:
        """Beta distribution sampling"""
        alpha = params.get("alpha", 1.0)
        beta = params.get("beta", 1.0)
        
        if alpha <= 0 or beta <= 0:
            raise ValueError("Alpha and beta must be positive")
        
        return np.random.beta(alpha, beta, size)
    
    def _weibull_distribution(self, params: Dict[str, Any], size: int) -> np.ndarray:
        """Weibull distribution sampling"""
        shape = params.get("shape", 1.0)
        scale = params.get("scale", 1.0)
        
        if shape <= 0 or scale <= 0:
            raise ValueError("Shape and scale must be positive")
        
        return np.random.weibull(shape, size) * scale
    
    def _poisson_distribution(self, params: Dict[str, Any], size: int) -> np.ndarray:
        """Poisson distribution sampling"""
        lambda_param = params.get("lambda", 1.0)
        
        if lambda_param <= 0:
            raise ValueError("Lambda must be positive")
        
        return np.random.poisson(lambda_param, size)
    
    def get_distribution_info(self, distribution_type: str) -> Dict[str, Any]:
        """Get information about a distribution"""
        if distribution_type not in self.supported_distributions:
            return {}
        
        info = {
            "normal": {
                "parameters": ["mean", "std"],
                "description": "Normal (Gaussian) distribution"
            },
            "lognormal": {
                "parameters": ["mean", "std"],
                "description": "Log-normal distribution"
            },
            "uniform": {
                "parameters": ["low", "high"],
                "description": "Uniform distribution"
            },
            "exponential": {
                "parameters": ["scale"],
                "description": "Exponential distribution"
            },
            "gamma": {
                "parameters": ["shape", "scale"],
                "description": "Gamma distribution"
            },
            "beta": {
                "parameters": ["alpha", "beta"],
                "description": "Beta distribution"
            },
            "weibull": {
                "parameters": ["shape", "scale"],
                "description": "Weibull distribution"
            },
            "poisson": {
                "parameters": ["lambda"],
                "description": "Poisson distribution"
            }
        }
        
        return info.get(distribution_type, {})
    
    def list_supported_distributions(self) -> list:
        """List all supported distributions"""
        return list(self.supported_distributions.keys())
