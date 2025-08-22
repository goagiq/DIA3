"""
Geopolitical Analyzer for Enhanced Report Generation System
Provides geopolitical analysis, regional risk assessment, and international relations analysis.
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum

logger = logging.getLogger(__name__)


class RegionType(Enum):
    """Geopolitical region types."""
    CONTINENT = "continent"
    COUNTRY = "country"
    REGION = "region"
    ALLIANCE = "alliance"
    ECONOMIC_BLOCK = "economic_block"


class ThreatLevel(Enum):
    """Threat level classifications."""
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class GeopoliticalRegion:
    """Geopolitical region analysis result."""
    region_name: str
    region_type: RegionType
    threat_level: ThreatLevel
    stability_score: float
    economic_indicators: Dict[str, float]
    political_indicators: Dict[str, float]
    security_concerns: List[str]
    opportunities: List[str]
    timestamp: datetime


@dataclass
class InternationalRelations:
    """International relations analysis result."""
    bilateral_relations: Dict[str, Dict[str, Any]]
    multilateral_agreements: List[Dict[str, Any]]
    conflict_zones: List[str]
    cooperation_areas: List[str]
    trade_relations: Dict[str, float]
    diplomatic_tensions: List[str]
    timestamp: datetime


@dataclass
class RegionalStability:
    """Regional stability analysis result."""
    overall_stability: float
    internal_factors: Dict[str, float]
    external_pressures: Dict[str, float]
    stability_trends: List[Dict[str, Any]]
    risk_factors: List[str]
    stability_forecast: Dict[str, Any]
    timestamp: datetime


class GeopoliticalAnalyzer:
    """Geopolitical analysis engine."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.cache = {}
        
    async def analyze_geopolitical_region(
        self,
        region_data: Dict[str, Any],
        historical_data: Optional[Dict[str, Any]] = None
    ) -> GeopoliticalRegion:
        """Analyze geopolitical characteristics of a region."""
        try:
            self.logger.info(f"Starting geopolitical analysis for region: {region_data.get('name', 'Unknown')}")
            
            region_name = region_data.get('name', 'Unknown')
            region_type = RegionType(region_data.get('type', 'region'))
            
            # Calculate stability score
            economic_growth = region_data.get('economic_growth', 0.0)
            political_stability = region_data.get('political_stability', 0.5)
            social_cohesion = region_data.get('social_cohesion', 0.5)
            security_level = region_data.get('security_level', 0.5)
            
            stability_score = (
                economic_growth * 0.3 +
                political_stability * 0.3 +
                social_cohesion * 0.2 +
                security_level * 0.2
            )
            
            # Determine threat level
            if stability_score > 0.8:
                threat_level = ThreatLevel.NONE
            elif stability_score > 0.6:
                threat_level = ThreatLevel.LOW
            elif stability_score > 0.4:
                threat_level = ThreatLevel.MEDIUM
            elif stability_score > 0.2:
                threat_level = ThreatLevel.HIGH
            else:
                threat_level = ThreatLevel.CRITICAL
            
            # Analyze economic indicators
            economic_indicators = {
                'gdp_growth': region_data.get('gdp_growth', 0.0),
                'inflation_rate': region_data.get('inflation_rate', 0.0),
                'unemployment_rate': region_data.get('unemployment_rate', 0.0),
                'trade_balance': region_data.get('trade_balance', 0.0),
                'foreign_investment': region_data.get('foreign_investment', 0.0)
            }
            
            # Analyze political indicators
            political_indicators = {
                'democracy_index': region_data.get('democracy_index', 0.5),
                'corruption_perception': region_data.get('corruption_perception', 0.5),
                'press_freedom': region_data.get('press_freedom', 0.5),
                'rule_of_law': region_data.get('rule_of_law', 0.5),
                'government_effectiveness': region_data.get('government_effectiveness', 0.5)
            }
            
            # Identify security concerns
            security_concerns = []
            if security_level < 0.5:
                security_concerns.append("Internal security threats")
            if political_stability < 0.5:
                security_concerns.append("Political instability")
            if social_cohesion < 0.5:
                security_concerns.append("Social unrest")
            if economic_growth < 0.0:
                security_concerns.append("Economic decline")
            
            # Identify opportunities
            opportunities = []
            if economic_growth > 0.05:
                opportunities.append("Economic growth potential")
            if political_stability > 0.7:
                opportunities.append("Political stability")
            if security_level > 0.7:
                opportunities.append("Security cooperation")
            if social_cohesion > 0.7:
                opportunities.append("Social development")
            
            result = GeopoliticalRegion(
                region_name=region_name,
                region_type=region_type,
                threat_level=threat_level,
                stability_score=stability_score,
                economic_indicators=economic_indicators,
                political_indicators=political_indicators,
                security_concerns=security_concerns,
                opportunities=opportunities,
                timestamp=datetime.now()
            )
            
            self.logger.info(f"Geopolitical analysis completed for {region_name}: {threat_level.value}")
            return result
            
        except Exception as e:
            self.logger.error(f"Error in geopolitical region analysis: {e}")
            raise
    
    async def analyze_international_relations(
        self,
        bilateral_data: Dict[str, Any],
        multilateral_data: Dict[str, Any],
        trade_data: Dict[str, Any]
    ) -> InternationalRelations:
        """Analyze international relations and diplomatic dynamics."""
        try:
            self.logger.info("Starting international relations analysis")
            
            # Analyze bilateral relations
            bilateral_relations = {}
            for country, data in bilateral_data.items():
                bilateral_relations[country] = {
                    'diplomatic_relations': data.get('diplomatic_relations', 'neutral'),
                    'trade_volume': data.get('trade_volume', 0.0),
                    'political_alignment': data.get('political_alignment', 0.5),
                    'security_cooperation': data.get('security_cooperation', 0.5),
                    'cultural_exchanges': data.get('cultural_exchanges', 0.5)
                }
            
            # Analyze multilateral agreements
            multilateral_agreements = []
            for agreement in multilateral_data.get('agreements', []):
                multilateral_agreements.append({
                    'name': agreement.get('name', ''),
                    'type': agreement.get('type', ''),
                    'members': agreement.get('members', []),
                    'effectiveness': agreement.get('effectiveness', 0.5),
                    'scope': agreement.get('scope', '')
                })
            
            # Identify conflict zones
            conflict_zones = []
            for country, data in bilateral_data.items():
                if data.get('conflict_level', 0) > 0.7:
                    conflict_zones.append(country)
            
            # Identify cooperation areas
            cooperation_areas = []
            if multilateral_data.get('economic_cooperation', False):
                cooperation_areas.append("Economic cooperation")
            if multilateral_data.get('security_cooperation', False):
                cooperation_areas.append("Security cooperation")
            if multilateral_data.get('environmental_cooperation', False):
                cooperation_areas.append("Environmental cooperation")
            if multilateral_data.get('cultural_cooperation', False):
                cooperation_areas.append("Cultural cooperation")
            
            # Analyze trade relations
            trade_relations = {}
            for country, volume in trade_data.items():
                trade_relations[country] = volume
            
            # Identify diplomatic tensions
            diplomatic_tensions = []
            for country, data in bilateral_data.items():
                if data.get('tension_level', 0) > 0.6:
                    diplomatic_tensions.append(f"Tensions with {country}")
            
            result = InternationalRelations(
                bilateral_relations=bilateral_relations,
                multilateral_agreements=multilateral_agreements,
                conflict_zones=conflict_zones,
                cooperation_areas=cooperation_areas,
                trade_relations=trade_relations,
                diplomatic_tensions=diplomatic_tensions,
                timestamp=datetime.now()
            )
            
            self.logger.info("International relations analysis completed")
            return result
            
        except Exception as e:
            self.logger.error(f"Error in international relations analysis: {e}")
            raise
    
    async def analyze_regional_stability(
        self,
        region_data: Dict[str, Any],
        historical_stability: List[Dict[str, Any]],
        external_factors: Dict[str, Any]
    ) -> RegionalStability:
        """Analyze regional stability and forecast trends."""
        try:
            self.logger.info("Starting regional stability analysis")
            
            # Calculate overall stability
            internal_stability = region_data.get('internal_stability', 0.5)
            external_stability = region_data.get('external_stability', 0.5)
            economic_stability = region_data.get('economic_stability', 0.5)
            social_stability = region_data.get('social_stability', 0.5)
            
            overall_stability = (
                internal_stability * 0.3 +
                external_stability * 0.3 +
                economic_stability * 0.2 +
                social_stability * 0.2
            )
            
            # Analyze internal factors
            internal_factors = {
                'political_stability': region_data.get('political_stability', 0.5),
                'economic_growth': region_data.get('economic_growth', 0.0),
                'social_cohesion': region_data.get('social_cohesion', 0.5),
                'institutional_strength': region_data.get('institutional_strength', 0.5),
                'security_capacity': region_data.get('security_capacity', 0.5)
            }
            
            # Analyze external pressures
            external_pressures = {
                'geopolitical_tensions': external_factors.get('geopolitical_tensions', 0.5),
                'economic_pressures': external_factors.get('economic_pressures', 0.5),
                'security_threats': external_factors.get('security_threats', 0.5),
                'environmental_challenges': external_factors.get('environmental_challenges', 0.5),
                'migration_pressures': external_factors.get('migration_pressures', 0.5)
            }
            
            # Analyze stability trends
            stability_trends = []
            for trend in historical_stability:
                stability_trends.append({
                    'period': trend.get('period', ''),
                    'stability_score': trend.get('stability_score', 0.5),
                    'key_factors': trend.get('key_factors', []),
                    'trend_direction': trend.get('trend_direction', 'stable')
                })
            
            # Identify risk factors
            risk_factors = []
            if overall_stability < 0.5:
                risk_factors.append("Low overall stability")
            if internal_factors['political_stability'] < 0.4:
                risk_factors.append("Political instability")
            if internal_factors['economic_growth'] < 0.0:
                risk_factors.append("Economic decline")
            if external_pressures['geopolitical_tensions'] > 0.7:
                risk_factors.append("High geopolitical tensions")
            if external_pressures['security_threats'] > 0.7:
                risk_factors.append("Security threats")
            
            # Generate stability forecast
            stability_forecast = self._generate_stability_forecast(
                overall_stability, stability_trends, external_pressures
            )
            
            result = RegionalStability(
                overall_stability=overall_stability,
                internal_factors=internal_factors,
                external_pressures=external_pressures,
                stability_trends=stability_trends,
                risk_factors=risk_factors,
                stability_forecast=stability_forecast,
                timestamp=datetime.now()
            )
            
            self.logger.info(f"Regional stability analysis completed: {overall_stability:.2f}")
            return result
            
        except Exception as e:
            self.logger.error(f"Error in regional stability analysis: {e}")
            raise
    
    def _generate_stability_forecast(
        self,
        current_stability: float,
        historical_trends: List[Dict[str, Any]],
        external_pressures: Dict[str, float]
    ) -> Dict[str, Any]:
        """Generate stability forecast based on current conditions and trends."""
        try:
            # Calculate trend direction
            if len(historical_trends) >= 2:
                recent_trends = historical_trends[-3:]
                trend_direction = sum(t['stability_score'] for t in recent_trends) / len(recent_trends)
                trend_momentum = trend_direction - current_stability
            else:
                trend_momentum = 0.0
            
            # Calculate external pressure impact
            external_pressure_score = sum(external_pressures.values()) / len(external_pressures)
            pressure_impact = (1 - external_pressure_score) * 0.2
            
            # Forecast stability
            forecast_stability = current_stability + trend_momentum + pressure_impact
            forecast_stability = max(0.0, min(1.0, forecast_stability))
            
            # Determine forecast confidence
            confidence = 0.7  # Base confidence
            if len(historical_trends) > 5:
                confidence += 0.2
            if external_pressure_score < 0.5:
                confidence += 0.1
            
            return {
                'forecast_stability': forecast_stability,
                'confidence_level': confidence,
                'trend_direction': 'improving' if trend_momentum > 0 else 'declining' if trend_momentum < 0 else 'stable',
                'key_factors': list(external_pressures.keys()),
                'forecast_period': '6_months'
            }
            
        except Exception as e:
            self.logger.error(f"Error generating stability forecast: {e}")
            return {
                'forecast_stability': current_stability,
                'confidence_level': 0.5,
                'trend_direction': 'unknown',
                'key_factors': [],
                'forecast_period': '6_months'
            }
    
    async def generate_comprehensive_geopolitical_analysis(
        self,
        regions_data: List[Dict[str, Any]],
        bilateral_data: Dict[str, Any],
        multilateral_data: Dict[str, Any],
        trade_data: Dict[str, Any],
        historical_data: Dict[str, Any],
        external_factors: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate comprehensive geopolitical analysis."""
        try:
            self.logger.info("Starting comprehensive geopolitical analysis")
            
            # Analyze all regions concurrently
            region_tasks = [
                self.analyze_geopolitical_region(region_data)
                for region_data in regions_data
            ]
            
            # Run analyses
            regions_analysis = await asyncio.gather(*region_tasks)
            international_relations = await self.analyze_international_relations(
                bilateral_data, multilateral_data, trade_data
            )
            
            # Analyze regional stability for each region
            stability_tasks = []
            for region_data in regions_data:
                region_name = region_data.get('name', 'Unknown')
                historical_stability = historical_data.get(region_name, {}).get('stability_trends', [])
                stability_tasks.append(
                    self.analyze_regional_stability(region_data, historical_stability, external_factors)
                )
            
            stability_analysis = await asyncio.gather(*stability_tasks)
            
            # Compile comprehensive analysis
            analysis = {
                'regions_analysis': [asdict(region) for region in regions_analysis],
                'international_relations': asdict(international_relations),
                'regional_stability': [asdict(stability) for stability in stability_analysis],
                'summary': {
                    'total_regions_analyzed': len(regions_analysis),
                    'high_risk_regions': len([r for r in regions_analysis if r.threat_level.value in ['high', 'critical']]),
                    'conflict_zones': international_relations.conflict_zones,
                    'cooperation_opportunities': international_relations.cooperation_areas,
                    'overall_stability_trend': 'improving' if sum(s.overall_stability for s in stability_analysis) / len(stability_analysis) > 0.6 else 'declining'
                },
                'timestamp': datetime.now().isoformat()
            }
            
            self.logger.info("Comprehensive geopolitical analysis completed")
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error in comprehensive geopolitical analysis: {e}")
            raise
