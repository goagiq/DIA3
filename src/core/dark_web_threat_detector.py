"""
Dark Web Threat Detection System

This module provides comprehensive dark web threat detection capabilities including:
- Pattern recognition for threat identification
- Anomaly detection for emerging threats
- Monte Carlo simulation for probability assessment
- Multi-source intelligence fusion
- Real-time threat monitoring
"""

import numpy as np
import asyncio
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from loguru import logger

from src.core.pattern_recognition.anomaly_detector import AnomalyDetector
from src.core.pattern_recognition.pattern_storage import PatternStorage
from src.core.monte_carlo.engine import MonteCarloEngine
from src.core.monte_carlo.config import MonteCarloConfig
from src.core.error_handler import with_error_handling


@dataclass
class DarkWebThreat:
    """Data class for representing dark web threats"""
    threat_id: str
    threat_type: str
    description: str
    source: str
    timestamp: datetime
    confidence_score: float
    severity_level: str
    indicators: List[str]
    probability: float
    impact_score: float
    mitigation_strategies: List[str]
    related_threats: List[str]


@dataclass
class ThreatAssessment:
    """Data class for threat assessment results"""
    threat_id: str
    probability_distribution: List[float]
    confidence_interval: Tuple[float, float]
    risk_score: float
    early_warning_indicators: List[str]
    recommended_actions: List[str]
    timeline_estimate: str


