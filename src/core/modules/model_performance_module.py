#!/usr/bin/env python3
"""
Model Performance Module

This module provides comprehensive model performance analysis and evaluation
capabilities, including accuracy comparison and performance metrics.
"""

import json
from typing import Dict, List, Any, Optional
from loguru import logger

from src.core.modules.base_module import BaseModule, ModuleConfig, TooltipData


class ModelPerformanceModule(BaseModule):
    """Model Performance Module for performance analysis and evaluation."""
    
    def __init__(self, config: Optional[ModuleConfig] = None):
        """Initialize the Model Performance Module."""
        super().__init__(config or ModuleConfig())
        
        # Set module properties
        self.config.title = "Model Performance Analysis"
        self.config.description = "Comprehensive model performance analysis and evaluation"
        self.config.enabled = True
        self.config.tooltips_enabled = True
        self.config.charts_enabled = True
        self.config.order = 18  # Model Performance is typically module 18
        
        # Initialize default tooltips
        self._initialize_default_tooltips()
    
    def get_required_data_keys(self) -> List[str]:
        """Get list of required data keys for this module."""
        return ["model_performance"]
    
    def generate_content(self, data: Dict[str, Any]) -> str:
        """Generate model performance content."""
        logger.info(f"Generating model performance content for {self.module_id}")
        
        try:
            # Extract model performance data
            performance_data = data.get("model_performance", {})
            
            # Generate main content sections
            content_parts = []
            
            # Model Performance Metrics
            performance_metrics = self._generate_performance_metrics(performance_data)
            content_parts.append(performance_metrics)
            
            # Accuracy Comparison
            accuracy_comparison = self._generate_accuracy_comparison(performance_data)
            content_parts.append(accuracy_comparison)
            
            # Performance Analysis
            performance_analysis = self._generate_performance_analysis(performance_data)
            content_parts.append(performance_analysis)
            
            # Model Evaluation
            model_evaluation = self._generate_model_evaluation(performance_data)
            content_parts.append(model_evaluation)
            
            # Combine all content
            content = "\n".join(content_parts)
            
            return content
            
        except Exception as e:
            logger.error(f"Error generating model performance content: {e}")
            return self._generate_error_content()
    
    def _generate_performance_metrics(self, data: Dict[str, Any]) -> str:
        """Generate model performance metrics section."""
        metrics_data = data.get("performance_metrics", {})
        
        # Extract performance metrics
        metrics = metrics_data.get("metrics", [])
        
        # Default metrics if not provided
        if not metrics:
            metrics = [
                {"model": "Linear Regression", "accuracy": 0.85, "precision": 0.83, "recall": 0.87, "f1_score": 0.85, "mae": 0.12, "rmse": 0.18},
                {"model": "Random Forest", "accuracy": 0.92, "precision": 0.91, "recall": 0.93, "f1_score": 0.92, "mae": 0.08, "rmse": 0.12},
                {"model": "Gradient Boosting", "accuracy": 0.94, "precision": 0.93, "recall": 0.95, "f1_score": 0.94, "mae": 0.06, "rmse": 0.09},
                {"model": "Neural Network", "accuracy": 0.96, "precision": 0.95, "recall": 0.97, "f1_score": 0.96, "mae": 0.04, "rmse": 0.07}
            ]
        
        # Generate radar chart data for performance comparison
        radar_data = {
            "labels": ["Accuracy", "Precision", "Recall", "F1 Score", "MAE", "RMSE"],
            "datasets": []
        }
        
        colors = [
            "rgba(255, 99, 132, 0.8)",
            "rgba(54, 162, 235, 0.8)",
            "rgba(255, 205, 86, 0.8)",
            "rgba(75, 192, 192, 0.8)"
        ]
        
        for i, metric in enumerate(metrics):
            # Normalize values for radar chart (0-1 scale)
            accuracy_score = metric["accuracy"]
            precision_score = metric["precision"]
            recall_score = metric["recall"]
            f1_score = metric["f1_score"]
            mae_score = 1 - (metric["mae"] / 0.2)  # Normalize MAE (lower is better)
            rmse_score = 1 - (metric["rmse"] / 0.3)  # Normalize RMSE (lower is better)
            
            radar_data["datasets"].append({
                "label": metric["model"],
                "data": [accuracy_score, precision_score, recall_score, f1_score, mae_score, rmse_score],
                "backgroundColor": colors[i % len(colors)],
                "borderColor": colors[i % len(colors)].replace("0.8", "1"),
                "borderWidth": 2,
                "pointBackgroundColor": colors[i % len(colors)],
                "pointBorderColor": "#fff",
                "pointHoverBackgroundColor": "#fff",
                "pointHoverBorderColor": colors[i % len(colors)]
            })
        
        content = f"""
        <div class="section" data-tooltip-{self.module_id}="performance_metrics">
            <h3>📊 Model Performance Metrics</h3>
            <p>Comprehensive analysis of model performance metrics and evaluation criteria.</p>
            
            <div class="metrics-table">
                <table>
                    <thead>
                        <tr>
                            <th>Model</th>
                            <th>Accuracy</th>
                            <th>Precision</th>
                            <th>Recall</th>
                            <th>F1 Score</th>
                            <th>MAE</th>
                            <th>RMSE</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        
        for metric in metrics:
            content += f"""
                        <tr>
                            <td>{metric['model']}</td>
                            <td>{metric['accuracy']:.1%}</td>
                            <td>{metric['precision']:.1%}</td>
                            <td>{metric['recall']:.1%}</td>
                            <td>{metric['f1_score']:.1%}</td>
                            <td>{metric['mae']:.3f}</td>
                            <td>{metric['rmse']:.3f}</td>
                        </tr>
            """
        
        content += f"""
                    </tbody>
                </table>
            </div>
            
            <div class="chart-container">
                <canvas id="modelPerformanceMetricsChart" width="400" height="300"></canvas>
            </div>
            
            <script>
                // Chart.js Model Performance Metrics
                const modelPerformanceMetricsCtx = document.getElementById('modelPerformanceMetricsChart').getContext('2d');
                new Chart(modelPerformanceMetricsCtx, {{
                    type: 'radar',
                    data: {json.dumps(radar_data)},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {{
                            r: {{
                                beginAtZero: true,
                                max: 1,
                                ticks: {{
                                    stepSize: 0.2
                                }}
                            }}
                        }},
                        plugins: {{
                            legend: {{
                                display: true,
                                position: 'bottom'
                            }}
                        }}
                    }}
                }});
            </script>
        </div>
        """
        
        return content
    
    def _generate_accuracy_comparison(self, data: Dict[str, Any]) -> str:
        """Generate accuracy comparison section."""
        comparison_data = data.get("accuracy_comparison", {})
        
        # Extract comparison metrics
        comparisons = comparison_data.get("comparisons", [])
        
        # Default comparisons if not provided
        if not comparisons:
            comparisons = [
                {"metric": "Overall Accuracy", "linear_regression": 0.85, "random_forest": 0.92, "gradient_boosting": 0.94, "neural_network": 0.96},
                {"metric": "Training Accuracy", "linear_regression": 0.87, "random_forest": 0.94, "gradient_boosting": 0.96, "neural_network": 0.98},
                {"metric": "Validation Accuracy", "linear_regression": 0.83, "random_forest": 0.90, "gradient_boosting": 0.92, "neural_network": 0.94},
                {"metric": "Test Accuracy", "linear_regression": 0.82, "random_forest": 0.89, "gradient_boosting": 0.91, "neural_network": 0.93}
            ]
        
        # Generate bar chart data for accuracy comparison
        bar_data = {
            "labels": [comp["metric"] for comp in comparisons],
            "datasets": [
                {
                    "label": "Linear Regression",
                    "data": [comp["linear_regression"] for comp in comparisons],
                    "backgroundColor": "rgba(255, 99, 132, 0.8)",
                    "borderColor": "rgba(255, 99, 132, 1)",
                    "borderWidth": 1
                },
                {
                    "label": "Random Forest",
                    "data": [comp["random_forest"] for comp in comparisons],
                    "backgroundColor": "rgba(54, 162, 235, 0.8)",
                    "borderColor": "rgba(54, 162, 235, 1)",
                    "borderWidth": 1
                },
                {
                    "label": "Gradient Boosting",
                    "data": [comp["gradient_boosting"] for comp in comparisons],
                    "backgroundColor": "rgba(255, 205, 86, 0.8)",
                    "borderColor": "rgba(255, 205, 86, 1)",
                    "borderWidth": 1
                },
                {
                    "label": "Neural Network",
                    "data": [comp["neural_network"] for comp in comparisons],
                    "backgroundColor": "rgba(75, 192, 192, 0.8)",
                    "borderColor": "rgba(75, 192, 192, 1)",
                    "borderWidth": 1
                }
            ]
        }
        
        content = f"""
        <div class="section" data-tooltip-{self.module_id}="accuracy_comparison">
            <h3>🎯 Accuracy Comparison</h3>
            <p>Detailed comparison of model accuracy across different evaluation criteria.</p>
            
            <div class="comparison-table">
                <table>
                    <thead>
                        <tr>
                            <th>Metric</th>
                            <th>Linear Regression</th>
                            <th>Random Forest</th>
                            <th>Gradient Boosting</th>
                            <th>Neural Network</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        
        for comp in comparisons:
            content += f"""
                        <tr>
                            <td>{comp['metric']}</td>
                            <td>{comp['linear_regression']:.1%}</td>
                            <td>{comp['random_forest']:.1%}</td>
                            <td>{comp['gradient_boosting']:.1%}</td>
                            <td>{comp['neural_network']:.1%}</td>
                        </tr>
            """
        
        content += f"""
                    </tbody>
                </table>
            </div>
            
            <div class="chart-container">
                <canvas id="accuracyComparisonChart" width="400" height="300"></canvas>
            </div>
            
            <script>
                // Chart.js Accuracy Comparison
                const accuracyComparisonCtx = document.getElementById('accuracyComparisonChart').getContext('2d');
                new Chart(accuracyComparisonCtx, {{
                    type: 'bar',
                    data: {json.dumps(bar_data)},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {{
                            x: {{
                                stacked: false,
                                title: {{
                                    display: true,
                                    text: 'Accuracy Metrics'
                                }}
                            }},
                            y: {{
                                beginAtZero: true,
                                max: 1,
                                title: {{
                                    display: true,
                                    text: 'Accuracy Score'
                                }}
                            }}
                        }},
                        plugins: {{
                            legend: {{
                                display: true,
                                position: 'top'
                            }}
                        }}
                    }}
                }});
            </script>
        </div>
        """
        
        return content
    
    def _generate_performance_analysis(self, data: Dict[str, Any]) -> str:
        """Generate performance analysis section."""
        analysis_data = data.get("performance_analysis", {})
        
        # Extract analysis metrics
        analysis_metrics = analysis_data.get("analysis_metrics", [])
        
        # Default analysis metrics if not provided
        if not analysis_metrics:
            analysis_metrics = [
                {"aspect": "Computational Efficiency", "linear_regression": 0.95, "random_forest": 0.75, "gradient_boosting": 0.70, "neural_network": 0.60},
                {"aspect": "Interpretability", "linear_regression": 0.90, "random_forest": 0.80, "gradient_boosting": 0.70, "neural_network": 0.30},
                {"aspect": "Scalability", "linear_regression": 0.85, "random_forest": 0.80, "gradient_boosting": 0.75, "neural_network": 0.90},
                {"aspect": "Robustness", "linear_regression": 0.70, "random_forest": 0.85, "gradient_boosting": 0.80, "neural_network": 0.75},
                {"aspect": "Feature Importance", "linear_regression": 0.60, "random_forest": 0.90, "gradient_boosting": 0.85, "neural_network": 0.40}
            ]
        
        # Generate analysis summary
        analysis_summary = analysis_data.get("summary", {
            "total_models": 4,
            "best_overall": "Neural Network",
            "best_interpretable": "Linear Regression",
            "best_balanced": "Random Forest"
        })
        
        content = f"""
        <div class="section" data-tooltip-{self.module_id}="performance_analysis">
            <h3>📈 Performance Analysis</h3>
            <p>Comprehensive analysis of model performance across multiple dimensions.</p>
            
            <div class="analysis-summary">
                <h4>Analysis Summary</h4>
                <div class="summary-grid">
                    <div class="summary-item">
                        <div class="summary-value">{analysis_summary['total_models']}</div>
                        <div class="summary-label">Total Models</div>
                    </div>
                    <div class="summary-item">
                        <div class="summary-value">{analysis_summary['best_overall']}</div>
                        <div class="summary-label">Best Overall</div>
                    </div>
                    <div class="summary-item">
                        <div class="summary-value">{analysis_summary['best_interpretable']}</div>
                        <div class="summary-label">Best Interpretable</div>
                    </div>
                    <div class="summary-item">
                        <div class="summary-value">{analysis_summary['best_balanced']}</div>
                        <div class="summary-label">Best Balanced</div>
                    </div>
                </div>
            </div>
            
            <div class="analysis-metrics">
                <h4>Performance Dimensions</h4>
                <div class="metrics-grid">
        """
        
        for metric in analysis_metrics:
            content += f"""
                    <div class="metric-card">
                        <h5>{metric['aspect']}</h5>
                        <div class="metric-values">
                            <div class="metric-value">
                                <span class="model-name">Linear Regression:</span>
                                <span class="model-score">{metric['linear_regression']:.1%}</span>
                            </div>
                            <div class="metric-value">
                                <span class="model-name">Random Forest:</span>
                                <span class="model-score">{metric['random_forest']:.1%}</span>
                            </div>
                            <div class="metric-value">
                                <span class="model-name">Gradient Boosting:</span>
                                <span class="model-score">{metric['gradient_boosting']:.1%}</span>
                            </div>
                            <div class="metric-value">
                                <span class="model-name">Neural Network:</span>
                                <span class="model-score">{metric['neural_network']:.1%}</span>
                            </div>
                        </div>
                    </div>
            """
        
        content += """
                </div>
            </div>
        </div>
        """
        
        return content
    
    def _generate_model_evaluation(self, data: Dict[str, Any]) -> str:
        """Generate model evaluation section."""
        evaluation_data = data.get("model_evaluation", {})
        
        # Extract evaluation criteria
        evaluation_criteria = evaluation_data.get("evaluation_criteria", [])
        
        # Default evaluation criteria if not provided
        if not evaluation_criteria:
            evaluation_criteria = [
                {"criterion": "Accuracy", "weight": 0.25, "linear_regression": 0.85, "random_forest": 0.92, "gradient_boosting": 0.94, "neural_network": 0.96},
                {"criterion": "Interpretability", "weight": 0.20, "linear_regression": 0.90, "random_forest": 0.80, "gradient_boosting": 0.70, "neural_network": 0.30},
                {"criterion": "Computational Cost", "weight": 0.15, "linear_regression": 0.95, "random_forest": 0.75, "gradient_boosting": 0.70, "neural_network": 0.60},
                {"criterion": "Robustness", "weight": 0.20, "linear_regression": 0.70, "random_forest": 0.85, "gradient_boosting": 0.80, "neural_network": 0.75},
                {"criterion": "Scalability", "weight": 0.20, "linear_regression": 0.85, "random_forest": 0.80, "gradient_boosting": 0.75, "neural_network": 0.90}
            ]
        
        # Calculate weighted scores
        weighted_scores = {}
        for model in ["linear_regression", "random_forest", "gradient_boosting", "neural_network"]:
            weighted_scores[model] = sum(
                criterion["weight"] * criterion[model] 
                for criterion in evaluation_criteria
            )
        
        # Generate line chart data for evaluation comparison
        line_data = {
            "labels": [criterion["criterion"] for criterion in evaluation_criteria],
            "datasets": [
                {
                    "label": "Linear Regression",
                    "data": [criterion["linear_regression"] for criterion in evaluation_criteria],
                    "borderColor": "rgba(255, 99, 132, 1)",
                    "backgroundColor": "rgba(255, 99, 132, 0.2)",
                    "tension": 0.4
                },
                {
                    "label": "Random Forest",
                    "data": [criterion["random_forest"] for criterion in evaluation_criteria],
                    "borderColor": "rgba(54, 162, 235, 1)",
                    "backgroundColor": "rgba(54, 162, 235, 0.2)",
                    "tension": 0.4
                },
                {
                    "label": "Gradient Boosting",
                    "data": [criterion["gradient_boosting"] for criterion in evaluation_criteria],
                    "borderColor": "rgba(255, 205, 86, 1)",
                    "backgroundColor": "rgba(255, 205, 86, 0.2)",
                    "tension": 0.4
                },
                {
                    "label": "Neural Network",
                    "data": [criterion["neural_network"] for criterion in evaluation_criteria],
                    "borderColor": "rgba(75, 192, 192, 1)",
                    "backgroundColor": "rgba(75, 192, 192, 0.2)",
                    "tension": 0.4
                }
            ]
        }
        
        content = f"""
        <div class="section" data-tooltip-{self.module_id}="model_evaluation">
            <h3>🔍 Model Evaluation</h3>
            <p>Comprehensive evaluation of models across multiple criteria with weighted scoring.</p>
            
            <div class="evaluation-table">
                <table>
                    <thead>
                        <tr>
                            <th>Criterion</th>
                            <th>Weight</th>
                            <th>Linear Regression</th>
                            <th>Random Forest</th>
                            <th>Gradient Boosting</th>
                            <th>Neural Network</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        
        for criterion in evaluation_criteria:
            content += f"""
                        <tr>
                            <td>{criterion['criterion']}</td>
                            <td>{criterion['weight']:.1%}</td>
                            <td>{criterion['linear_regression']:.1%}</td>
                            <td>{criterion['random_forest']:.1%}</td>
                            <td>{criterion['gradient_boosting']:.1%}</td>
                            <td>{criterion['neural_network']:.1%}</td>
                        </tr>
            """
        
        content += f"""
                    </tbody>
                </table>
            </div>
            
            <div class="weighted-scores">
                <h4>Weighted Overall Scores</h4>
                <div class="scores-grid">
                    <div class="score-item">
                        <div class="score-label">Linear Regression</div>
                        <div class="score-value">{weighted_scores['linear_regression']:.3f}</div>
                    </div>
                    <div class="score-item">
                        <div class="score-label">Random Forest</div>
                        <div class="score-value">{weighted_scores['random_forest']:.3f}</div>
                    </div>
                    <div class="score-item">
                        <div class="score-label">Gradient Boosting</div>
                        <div class="score-value">{weighted_scores['gradient_boosting']:.3f}</div>
                    </div>
                    <div class="score-item">
                        <div class="score-label">Neural Network</div>
                        <div class="score-value">{weighted_scores['neural_network']:.3f}</div>
                    </div>
                </div>
            </div>
            
            <div class="chart-container">
                <canvas id="modelEvaluationChart" width="400" height="300"></canvas>
            </div>
            
            <script>
                // Chart.js Model Evaluation
                const modelEvaluationCtx = document.getElementById('modelEvaluationChart').getContext('2d');
                new Chart(modelEvaluationCtx, {{
                    type: 'line',
                    data: {json.dumps(line_data)},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {{
                            x: {{
                                title: {{
                                    display: true,
                                    text: 'Evaluation Criteria'
                                }}
                            }},
                            y: {{
                                beginAtZero: true,
                                max: 1,
                                title: {{
                                    display: true,
                                    text: 'Score'
                                }}
                            }}
                        }},
                        plugins: {{
                            legend: {{
                                display: true,
                                position: 'top'
                            }}
                        }}
                    }}
                }});
            </script>
        </div>
        """
        
        return content
    
    def _initialize_default_tooltips(self):
        """Initialize default tooltip data for the module."""
        tooltip_data = {
            "performance_metrics": TooltipData(
                title="Model Performance Metrics",
                description="Comprehensive analysis of model performance metrics including accuracy, precision, recall, F1 score, MAE, and RMSE for various machine learning models",
                source="Source: Model Performance Analytics Framework",
                strategic_impact="Strategic Impact: Critical for selecting optimal models for strategic analysis and decision-making",
                recommendations="Recommendations: Use ensemble methods for improved accuracy and consider model complexity vs performance trade-offs",
                use_cases="Use Cases: Model selection, performance optimization, strategic analysis, decision support"
            ),
            "accuracy_comparison": TooltipData(
                title="Accuracy Comparison",
                description="Detailed comparison of model accuracy across different evaluation criteria including overall, training, validation, and test accuracy",
                source="Source: Accuracy Assessment Framework",
                strategic_impact="Strategic Impact: Essential for understanding model reliability and generalization capabilities",
                recommendations="Recommendations: Focus on validation and test accuracy for real-world performance assessment",
                use_cases="Use Cases: Model validation, performance assessment, strategic planning, risk management"
            ),
            "performance_analysis": TooltipData(
                title="Performance Analysis",
                description="Comprehensive analysis of model performance across multiple dimensions including computational efficiency, interpretability, scalability, and robustness",
                source="Source: Performance Analysis Framework",
                strategic_impact="Strategic Impact: Important for understanding model trade-offs and selecting appropriate models for different scenarios",
                recommendations="Recommendations: Balance performance metrics based on specific requirements and constraints",
                use_cases="Use Cases: Model selection, performance optimization, strategic planning, resource allocation"
            ),
            "model_evaluation": TooltipData(
                title="Model Evaluation",
                description="Comprehensive evaluation of models across multiple criteria with weighted scoring for optimal model selection",
                source="Source: Model Evaluation Framework",
                strategic_impact="Strategic Impact: Critical for making informed decisions about model selection and deployment",
                recommendations="Recommendations: Use weighted scoring based on strategic priorities and operational constraints",
                use_cases="Use Cases: Model selection, strategic planning, performance optimization, decision support"
            )
        }
        
        # Add tooltip data to the module
        for tooltip_id, tooltip_data_obj in tooltip_data.items():
            self.add_tooltip(tooltip_id, tooltip_data_obj)
    
    def _generate_error_content(self) -> str:
        """Generate error content when data processing fails."""
        return """
        <div class="section">
            <h3>📊 Model Performance Analysis</h3>
            <p>Comprehensive model performance analysis and evaluation.</p>
            
            <div class="error-message">
                <p>⚠️ Unable to generate model performance analysis due to data processing issues.</p>
                <p>Please ensure model performance data is properly formatted and available.</p>
            </div>
            
            <div class="charts-grid">
                <div class="chart-section" data-tooltip="model_performance_chart">
                    <h3>Model Performance Metrics</h3>
                    <canvas id="modelPerformanceChart" width="400" height="300"></canvas>
                </div>
                <div class="chart-section" data-tooltip="accuracy_comparison_chart">
                    <h3>Accuracy Comparison</h3>
                    <canvas id="accuracyComparisonChart" width="400" height="300"></canvas>
                </div>
            </div>
        </div>
        """
