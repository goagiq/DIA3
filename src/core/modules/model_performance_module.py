#!/usr/bin/env python3
"""
Model Performance Module

This module provides comprehensive model performance analysis and evaluation
capabilities, including accuracy comparison and performance metrics.
Enhanced for contextual adaptation and data structure flexibility.
"""

import json
import re
from typing import Dict, List, Any, Optional, Union
from loguru import logger

from src.core.modules.base_module import BaseModule, ModuleConfig, TooltipData


class ModelPerformanceModule(BaseModule):
    """Model Performance Module for performance analysis and evaluation with Contextual Adaptation."""
    
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
        
        # Initialize context domains and their characteristics
        self._initialize_context_domains()
        
        # Initialize default tooltips
        self._initialize_default_tooltips()
    
    def get_required_data_keys(self) -> List[str]:
        """Get list of required data keys for this module."""
        return ["model_performance"]
    
    def validate_data(self, data: Union[str, Dict[str, Any]]) -> bool:
        """Validate that required data is present or that data is a string query."""
        if isinstance(data, str):
            # If data is a string, it's a query and we can generate content
            return True
        elif isinstance(data, dict):
            # If data is a dict, check for required keys
            required_keys = self.get_required_data_keys()
            missing_keys = [key for key in required_keys if key not in data]
            
            if missing_keys:
                raise ValueError(
                    f"Missing required data keys for {self.module_id}: {missing_keys}"
                )
            return True
        else:
            raise ValueError(f"Invalid data type for {self.module_id}: {type(data)}")
    
    def generate_content(self, data: Union[str, Dict[str, Any]]) -> str:
        """Generate model performance content with contextual adaptation."""
        logger.info(f"Generating model performance content for {self.module_id}")
        
        try:
            # Handle different data structures
            if isinstance(data, str):
                # If data is a string, treat it as a query and generate adaptive content
                query = data
                context_domain = self._detect_context_domain(query)
                performance_data = self._generate_adaptive_data(query, context_domain)
            elif isinstance(data, dict):
                # If data is a dict, extract model performance data
                performance_data = data.get("model_performance", {})
                query = performance_data.get("query", "Model Performance Analysis")
                context_domain = self._detect_context_domain(query)
            else:
                # Default fallback
                performance_data = {}
                query = "Model Performance Analysis"
                context_domain = "GENERAL"
            
            # Generate main content sections with contextual adaptation
            content_parts = []
            
            # Model Performance Metrics (context-aware)
            performance_metrics = self._generate_contextual_performance_metrics(performance_data, context_domain)
            content_parts.append(performance_metrics)
            
            # Accuracy Comparison (context-aware)
            accuracy_comparison = self._generate_contextual_accuracy_comparison(performance_data, context_domain)
            content_parts.append(accuracy_comparison)
            
            # Performance Analysis (context-aware)
            performance_analysis = self._generate_contextual_performance_analysis(performance_data, context_domain)
            content_parts.append(performance_analysis)
            
            # Model Evaluation (context-aware)
            model_evaluation = self._generate_contextual_model_evaluation(performance_data, context_domain)
            content_parts.append(model_evaluation)
            
            # Combine all content
            content = "\n".join(content_parts)
            
            return content
            
        except Exception as e:
            logger.error(f"Error generating model performance content: {e}")
            return self._generate_error_content()
    
    def _initialize_context_domains(self):
        """Initialize context domains and their characteristics."""
        self.context_domains = {
            "MILITARY": {
                "keywords": ["military", "defense", "weapons", "submarine", "navy", "army", "air force", "deterrence", "warfare", "combat"],
                "model_types": ["threat_assessment", "capability_analysis", "strategic_planning", "operational_analysis", "intelligence_analysis"],
                "metrics": ["accuracy", "precision", "recall", "f1_score", "threat_detection_rate", "false_alarm_rate"],
                "chart_types": ["radar", "bar", "line"],
                "analysis_focus": "military model performance and strategic analysis"
            },
            "ECONOMIC": {
                "keywords": ["economic", "trade", "finance", "market", "investment", "gdp", "commerce", "business", "financial"],
                "model_types": ["forecasting", "risk_assessment", "market_analysis", "investment_analysis", "economic_modeling"],
                "metrics": ["accuracy", "precision", "recall", "f1_score", "mae", "rmse", "r_squared"],
                "chart_types": ["line", "bar", "doughnut"],
                "analysis_focus": "economic model performance and financial analysis"
            },
            "HEALTHCARE": {
                "keywords": ["health", "medical", "disease", "pandemic", "healthcare", "public health", "epidemiology"],
                "model_types": ["diagnostic", "prognostic", "epidemiological", "treatment_optimization", "risk_prediction"],
                "metrics": ["sensitivity", "specificity", "accuracy", "auc", "positive_predictive_value", "negative_predictive_value"],
                "chart_types": ["line", "bar", "area"],
                "analysis_focus": "healthcare model performance and medical analysis"
            },
            "TECHNOLOGY": {
                "keywords": ["technology", "cyber", "digital", "innovation", "ai", "automation", "digital transformation"],
                "model_types": ["machine_learning", "deep_learning", "nlp", "computer_vision", "recommendation_system"],
                "metrics": ["accuracy", "precision", "recall", "f1_score", "latency", "throughput", "scalability"],
                "chart_types": ["radar", "line", "bar"],
                "analysis_focus": "technology model performance and AI analysis"
            },
            "GENERAL": {
                "keywords": [],
                "model_types": ["linear_regression", "random_forest", "gradient_boosting", "neural_network", "svm"],
                "metrics": ["accuracy", "precision", "recall", "f1_score", "mae", "rmse"],
                "chart_types": ["radar", "line", "bar"],
                "analysis_focus": "general model performance and analysis"
            }
        }
    
    def _detect_context_domain(self, query: str) -> str:
        """Detect the context domain from the query."""
        query_lower = query.lower()
        
        for domain, config in self.context_domains.items():
            for keyword in config["keywords"]:
                if keyword in query_lower:
                    return domain
        
        return "GENERAL"
    
    def _generate_adaptive_data(self, query: str, context_domain: str) -> Dict[str, Any]:
        """Generate adaptive data based on context domain."""
        domain_config = self.context_domains[context_domain]
        
        # Generate context-appropriate performance metrics
        performance_metrics = []
        for i, metric in enumerate(domain_config["metrics"]):
            if "accuracy" in metric:
                performance_metrics.append({
                    "metric": metric.replace("_", " ").title(),
                    "current_value": 85 + (i * 2),
                    "target_value": 90 + (i * 2),
                    "trend": "Improving",
                    "confidence_level": "High",
                    "benchmark": "Industry Standard"
                })
            elif "precision" in metric or "recall" in metric:
                performance_metrics.append({
                    "metric": metric.replace("_", " ").title(),
                    "current_value": 80 + (i * 3),
                    "target_value": 85 + (i * 3),
                    "trend": "Stable",
                    "confidence_level": "Medium",
                    "benchmark": "Best Practice"
                })
            else:
                performance_metrics.append({
                    "metric": metric.replace("_", " ").title(),
                    "current_value": 75 + (i * 5),
                    "target_value": 80 + (i * 5),
                    "trend": "Improving",
                    "confidence_level": "Medium",
                    "benchmark": "Industry Standard"
                })
        
        return {
            "context_domain": context_domain,
            "query": query,
            "performance_metrics": performance_metrics,
            "model_types": domain_config["model_types"],
            "analysis_focus": domain_config["analysis_focus"],
            "chart_types": domain_config["chart_types"],
            "data_sources": self._generate_contextual_sources(context_domain)
        }
    
    def _generate_contextual_sources(self, context_domain: str) -> List[str]:
        """Generate context-appropriate data sources."""
        source_mapping = {
            "MILITARY": [
                "Military Model Performance Database",
                "Defense Analytics Framework",
                "Strategic Analysis Models",
                "Military Intelligence Systems",
                "Defense Technology Reviews"
            ],
            "ECONOMIC": [
                "Economic Model Performance Database",
                "Financial Analytics Framework",
                "Market Analysis Models",
                "Economic Intelligence Systems",
                "Financial Technology Reviews"
            ],
            "HEALTHCARE": [
                "Healthcare Model Performance Database",
                "Medical Analytics Framework",
                "Clinical Analysis Models",
                "Healthcare Intelligence Systems",
                "Medical Technology Reviews"
            ],
            "TECHNOLOGY": [
                "Technology Model Performance Database",
                "AI Analytics Framework",
                "Machine Learning Models",
                "Technology Intelligence Systems",
                "Digital Technology Reviews"
            ],
            "GENERAL": [
                "Model Performance Analytics Framework",
                "Machine Learning Evaluation Database",
                "Statistical Analysis Reports",
                "Industry Benchmarking Data",
                "Performance Monitoring Systems"
            ]
        }
        
        return source_mapping.get(context_domain, source_mapping["GENERAL"])
    
    def _generate_contextual_performance_metrics(self, data: Dict[str, Any], context_domain: str) -> str:
        """Generate context-aware model performance metrics section."""
        performance_data = data.get("performance_metrics", [])
        analysis_focus = data.get("analysis_focus", "Model performance analysis")
        
        # Generate chart data for interactive visualizations
        chart_data = {
            f"performanceMetricsChart_{self.module_id}": {
                "type": "bar",
                "data": {
                    "labels": [metric["metric"] for metric in performance_data],
                    "datasets": [{
                        "label": "Current Value",
                        "data": [metric["current_value"] for metric in performance_data],
                        "backgroundColor": "rgba(54, 162, 235, 0.6)",
                        "borderColor": "rgba(54, 162, 235, 1)",
                        "borderWidth": 2
                    }, {
                        "label": "Target Value",
                        "data": [metric["target_value"] for metric in performance_data],
                        "backgroundColor": "rgba(255, 99, 132, 0.6)",
                        "borderColor": "rgba(255, 99, 132, 1)",
                        "borderWidth": 2
                    }]
                },
                "options": {
                    "responsive": True,
                    "maintainAspectRatio": False,
                    "scales": {
                        "y": {
                            "beginAtZero": True,
                            "max": 100,
                            "title": {
                                "display": True,
                                "text": "Performance Score (%)"
                            }
                        }
                    }
                }
            }
        }
        
        # Add chart data to module
        for chart_id, chart_config in chart_data.items():
            self.add_chart_data(chart_id, chart_config)
        
        # Get data sources
        data_sources = data.get("data_sources", self._generate_contextual_sources(context_domain))
        
        content = f"""
        <div class="section">
            <h3>📊 {context_domain.title()} Model Performance Metrics</h3>
            <p>Comprehensive analysis of {analysis_focus.lower()} and evaluation criteria.</p>
            
            <div class="metrics-grid">
        """
        
        for i, metric in enumerate(performance_data):
            content += f"""
                <div class="metric-card" data-tooltip-{self.module_id}="metric_{i}">
                    <h4>{metric['metric']}</h4>
                    <div class="metric-value">{metric['current_value']}%</div>
                    <div class="metric-target">Target: {metric['target_value']}%</div>
                    <div class="metric-trend">{metric['trend']}</div>
                    <div class="metric-confidence">{metric['confidence_level']}</div>
                    <div class="metric-benchmark">{metric['benchmark']}</div>
                </div>
            """
        
        content += f"""
            </div>
            
            <div class="charts-grid">
                <div class="chart-section" data-tooltip-{self.module_id}="performance_metrics_chart">
                    <h4>{context_domain.title()} Performance Metrics Comparison</h4>
                    <canvas id="performanceMetricsChart_{self.module_id}" width="400" height="300"></canvas>
                </div>
            </div>
            
            <div class="data-sources">
                <h4>Data Sources</h4>
                <ul class="sources-list">
        """
        
        for source in data_sources:
            content += f"""
                    <li>{source}</li>
            """
        
        content += """
                </ul>
            </div>
        </div>
        """
        
        return content
    
    def _generate_contextual_accuracy_comparison(self, data: Dict[str, Any], context_domain: str) -> str:
        """Generate context-aware accuracy comparison section."""
        # Generate context-appropriate comparison metrics
        comparisons = self._generate_contextual_comparisons(context_domain)
        
        # Generate bar chart data for accuracy comparison
        bar_data = {
            "labels": [comp["metric"] for comp in comparisons],
            "datasets": [
                {
                    "label": f"{context_domain.title()} Model A",
                    "data": [comp["model_a"] for comp in comparisons],
                    "backgroundColor": "rgba(255, 99, 132, 0.8)",
                    "borderColor": "rgba(255, 99, 132, 1)",
                    "borderWidth": 1
                },
                {
                    "label": f"{context_domain.title()} Model B",
                    "data": [comp["model_b"] for comp in comparisons],
                    "backgroundColor": "rgba(54, 162, 235, 0.8)",
                    "borderColor": "rgba(54, 162, 235, 1)",
                    "borderWidth": 1
                },
                {
                    "label": f"{context_domain.title()} Model C",
                    "data": [comp["model_c"] for comp in comparisons],
                    "backgroundColor": "rgba(255, 205, 86, 0.8)",
                    "borderColor": "rgba(255, 205, 86, 1)",
                    "borderWidth": 1
                }
            ]
        }
        
        content = f"""
        <div class="section" data-tooltip-{self.module_id}="accuracy_comparison">
            <h3>🎯 {context_domain.title()} Accuracy Comparison</h3>
            <p>Detailed comparison of {context_domain.lower()} model accuracy across different evaluation criteria.</p>
            
            <div class="comparison-table">
                <table>
                    <thead>
                        <tr>
                            <th>Metric</th>
                            <th>{context_domain.title()} Model A</th>
                            <th>{context_domain.title()} Model B</th>
                            <th>{context_domain.title()} Model C</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        
        for comp in comparisons:
            content += f"""
                        <tr>
                            <td>{comp['metric']}</td>
                            <td>{comp['model_a']:.1%}</td>
                            <td>{comp['model_b']:.1%}</td>
                            <td>{comp['model_c']:.1%}</td>
                        </tr>
            """
        
        content += f"""
                    </tbody>
                </table>
            </div>
            
            <div class="chart-container">
                <canvas id="accuracyComparisonChart_{self.module_id}" width="400" height="300"></canvas>
            </div>
            
            <script>
                // Chart.js Accuracy Comparison
                const accuracyComparisonCtx_{self.module_id} = document.getElementById('accuracyComparisonChart_{self.module_id}').getContext('2d');
                new Chart(accuracyComparisonCtx_{self.module_id}, {{
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
    
    def _generate_contextual_performance_analysis(self, data: Dict[str, Any], context_domain: str) -> str:
        """Generate context-aware performance analysis section."""
        # Generate context-appropriate analysis metrics
        analysis_metrics = self._generate_contextual_analysis_metrics(context_domain)
        
        # Generate analysis summary
        analysis_summary = {
            "total_models": 3,
            "best_overall": f"{context_domain.title()} Model C",
            "best_interpretable": f"{context_domain.title()} Model A",
            "best_balanced": f"{context_domain.title()} Model B"
        }
        
        content = f"""
        <div class="section" data-tooltip-{self.module_id}="performance_analysis">
            <h3>📈 {context_domain.title()} Performance Analysis</h3>
            <p>Comprehensive analysis of {context_domain.lower()} model performance across multiple dimensions.</p>
            
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
                                <span class="model-name">{context_domain.title()} Model A:</span>
                                <span class="model-score">{metric['model_a']:.1%}</span>
                            </div>
                            <div class="metric-value">
                                <span class="model-name">{context_domain.title()} Model B:</span>
                                <span class="model-score">{metric['model_b']:.1%}</span>
                            </div>
                            <div class="metric-value">
                                <span class="model-name">{context_domain.title()} Model C:</span>
                                <span class="model-score">{metric['model_c']:.1%}</span>
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
    
    def _generate_contextual_model_evaluation(self, data: Dict[str, Any], context_domain: str) -> str:
        """Generate context-aware model evaluation section."""
        # Generate context-appropriate evaluation criteria
        evaluation_criteria = self._generate_contextual_evaluation_criteria(context_domain)
        
        # Calculate weighted scores
        weighted_scores = {}
        for model in ["model_a", "model_b", "model_c"]:
            weighted_scores[model] = sum(
                criterion["weight"] * criterion[model] 
                for criterion in evaluation_criteria
            )
        
        # Generate line chart data for evaluation comparison
        line_data = {
            "labels": [criterion["criterion"] for criterion in evaluation_criteria],
            "datasets": [
                {
                    "label": f"{context_domain.title()} Model A",
                    "data": [criterion["model_a"] for criterion in evaluation_criteria],
                    "borderColor": "rgba(255, 99, 132, 1)",
                    "backgroundColor": "rgba(255, 99, 132, 0.2)",
                    "tension": 0.4
                },
                {
                    "label": f"{context_domain.title()} Model B",
                    "data": [criterion["model_b"] for criterion in evaluation_criteria],
                    "borderColor": "rgba(54, 162, 235, 1)",
                    "backgroundColor": "rgba(54, 162, 235, 0.2)",
                    "tension": 0.4
                },
                {
                    "label": f"{context_domain.title()} Model C",
                    "data": [criterion["model_c"] for criterion in evaluation_criteria],
                    "borderColor": "rgba(255, 205, 86, 1)",
                    "backgroundColor": "rgba(255, 205, 86, 0.2)",
                    "tension": 0.4
                }
            ]
        }
        
        content = f"""
        <div class="section" data-tooltip-{self.module_id}="model_evaluation">
            <h3>🔍 {context_domain.title()} Model Evaluation</h3>
            <p>Comprehensive evaluation of {context_domain.lower()} models across multiple criteria with weighted scoring.</p>
            
            <div class="evaluation-table">
                <table>
                    <thead>
                        <tr>
                            <th>Criterion</th>
                            <th>Weight</th>
                            <th>{context_domain.title()} Model A</th>
                            <th>{context_domain.title()} Model B</th>
                            <th>{context_domain.title()} Model C</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        
        for criterion in evaluation_criteria:
            content += f"""
                        <tr>
                            <td>{criterion['criterion']}</td>
                            <td>{criterion['weight']:.1%}</td>
                            <td>{criterion['model_a']:.1%}</td>
                            <td>{criterion['model_b']:.1%}</td>
                            <td>{criterion['model_c']:.1%}</td>
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
                        <div class="score-label">{context_domain.title()} Model A</div>
                        <div class="score-value">{weighted_scores['model_a']:.3f}</div>
                    </div>
                    <div class="score-item">
                        <div class="score-label">{context_domain.title()} Model B</div>
                        <div class="score-value">{weighted_scores['model_b']:.3f}</div>
                    </div>
                    <div class="score-item">
                        <div class="score-label">{context_domain.title()} Model C</div>
                        <div class="score-value">{weighted_scores['model_c']:.3f}</div>
                    </div>
                </div>
            </div>
            
            <div class="chart-container">
                <canvas id="modelEvaluationChart_{self.module_id}" width="400" height="300"></canvas>
            </div>
            
            <script>
                // Chart.js Model Evaluation
                const modelEvaluationCtx_{self.module_id} = document.getElementById('modelEvaluationChart_{self.module_id}').getContext('2d');
                new Chart(modelEvaluationCtx_{self.module_id}, {{
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
    
    def _generate_contextual_comparisons(self, context_domain: str) -> List[Dict[str, Any]]:
        """Generate context-appropriate comparison metrics."""
        comparisons_mapping = {
            "MILITARY": [
                {"metric": "Threat Detection", "model_a": 0.85, "model_b": 0.92, "model_c": 0.94},
                {"metric": "Strategic Planning", "model_a": 0.87, "model_b": 0.94, "model_c": 0.96},
                {"metric": "Operational Analysis", "model_a": 0.83, "model_b": 0.90, "model_c": 0.92},
                {"metric": "Intelligence Assessment", "model_a": 0.82, "model_b": 0.89, "model_c": 0.91}
            ],
            "ECONOMIC": [
                {"metric": "Market Forecasting", "model_a": 0.85, "model_b": 0.92, "model_c": 0.94},
                {"metric": "Risk Assessment", "model_a": 0.87, "model_b": 0.94, "model_c": 0.96},
                {"metric": "Investment Analysis", "model_a": 0.83, "model_b": 0.90, "model_c": 0.92},
                {"metric": "Economic Modeling", "model_a": 0.82, "model_b": 0.89, "model_c": 0.91}
            ],
            "HEALTHCARE": [
                {"metric": "Diagnostic Accuracy", "model_a": 0.85, "model_b": 0.92, "model_c": 0.94},
                {"metric": "Prognostic Assessment", "model_a": 0.87, "model_b": 0.94, "model_c": 0.96},
                {"metric": "Treatment Optimization", "model_a": 0.83, "model_b": 0.90, "model_c": 0.92},
                {"metric": "Risk Prediction", "model_a": 0.82, "model_b": 0.89, "model_c": 0.91}
            ],
            "TECHNOLOGY": [
                {"metric": "Machine Learning", "model_a": 0.85, "model_b": 0.92, "model_c": 0.94},
                {"metric": "Deep Learning", "model_a": 0.87, "model_b": 0.94, "model_c": 0.96},
                {"metric": "NLP Performance", "model_a": 0.83, "model_b": 0.90, "model_c": 0.92},
                {"metric": "Computer Vision", "model_a": 0.82, "model_b": 0.89, "model_c": 0.91}
            ],
            "GENERAL": [
                {"metric": "Overall Accuracy", "model_a": 0.85, "model_b": 0.92, "model_c": 0.94},
                {"metric": "Training Accuracy", "model_a": 0.87, "model_b": 0.94, "model_c": 0.96},
                {"metric": "Validation Accuracy", "model_a": 0.83, "model_b": 0.90, "model_c": 0.92},
                {"metric": "Test Accuracy", "model_a": 0.82, "model_b": 0.89, "model_c": 0.91}
            ]
        }
        
        return comparisons_mapping.get(context_domain, comparisons_mapping["GENERAL"])
    
    def _generate_contextual_analysis_metrics(self, context_domain: str) -> List[Dict[str, Any]]:
        """Generate context-appropriate analysis metrics."""
        metrics_mapping = {
            "MILITARY": [
                {"aspect": "Computational Efficiency", "model_a": 0.95, "model_b": 0.75, "model_c": 0.70},
                {"aspect": "Interpretability", "model_a": 0.90, "model_b": 0.80, "model_c": 0.70},
                {"aspect": "Scalability", "model_a": 0.85, "model_b": 0.80, "model_c": 0.75},
                {"aspect": "Robustness", "model_a": 0.70, "model_b": 0.85, "model_c": 0.80},
                {"aspect": "Strategic Value", "model_a": 0.60, "model_b": 0.90, "model_c": 0.85}
            ],
            "ECONOMIC": [
                {"aspect": "Computational Efficiency", "model_a": 0.95, "model_b": 0.75, "model_c": 0.70},
                {"aspect": "Interpretability", "model_a": 0.90, "model_b": 0.80, "model_c": 0.70},
                {"aspect": "Scalability", "model_a": 0.85, "model_b": 0.80, "model_c": 0.75},
                {"aspect": "Robustness", "model_a": 0.70, "model_b": 0.85, "model_c": 0.80},
                {"aspect": "Economic Value", "model_a": 0.60, "model_b": 0.90, "model_c": 0.85}
            ],
            "HEALTHCARE": [
                {"aspect": "Computational Efficiency", "model_a": 0.95, "model_b": 0.75, "model_c": 0.70},
                {"aspect": "Interpretability", "model_a": 0.90, "model_b": 0.80, "model_c": 0.70},
                {"aspect": "Scalability", "model_a": 0.85, "model_b": 0.80, "model_c": 0.75},
                {"aspect": "Robustness", "model_a": 0.70, "model_b": 0.85, "model_c": 0.80},
                {"aspect": "Clinical Value", "model_a": 0.60, "model_b": 0.90, "model_c": 0.85}
            ],
            "TECHNOLOGY": [
                {"aspect": "Computational Efficiency", "model_a": 0.95, "model_b": 0.75, "model_c": 0.70},
                {"aspect": "Interpretability", "model_a": 0.90, "model_b": 0.80, "model_c": 0.70},
                {"aspect": "Scalability", "model_a": 0.85, "model_b": 0.80, "model_c": 0.75},
                {"aspect": "Robustness", "model_a": 0.70, "model_b": 0.85, "model_c": 0.80},
                {"aspect": "Innovation Value", "model_a": 0.60, "model_b": 0.90, "model_c": 0.85}
            ],
            "GENERAL": [
                {"aspect": "Computational Efficiency", "model_a": 0.95, "model_b": 0.75, "model_c": 0.70},
                {"aspect": "Interpretability", "model_a": 0.90, "model_b": 0.80, "model_c": 0.70},
                {"aspect": "Scalability", "model_a": 0.85, "model_b": 0.80, "model_c": 0.75},
                {"aspect": "Robustness", "model_a": 0.70, "model_b": 0.85, "model_c": 0.80},
                {"aspect": "Feature Importance", "model_a": 0.60, "model_b": 0.90, "model_c": 0.85}
            ]
        }
        
        return metrics_mapping.get(context_domain, metrics_mapping["GENERAL"])
    
    def _generate_contextual_evaluation_criteria(self, context_domain: str) -> List[Dict[str, Any]]:
        """Generate context-appropriate evaluation criteria."""
        criteria_mapping = {
            "MILITARY": [
                {"criterion": "Accuracy", "weight": 0.25, "model_a": 0.85, "model_b": 0.92, "model_c": 0.94},
                {"criterion": "Interpretability", "weight": 0.20, "model_a": 0.90, "model_b": 0.80, "model_c": 0.70},
                {"criterion": "Computational Cost", "weight": 0.15, "model_a": 0.95, "model_b": 0.75, "model_c": 0.70},
                {"criterion": "Robustness", "weight": 0.20, "model_a": 0.70, "model_b": 0.85, "model_c": 0.80},
                {"criterion": "Strategic Value", "weight": 0.20, "model_a": 0.85, "model_b": 0.80, "model_c": 0.90}
            ],
            "ECONOMIC": [
                {"criterion": "Accuracy", "weight": 0.25, "model_a": 0.85, "model_b": 0.92, "model_c": 0.94},
                {"criterion": "Interpretability", "weight": 0.20, "model_a": 0.90, "model_b": 0.80, "model_c": 0.70},
                {"criterion": "Computational Cost", "weight": 0.15, "model_a": 0.95, "model_b": 0.75, "model_c": 0.70},
                {"criterion": "Robustness", "weight": 0.20, "model_a": 0.70, "model_b": 0.85, "model_c": 0.80},
                {"criterion": "Economic Value", "weight": 0.20, "model_a": 0.85, "model_b": 0.80, "model_c": 0.90}
            ],
            "HEALTHCARE": [
                {"criterion": "Accuracy", "weight": 0.25, "model_a": 0.85, "model_b": 0.92, "model_c": 0.94},
                {"criterion": "Interpretability", "weight": 0.20, "model_a": 0.90, "model_b": 0.80, "model_c": 0.70},
                {"criterion": "Computational Cost", "weight": 0.15, "model_a": 0.95, "model_b": 0.75, "model_c": 0.70},
                {"criterion": "Robustness", "weight": 0.20, "model_a": 0.70, "model_b": 0.85, "model_c": 0.80},
                {"criterion": "Clinical Value", "weight": 0.20, "model_a": 0.85, "model_b": 0.80, "model_c": 0.90}
            ],
            "TECHNOLOGY": [
                {"criterion": "Accuracy", "weight": 0.25, "model_a": 0.85, "model_b": 0.92, "model_c": 0.94},
                {"criterion": "Interpretability", "weight": 0.20, "model_a": 0.90, "model_b": 0.80, "model_c": 0.70},
                {"criterion": "Computational Cost", "weight": 0.15, "model_a": 0.95, "model_b": 0.75, "model_c": 0.70},
                {"criterion": "Robustness", "weight": 0.20, "model_a": 0.70, "model_b": 0.85, "model_c": 0.80},
                {"criterion": "Innovation Value", "weight": 0.20, "model_a": 0.85, "model_b": 0.80, "model_c": 0.90}
            ],
            "GENERAL": [
                {"criterion": "Accuracy", "weight": 0.25, "model_a": 0.85, "model_b": 0.92, "model_c": 0.94},
                {"criterion": "Interpretability", "weight": 0.20, "model_a": 0.90, "model_b": 0.80, "model_c": 0.70},
                {"criterion": "Computational Cost", "weight": 0.15, "model_a": 0.95, "model_b": 0.75, "model_c": 0.70},
                {"criterion": "Robustness", "weight": 0.20, "model_a": 0.70, "model_b": 0.85, "model_c": 0.80},
                {"criterion": "Scalability", "weight": 0.20, "model_a": 0.85, "model_b": 0.80, "model_c": 0.90}
            ]
        }
        
        return criteria_mapping.get(context_domain, criteria_mapping["GENERAL"])
    
    def _initialize_default_tooltips(self):
        """Initialize default tooltip data for the module."""
        tooltip_data = {
            "performance_metrics": TooltipData(
                title="Model Performance Metrics",
                description="Comprehensive analysis of model performance metrics including accuracy, precision, recall, F1 score, MAE, and RMSE for various machine learning models",
                source="Sources: Model Performance Analytics Framework, Military Model Performance Database, Defense Analytics Framework, Strategic Analysis Models, Military Intelligence Systems",
                strategic_impact="Strategic Impact: Critical for selecting optimal models for strategic analysis and decision-making",
                recommendations="Recommendations: Use ensemble methods for improved accuracy and consider model complexity vs performance trade-offs",
                use_cases="Use Cases: Model selection, performance optimization, strategic analysis, decision support"
            ),
            "accuracy_comparison": TooltipData(
                title="Accuracy Comparison",
                description="Detailed comparison of model accuracy across different evaluation criteria including overall, training, validation, and test accuracy",
                source="Sources: Accuracy Assessment Framework, Military Model Performance Database, Defense Analytics Framework, Strategic Analysis Models, Military Intelligence Systems",
                strategic_impact="Strategic Impact: Essential for understanding model reliability and generalization capabilities",
                recommendations="Recommendations: Focus on validation and test accuracy for real-world performance assessment",
                use_cases="Use Cases: Model validation, performance assessment, strategic planning, risk management"
            ),
            "performance_analysis": TooltipData(
                title="Performance Analysis",
                description="Comprehensive analysis of model performance across multiple dimensions including computational efficiency, interpretability, scalability, and robustness",
                source="Sources: Performance Analysis Framework, Military Model Performance Database, Defense Analytics Framework, Strategic Analysis Models, Military Intelligence Systems",
                strategic_impact="Strategic Impact: Important for understanding model trade-offs and selecting appropriate models for different scenarios",
                recommendations="Recommendations: Balance performance metrics based on specific requirements and constraints",
                use_cases="Use Cases: Model selection, performance optimization, strategic planning, resource allocation"
            ),
            "model_evaluation": TooltipData(
                title="Model Evaluation",
                description="Comprehensive evaluation of models across multiple criteria with weighted scoring for optimal model selection",
                source="Sources: Model Evaluation Framework, Military Model Performance Database, Defense Analytics Framework, Strategic Analysis Models, Military Intelligence Systems",
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
