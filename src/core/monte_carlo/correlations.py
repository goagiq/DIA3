"""
Correlation Engine
Handle correlated variables in Monte Carlo simulations
"""

import numpy as np
from typing import List, Optional, Tuple
from scipy import stats
import logging

logger = logging.getLogger(__name__)


class CorrelationEngine:
    """Engine for handling correlated variables in Monte Carlo simulations"""
    
    def __init__(self):
        self.supported_copulas = ["gaussian", "student_t"]
    
    def generate_correlated_samples(self, 
                                  distributions: List[str],
                                  params: List[dict],
                                  correlation_matrix: List[List[float]],
                                  size: int = 1000,
                                  copula_type: str = "gaussian") -> np.ndarray:
        """Generate correlated samples using copula method"""
        
        if len(distributions) != len(params):
            raise ValueError("Number of distributions must match number of parameter sets")
        
        if len(distributions) != len(correlation_matrix):
            raise ValueError("Number of distributions must match correlation matrix size")
        
        # Validate correlation matrix
        if not self._is_valid_correlation_matrix(correlation_matrix):
            raise ValueError("Invalid correlation matrix")
        
        # Generate correlated uniform samples using copula
        uniform_samples = self._generate_correlated_uniform(
            correlation_matrix, size, copula_type
        )
        
        # Transform uniform samples to desired distributions
        correlated_samples = np.zeros((size, len(distributions)))
        
        for i, (dist_type, dist_params) in enumerate(zip(distributions, params)):
            correlated_samples[:, i] = self._transform_uniform_to_distribution(
                uniform_samples[:, i], dist_type, dist_params
            )
        
        return correlated_samples
    
    def _is_valid_correlation_matrix(self, matrix: List[List[float]]) -> bool:
        """Validate correlation matrix"""
        matrix = np.array(matrix)
        
        # Check if matrix is square
        if matrix.shape[0] != matrix.shape[1]:
            return False
        
        # Check if diagonal elements are 1
        if not np.allclose(np.diag(matrix), 1.0):
            return False
        
        # Check if matrix is symmetric
        if not np.allclose(matrix, matrix.T):
            return False
        
        # Check if matrix is positive semi-definite
        try:
            np.linalg.cholesky(matrix)
            return True
        except np.linalg.LinAlgError:
            return False
    
    def _generate_correlated_uniform(self, 
                                   correlation_matrix: List[List[float]],
                                   size: int,
                                   copula_type: str = "gaussian") -> np.ndarray:
        """Generate correlated uniform samples using copula"""
        
        if copula_type not in self.supported_copulas:
            raise ValueError(f"Unsupported copula type: {copula_type}")
        
        if copula_type == "gaussian":
            return self._gaussian_copula(correlation_matrix, size)
        elif copula_type == "student_t":
            return self._student_t_copula(correlation_matrix, size, df=5)
    
    def _gaussian_copula(self, correlation_matrix: List[List[float]], 
                        size: int) -> np.ndarray:
        """Generate samples using Gaussian copula"""
        
        # Generate correlated normal samples
        correlation_matrix = np.array(correlation_matrix)
        normal_samples = np.random.multivariate_normal(
            mean=np.zeros(len(correlation_matrix)),
            cov=correlation_matrix,
            size=size
        )
        
        # Transform to uniform using normal CDF
        uniform_samples = stats.norm.cdf(normal_samples)
        
        return uniform_samples
    
    def _student_t_copula(self, correlation_matrix: List[List[float]], 
                         size: int, df: int = 5) -> np.ndarray:
        """Generate samples using Student-t copula"""
        
        # Generate correlated t-distributed samples
        correlation_matrix = np.array(correlation_matrix)
        t_samples = np.random.multivariate_t(
            loc=np.zeros(len(correlation_matrix)),
            shape=correlation_matrix,
            df=df,
            size=size
        )
        
        # Transform to uniform using t CDF
        uniform_samples = stats.t.cdf(t_samples, df=df)
        
        return uniform_samples
    
    def _transform_uniform_to_distribution(self, 
                                         uniform_samples: np.ndarray,
                                         distribution_type: str,
                                         params: dict) -> np.ndarray:
        """Transform uniform samples to desired distribution using inverse CDF"""
        
        if distribution_type == "normal":
            return stats.norm.ppf(uniform_samples, 
                                loc=params.get("mean", 0), 
                                scale=params.get("std", 1))
        
        elif distribution_type == "lognormal":
            return stats.lognorm.ppf(uniform_samples, 
                                   s=params.get("std", 1),
                                   scale=np.exp(params.get("mean", 0)))
        
        elif distribution_type == "uniform":
            return stats.uniform.ppf(uniform_samples,
                                   loc=params.get("low", 0),
                                   scale=params.get("high", 1) - params.get("low", 0))
        
        elif distribution_type == "exponential":
            return stats.expon.ppf(uniform_samples,
                                 scale=params.get("scale", 1))
        
        elif distribution_type == "gamma":
            return stats.gamma.ppf(uniform_samples,
                                 a=params.get("shape", 1),
                                 scale=params.get("scale", 1))
        
        elif distribution_type == "beta":
            return stats.beta.ppf(uniform_samples,
                                a=params.get("alpha", 1),
                                b=params.get("beta", 1))
        
        elif distribution_type == "weibull":
            return stats.weibull_min.ppf(uniform_samples,
                                       c=params.get("shape", 1),
                                       scale=params.get("scale", 1))
        
        elif distribution_type == "poisson":
            # Poisson is discrete, so we need a different approach
            # For now, use exponential as approximation
            return stats.expon.ppf(uniform_samples,
                                 scale=params.get("lambda", 1))
        
        else:
            # For other distributions, use scipy's generic method
            dist = getattr(stats, distribution_type)
            return dist.ppf(uniform_samples, **params)
    
    def estimate_correlation_matrix(self, samples: np.ndarray) -> np.ndarray:
        """Estimate correlation matrix from samples"""
        return np.corrcoef(samples.T)
    
    def test_correlation_significance(self, 
                                    samples: np.ndarray,
                                    alpha: float = 0.05) -> Tuple[np.ndarray, np.ndarray]:
        """Test significance of correlations"""
        
        n = samples.shape[0]
        p = samples.shape[1]
        
        # Calculate correlation matrix
        corr_matrix = np.corrcoef(samples.T)
        
        # Calculate t-statistics
        t_stats = corr_matrix * np.sqrt((n - 2) / (1 - corr_matrix**2))
        
        # Calculate p-values (two-tailed test)
        p_values = 2 * (1 - stats.t.cdf(np.abs(t_stats), df=n-2))
        
        # Create significance matrix
        significance_matrix = p_values < alpha
        
        return corr_matrix, significance_matrix
    
    def generate_correlation_matrix(self, 
                                  size: int,
                                  method: str = "random",
                                  **kwargs) -> np.ndarray:
        """Generate a valid correlation matrix"""
        
        if method == "random":
            return self._generate_random_correlation_matrix(size, **kwargs)
        elif method == "toeplitz":
            return self._generate_toeplitz_correlation_matrix(size, **kwargs)
        else:
            raise ValueError(f"Unknown method: {method}")
    
    def _generate_random_correlation_matrix(self, 
                                          size: int,
                                          min_corr: float = -0.8,
                                          max_corr: float = 0.8) -> np.ndarray:
        """Generate a random valid correlation matrix"""
        
        # Generate random matrix
        A = np.random.uniform(min_corr, max_corr, (size, size))
        
        # Make it symmetric
        A = (A + A.T) / 2
        
        # Set diagonal to 1
        np.fill_diagonal(A, 1.0)
        
        # Make it positive semi-definite
        eigenvals, eigenvecs = np.linalg.eigh(A)
        eigenvals = np.maximum(eigenvals, 0.01)  # Ensure positive eigenvalues
        
        A = eigenvecs @ np.diag(eigenvals) @ eigenvecs.T
        
        # Normalize to get correlation matrix
        D = np.sqrt(np.diag(A))
        A = A / np.outer(D, D)
        
        return A
    
    def _generate_toeplitz_correlation_matrix(self, 
                                            size: int,
                                            rho: float = 0.5) -> np.ndarray:
        """Generate a Toeplitz correlation matrix"""
        
        A = np.zeros((size, size))
        for i in range(size):
            for j in range(size):
                A[i, j] = rho ** abs(i - j)
        
        return A
