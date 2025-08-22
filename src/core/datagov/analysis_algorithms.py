"""
Analysis Algorithms for Data.gov Integration - Phase 3
Implements advanced analysis algorithms for trend identification, correlation analysis, and anomaly detection.
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional, Tuple
import numpy as np
import pandas as pd
from scipy import stats
from scipy.signal import find_peaks
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, DBSCAN
from sklearn.ensemble import IsolationForest
from sklearn.covariance import EllipticEnvelope
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)

class AdvancedAnalysisEngine:
    """Advanced analysis engine for Data.gov data analysis."""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=0.95)  # Preserve 95% variance
        self.anomaly_detectors = {
            'isolation_forest': IsolationForest(contamination=0.1, random_state=42),
            'elliptic_envelope': EllipticEnvelope(contamination=0.1, random_state=42)
        }
        self.clustering_models = {
            'kmeans': KMeans(n_clusters=5, random_state=42),
            'dbscan': DBSCAN(eps=0.5, min_samples=5)
        }
        
    async def identify_trends(self, time_series_data: List[Dict[str, Any]], 
                            variable: str, window_size: int = 12) -> Dict[str, Any]:
        """Identify trends in time series data."""
        try:
            logger.info(f"Identifying trends for variable: {variable}")
            
            # Convert to DataFrame
            df = pd.DataFrame(time_series_data)
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
            
            if variable not in df.columns:
                return {"status": "error", "message": f"Variable {variable} not found in data"}
            
            # Calculate moving averages
            df[f'{variable}_ma'] = df[variable].rolling(window=window_size).mean()
            df[f'{variable}_ema'] = df[variable].ewm(span=window_size).mean()
            
            # Calculate trend direction
            df['trend_direction'] = np.where(df[variable] > df[f'{variable}_ma'], 'up', 'down')
            
            # Calculate trend strength using linear regression
            x = np.arange(len(df))
            y = df[variable].values
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
            
            # Calculate seasonality
            seasonal_pattern = self._detect_seasonality(df[variable].values)
            
            # Identify trend changes
            trend_changes = self._detect_trend_changes(df[variable].values)
            
            # Calculate volatility
            volatility = df[variable].rolling(window=window_size).std().mean()
            
            return {
                "status": "success",
                "variable": variable,
                "trend_analysis": {
                    "slope": float(slope),
                    "intercept": float(intercept),
                    "r_squared": float(r_value ** 2),
                    "p_value": float(p_value),
                    "trend_strength": "strong" if abs(slope) > 0.1 else "weak",
                    "trend_direction": "increasing" if slope > 0 else "decreasing"
                },
                "seasonality": seasonal_pattern,
                "trend_changes": trend_changes,
                "volatility": float(volatility),
                "moving_averages": {
                    "simple_ma": df[f'{variable}_ma'].tolist(),
                    "exponential_ma": df[f'{variable}_ema'].tolist()
                },
                "data_points": len(df),
                "analysis_period": {
                    "start": df['date'].min().isoformat(),
                    "end": df['date'].max().isoformat()
                }
            }
            
        except Exception as e:
            logger.error(f"Error identifying trends: {e}")
            return {"status": "error", "message": str(e)}
    
    async def correlation_analysis(self, data: List[Dict[str, Any]], 
                                 variables: List[str]) -> Dict[str, Any]:
        """Perform correlation analysis between variables."""
        try:
            logger.info(f"Performing correlation analysis for variables: {variables}")
            
            # Convert to DataFrame
            df = pd.DataFrame(data)
            
            # Check if all variables exist
            missing_vars = [var for var in variables if var not in df.columns]
            if missing_vars:
                return {"status": "error", "message": f"Variables not found: {missing_vars}"}
            
            # Calculate correlation matrix
            correlation_matrix = df[variables].corr()
            
            # Calculate pairwise correlations
            correlations = []
            for i, var1 in enumerate(variables):
                for j, var2 in enumerate(variables[i+1:], i+1):
                    corr_value = correlation_matrix.iloc[i, j]
                    correlations.append({
                        "variable1": var1,
                        "variable2": var2,
                        "correlation": float(corr_value),
                        "strength": self._interpret_correlation(corr_value),
                        "significance": self._calculate_significance(df[var1], df[var2])
                    })
            
            # Sort by absolute correlation value
            correlations.sort(key=lambda x: abs(x['correlation']), reverse=True)
            
            # Identify strong correlations
            strong_correlations = [c for c in correlations if abs(c['correlation']) > 0.7]
            moderate_correlations = [c for c in correlations if 0.3 < abs(c['correlation']) <= 0.7]
            
            return {
                "status": "success",
                "variables": variables,
                "correlation_matrix": correlation_matrix.to_dict(),
                "pairwise_correlations": correlations,
                "strong_correlations": strong_correlations,
                "moderate_correlations": moderate_correlations,
                "summary": {
                    "total_pairs": len(correlations),
                    "strong_pairs": len(strong_correlations),
                    "moderate_pairs": len(moderate_correlations),
                    "average_correlation": float(correlation_matrix.values[np.triu_indices_from(correlation_matrix.values, k=1)].mean())
                }
            }
            
        except Exception as e:
            logger.error(f"Error performing correlation analysis: {e}")
            return {"status": "error", "message": str(e)}
    
    async def detect_anomalies(self, data: List[Dict[str, Any]], 
                             variables: List[str], method: str = 'isolation_forest') -> Dict[str, Any]:
        """Detect anomalies in the data."""
        try:
            logger.info(f"Detecting anomalies using method: {method}")
            
            # Convert to DataFrame
            df = pd.DataFrame(data)
            
            # Check if all variables exist
            missing_vars = [var for var in variables if var not in df.columns]
            if missing_vars:
                return {"status": "error", "message": f"Variables not found: {missing_vars}"}
            
            # Prepare data for anomaly detection
            X = df[variables].fillna(df[variables].mean())
            X_scaled = self.scaler.fit_transform(X)
            
            # Apply anomaly detection
            if method == 'isolation_forest':
                detector = self.anomaly_detectors['isolation_forest']
            elif method == 'elliptic_envelope':
                detector = self.anomaly_detectors['elliptic_envelope']
            else:
                return {"status": "error", "message": f"Unknown method: {method}"}
            
            # Detect anomalies
            anomaly_labels = detector.fit_predict(X_scaled)
            anomaly_scores = detector.decision_function(X_scaled)
            
            # Identify anomalous points
            anomalous_indices = np.where(anomaly_labels == -1)[0]
            anomalous_data = df.iloc[anomalous_indices].to_dict('records')
            
            # Calculate anomaly statistics
            anomaly_stats = {
                "total_points": len(df),
                "anomalous_points": len(anomalous_indices),
                "anomaly_percentage": float(len(anomalous_indices) / len(df) * 100),
                "average_anomaly_score": float(np.mean(anomaly_scores)),
                "max_anomaly_score": float(np.max(anomaly_scores)),
                "min_anomaly_score": float(np.min(anomaly_scores))
            }
            
            # Analyze anomalous points by variable
            variable_analysis = {}
            for var in variables:
                var_data = df[var].values
                var_anomalies = var_data[anomalous_indices]
                var_stats = {
                    "mean": float(np.mean(var_data)),
                    "std": float(np.std(var_data)),
                    "anomaly_mean": float(np.mean(var_anomalies)),
                    "anomaly_std": float(np.std(var_anomalies)),
                    "z_score_threshold": float(np.mean(var_data) + 2 * np.std(var_data))
                }
                variable_analysis[var] = var_stats
            
            return {
                "status": "success",
                "method": method,
                "variables": variables,
                "anomaly_labels": anomaly_labels.tolist(),
                "anomaly_scores": anomaly_scores.tolist(),
                "anomalous_data": anomalous_data,
                "statistics": anomaly_stats,
                "variable_analysis": variable_analysis
            }
            
        except Exception as e:
            logger.error(f"Error detecting anomalies: {e}")
            return {"status": "error", "message": str(e)}
    
    async def cluster_analysis(self, data: List[Dict[str, Any]], 
                             variables: List[str], method: str = 'kmeans') -> Dict[str, Any]:
        """Perform cluster analysis on the data."""
        try:
            logger.info(f"Performing cluster analysis using method: {method}")
            
            # Convert to DataFrame
            df = pd.DataFrame(data)
            
            # Check if all variables exist
            missing_vars = [var for var in variables if var not in df.columns]
            if missing_vars:
                return {"status": "error", "message": f"Variables not found: {missing_vars}"}
            
            # Prepare data for clustering
            X = df[variables].fillna(df[variables].mean())
            X_scaled = self.scaler.fit_transform(X)
            
            # Apply clustering
            if method == 'kmeans':
                clusterer = self.clustering_models['kmeans']
            elif method == 'dbscan':
                clusterer = self.clustering_models['dbscan']
            else:
                return {"status": "error", "message": f"Unknown method: {method}"}
            
            # Perform clustering
            cluster_labels = clusterer.fit_predict(X_scaled)
            
            # Analyze clusters
            df['cluster'] = cluster_labels
            cluster_analysis = {}
            
            for cluster_id in np.unique(cluster_labels):
                if cluster_id == -1:  # Noise points in DBSCAN
                    cluster_name = "noise"
                else:
                    cluster_name = f"cluster_{cluster_id}"
                
                cluster_data = df[df['cluster'] == cluster_id]
                cluster_stats = {}
                
                for var in variables:
                    var_stats = {
                        "mean": float(cluster_data[var].mean()),
                        "std": float(cluster_data[var].std()),
                        "min": float(cluster_data[var].min()),
                        "max": float(cluster_data[var].max()),
                        "count": int(len(cluster_data))
                    }
                    cluster_stats[var] = var_stats
                
                cluster_analysis[cluster_name] = {
                    "size": int(len(cluster_data)),
                    "percentage": float(len(cluster_data) / len(df) * 100),
                    "statistics": cluster_stats
                }
            
            # Calculate cluster quality metrics
            if method == 'kmeans':
                inertia = clusterer.inertia_
                silhouette_score = self._calculate_silhouette_score(X_scaled, cluster_labels)
            else:
                inertia = None
                silhouette_score = None
            
            return {
                "status": "success",
                "method": method,
                "variables": variables,
                "cluster_labels": cluster_labels.tolist(),
                "cluster_analysis": cluster_analysis,
                "quality_metrics": {
                    "inertia": inertia,
                    "silhouette_score": silhouette_score,
                    "n_clusters": len(np.unique(cluster_labels[cluster_labels != -1]))
                },
                "total_points": len(df)
            }
            
        except Exception as e:
            logger.error(f"Error performing cluster analysis: {e}")
            return {"status": "error", "message": str(e)}
    
    async def pattern_recognition(self, time_series_data: List[Dict[str, Any]], 
                                variable: str) -> Dict[str, Any]:
        """Recognize patterns in time series data."""
        try:
            logger.info(f"Recognizing patterns for variable: {variable}")
            
            # Convert to DataFrame
            df = pd.DataFrame(time_series_data)
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
            
            if variable not in df.columns:
                return {"status": "error", "message": f"Variable {variable} not found in data"}
            
            values = df[variable].values
            
            # Detect peaks and troughs
            peaks, _ = find_peaks(values, height=np.mean(values))
            troughs, _ = find_peaks(-values, height=-np.mean(values))
            
            # Detect cycles
            cycles = self._detect_cycles(values)
            
            # Detect seasonality
            seasonality = self._detect_seasonality(values)
            
            # Detect structural breaks
            structural_breaks = self._detect_structural_breaks(values)
            
            # Calculate autocorrelation
            autocorr = self._calculate_autocorrelation(values)
            
            return {
                "status": "success",
                "variable": variable,
                "patterns": {
                    "peaks": peaks.tolist(),
                    "troughs": troughs.tolist(),
                    "cycles": cycles,
                    "seasonality": seasonality,
                    "structural_breaks": structural_breaks,
                    "autocorrelation": autocorr
                },
                "statistics": {
                    "n_peaks": len(peaks),
                    "n_troughs": len(troughs),
                    "n_cycles": len(cycles),
                    "data_points": len(values)
                }
            }
            
        except Exception as e:
            logger.error(f"Error recognizing patterns: {e}")
            return {"status": "error", "message": str(e)}
    
    async def comparative_analysis(self, data_sets: Dict[str, List[Dict[str, Any]]], 
                                 variables: List[str]) -> Dict[str, Any]:
        """Perform comparative analysis between different data sets."""
        try:
            logger.info(f"Performing comparative analysis for {len(data_sets)} data sets")
            
            comparative_results = {}
            
            for dataset_name, data in data_sets.items():
                df = pd.DataFrame(data)
                
                # Calculate basic statistics for each variable
                dataset_stats = {}
                for var in variables:
                    if var in df.columns:
                        var_data = df[var].dropna()
                        if len(var_data) > 0:
                            dataset_stats[var] = {
                                "mean": float(var_data.mean()),
                                "std": float(var_data.std()),
                                "min": float(var_data.min()),
                                "max": float(var_data.max()),
                                "median": float(var_data.median()),
                                "count": int(len(var_data))
                            }
                
                comparative_results[dataset_name] = dataset_stats
            
            # Perform statistical tests between datasets
            statistical_tests = {}
            dataset_names = list(data_sets.keys())
            
            for i, dataset1 in enumerate(dataset_names):
                for dataset2 in dataset_names[i+1:]:
                    for var in variables:
                        df1 = pd.DataFrame(data_sets[dataset1])
                        df2 = pd.DataFrame(data_sets[dataset2])
                        
                        if var in df1.columns and var in df2.columns:
                            data1 = df1[var].dropna()
                            data2 = df2[var].dropna()
                            
                            if len(data1) > 0 and len(data2) > 0:
                                # Perform t-test
                                t_stat, p_value = stats.ttest_ind(data1, data2)
                                
                                # Perform Mann-Whitney U test
                                u_stat, u_p_value = stats.mannwhitneyu(data1, data2, alternative='two-sided')
                                
                                test_key = f"{dataset1}_vs_{dataset2}_{var}"
                                statistical_tests[test_key] = {
                                    "t_test": {
                                        "statistic": float(t_stat),
                                        "p_value": float(p_value),
                                        "significant": p_value < 0.05
                                    },
                                    "mann_whitney": {
                                        "statistic": float(u_stat),
                                        "p_value": float(u_p_value),
                                        "significant": u_p_value < 0.05
                                    }
                                }
            
            return {
                "status": "success",
                "datasets": list(data_sets.keys()),
                "variables": variables,
                "comparative_statistics": comparative_results,
                "statistical_tests": statistical_tests,
                "summary": {
                    "n_datasets": len(data_sets),
                    "n_variables": len(variables),
                    "n_tests": len(statistical_tests)
                }
            }
            
        except Exception as e:
            logger.error(f"Error performing comparative analysis: {e}")
            return {"status": "error", "message": str(e)}
    
    def _detect_seasonality(self, values: np.ndarray) -> Dict[str, Any]:
        """Detect seasonality in time series data."""
        try:
            # Simple seasonality detection using autocorrelation
            autocorr = np.correlate(values, values, mode='full')
            autocorr = autocorr[len(autocorr)//2:]
            
            # Find peaks in autocorrelation (potential seasonal periods)
            peaks, _ = find_peaks(autocorr[:len(autocorr)//2])
            
            if len(peaks) > 0:
                seasonal_period = peaks[0]
                seasonal_strength = autocorr[seasonal_period] / autocorr[0]
                
                return {
                    "detected": True,
                    "period": int(seasonal_period),
                    "strength": float(seasonal_strength),
                    "strong": seasonal_strength > 0.5
                }
            else:
                return {
                    "detected": False,
                    "period": None,
                    "strength": 0.0,
                    "strong": False
                }
                
        except Exception as e:
            logger.error(f"Error detecting seasonality: {e}")
            return {"detected": False, "error": str(e)}
    
    def _detect_trend_changes(self, values: np.ndarray, window: int = 10) -> List[int]:
        """Detect trend changes in time series data."""
        try:
            # Calculate rolling mean
            rolling_mean = pd.Series(values).rolling(window=window).mean()
            
            # Calculate rolling slope
            rolling_slope = pd.Series(values).rolling(window=window).apply(
                lambda x: np.polyfit(range(len(x)), x, 1)[0] if len(x) > 1 else 0
            )
            
            # Find points where slope changes sign
            trend_changes = []
            for i in range(1, len(rolling_slope)):
                if (rolling_slope[i-1] > 0 and rolling_slope[i] < 0) or \
                   (rolling_slope[i-1] < 0 and rolling_slope[i] > 0):
                    trend_changes.append(i)
            
            return trend_changes
            
        except Exception as e:
            logger.error(f"Error detecting trend changes: {e}")
            return []
    
    def _detect_cycles(self, values: np.ndarray) -> List[Dict[str, Any]]:
        """Detect cycles in time series data."""
        try:
            # Simple cycle detection using peak analysis
            peaks, _ = find_peaks(values, distance=5)
            troughs, _ = find_peaks(-values, distance=5)
            
            cycles = []
            for i in range(min(len(peaks), len(troughs))):
                cycle = {
                    "start": int(troughs[i]),
                    "peak": int(peaks[i]),
                    "end": int(troughs[i+1]) if i+1 < len(troughs) else len(values)-1,
                    "amplitude": float(values[peaks[i]] - values[troughs[i]]),
                    "duration": int(peaks[i] - troughs[i])
                }
                cycles.append(cycle)
            
            return cycles
            
        except Exception as e:
            logger.error(f"Error detecting cycles: {e}")
            return []
    
    def _detect_structural_breaks(self, values: np.ndarray) -> List[int]:
        """Detect structural breaks in time series data."""
        try:
            # Simple structural break detection using rolling statistics
            rolling_mean = pd.Series(values).rolling(window=20).mean()
            rolling_std = pd.Series(values).rolling(window=20).std()
            
            # Find points where mean or std changes significantly
            breaks = []
            for i in range(20, len(values)):
                if abs(values[i] - rolling_mean[i]) > 2 * rolling_std[i]:
                    breaks.append(i)
            
            return breaks
            
        except Exception as e:
            logger.error(f"Error detecting structural breaks: {e}")
            return []
    
    def _calculate_autocorrelation(self, values: np.ndarray, max_lag: int = 20) -> List[float]:
        """Calculate autocorrelation for time series data."""
        try:
            autocorr = []
            for lag in range(1, min(max_lag + 1, len(values) // 2)):
                corr = np.corrcoef(values[:-lag], values[lag:])[0, 1]
                autocorr.append(float(corr) if not np.isnan(corr) else 0.0)
            
            return autocorr
            
        except Exception as e:
            logger.error(f"Error calculating autocorrelation: {e}")
            return []
    
    def _interpret_correlation(self, corr_value: float) -> str:
        """Interpret correlation strength."""
        abs_corr = abs(corr_value)
        if abs_corr >= 0.8:
            return "very strong"
        elif abs_corr >= 0.6:
            return "strong"
        elif abs_corr >= 0.4:
            return "moderate"
        elif abs_corr >= 0.2:
            return "weak"
        else:
            return "very weak"
    
    def _calculate_significance(self, var1: pd.Series, var2: pd.Series) -> bool:
        """Calculate statistical significance of correlation."""
        try:
            # Remove NaN values
            mask = ~(var1.isna() | var2.isna())
            var1_clean = var1[mask]
            var2_clean = var2[mask]
            
            if len(var1_clean) < 3:
                return False
            
            # Calculate correlation and p-value
            corr, p_value = stats.pearsonr(var1_clean, var2_clean)
            return p_value < 0.05
            
        except Exception:
            return False
    
    def _calculate_silhouette_score(self, X: np.ndarray, labels: np.ndarray) -> float:
        """Calculate silhouette score for clustering."""
        try:
            from sklearn.metrics import silhouette_score
            return float(silhouette_score(X, labels))
        except Exception:
            return 0.0