class DarkWebThreatDetector:
    """
    Comprehensive dark web threat detection system combining pattern recognition,
    anomaly detection, and Monte Carlo simulation for probability assessment.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or self._default_config()
        self.anomaly_detector = AnomalyDetector()
        self.pattern_storage = PatternStorage()
        self.monte_carlo_engine = MonteCarloEngine(MonteCarloConfig())
        
        # Threat databases
        self.known_threats = {}
        self.emerging_threats = {}
        self.threat_patterns = {}
        self.anomaly_thresholds = {}
        
        # Analysis results cache
        self.analysis_cache = {}
        self.threat_history = []
        
        logger.info("Dark Web Threat Detector initialized successfully")
    
    def _default_config(self) -> Dict[str, Any]:
        """Default configuration for the threat detector"""
        return {
            "anomaly_threshold": 0.85,
            "pattern_confidence_threshold": 0.75,
            "monte_carlo_simulations": 10000,
            "probability_confidence_level": 0.95,
            "threat_categories": [
                "cyber_attack",
                "data_breach",
                "ransomware",
                "apt_activity",
                "supply_chain_attack",
                "social_engineering",
                "insider_threat",
                "nation_state_activity"
            ],
            "data_sources": [
                "dark_web_forums",
                "paste_sites",
                "telegram_channels",
                "discord_servers",
                "irc_channels",
                "marketplaces",
                "social_media",
                "news_sources"
            ]
        }
    
    @with_error_handling("dark_web_threat_detection")
    async def detect_emerging_threats(
        self,
        data_sources: List[Dict[str, Any]],
        time_window: Optional[timedelta] = None
    ) -> Dict[str, Any]:
        """
        Detect emerging threats from dark web data sources using pattern recognition
        and anomaly detection.
        
        Args:
            data_sources: List of data source dictionaries containing threat data
            time_window: Time window for analysis (default: last 30 days)
            
        Returns:
            Dictionary containing detected threats and analysis results
        """
        try:
            logger.info("Starting dark web threat detection analysis")
            
            if not data_sources:
                return {"error": "No data sources provided"}
            
            time_window = time_window or timedelta(days=30)
            cutoff_time = datetime.now() - time_window
            
            # Extract and preprocess threat data
            threat_data = await self._extract_threat_data(data_sources, cutoff_time)
            
            # Perform pattern recognition analysis
            pattern_results = await self._analyze_threat_patterns(threat_data)
            
            # Perform anomaly detection
            anomaly_results = await self._detect_threat_anomalies(threat_data)
            
            # Identify emerging threats
            emerging_threats = await self._identify_emerging_threats(
                pattern_results, anomaly_results
            )
            
            # Assess threat probabilities using Monte Carlo simulation
            threat_assessments = await self._assess_threat_probabilities(emerging_threats)
            
            # Generate comprehensive report
            report = await self._generate_threat_report(
                emerging_threats, threat_assessments, pattern_results, anomaly_results
            )
            
            # Cache results
            self._cache_analysis_results(report)
            
            return report
            
        except Exception as e:
            logger.error(f"Dark web threat detection failed: {e}")
            return {"error": str(e)}
    
    async def _extract_threat_data(
        self,
        data_sources: List[Dict[str, Any]],
        cutoff_time: datetime
    ) -> List[Dict[str, Any]]:
        """Extract and preprocess threat data from various sources"""
        threat_data = []
        
        for source in data_sources:
            try:
                source_type = source.get("type", "unknown")
                source_data = source.get("data", [])
                
                for item in source_data:
                    # Filter by timestamp
                    item_timestamp = datetime.fromisoformat(item.get("timestamp", ""))
                    if item_timestamp < cutoff_time:
                        continue
                    
                    # Extract threat indicators
                    threat_indicators = self._extract_threat_indicators(item, source_type)
                    
                    if threat_indicators:
                        threat_data.append({
                            "source": source_type,
                            "timestamp": item_timestamp,
                            "content": item.get("content", ""),
                            "indicators": threat_indicators,
                            "metadata": item.get("metadata", {})
                        })
                        
            except Exception as e:
                logger.warning(f"Error processing data source {source.get('name', 'unknown')}: {e}")
                continue
        
        logger.info(f"Extracted {len(threat_data)} threat data points")
        return threat_data
    
    def _extract_threat_indicators(
        self,
        item: Dict[str, Any],
        source_type: str
    ) -> List[str]:
        """Extract threat indicators from data item"""
        indicators = []
        content = item.get("content", "").lower()
        
        # Define threat indicator patterns
        threat_patterns = {
            "cyber_attack": [
                "exploit", "vulnerability", "zero-day", "payload", "malware",
                "trojan", "backdoor", "rootkit", "keylogger", "ransomware"
            ],
            "data_breach": [
                "database dump", "credentials", "password", "email list",
                "personal data", "credit card", "ssn", "social security"
            ],
            "apt_activity": [
                "nation state", "government", "espionage", "cyber espionage",
                "advanced persistent threat", "apt", "state-sponsored"
            ],
            "supply_chain": [
                "supply chain", "vendor", "third party", "software update",
                "compromise", "backdoor", "malicious update"
            ]
        }
        
        # Check for threat indicators
        for threat_type, patterns in threat_patterns.items():
            for pattern in patterns:
                if pattern in content:
                    indicators.append(f"{threat_type}:{pattern}")
        
        # Add source-specific indicators
        if source_type == "marketplace":
            if any(word in content for word in ["sell", "buy", "price", "offer"]):
                indicators.append("marketplace_activity")
        
        return indicators
    
    async def _analyze_threat_patterns(
        self,
        threat_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze threat patterns using pattern recognition"""
        try:
            # Group data by time periods
            time_groups = self._group_data_by_time(threat_data)
            
            # Analyze patterns in each time group
            pattern_results = {}
            for time_period, data in time_groups.items():
                # Extract numerical features for pattern analysis
                features = self._extract_pattern_features(data)
                
                # Perform pattern recognition
                patterns = await self.pattern_storage.analyze_patterns(features)
                
                pattern_results[time_period] = {
                    "patterns": patterns,
                    "data_count": len(data),
                    "feature_vector": features
                }
            
            return pattern_results
            
        except Exception as e:
            logger.error(f"Pattern analysis failed: {e}")
            return {"error": str(e)}
    
    def _group_data_by_time(
        self,
        threat_data: List[Dict[str, Any]]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Group threat data by time periods"""
        time_groups = {}
        
        for item in threat_data:
            timestamp = item["timestamp"]
            # Group by day
            day_key = timestamp.strftime("%Y-%m-%d")
            
            if day_key not in time_groups:
                time_groups[day_key] = []
            
            time_groups[day_key].append(item)
        
        return time_groups
    
    def _extract_pattern_features(
        self,
        data: List[Dict[str, Any]]
    ) -> List[float]:
        """Extract numerical features for pattern analysis"""
        features = []
        
        if not data:
            return features
        
        # Count indicators by type
        indicator_counts = {}
        for item in data:
            for indicator in item.get("indicators", []):
                indicator_type = indicator.split(":")[0] if ":" in indicator else indicator
                indicator_counts[indicator_type] = indicator_counts.get(indicator_type, 0) + 1
        
        # Convert to feature vector
        for threat_type in self.config["threat_categories"]:
            features.append(indicator_counts.get(threat_type, 0))
        
        # Add temporal features
        timestamps = [item["timestamp"] for item in data]
        if timestamps:
            features.append(len(timestamps))  # Volume
            features.append(np.std([ts.hour for ts in timestamps]))  # Time spread
        
        return features
    
    async def _detect_threat_anomalies(
        self,
        threat_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Detect anomalies in threat data"""
        try:
            # Extract numerical data for anomaly detection
            numerical_data = []
            for item in threat_data:
                # Count indicators as numerical feature
                indicator_count = len(item.get("indicators", []))
                numerical_data.append(indicator_count)
            
            if len(numerical_data) < 3:
                return {"anomalies": [], "anomaly_score": 0.0}
            
            # Perform anomaly detection
            anomaly_result = await self.anomaly_detector.detect_anomalies(
                numerical_data, detection_method="combined"
            )
            
            # Map anomalies back to threat data
            anomalies = []
            if "anomalies" in anomaly_result:
                for anomaly in anomaly_result["anomalies"]:
                    if anomaly["index"] < len(threat_data):
                        threat_item = threat_data[anomaly["index"]]
                        anomalies.append({
                            "threat_data": threat_item,
                            "anomaly_score": anomaly.get("score", 0.0),
                            "severity": anomaly.get("severity", "medium")
                        })
            
            return {
                "anomalies": anomalies,
                "anomaly_score": anomaly_result.get("overall_score", 0.0),
                "detection_method": anomaly_result.get("method", "unknown")
            }
            
        except Exception as e:
            logger.error(f"Anomaly detection failed: {e}")
            return {"error": str(e)}
    
    async def _identify_emerging_threats(
        self,
        pattern_results: Dict[str, Any],
        anomaly_results: Dict[str, Any]
    ) -> List[DarkWebThreat]:
        """Identify emerging threats from pattern and anomaly analysis"""
        emerging_threats = []
        
        try:
            # Process anomalies as potential emerging threats
            for anomaly in anomaly_results.get("anomalies", []):
                threat_data = anomaly["threat_data"]
                
                # Create threat object
                threat = DarkWebThreat(
                    threat_id=str(uuid.uuid4()),
                    threat_type=self._classify_threat_type(threat_data),
                    description=self._generate_threat_description(threat_data),
                    source=threat_data["source"],
                    timestamp=threat_data["timestamp"],
                    confidence_score=anomaly["anomaly_score"],
                    severity_level=anomaly["severity"],
                    indicators=threat_data["indicators"],
                    probability=0.0,  # Will be calculated by Monte Carlo
                    impact_score=0.0,  # Will be calculated by Monte Carlo
                    mitigation_strategies=[],
                    related_threats=[]
                )
                
                emerging_threats.append(threat)
            
            # Process pattern-based threats
            pattern_threats = await self._extract_pattern_threats(pattern_results)
            emerging_threats.extend(pattern_threats)
            
            # Remove duplicates and sort by confidence
            unique_threats = self._deduplicate_threats(emerging_threats)
            unique_threats.sort(key=lambda x: x.confidence_score, reverse=True)
            
            logger.info(f"Identified {len(unique_threats)} emerging threats")
            return unique_threats
            
        except Exception as e:
            logger.error(f"Threat identification failed: {e}")
            return []
    
    def _classify_threat_type(self, threat_data: Dict[str, Any]) -> str:
        """Classify threat type based on indicators"""
        indicators = threat_data.get("indicators", [])
        
        # Count indicators by type
        type_counts = {}
        for indicator in indicators:
            if ":" in indicator:
                threat_type = indicator.split(":")[0]
                type_counts[threat_type] = type_counts.get(threat_type, 0) + 1
        
        # Return most common type
        if type_counts:
            return max(type_counts, key=type_counts.get)
        
        return "unknown"
    
    def _generate_threat_description(self, threat_data: Dict[str, Any]) -> str:
        """Generate threat description from data"""
        indicators = threat_data.get("indicators", [])
        source = threat_data.get("source", "unknown")
        
        if indicators:
            indicator_types = set()
            for indicator in indicators:
                if ":" in indicator:
                    indicator_types.add(indicator.split(":")[0])
            
            types_str = ", ".join(indicator_types)
            return f"Potential {types_str} activity detected from {source}"
        
        return f"Unusual activity detected from {source}"
    
    async def _extract_pattern_threats(
        self,
        pattern_results: Dict[str, Any]
    ) -> List[DarkWebThreat]:
        """Extract threats from pattern analysis results"""
        threats = []
        
        try:
            for time_period, result in pattern_results.items():
                if "patterns" in result and result["patterns"]:
                    # Create threat from significant pattern
                    threat = DarkWebThreat(
                        threat_id=str(uuid.uuid4()),
                        threat_type="pattern_based",
                        description=f"Pattern-based threat detected in {time_period}",
                        source="pattern_analysis",
                        timestamp=datetime.now(),
                        confidence_score=result["patterns"].get("confidence", 0.5),
                        severity_level="medium",
                        indicators=["pattern_detected"],
                        probability=0.0,
                        impact_score=0.0,
                        mitigation_strategies=[],
                        related_threats=[]
                    )
                    
                    threats.append(threat)
            
            return threats
            
        except Exception as e:
            logger.error(f"Pattern threat extraction failed: {e}")
            return []
    
    def _deduplicate_threats(self, threats: List[DarkWebThreat]) -> List[DarkWebThreat]:
        """Remove duplicate threats based on similarity"""
        unique_threats = []
        
        for threat in threats:
            is_duplicate = False
            
            for existing_threat in unique_threats:
                # Check similarity based on type, source, and indicators
                if (threat.threat_type == existing_threat.threat_type and
                    threat.source == existing_threat.source and
                    len(set(threat.indicators) & set(existing_threat.indicators)) > 0):
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                unique_threats.append(threat)
        
        return unique_threats
    
    async def _assess_threat_probabilities(
        self,
        emerging_threats: List[DarkWebThreat]
    ) -> Dict[str, ThreatAssessment]:
        """Assess threat probabilities using Monte Carlo simulation"""
        threat_assessments = {}
        
        try:
            for threat in emerging_threats:
                # Define simulation parameters based on threat characteristics
                simulation_params = self._define_simulation_parameters(threat)
                
                # Run Monte Carlo simulation
                simulation_result = await self.monte_carlo_engine.run_simulation(
                    parameters=simulation_params,
                    num_simulations=self.config["monte_carlo_simulations"]
                )
                
                # Analyze results
                if "results" in simulation_result:
                    results = simulation_result["results"]
                    
                    # Calculate probability distribution
                    probability_distribution = self._calculate_probability_distribution(results)
                    
                    # Calculate confidence interval
                    confidence_interval = self._calculate_confidence_interval(
                        results, self.config["probability_confidence_level"]
                    )
                    
                    # Calculate risk score
                    risk_score = self._calculate_risk_score(threat, results)
                    
                    # Generate assessment
                    assessment = ThreatAssessment(
                        threat_id=threat.threat_id,
                        probability_distribution=probability_distribution,
                        confidence_interval=confidence_interval,
                        risk_score=risk_score,
                        early_warning_indicators=self._identify_early_warning_indicators(threat),
                        recommended_actions=self._generate_recommended_actions(threat, risk_score),
                        timeline_estimate=self._estimate_threat_timeline(threat, results)
                    )
                    
                    threat_assessments[threat.threat_id] = assessment
                    
                    # Update threat with calculated values
                    threat.probability = confidence_interval[1]  # Upper bound
                    threat.impact_score = risk_score
                
        except Exception as e:
            logger.error(f"Threat probability assessment failed: {e}")
        
        return threat_assessments
    
    def _define_simulation_parameters(self, threat: DarkWebThreat) -> Dict[str, Any]:
        """Define Monte Carlo simulation parameters for threat assessment"""
        base_params = {
            "threat_confidence": threat.confidence_score,
            "threat_severity": self._severity_to_numeric(threat.severity_level),
            "indicator_count": len(threat.indicators),
            "source_reliability": self._assess_source_reliability(threat.source),
            "temporal_factors": self._calculate_temporal_factors(threat.timestamp)
        }
        
        # Add threat-specific parameters
        if "cyber_attack" in threat.threat_type:
            base_params.update({
                "attack_complexity": np.random.uniform(0.3, 0.9),
                "target_vulnerability": np.random.uniform(0.2, 0.8),
                "defense_effectiveness": np.random.uniform(0.4, 0.9)
            })
        elif "data_breach" in threat.threat_type:
            base_params.update({
                "data_sensitivity": np.random.uniform(0.5, 1.0),
                "breach_scale": np.random.uniform(0.1, 0.8),
                "detection_likelihood": np.random.uniform(0.2, 0.7)
            })
        
        return base_params
    
    def _severity_to_numeric(self, severity: str) -> float:
        """Convert severity level to numeric value"""
        severity_map = {
            "low": 0.25,
            "medium": 0.5,
            "high": 0.75,
            "critical": 1.0
        }
        return severity_map.get(severity, 0.5)
    
    def _assess_source_reliability(self, source: str) -> float:
        """Assess reliability of threat source"""
        reliability_map = {
            "dark_web_forums": 0.6,
            "paste_sites": 0.4,
            "telegram_channels": 0.7,
            "discord_servers": 0.5,
            "irc_channels": 0.3,
            "marketplaces": 0.8,
            "social_media": 0.3,
            "news_sources": 0.9
        }
        return reliability_map.get(source, 0.5)
    
    def _calculate_temporal_factors(self, timestamp: datetime) -> float:
        """Calculate temporal factors affecting threat probability"""
        time_diff = datetime.now() - timestamp
        hours_diff = time_diff.total_seconds() / 3600
        
        # Recent threats have higher probability
        if hours_diff < 24:
            return 1.0
        elif hours_diff < 168:  # 1 week
            return 0.8
        elif hours_diff < 720:  # 1 month
            return 0.6
        else:
            return 0.3
    
    def _calculate_probability_distribution(self, results: List[float]) -> List[float]:
        """Calculate probability distribution from simulation results"""
        if not results:
            return []
        
        # Create histogram of results
        hist, bins = np.histogram(results, bins=20, density=True)
        return hist.tolist()
    
    def _calculate_confidence_interval(
        self,
        results: List[float],
        confidence_level: float
    ) -> Tuple[float, float]:
        """Calculate confidence interval for simulation results"""
        if not results:
            return (0.0, 0.0)
        
        alpha = 1 - confidence_level
        lower_percentile = (alpha / 2) * 100
        upper_percentile = (1 - alpha / 2) * 100
        
        lower_bound = np.percentile(results, lower_percentile)
        upper_bound = np.percentile(results, upper_percentile)
        
        return (float(lower_bound), float(upper_bound))
    
    def _calculate_risk_score(self, threat: DarkWebThreat, results: List[float]) -> float:
        """Calculate risk score based on threat characteristics and simulation results"""
        if not results:
            return 0.0
        
        # Base risk factors
        severity_score = self._severity_to_numeric(threat.severity_level)
        confidence_score = threat.confidence_score
        indicator_score = min(len(threat.indicators) / 10.0, 1.0)
        
        # Simulation-based risk
        simulation_mean = np.mean(results)
        simulation_std = np.std(results)
        
        # Combined risk score
        risk_score = (
            0.3 * severity_score +
            0.2 * confidence_score +
            0.2 * indicator_score +
            0.3 * simulation_mean
        )
        
        return min(risk_score, 1.0)
    
    def _identify_early_warning_indicators(self, threat: DarkWebThreat) -> List[str]:
        """Identify early warning indicators for the threat"""
        indicators = []
        
        # Add threat-specific indicators
        if "cyber_attack" in threat.threat_type:
            indicators.extend([
                "Unusual network traffic patterns",
                "Failed login attempts",
                "Suspicious file downloads",
                "System performance degradation"
            ])
        elif "data_breach" in threat.threat_type:
            indicators.extend([
                "Unusual data access patterns",
                "Large data transfers",
                "Unauthorized account access",
                "Database performance issues"
            ])
        
        # Add general indicators
        indicators.extend([
            "Increased dark web chatter",
            "New threat actor activity",
            "Tool and technique evolution",
            "Target reconnaissance activity"
        ])
        
        return indicators
    
    def _generate_recommended_actions(
        self,
        threat: DarkWebThreat,
        risk_score: float
    ) -> List[str]:
        """Generate recommended actions based on threat and risk score"""
        actions = []
        
        if risk_score > 0.8:
            actions.extend([
                "Immediate threat response activation",
                "Enhanced monitoring and alerting",
                "Security team notification",
                "Incident response preparation"
            ])
        elif risk_score > 0.6:
            actions.extend([
                "Increased monitoring frequency",
                "Threat intelligence sharing",
                "Security controls review",
                "Staff awareness training"
            ])
        else:
            actions.extend([
                "Continued monitoring",
                "Threat intelligence collection",
                "Baseline security maintenance"
            ])
        
        return actions
    
    def _estimate_threat_timeline(self, threat: DarkWebThreat, results: List[float]) -> str:
        """Estimate timeline for threat materialization"""
        if not results:
            return "Unknown"
        
        # Use simulation results to estimate timeline
        mean_probability = np.mean(results)
        
        if mean_probability > 0.8:
            return "Immediate (0-24 hours)"
        elif mean_probability > 0.6:
            return "Short-term (1-7 days)"
        elif mean_probability > 0.4:
            return "Medium-term (1-4 weeks)"
        else:
            return "Long-term (1-6 months)"
    
    async def _generate_threat_report(
        self,
        emerging_threats: List[DarkWebThreat],
        threat_assessments: Dict[str, ThreatAssessment],
        pattern_results: Dict[str, Any],
        anomaly_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate comprehensive threat report"""
        try:
            report = {
                "report_id": str(uuid.uuid4()),
                "timestamp": datetime.now().isoformat(),
                "summary": {
                    "total_threats_detected": len(emerging_threats),
                    "high_risk_threats": len([t for t in emerging_threats if t.severity_level in ["high", "critical"]]),
                    "average_confidence": np.mean([t.confidence_score for t in emerging_threats]) if emerging_threats else 0.0,
                    "anomaly_score": anomaly_results.get("anomaly_score", 0.0)
                },
                "threats": [],
                "assessments": {},
                "recommendations": self._generate_overall_recommendations(emerging_threats, threat_assessments),
                "methodology": {
                    "pattern_analysis": "Applied pattern recognition to identify recurring threat patterns",
                    "anomaly_detection": "Used statistical and machine learning methods to detect unusual activity",
                    "monte_carlo_simulation": f"Performed {self.config['monte_carlo_simulations']} simulations for probability assessment"
                }
            }
            
            # Add threat details
            for threat in emerging_threats:
                threat_dict = {
                    "threat_id": threat.threat_id,
                    "threat_type": threat.threat_type,
                    "description": threat.description,
                    "source": threat.source,
                    "timestamp": threat.timestamp.isoformat(),
                    "confidence_score": threat.confidence_score,
                    "severity_level": threat.severity_level,
                    "indicators": threat.indicators,
                    "probability": threat.probability,
                    "impact_score": threat.impact_score
                }
                report["threats"].append(threat_dict)
            
            # Add assessment details
            for threat_id, assessment in threat_assessments.items():
                assessment_dict = {
                    "probability_distribution": assessment.probability_distribution,
                    "confidence_interval": assessment.confidence_interval,
                    "risk_score": assessment.risk_score,
                    "early_warning_indicators": assessment.early_warning_indicators,
                    "recommended_actions": assessment.recommended_actions,
                    "timeline_estimate": assessment.timeline_estimate
                }
                report["assessments"][threat_id] = assessment_dict
            
            return report
            
        except Exception as e:
            logger.error(f"Report generation failed: {e}")
            return {"error": str(e)}
    
    def _generate_overall_recommendations(
        self,
        threats: List[DarkWebThreat],
        assessments: Dict[str, ThreatAssessment]
    ) -> List[str]:
        """Generate overall recommendations based on all threats"""
        recommendations = []
        
        if not threats:
            recommendations.append("Continue monitoring for new threats")
            return recommendations
        
        # High-level recommendations based on threat landscape
        high_risk_count = len([t for t in threats if t.severity_level in ["high", "critical"]])
        
        if high_risk_count > 0:
            recommendations.append(f"Activate enhanced security posture due to {high_risk_count} high-risk threats")
            recommendations.append("Implement additional monitoring and alerting")
            recommendations.append("Review and update incident response procedures")
        
        # Recommendations based on threat types
        threat_types = [t.threat_type for t in threats]
        if "cyber_attack" in threat_types:
            recommendations.append("Strengthen network security controls")
            recommendations.append("Implement advanced threat detection")
        
        if "data_breach" in threat_types:
            recommendations.append("Enhance data protection measures")
            recommendations.append("Review access controls and permissions")
        
        # General recommendations
        recommendations.extend([
            "Share threat intelligence with partners",
            "Conduct security awareness training",
            "Update threat detection signatures",
            "Review and test incident response plans"
        ])
        
        return recommendations
    
    def _cache_analysis_results(self, report: Dict[str, Any]):
        """Cache analysis results for future reference"""
        try:
            cache_key = f"dark_web_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            self.analysis_cache[cache_key] = {
                "timestamp": datetime.now().isoformat(),
                "report": report
            }
            
            # Keep only recent results
            if len(self.analysis_cache) > 10:
                oldest_key = min(self.analysis_cache.keys())
                del self.analysis_cache[oldest_key]
                
        except Exception as e:
            logger.warning(f"Failed to cache analysis results: {e}")
    
    @with_error_handling("dark_web_monitoring")
    async def start_real_time_monitoring(
        self,
        data_sources: List[Dict[str, Any]],
        monitoring_interval: int = 3600  # 1 hour
    ) -> Dict[str, Any]:
        """
        Start real-time monitoring of dark web sources for emerging threats.
        
        Args:
            data_sources: List of data sources to monitor
            monitoring_interval: Monitoring interval in seconds
            
        Returns:
            Dictionary containing monitoring status and results
        """
        try:
            logger.info(f"Starting real-time dark web monitoring with {len(data_sources)} sources")
            
            monitoring_results = {
                "monitoring_id": str(uuid.uuid4()),
                "start_time": datetime.now().isoformat(),
                "data_sources": len(data_sources),
                "monitoring_interval": monitoring_interval,
                "status": "active",
                "results": []
            }
            
            # Start monitoring loop
            while True:
                try:
                    # Perform threat detection
                    detection_result = await self.detect_emerging_threats(data_sources)
                    
                    if "error" not in detection_result:
                        monitoring_results["results"].append({
                            "timestamp": datetime.now().isoformat(),
                            "threats_detected": len(detection_result.get("threats", [])),
                            "high_risk_count": len([t for t in detection_result.get("threats", []) 
                                                   if t.get("severity_level") in ["high", "critical"]])
                        })
                    
                    # Wait for next monitoring cycle
                    await asyncio.sleep(monitoring_interval)
                    
                except asyncio.CancelledError:
                    logger.info("Dark web monitoring cancelled")
                    break
                except Exception as e:
                    logger.error(f"Monitoring cycle failed: {e}")
                    await asyncio.sleep(60)  # Wait 1 minute before retrying
            
            monitoring_results["end_time"] = datetime.now().isoformat()
            monitoring_results["status"] = "completed"
            
            return monitoring_results
            
        except Exception as e:
            logger.error(f"Real-time monitoring failed: {e}")
            return {"error": str(e)}
