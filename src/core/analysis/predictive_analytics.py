#!/usr/bin/env python3
"""
Predictive Analytics Module for Enhanced Reports
Provides machine learning based predictions and modeling capabilities.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional, Tuple
import json
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

class PredictiveAnalytics:
    """Advanced predictive analytics for strategic analysis."""
    
    def __init__(self):
        """Initialize the predictive analytics engine."""
        self.results = {}
        self.models = {}
        
    def create_sample_data(self, n_samples: int = 1000, n_features: int = 5) -> Tuple[pd.DataFrame, pd.Series]:
        """Create sample data for predictive modeling."""
        np.random.seed(42)
        
        # Generate features
        features = {}
        for i in range(n_features):
            features[f'feature_{i+1}'] = np.random.normal(0, 1, n_samples)
        
        # Create target variable with some correlation to features
        target = (0.3 * features['feature_1'] + 
                 0.2 * features['feature_2'] + 
                 0.1 * features['feature_3'] + 
                 np.random.normal(0, 0.5, n_samples))
        
        X = pd.DataFrame(features)
        y = pd.Series(target, name='target')
        
        return X, y
    
    def perform_regression_analysis(self, X: pd.DataFrame, y: pd.Series, 
                                  test_size: float = 0.2) -> Dict[str, Any]:
        """Perform regression analysis using multiple models."""
        try:
            from sklearn.model_selection import train_test_split
            from sklearn.linear_model import LinearRegression, Ridge, Lasso
            from sklearn.ensemble import RandomForestRegressor
            from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
            
            # Define models
            models = {
                'Linear Regression': LinearRegression(),
                'Ridge Regression': Ridge(alpha=1.0),
                'Lasso Regression': Lasso(alpha=0.1),
                'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42)
            }
            
            results = {}
            
            for name, model in models.items():
                # Train model
                model.fit(X_train, y_train)
                
                # Make predictions
                y_pred = model.predict(X_test)
                
                # Calculate metrics
                mse = mean_squared_error(y_test, y_pred)
                rmse = np.sqrt(mse)
                mae = mean_absolute_error(y_test, y_pred)
                r2 = r2_score(y_test, y_pred)
                
                # Feature importance (for applicable models)
                feature_importance = None
                if hasattr(model, 'feature_importances_'):
                    feature_importance = dict(zip(X.columns, model.feature_importances_))
                elif hasattr(model, 'coef_'):
                    feature_importance = dict(zip(X.columns, model.coef_))
                
                results[name] = {
                    'model': model,
                    'predictions': y_pred.tolist(),
                    'metrics': {
                        'mse': mse,
                        'rmse': rmse,
                        'mae': mae,
                        'r2': r2
                    },
                    'feature_importance': feature_importance
                }
            
            # Model comparison
            model_comparison = {}
            for name, result in results.items():
                model_comparison[name] = {
                    'r2': result['metrics']['r2'],
                    'rmse': result['metrics']['rmse'],
                    'mae': result['metrics']['mae']
                }
            
            return {
                'models': results,
                'model_comparison': model_comparison,
                'best_model': max(model_comparison.items(), key=lambda x: x[1]['r2'])[0],
                'data_info': {
                    'n_samples': len(X),
                    'n_features': len(X.columns),
                    'train_size': len(X_train),
                    'test_size': len(X_test)
                }
            }
            
        except Exception as e:
            return {
                'error': f'Regression analysis failed: {str(e)}'
            }
    
    def perform_classification_analysis(self, X: pd.DataFrame, y: pd.Series, 
                                      test_size: float = 0.2) -> Dict[str, Any]:
        """Perform classification analysis using multiple models."""
        try:
            from sklearn.model_selection import train_test_split
            from sklearn.linear_model import LogisticRegression
            from sklearn.ensemble import RandomForestClassifier
            from sklearn.svm import SVC
            from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
            
            # Convert target to binary classification if needed
            if y.nunique() > 2:
                y_binary = (y > y.median()).astype(int)
            else:
                y_binary = y
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(X, y_binary, test_size=test_size, random_state=42)
            
            # Define models
            models = {
                'Logistic Regression': LogisticRegression(random_state=42),
                'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
                'SVM': SVC(random_state=42)
            }
            
            results = {}
            
            for name, model in models.items():
                # Train model
                model.fit(X_train, y_train)
                
                # Make predictions
                y_pred = model.predict(X_test)
                
                # Calculate metrics
                accuracy = accuracy_score(y_test, y_pred)
                precision = precision_score(y_test, y_pred, average='weighted')
                recall = recall_score(y_test, y_pred, average='weighted')
                f1 = f1_score(y_test, y_pred, average='weighted')
                
                # Confusion matrix
                cm = confusion_matrix(y_test, y_pred)
                
                # Feature importance (for applicable models)
                feature_importance = None
                if hasattr(model, 'feature_importances_'):
                    feature_importance = dict(zip(X.columns, model.feature_importances_))
                elif hasattr(model, 'coef_'):
                    feature_importance = dict(zip(X.columns, model.coef_[0]))
                
                results[name] = {
                    'model': model,
                    'predictions': y_pred.tolist(),
                    'metrics': {
                        'accuracy': accuracy,
                        'precision': precision,
                        'recall': recall,
                        'f1': f1
                    },
                    'confusion_matrix': cm.tolist(),
                    'feature_importance': feature_importance
                }
            
            # Model comparison
            model_comparison = {}
            for name, result in results.items():
                model_comparison[name] = {
                    'accuracy': result['metrics']['accuracy'],
                    'precision': result['metrics']['precision'],
                    'recall': result['metrics']['recall'],
                    'f1': result['metrics']['f1']
                }
            
            return {
                'models': results,
                'model_comparison': model_comparison,
                'best_model': max(model_comparison.items(), key=lambda x: x[1]['f1'])[0],
                'data_info': {
                    'n_samples': len(X),
                    'n_features': len(X.columns),
                    'n_classes': y_binary.nunique(),
                    'train_size': len(X_train),
                    'test_size': len(X_test)
                }
            }
            
        except Exception as e:
            return {
                'error': f'Classification analysis failed: {str(e)}'
            }
    
    def perform_clustering_analysis(self, X: pd.DataFrame, n_clusters: int = 3) -> Dict[str, Any]:
        """Perform clustering analysis using K-means."""
        try:
            from sklearn.cluster import KMeans
            from sklearn.preprocessing import StandardScaler
            from sklearn.metrics import silhouette_score
            
            # Standardize features
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            # Perform clustering
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            cluster_labels = kmeans.fit_predict(X_scaled)
            
            # Calculate metrics
            silhouette_avg = silhouette_score(X_scaled, cluster_labels)
            
            # Cluster analysis
            cluster_analysis = {}
            for i in range(n_clusters):
                cluster_mask = cluster_labels == i
                cluster_data = X[cluster_mask]
                
                cluster_analysis[f'cluster_{i}'] = {
                    'size': int(cluster_mask.sum()),
                    'percentage': float(cluster_mask.sum() / len(X) * 100),
                    'mean_values': cluster_data.mean().to_dict(),
                    'std_values': cluster_data.std().to_dict()
                }
            
            return {
                'cluster_labels': cluster_labels.tolist(),
                'cluster_centers': kmeans.cluster_centers_.tolist(),
                'silhouette_score': silhouette_avg,
                'cluster_analysis': cluster_analysis,
                'n_clusters': n_clusters,
                'data_info': {
                    'n_samples': len(X),
                    'n_features': len(X.columns)
                }
            }
            
        except Exception as e:
            return {
                'error': f'Clustering analysis failed: {str(e)}'
            }
    
    def generate_predictive_report(self, analysis_results: Dict[str, Any], output_path: str = None) -> str:
        """Generate comprehensive predictive analytics report."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            if output_path is None:
                output_path = f"Results/predictive_analytics_report_{timestamp}.html"
            
            # Create HTML report
            html_content = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Predictive Analytics Report</title>
                <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
                <style>
                    body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 20px; }}
                    .header {{ background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white; padding: 20px; border-radius: 10px; }}
                    .section {{ margin: 20px 0; padding: 20px; background: #f8f9fa; border-radius: 10px; }}
                    .metric {{ display: inline-block; margin: 10px; padding: 15px; background: white; border-radius: 8px; text-align: center; }}
                    .metric-value {{ font-size: 2em; font-weight: bold; }}
                    .chart-container {{ width: 100%; max-width: 600px; margin: 20px auto; }}
                    .results-table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                    .results-table th, .results-table td {{ padding: 10px; border: 1px solid #ddd; text-align: center; }}
                    .results-table th {{ background: #1e3c72; color: white; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>Predictive Analytics Report</h1>
                    <p>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
                </div>
                
                <div class="section">
                    <h2>Analysis Summary</h2>
                    <div class="metric">
                        <div class="metric-value">
                            {analysis_results.get('data_info', {}).get('n_samples', 0)}
                        </div>
                        <div>Total Samples</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">
                            {analysis_results.get('data_info', {}).get('n_features', 0)}
                        </div>
                        <div>Features</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">
                            {analysis_results.get('best_model', 'N/A')}
                        </div>
                        <div>Best Model</div>
                    </div>
                </div>
                
                <div class="section">
                    <h2>Model Performance Comparison</h2>
                    <div class="chart-container">
                        <canvas id="performanceChart"></canvas>
                    </div>
                </div>
                
                <div class="section">
                    <h2>Detailed Results</h2>
                    {self._generate_detailed_results_html(analysis_results)}
                </div>
                
                <script>
                    // Performance Comparison Chart
                    const ctx = document.getElementById('performanceChart').getContext('2d');
                    new Chart(ctx, {{
                        type: 'bar',
                        data: {{
                            labels: {list(analysis_results.get('model_comparison', {}).keys())},
                            datasets: [
                                {{
                                    label: 'R² Score',
                                    data: {[v.get('r2', 0) for v in analysis_results.get('model_comparison', {}).values()]},
                                    backgroundColor: '#1e3c72'
                                }},
                                {{
                                    label: 'RMSE',
                                    data: {[v.get('rmse', 0) for v in analysis_results.get('model_comparison', {}).values()]},
                                    backgroundColor: '#dc3545'
                                }}
                            ]
                        }},
                        options: {{
                            responsive: true,
                            plugins: {{
                                title: {{
                                    display: true,
                                    text: 'Model Performance Comparison'
                                }}
                            }},
                            scales: {{
                                y: {{
                                    beginAtZero: true
                                }}
                            }}
                        }}
                    }});
                </script>
            </body>
            </html>
            """
            
            # Save report
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            return output_path
            
        except Exception as e:
            return f"Report generation failed: {str(e)}"
    
    def _generate_detailed_results_html(self, analysis_results: Dict[str, Any]) -> str:
        """Generate HTML for detailed results."""
        html = ""
        
        # Model comparison table
        if 'model_comparison' in analysis_results:
            html += "<h3>Model Comparison</h3>"
            html += "<table class='results-table'>"
            html += "<thead><tr><th>Model</th><th>R² Score</th><th>RMSE</th><th>MAE</th></tr></thead>"
            html += "<tbody>"
            
            for model_name, metrics in analysis_results['model_comparison'].items():
                html += f"""
                <tr>
                    <td>{model_name}</td>
                    <td>{metrics.get('r2', 0):.4f}</td>
                    <td>{metrics.get('rmse', 0):.4f}</td>
                    <td>{metrics.get('mae', 0):.4f}</td>
                </tr>
                """
            
            html += "</tbody></table>"
        
        # Feature importance
        if 'models' in analysis_results:
            html += "<h3>Feature Importance (Best Model)</h3>"
            best_model_name = analysis_results.get('best_model', '')
            if best_model_name in analysis_results['models']:
                feature_importance = analysis_results['models'][best_model_name].get('feature_importance', {})
                if feature_importance:
                    html += "<table class='results-table'>"
                    html += "<thead><tr><th>Feature</th><th>Importance</th></tr></thead>"
                    html += "<tbody>"
                    
                    for feature, importance in sorted(feature_importance.items(), key=lambda x: abs(x[1]), reverse=True):
                        html += f"<tr><td>{feature}</td><td>{importance:.4f}</td></tr>"
                    
                    html += "</tbody></table>"
        
        return html

# Create global instance
predictive_analytics = PredictiveAnalytics()

