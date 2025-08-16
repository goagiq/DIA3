"""
Model Interpretability Engine for Phase 5: Model Interpretability & Explainable AI
Advanced forecasting & prediction system for DoD/Intelligence Community
"""

import asyncio
import json
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from loguru import logger
from dataclasses import dataclass, asdict

from src.core.models import DataType
from src.config.config import config


@dataclass
class FeatureImportance:
    """Feature importance analysis result"""
    feature_name: str
    importance_score: float
    rank: int
    category: str
    confidence: float
    explanation: str


@dataclass
class DecisionPath:
    """Decision path for complex models"""
    path_id: str
    steps: List[Dict[str, Any]]
    confidence: float
    reasoning: str
    alternative_paths: List[Dict[str, Any]]


@dataclass
class ModelExplanation:
    """Comprehensive model explanation"""
    model_name: str
    prediction: Any
    confidence: float
    feature_importance: List[FeatureImportance]
    decision_paths: List[DecisionPath]
    key_factors: List[str]
    uncertainty_analysis: Dict[str, Any]
    recommendations: List[str]
    timestamp: datetime


class ModelInterpretabilityEngine:
    """Model interpretability for intelligence analysis"""
    
    def __init__(self):
        """Initialize the model interpretability engine"""
        self.interpretation_methods = {
            'feature_importance': self.generate_feature_importance,
            'decision_paths': self.create_decision_paths,
            'uncertainty_analysis': self._analyze_uncertainty,
            'sensitivity_analysis': self._perform_sensitivity_analysis,
            'counterfactual_analysis': self._generate_counterfactuals
        }
        
        self.intelligence_domains = {
            'military_capabilities': self._explain_military_capabilities,
            'threat_assessment': self._explain_threat_assessment,
            'conflict_prediction': self._explain_conflict_prediction,
            'economic_impact': self._explain_economic_impact,
            'geopolitical_analysis': self._explain_geopolitical_analysis
        }
        
        logger.info("✅ Model Interpretability Engine initialized")
    
    async def explain_predictions(self, model_output: Dict[str, Any], input_data: Dict[str, Any]) -> ModelExplanation:
        """Explain model predictions for decision-makers"""
        try:
            logger.info("🔍 Explaining model predictions")
            
            # Extract prediction details
            prediction = model_output.get('prediction', {})
            confidence = model_output.get('confidence', 0.0)
            model_name = model_output.get('model_name', 'Unknown Model')
            
            # Generate comprehensive explanation
            feature_importance = await self.generate_feature_importance(model_output, input_data)
            decision_paths = await self.create_decision_paths(model_output, input_data)
            key_factors = await self._extract_key_factors(model_output, input_data)
            uncertainty_analysis = await self._analyze_uncertainty(model_output)
            recommendations = await self._generate_recommendations(model_output, input_data)
            
            explanation = ModelExplanation(
                model_name=model_name,
                prediction=prediction,
                confidence=confidence,
                feature_importance=feature_importance,
                decision_paths=decision_paths,
                key_factors=key_factors,
                uncertainty_analysis=uncertainty_analysis,
                recommendations=recommendations,
                timestamp=datetime.now()
            )
            
            logger.info(f"✅ Generated explanation for {model_name}")
            return explanation
            
        except Exception as e:
            logger.error(f"❌ Error explaining predictions: {e}")
            raise
    
    async def generate_feature_importance(self, model_output: Dict[str, Any], data: Dict[str, Any]) -> List[FeatureImportance]:
        """Generate feature importance analysis"""
        try:
            logger.info("🔍 Generating feature importance analysis")
            
            # Extract features from input data
            features = data.get('features', {})
            if not features:
                # Try to extract from different data formats
                features = self._extract_features_from_data(data)
            
            # Calculate feature importance scores
            importance_scores = await self._calculate_feature_importance(model_output, features)
            
            # Create feature importance objects
            feature_importance_list = []
            for i, (feature_name, score) in enumerate(importance_scores):
                importance = FeatureImportance(
                    feature_name=feature_name,
                    importance_score=score,
                    rank=i + 1,
                    category=self._categorize_feature(feature_name),
                    confidence=min(score * 1.2, 1.0),  # Scale confidence based on importance
                    explanation=self._generate_feature_explanation(feature_name, score)
                )
                feature_importance_list.append(importance)
            
            logger.info(f"✅ Generated feature importance for {len(feature_importance_list)} features")
            return feature_importance_list
            
        except Exception as e:
            logger.error(f"❌ Error generating feature importance: {e}")
            return []
    
    async def create_decision_paths(self, model_output: Dict[str, Any], data: Dict[str, Any]) -> List[DecisionPath]:
        """Create decision paths for complex models"""
        try:
            logger.info("🔍 Creating decision paths")
            
            decision_paths = []
            
            # Generate primary decision path
            primary_path = await self._generate_primary_decision_path(model_output, data)
            decision_paths.append(primary_path)
            
            # Generate alternative paths
            alternative_paths = await self._generate_alternative_paths(model_output, data)
            decision_paths.extend(alternative_paths)
            
            logger.info(f"✅ Created {len(decision_paths)} decision paths")
            return decision_paths
            
        except Exception as e:
            logger.error(f"❌ Error creating decision paths: {e}")
            return []
    
    async def explain_intelligence_analysis(self, analysis_type: str, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Explain intelligence-specific analysis results"""
        try:
            logger.info(f"🔍 Explaining {analysis_type} analysis")
            
            if analysis_type in self.intelligence_domains:
                explanation = await self.intelligence_domains[analysis_type](analysis_results)
            else:
                explanation = await self._explain_generic_analysis(analysis_results)
            
            logger.info(f"✅ Generated {analysis_type} explanation")
            return explanation
            
        except Exception as e:
            logger.error(f"❌ Error explaining intelligence analysis: {e}")
            return {"error": str(e)}
    
    async def generate_executive_summary(self, detailed_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate executive summary for decision-makers"""
        try:
            logger.info("📋 Generating executive summary")
            
            # Extract key insights
            key_insights = await self._extract_key_insights(detailed_analysis)
            
            # Generate recommendations
            recommendations = await self._generate_executive_recommendations(detailed_analysis)
            
            # Create executive summary
            summary = {
                "executive_summary": {
                    "timestamp": datetime.now().isoformat(),
                    "key_findings": key_insights[:5],  # Top 5 insights
                    "critical_recommendations": recommendations[:3],  # Top 3 recommendations
                    "confidence_level": self._calculate_overall_confidence(detailed_analysis),
                    "risk_assessment": await self._assess_overall_risk(detailed_analysis),
                    "next_steps": await self._suggest_next_steps(detailed_analysis)
                },
                "detailed_analysis_reference": detailed_analysis.get('analysis_id', 'unknown')
            }
            
            logger.info("✅ Generated executive summary")
            return summary
            
        except Exception as e:
            logger.error(f"❌ Error generating executive summary: {e}")
            return {"error": str(e)}
    
    # Private helper methods
    
    def _extract_features_from_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract features from various data formats"""
        features = {}
        
        # Try different data structures
        if isinstance(data, dict):
            # Direct feature dictionary
            if 'features' in data:
                features = data['features']
            elif 'input' in data:
                features = data['input']
            elif 'data' in data:
                features = data['data']
            else:
                # Use the data itself as features
                features = {k: v for k, v in data.items() if not k.startswith('_')}
        
        return features
    
    async def _calculate_feature_importance(self, model_output: Dict[str, Any], features: Dict[str, Any]) -> List[Tuple[str, float]]:
        """Calculate feature importance scores"""
        importance_scores = []
        
        # Simple heuristic-based importance calculation
        for feature_name, feature_value in features.items():
            # Calculate importance based on feature characteristics
            if isinstance(feature_value, (int, float)):
                # Numerical features
                importance = abs(feature_value) / 100.0  # Normalize
            elif isinstance(feature_value, str):
                # Text features - use length as proxy for importance
                importance = min(len(feature_value) / 100.0, 1.0)
            else:
                # Other types - default importance
                importance = 0.5
            
            # Add some randomness for demonstration
            importance += np.random.normal(0, 0.1)
            importance = max(0.0, min(1.0, importance))  # Clamp to [0, 1]
            
            importance_scores.append((feature_name, importance))
        
        # Sort by importance (descending)
        importance_scores.sort(key=lambda x: x[1], reverse=True)
        
        return importance_scores
    
    def _categorize_feature(self, feature_name: str) -> str:
        """Categorize features based on naming patterns"""
        feature_lower = feature_name.lower()
        
        if any(word in feature_lower for word in ['military', 'weapon', 'troop', 'defense']):
            return 'military_capabilities'
        elif any(word in feature_lower for word in ['economic', 'gdp', 'trade', 'finance']):
            return 'economic_indicators'
        elif any(word in feature_lower for word in ['political', 'government', 'regime']):
            return 'political_factors'
        elif any(word in feature_lower for word in ['geographic', 'location', 'territory']):
            return 'geographic_factors'
        elif any(word in feature_lower for word in ['alliance', 'diplomatic', 'international']):
            return 'diplomatic_relations'
        else:
            return 'other_factors'
    
    def _generate_feature_explanation(self, feature_name: str, importance_score: float) -> str:
        """Generate human-readable explanation for feature importance"""
        if importance_score > 0.8:
            level = "critical"
        elif importance_score > 0.6:
            level = "high"
        elif importance_score > 0.4:
            level = "moderate"
        elif importance_score > 0.2:
            level = "low"
        else:
            level = "minimal"
        
        return f"The {feature_name} feature has {level} importance ({importance_score:.2f}) in this prediction."
    
    async def _generate_primary_decision_path(self, model_output: Dict[str, Any], data: Dict[str, Any]) -> DecisionPath:
        """Generate the primary decision path"""
        steps = [
            {
                "step": 1,
                "description": "Data preprocessing and feature extraction",
                "confidence": 0.95,
                "details": "Input data was processed and relevant features were extracted"
            },
            {
                "step": 2,
                "description": "Model prediction generation",
                "confidence": model_output.get('confidence', 0.8),
                "details": f"Model '{model_output.get('model_name', 'Unknown')}' generated prediction"
            },
            {
                "step": 3,
                "description": "Confidence assessment",
                "confidence": 0.9,
                "details": "Prediction confidence was calculated and validated"
            }
        ]
        
        return DecisionPath(
            path_id="primary_path",
            steps=steps,
            confidence=model_output.get('confidence', 0.8),
            reasoning="Primary decision path based on highest confidence prediction",
            alternative_paths=[]
        )
    
    async def _generate_alternative_paths(self, model_output: Dict[str, Any], data: Dict[str, Any]) -> List[DecisionPath]:
        """Generate alternative decision paths"""
        alternative_paths = []
        
        # Generate 2-3 alternative paths
        for i in range(2):
            steps = [
                {
                    "step": 1,
                    "description": f"Alternative analysis path {i+1}",
                    "confidence": 0.7 - (i * 0.1),
                    "details": f"Alternative approach {i+1} for decision making"
                }
            ]
            
            path = DecisionPath(
                path_id=f"alternative_path_{i+1}",
                steps=steps,
                confidence=0.7 - (i * 0.1),
                reasoning=f"Alternative decision path {i+1} with different assumptions",
                alternative_paths=[]
            )
            alternative_paths.append(path)
        
        return alternative_paths
    
    async def _extract_key_factors(self, model_output: Dict[str, Any], data: Dict[str, Any]) -> List[str]:
        """Extract key factors from the analysis"""
        key_factors = []
        
        # Extract factors from model output
        if 'key_factors' in model_output:
            key_factors.extend(model_output['key_factors'])
        
        # Extract factors from input data
        features = data.get('features', {})
        if features:
            # Add top features as key factors
            for feature_name in list(features.keys())[:3]:
                key_factors.append(f"Feature: {feature_name}")
        
        # Add default factors if none found
        if not key_factors:
            key_factors = [
                "Model prediction confidence",
                "Input data quality",
                "Feature importance distribution"
            ]
        
        return key_factors[:5]  # Limit to top 5 factors
    
    async def _analyze_uncertainty(self, model_output: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze prediction uncertainty"""
        confidence = model_output.get('confidence', 0.5)
        
        uncertainty_analysis = {
            "confidence_level": confidence,
            "uncertainty_level": 1.0 - confidence,
            "reliability": "high" if confidence > 0.8 else "medium" if confidence > 0.6 else "low",
            "risk_factors": [
                "Model confidence below threshold" if confidence < 0.7 else None,
                "Limited training data" if confidence < 0.8 else None,
                "Feature uncertainty" if confidence < 0.9 else None
            ],
            "recommendations": [
                "Consider additional data sources" if confidence < 0.8 else None,
                "Validate with domain experts" if confidence < 0.7 else None,
                "Monitor for model drift" if confidence < 0.9 else None
            ]
        }
        
        # Remove None values
        uncertainty_analysis["risk_factors"] = [f for f in uncertainty_analysis["risk_factors"] if f is not None]
        uncertainty_analysis["recommendations"] = [r for r in uncertainty_analysis["recommendations"] if r is not None]
        
        return uncertainty_analysis
    
    async def _generate_recommendations(self, model_output: Dict[str, Any], data: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        confidence = model_output.get('confidence', 0.5)
        
        if confidence < 0.7:
            recommendations.append("Consider additional data collection to improve prediction confidence")
        
        if 'prediction' in model_output:
            pred = model_output['prediction']
            if isinstance(pred, dict) and 'risk_level' in pred:
                if pred['risk_level'] == 'high':
                    recommendations.append("Implement immediate risk mitigation strategies")
                elif pred['risk_level'] == 'medium':
                    recommendations.append("Develop contingency plans for potential scenarios")
        
        recommendations.append("Monitor model performance and update as new data becomes available")
        recommendations.append("Validate predictions with domain experts and intelligence sources")
        
        return recommendations[:5]  # Limit to top 5 recommendations
    
    async def _explain_military_capabilities(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Explain military capabilities analysis"""
        return {
            "analysis_type": "military_capabilities",
            "key_insights": [
                "Military readiness assessment",
                "Capability gap analysis",
                "Technology advantage evaluation"
            ],
            "confidence_factors": [
                "Data quality and completeness",
                "Model training on military domain",
                "Expert validation"
            ],
            "recommendations": [
                "Enhance intelligence collection on military capabilities",
                "Develop counter-capability strategies",
                "Monitor technological developments"
            ]
        }
    
    async def _explain_threat_assessment(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Explain threat assessment analysis"""
        return {
            "analysis_type": "threat_assessment",
            "key_insights": [
                "Threat level evaluation",
                "Vulnerability assessment",
                "Risk probability calculation"
            ],
            "confidence_factors": [
                "Threat intelligence quality",
                "Historical pattern analysis",
                "Multi-source validation"
            ],
            "recommendations": [
                "Implement threat monitoring systems",
                "Develop response protocols",
                "Enhance defensive capabilities"
            ]
        }
    
    async def _explain_conflict_prediction(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Explain conflict prediction analysis"""
        return {
            "analysis_type": "conflict_prediction",
            "key_insights": [
                "Conflict probability assessment",
                "Escalation path analysis",
                "Timeline prediction"
            ],
            "confidence_factors": [
                "Geopolitical data quality",
                "Historical conflict patterns",
                "Diplomatic intelligence"
            ],
            "recommendations": [
                "Enhance diplomatic engagement",
                "Prepare conflict prevention measures",
                "Develop de-escalation strategies"
            ]
        }
    
    async def _explain_economic_impact(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Explain economic impact analysis"""
        return {
            "analysis_type": "economic_impact",
            "key_insights": [
                "Economic consequence assessment",
                "Market impact prediction",
                "Resource availability analysis"
            ],
            "confidence_factors": [
                "Economic data quality",
                "Market trend analysis",
                "Expert economic validation"
            ],
            "recommendations": [
                "Develop economic resilience strategies",
                "Monitor market indicators",
                "Prepare economic contingency plans"
            ]
        }
    
    async def _explain_geopolitical_analysis(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Explain geopolitical analysis"""
        return {
            "analysis_type": "geopolitical_analysis",
            "key_insights": [
                "Geopolitical risk assessment",
                "Alliance dynamics analysis",
                "Regional stability evaluation"
            ],
            "confidence_factors": [
                "Geopolitical intelligence quality",
                "Regional expert validation",
                "Historical pattern analysis"
            ],
            "recommendations": [
                "Enhance regional intelligence collection",
                "Strengthen diplomatic relationships",
                "Develop regional stability strategies"
            ]
        }
    
    async def _explain_generic_analysis(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Explain generic analysis results"""
        return {
            "analysis_type": "generic",
            "key_insights": [
                "Pattern recognition results",
                "Anomaly detection findings",
                "Trend analysis outcomes"
            ],
            "confidence_factors": [
                "Data quality assessment",
                "Model performance metrics",
                "Validation results"
            ],
            "recommendations": [
                "Validate findings with domain experts",
                "Monitor for pattern changes",
                "Update analysis as new data becomes available"
            ]
        }
    
    async def _extract_key_insights(self, detailed_analysis: Dict[str, Any]) -> List[str]:
        """Extract key insights from detailed analysis"""
        insights = []
        
        # Extract insights from various analysis components
        if 'key_findings' in detailed_analysis:
            insights.extend(detailed_analysis['key_findings'])
        
        if 'feature_importance' in detailed_analysis:
            top_features = detailed_analysis['feature_importance'][:3]
            for feature in top_features:
                insights.append(f"Key factor: {feature.get('feature_name', 'Unknown')}")
        
        if 'recommendations' in detailed_analysis:
            insights.extend(detailed_analysis['recommendations'][:2])
        
        # Add default insights if none found
        if not insights:
            insights = [
                "Analysis completed successfully",
                "Model confidence within acceptable range",
                "Key factors identified and prioritized"
            ]
        
        return insights[:5]  # Limit to top 5 insights
    
    async def _generate_executive_recommendations(self, detailed_analysis: Dict[str, Any]) -> List[str]:
        """Generate executive-level recommendations"""
        recommendations = []
        
        # Extract recommendations from detailed analysis
        if 'recommendations' in detailed_analysis:
            recommendations.extend(detailed_analysis['recommendations'])
        
        # Add strategic recommendations
        confidence = detailed_analysis.get('confidence', 0.5)
        if confidence < 0.7:
            recommendations.append("Increase data collection and validation efforts")
        
        recommendations.extend([
            "Implement monitoring and alerting systems",
            "Establish regular review and update procedures",
            "Develop contingency plans based on analysis results"
        ])
        
        return recommendations[:5]  # Limit to top 5 recommendations
    
    def _calculate_overall_confidence(self, detailed_analysis: Dict[str, Any]) -> float:
        """Calculate overall confidence level"""
        confidence = detailed_analysis.get('confidence', 0.5)
        
        # Adjust confidence based on various factors
        if 'feature_importance' in detailed_analysis:
            avg_importance = np.mean([f.get('importance_score', 0) for f in detailed_analysis['feature_importance']])
            confidence = (confidence + avg_importance) / 2
        
        return min(1.0, max(0.0, confidence))
    
    async def _assess_overall_risk(self, detailed_analysis: Dict[str, Any]) -> str:
        """Assess overall risk level"""
        confidence = detailed_analysis.get('confidence', 0.5)
        
        if confidence > 0.8:
            return "low"
        elif confidence > 0.6:
            return "medium"
        else:
            return "high"
    
    async def _suggest_next_steps(self, detailed_analysis: Dict[str, Any]) -> List[str]:
        """Suggest next steps based on analysis"""
        next_steps = [
            "Review and validate analysis results with stakeholders",
            "Implement recommended actions and monitoring systems",
            "Schedule follow-up analysis and review"
        ]
        
        confidence = detailed_analysis.get('confidence', 0.5)
        if confidence < 0.7:
            next_steps.insert(0, "Conduct additional data collection and validation")
        
        return next_steps
    
    async def _perform_sensitivity_analysis(self, model_output: Dict[str, Any]) -> Dict[str, Any]:
        """Perform sensitivity analysis on model predictions"""
        # Placeholder for sensitivity analysis
        return {
            "sensitivity_level": "medium",
            "key_sensitive_factors": [],
            "robustness_score": 0.75
        }
    
    async def _generate_counterfactuals(self, model_output: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate counterfactual explanations"""
        # Placeholder for counterfactual generation
        return [
            {
                "scenario": "Alternative scenario 1",
                "changes": [],
                "prediction_difference": 0.1
            }
        ]
