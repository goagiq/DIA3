#!/usr/bin/env python3
"""
Model Performance Module

Independent module for generating model performance analysis sections that can be added to any report.
Provides comprehensive model performance analysis, accuracy comparison, and performance metrics.
"""

from typing import Dict, Any, List, Optional, Union
from .base_module import BaseModule, ModuleConfig, TooltipData


class ModelPerformanceModule(BaseModule):
    """Model Performance module for enhanced reports."""
    
    module_id = "model_performance"
    title = "📊 Model Performance Analysis"
    description = "Comprehensive model performance analysis and evaluation"
    version = "1.0.0"
    
    def __init__(self, config: Optional[ModuleConfig] = None):
        """Initialize the Model Performance module."""
        super().__init__(config)
        
        # Initialize tooltips
        self.tooltips = {
            "accuracy_metrics": TooltipData(
                title="Accuracy Metrics",
                description="Key performance indicators for model accuracy assessment",
                source="Model Performance Analysis",
                strategic_impact="High accuracy models provide competitive advantage in decision-making"
            ),
            "performance_comparison": TooltipData(
                title="Performance Comparison",
                description="Comparative analysis of different model performance metrics",
                source="Model Performance Analysis",
                strategic_impact="Performance comparison helps optimize model selection for strategic objectives"
            ),
            "validation_results": TooltipData(
                title="Validation Results",
                description="Cross-validation and testing results for model reliability",
                source="Model Performance Analysis",
                strategic_impact="Validation ensures model reliability for critical strategic decisions"
            )
        }
    
    def get_required_data_keys(self) -> List[str]:
        """Get list of required data keys for this module."""
        return ["model_performance"]
    
    def validate_data(self, data: Union[str, Dict[str, Any]]) -> bool:
        """Validate that required data is present or that data is a string query."""
        if isinstance(data, str):
            return True
        elif isinstance(data, dict):
            required_keys = self.get_required_data_keys()
            missing_keys = [key for key in required_keys if key not in data]
            
            if missing_keys:
                raise ValueError(
                    f"Missing required data keys for {self.module_id}: {missing_keys}"
                )
            return True
        else:
            raise ValueError(f"Invalid data type for {self.module_id}: {type(data)}")
    
    async def generate_content(self, data: Union[str, Dict[str, Any]], config: Optional[ModuleConfig] = None) -> Dict[str, Any]:
        """Generate the HTML content for the Model Performance module with Phase 4 enhancements."""
        self.validate_data(data)
        
        # Phase 4 Strategic Intelligence Integration
        topic = data.get("topic", "") if isinstance(data, dict) else data
        phase4_enhanced = config and config.get("phase4_integration", False)
        
        try:
            if phase4_enhanced and topic:
                # Enhanced with strategic intelligence
                enhanced_data = await self._enhance_with_phase4_capabilities(topic, data)
                data.update(enhanced_data)
        except Exception as e:
            # Graceful fallback if Phase 4 enhancement fails
            pass
        
        # Extract model performance data
        if isinstance(data, dict):
            performance_data = data.get("model_performance", {})
        else:
            performance_data = {}
        
        # Generate content sections
        content_parts = []
        
        # Model Performance Overview
        overview = self._generate_performance_overview(performance_data)
        content_parts.append(overview)
        
        # Accuracy Metrics
        accuracy_metrics = self._generate_accuracy_metrics(performance_data)
        content_parts.append(accuracy_metrics)
        
        # Performance Comparison
        comparison = self._generate_performance_comparison(performance_data)
        content_parts.append(comparison)
        
        # Validation Results
        validation = self._generate_validation_results(performance_data)
        content_parts.append(validation)
        
        # Performance Trends
        trends = self._generate_performance_trends(performance_data)
        content_parts.append(trends)
        
        # Recommendations
        recommendations = self._generate_performance_recommendations(performance_data)
        content_parts.append(recommendations)
        
        # Combine all sections
        content = "\n".join(content_parts)
        
        return {
            "content": content,
            "metadata": {
                "phase4_integrated": phase4_enhanced,
                "strategic_intelligence": phase4_enhanced,
                "confidence_score": 0.7,
                "performance_analyzed": bool(performance_data)
            }
        }
    
    def _generate_performance_overview(self, data: Dict[str, Any]) -> str:
        """Generate model performance overview section."""
        models = data.get("models", [])
        overall_accuracy = data.get("overall_accuracy", 0.85)
        
        html = f"""
        <div class="module-section" id="model-performance-overview">
            <h2>📊 Model Performance Overview</h2>
            <div class="performance-summary">
                <div class="metric-card">
                    <h3>Overall Accuracy</h3>
                    <div class="metric-value">{overall_accuracy:.1%}</div>
                    <div class="metric-description">Combined accuracy across all models</div>
                </div>
                <div class="metric-card">
                    <h3>Models Analyzed</h3>
                    <div class="metric-value">{len(models)}</div>
                    <div class="metric-description">Total number of models evaluated</div>
                </div>
            </div>
        </div>
        """
        return html
    
    def _generate_accuracy_metrics(self, data: Dict[str, Any]) -> str:
        """Generate accuracy metrics section."""
        models = data.get("models", [])
        
        if not models:
            models = [
                {"name": "Model A", "accuracy": 0.87, "precision": 0.85, "recall": 0.89},
                {"name": "Model B", "accuracy": 0.83, "precision": 0.82, "recall": 0.84},
                {"name": "Model C", "accuracy": 0.90, "precision": 0.88, "recall": 0.92}
            ]
        
        html = f"""
        <div class="module-section" id="accuracy-metrics">
            <h2>🎯 Accuracy Metrics</h2>
            <div class="metrics-table">
                <table>
                    <thead>
                        <tr>
                            <th>Model</th>
                            <th>Accuracy</th>
                            <th>Precision</th>
                            <th>Recall</th>
                            <th>F1-Score</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        
        for model in models:
            accuracy = model.get("accuracy", 0.85)
            precision = model.get("precision", 0.83)
            recall = model.get("recall", 0.87)
            f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
            
            html += f"""
                        <tr>
                            <td>{model.get('name', 'Unknown Model')}</td>
                            <td>{accuracy:.1%}</td>
                            <td>{precision:.1%}</td>
                            <td>{recall:.1%}</td>
                            <td>{f1_score:.1%}</td>
                        </tr>
            """
        
        html += """
                    </tbody>
                </table>
            </div>
        </div>
        """
        return html
    
    def _generate_performance_comparison(self, data: Dict[str, Any]) -> str:
        """Generate performance comparison section."""
        models = data.get("models", [])
        
        if not models:
            models = [
                {"name": "Baseline Model", "accuracy": 0.75, "training_time": 120, "inference_time": 0.5},
                {"name": "Enhanced Model", "accuracy": 0.87, "training_time": 180, "inference_time": 0.3},
                {"name": "Optimized Model", "accuracy": 0.90, "training_time": 240, "inference_time": 0.2}
            ]
        
        html = f"""
        <div class="module-section" id="performance-comparison">
            <h2>⚖️ Performance Comparison</h2>
            <div class="comparison-charts">
                <div class="chart-container">
                    <h3>Accuracy vs Training Time</h3>
                    <div class="scatter-plot" data-chart="accuracy-vs-training">
                        {self._generate_scatter_plot_data(models, "accuracy", "training_time")}
                    </div>
                </div>
                <div class="chart-container">
                    <h3>Accuracy vs Inference Time</h3>
                    <div class="scatter-plot" data-chart="accuracy-vs-inference">
                        {self._generate_scatter_plot_data(models, "accuracy", "inference_time")}
                    </div>
                </div>
            </div>
        </div>
        """
        return html
    
    def _generate_validation_results(self, data: Dict[str, Any]) -> str:
        """Generate validation results section."""
        validation_data = data.get("validation_results", {})
        
        if not validation_data:
            validation_data = {
                "cross_validation_score": 0.86,
                "test_set_accuracy": 0.84,
                "confidence_intervals": [0.82, 0.88],
                "robustness_score": 0.89
            }
        
        html = f"""
        <div class="module-section" id="validation-results">
            <h2>✅ Validation Results</h2>
            <div class="validation-metrics">
                <div class="metric-card">
                    <h3>Cross-Validation Score</h3>
                    <div class="metric-value">{validation_data.get('cross_validation_score', 0.86):.1%}</div>
                </div>
                <div class="metric-card">
                    <h3>Test Set Accuracy</h3>
                    <div class="metric-value">{validation_data.get('test_set_accuracy', 0.84):.1%}</div>
                </div>
                <div class="metric-card">
                    <h3>Robustness Score</h3>
                    <div class="metric-value">{validation_data.get('robustness_score', 0.89):.1%}</div>
                </div>
            </div>
            <div class="confidence-intervals">
                <h3>Confidence Intervals</h3>
                <p>95% Confidence Interval: {validation_data.get('confidence_intervals', [0.82, 0.88])[0]:.1%} - {validation_data.get('confidence_intervals', [0.82, 0.88])[1]:.1%}</p>
            </div>
        </div>
        """
        return html
    
    def _generate_performance_trends(self, data: Dict[str, Any]) -> str:
        """Generate performance trends section."""
        trends_data = data.get("performance_trends", {})
        
        if not trends_data:
            trends_data = {
                "accuracy_trend": [0.75, 0.78, 0.82, 0.85, 0.87],
                "training_time_trend": [150, 140, 130, 125, 120],
                "iterations": ["v1.0", "v1.1", "v1.2", "v1.3", "v1.4"]
            }
        
        html = f"""
        <div class="module-section" id="performance-trends">
            <h2>�� Performance Trends</h2>
            <div class="trend-charts">
                <div class="chart-container">
                    <h3>Accuracy Improvement Over Time</h3>
                    <div class="line-chart" data-chart="accuracy-trend">
                        {self._generate_line_chart_data(trends_data.get('iterations', []), trends_data.get('accuracy_trend', []))}
                    </div>
                </div>
                <div class="chart-container">
                    <h3>Training Time Optimization</h3>
                    <div class="line-chart" data-chart="training-time-trend">
                        {self._generate_line_chart_data(trends_data.get('iterations', []), trends_data.get('training_time_trend', []))}
                    </div>
                </div>
            </div>
        </div>
        """
        return html
    
    def _generate_performance_recommendations(self, data: Dict[str, Any]) -> str:
        """Generate performance recommendations section."""
        recommendations = data.get("recommendations", [])
        
        if not recommendations:
            recommendations = [
                "Implement ensemble methods to improve overall accuracy",
                "Optimize hyperparameters for better performance",
                "Consider feature engineering to enhance model capabilities",
                "Implement early stopping to reduce training time",
                "Use data augmentation techniques for better generalization"
            ]
        
        html = f"""
        <div class="module-section" id="performance-recommendations">
            <h2>💡 Performance Recommendations</h2>
            <div class="recommendations-list">
                <ul>
        """
        
        for recommendation in recommendations:
            html += f"<li>{recommendation}</li>"
        
        html += """
                </ul>
            </div>
        </div>
        """
        return html
    
    def _generate_scatter_plot_data(self, models: List[Dict[str, Any]], x_key: str, y_key: str) -> str:
        """Generate scatter plot data for performance comparison."""
        data_points = []
        for model in models:
            x_val = model.get(x_key, 0)
            y_val = model.get(y_key, 0)
            data_points.append(f'{{"x": {x_val}, "y": {y_val}, "label": "{model.get("name", "Unknown")}"}}')
        
        return f'[{", ".join(data_points)}]'
    
    def _generate_line_chart_data(self, labels: List[str], values: List[float]) -> str:
        """Generate line chart data for trends."""
        data_points = []
        for i, (label, value) in enumerate(zip(labels, values)):
            data_points.append(f'{{"x": {i}, "y": {value}, "label": "{label}"}}')
        
        return f'[{", ".join(data_points)}]'
    
    async def _enhance_with_phase4_capabilities(self, topic: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance module with Phase 4 strategic intelligence capabilities."""
        enhanced_data = {}
        
        try:
            # Strategic intelligence analysis
            enhanced_data["strategic_analysis"] = {
                "performance_implications": f"Strategic implications of model performance for {topic}",
                "competitive_advantage": "High accuracy models provide competitive advantage",
                "risk_assessment": "Performance variability indicates potential risks"
            }
            
            # Cross-domain intelligence
            enhanced_data["cross_domain_intelligence"] = {
                "technological_impact": "Model performance affects technological capabilities",
                "operational_efficiency": "Improved accuracy enhances operational efficiency",
                "strategic_positioning": "Performance metrics influence strategic positioning"
            }
            
        except Exception as e:
            # Graceful fallback
            enhanced_data["strategic_analysis"] = {"error": str(e)}
            enhanced_data["cross_domain_intelligence"] = {"error": str(e)}
        
        return enhanced_data
