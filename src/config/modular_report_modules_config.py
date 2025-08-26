"""
Modular Report Modules Configuration

Comprehensive configuration for all 22 modular report modules with:
- Contextual adaptive capabilities
- Data structure handling (string, dict)
- Domain-specific configurations
- Interactive visualizations
- Advanced tooltips
"""

from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, field
from enum import Enum
import json


class DataStructureType(Enum):
    """Supported data structure types."""
    STRING = "string"
    DICT = "dict"
    MIXED = "mixed"


class ContextDomain(Enum):
    """Supported context domains."""
    HEALTHCARE = "healthcare"
    TECHNOLOGY = "technology"
    FINANCE = "finance"
    GEOPOLITICAL = "geopolitical"
    MILITARY = "military"
    ECONOMIC = "economic"
    CYBERSECURITY = "cybersecurity"
    GENERAL = "general"


@dataclass
class AdaptiveDataConfig:
    """Configuration for adaptive data handling."""
    supported_structures: List[DataStructureType] = field(default_factory=lambda: [
        DataStructureType.STRING, 
        DataStructureType.DICT, 
        DataStructureType.MIXED
    ])
    auto_detect_structure: bool = True
    fallback_to_string: bool = True
    data_validation: bool = True
    structure_mapping: Dict[str, str] = field(default_factory=dict)
    context_keywords: Dict[ContextDomain, List[str]] = field(default_factory=dict)


@dataclass
class ModuleAdaptiveConfig:
    """Adaptive configuration for individual modules."""
    enabled: bool = True
    context_domains: List[ContextDomain] = field(default_factory=lambda: [ContextDomain.GENERAL])
    data_structures: List[DataStructureType] = field(default_factory=lambda: [
        DataStructureType.STRING, 
        DataStructureType.DICT
    ])
    auto_adapt: bool = True
    confidence_threshold: float = 0.7
    fallback_strategy: str = "string_processing"
    interactive_features: bool = True
    tooltips_enabled: bool = True
    charts_enabled: bool = True
    custom_styles: Dict[str, str] = field(default_factory=dict)
    data_sources: Dict[str, str] = field(default_factory=dict)
    confidence_scores: Dict[str, float] = field(default_factory=dict)


class ModularReportModulesConfig:
    """Comprehensive configuration for all 22 modular report modules."""
    
    def __init__(self):
        """Initialize the modular report modules configuration."""
        self.modules_config = self._initialize_modules_config()
        self.adaptive_config = self._initialize_adaptive_config()
        self.context_mapping = self._initialize_context_mapping()
        self.data_structure_handlers = self._initialize_data_structure_handlers()
    
    def _initialize_modules_config(self) -> Dict[str, ModuleAdaptiveConfig]:
        """Initialize configuration for all 22 modules."""
        return {
            # 1. Strategic Recommendations Module
            "strategic_recommendations": ModuleAdaptiveConfig(
                context_domains=[ContextDomain.GENERAL, ContextDomain.GEOPOLITICAL, ContextDomain.MILITARY],
                data_structures=[DataStructureType.DICT, DataStructureType.STRING],
                confidence_threshold=0.8,
                interactive_features=True,
                custom_styles={"background": "#f8f9fa", "border": "2px solid #007bff"}
            ),
            
            # 2. Executive Summary Module
            "executive_summary": ModuleAdaptiveConfig(
                context_domains=[ContextDomain.GENERAL],
                data_structures=[DataStructureType.STRING, DataStructureType.DICT],
                confidence_threshold=0.9,
                interactive_features=False,
                custom_styles={"background": "#ffffff", "border": "1px solid #dee2e6"}
            ),
            
            # 3. Geopolitical Impact Module
            "geopolitical_impact": ModuleAdaptiveConfig(
                context_domains=[ContextDomain.GEOPOLITICAL, ContextDomain.MILITARY],
                data_structures=[DataStructureType.DICT, DataStructureType.MIXED],
                confidence_threshold=0.75,
                interactive_features=True,
                custom_styles={"background": "#fff3cd", "border": "2px solid #ffc107"}
            ),
            
            # 4. Trade Impact Module
            "trade_impact": ModuleAdaptiveConfig(
                context_domains=[ContextDomain.ECONOMIC, ContextDomain.FINANCE],
                data_structures=[DataStructureType.DICT, DataStructureType.MIXED],
                confidence_threshold=0.8,
                interactive_features=True,
                custom_styles={"background": "#d1ecf1", "border": "2px solid #17a2b8"}
            ),
            
            # 5. Balance of Power Module
            "balance_of_power": ModuleAdaptiveConfig(
                context_domains=[ContextDomain.GEOPOLITICAL, ContextDomain.MILITARY],
                data_structures=[DataStructureType.DICT, DataStructureType.MIXED],
                confidence_threshold=0.85,
                interactive_features=True,
                custom_styles={"background": "#f8d7da", "border": "2px solid #dc3545"}
            ),
            
            # 6. Risk Assessment Module
            "risk_assessment": ModuleAdaptiveConfig(
                context_domains=[ContextDomain.GENERAL, ContextDomain.CYBERSECURITY],
                data_structures=[DataStructureType.DICT, DataStructureType.STRING],
                confidence_threshold=0.8,
                interactive_features=True,
                custom_styles={"background": "#fff3cd", "border": "2px solid #ffc107"}
            ),
            

            
            # 8. Strategic Analysis Module
            "strategic_analysis": ModuleAdaptiveConfig(
                context_domains=[ContextDomain.GENERAL, ContextDomain.MILITARY],
                data_structures=[DataStructureType.DICT, DataStructureType.STRING],
                confidence_threshold=0.8,
                interactive_features=True,
                custom_styles={"background": "#d4edda", "border": "2px solid #28a745"}
            ),
            
            # 9. Enhanced Data Analysis Module
            "enhanced_data_analysis": ModuleAdaptiveConfig(
                context_domains=[ContextDomain.GENERAL, ContextDomain.TECHNOLOGY],
                data_structures=[DataStructureType.DICT, DataStructureType.MIXED],
                confidence_threshold=0.75,
                interactive_features=True,
                custom_styles={"background": "#cce5ff", "border": "2px solid #007bff"}
            ),
            
            # 10. Regional Sentiment Module
            "regional_sentiment": ModuleAdaptiveConfig(
                context_domains=[ContextDomain.GEOPOLITICAL, ContextDomain.ECONOMIC],
                data_structures=[DataStructureType.DICT, DataStructureType.MIXED],
                confidence_threshold=0.7,
                interactive_features=True,
                custom_styles={"background": "#f8f9fa", "border": "2px solid #6c757d"}
            ),
            
            # 11. Implementation Timeline Module
            "implementation_timeline": ModuleAdaptiveConfig(
                context_domains=[ContextDomain.GENERAL, ContextDomain.TECHNOLOGY],
                data_structures=[DataStructureType.DICT, DataStructureType.STRING],
                confidence_threshold=0.8,
                interactive_features=True,
                custom_styles={"background": "#e2e3e5", "border": "2px solid #6c757d"}
            ),
            
            # 12. Acquisition Programs Module
            "acquisition_programs": ModuleAdaptiveConfig(
                context_domains=[ContextDomain.MILITARY, ContextDomain.TECHNOLOGY],
                data_structures=[DataStructureType.DICT, DataStructureType.MIXED],
                confidence_threshold=0.8,
                interactive_features=True,
                custom_styles={"background": "#d1ecf1", "border": "2px solid #17a2b8"}
            ),
            
            # 13. Forecasting Module
            "forecasting": ModuleAdaptiveConfig(
                context_domains=[ContextDomain.GENERAL, ContextDomain.ECONOMIC],
                data_structures=[DataStructureType.DICT, DataStructureType.MIXED],
                confidence_threshold=0.7,
                interactive_features=True,
                custom_styles={"background": "#fff3cd", "border": "2px solid #ffc107"}
            ),
            
            # 14. Operational Considerations Module
            "operational_considerations": ModuleAdaptiveConfig(
                context_domains=[ContextDomain.MILITARY, ContextDomain.GENERAL],
                data_structures=[DataStructureType.DICT, DataStructureType.STRING],
                confidence_threshold=0.8,
                interactive_features=True,
                custom_styles={"background": "#d4edda", "border": "2px solid #28a745"}
            ),
            
            # 15. Regional Security Module
            "regional_security": ModuleAdaptiveConfig(
                context_domains=[ContextDomain.GEOPOLITICAL, ContextDomain.MILITARY],
                data_structures=[DataStructureType.DICT, DataStructureType.MIXED],
                confidence_threshold=0.8,
                interactive_features=True,
                custom_styles={"background": "#f8d7da", "border": "2px solid #dc3545"}
            ),
            
            # 16. Economic Analysis Module
            "economic_analysis": ModuleAdaptiveConfig(
                context_domains=[ContextDomain.ECONOMIC, ContextDomain.FINANCE],
                data_structures=[DataStructureType.DICT, DataStructureType.MIXED],
                confidence_threshold=0.8,
                interactive_features=True,
                custom_styles={"background": "#cce5ff", "border": "2px solid #007bff"}
            ),
            
            # 17. Comparison Analysis Module
            "comparison_analysis": ModuleAdaptiveConfig(
                context_domains=[ContextDomain.GENERAL],
                data_structures=[DataStructureType.DICT, DataStructureType.MIXED],
                confidence_threshold=0.75,
                interactive_features=True,
                custom_styles={"background": "#e2e3e5", "border": "2px solid #6c757d"}
            ),
            
            # 18. Advanced Forecasting Module
            "advanced_forecasting": ModuleAdaptiveConfig(
                context_domains=[ContextDomain.GENERAL, ContextDomain.TECHNOLOGY],
                data_structures=[DataStructureType.DICT, DataStructureType.MIXED],
                confidence_threshold=0.7,
                interactive_features=True,
                custom_styles={"background": "#fff3cd", "border": "2px solid #ffc107"}
            ),
            
            # 19. Model Performance Module
            "model_performance": ModuleAdaptiveConfig(
                context_domains=[ContextDomain.TECHNOLOGY, ContextDomain.GENERAL],
                data_structures=[DataStructureType.DICT, DataStructureType.MIXED],
                confidence_threshold=0.8,
                interactive_features=True,
                custom_styles={"background": "#d1ecf1", "border": "2px solid #17a2b8"}
            ),
            
            # 20. Strategic Capability Module
            "strategic_capability": ModuleAdaptiveConfig(
                context_domains=[ContextDomain.MILITARY, ContextDomain.GEOPOLITICAL],
                data_structures=[DataStructureType.DICT, DataStructureType.MIXED],
                confidence_threshold=0.8,
                interactive_features=True,
                custom_styles={"background": "#d4edda", "border": "2px solid #28a745"}
            ),
            
            # 21. Predictive Analytics Module
            "predictive_analytics": ModuleAdaptiveConfig(
                context_domains=[ContextDomain.TECHNOLOGY, ContextDomain.GENERAL],
                data_structures=[DataStructureType.DICT, DataStructureType.MIXED],
                confidence_threshold=0.7,
                interactive_features=True,
                custom_styles={"background": "#cce5ff", "border": "2px solid #007bff"}
            ),
            
            # 22. Scenario Analysis Module
            "scenario_analysis": ModuleAdaptiveConfig(
                context_domains=[ContextDomain.GENERAL, ContextDomain.GEOPOLITICAL],
                data_structures=[DataStructureType.DICT, DataStructureType.MIXED],
                confidence_threshold=0.75,
                interactive_features=True,
                custom_styles={"background": "#f8f9fa", "border": "2px solid #6c757d"}
            )
        }
    
    def _initialize_adaptive_config(self) -> AdaptiveDataConfig:
        """Initialize adaptive data configuration."""
        return AdaptiveDataConfig(
            supported_structures=[DataStructureType.STRING, DataStructureType.DICT, DataStructureType.MIXED],
            auto_detect_structure=True,
            fallback_to_string=True,
            data_validation=True,
            structure_mapping={
                "string": "text_analysis",
                "dict": "structured_analysis",
                "mixed": "hybrid_analysis"
            },
            context_keywords={
                ContextDomain.HEALTHCARE: ["health", "medical", "patient", "treatment", "diagnosis", "clinical"],
                ContextDomain.TECHNOLOGY: ["ai", "technology", "software", "digital", "innovation", "automation"],
                ContextDomain.FINANCE: ["financial", "investment", "market", "economic", "trading", "banking"],
                ContextDomain.GEOPOLITICAL: ["political", "diplomatic", "international", "foreign", "policy", "relations"],
                ContextDomain.MILITARY: ["military", "defense", "strategic", "tactical", "weapons", "security"],
                ContextDomain.ECONOMIC: ["economic", "trade", "commerce", "business", "market", "financial"],
                ContextDomain.CYBERSECURITY: ["cyber", "security", "digital", "threat", "attack", "protection"],
                ContextDomain.GENERAL: ["analysis", "report", "study", "research", "assessment", "evaluation"]
            }
        )
    
    def _initialize_context_mapping(self) -> Dict[str, ContextDomain]:
        """Initialize context domain mapping for modules."""
        return {
            "strategic_recommendations": ContextDomain.GENERAL,
            "executive_summary": ContextDomain.GENERAL,
            "geopolitical_impact": ContextDomain.GEOPOLITICAL,
            "trade_impact": ContextDomain.ECONOMIC,
            "balance_of_power": ContextDomain.GEOPOLITICAL,
            "risk_assessment": ContextDomain.GENERAL,
            "strategic_analysis": ContextDomain.GENERAL,
            "enhanced_data_analysis": ContextDomain.TECHNOLOGY,
            "regional_sentiment": ContextDomain.GEOPOLITICAL,
            "implementation_timeline": ContextDomain.GENERAL,
            "acquisition_programs": ContextDomain.MILITARY,
            "forecasting": ContextDomain.GENERAL,
            "operational_considerations": ContextDomain.MILITARY,
            "regional_security": ContextDomain.GEOPOLITICAL,
            "economic_analysis": ContextDomain.ECONOMIC,
            "comparison_analysis": ContextDomain.GENERAL,
            "advanced_forecasting": ContextDomain.TECHNOLOGY,
            "model_performance": ContextDomain.TECHNOLOGY,
            "strategic_capability": ContextDomain.MILITARY,
            "predictive_analytics": ContextDomain.TECHNOLOGY,
            "scenario_analysis": ContextDomain.GENERAL
        }
    
    def _initialize_data_structure_handlers(self) -> Dict[DataStructureType, Dict[str, Any]]:
        """Initialize data structure handlers."""
        return {
            DataStructureType.STRING: {
                "processor": "text_analysis_processor",
                "validation": "string_validation",
                "transformation": "text_to_structured",
                "fallback": "direct_text_processing"
            },
            DataStructureType.DICT: {
                "processor": "structured_data_processor",
                "validation": "dict_validation",
                "transformation": "dict_to_module_format",
                "fallback": "dict_key_extraction"
            },
            DataStructureType.MIXED: {
                "processor": "hybrid_processor",
                "validation": "mixed_validation",
                "transformation": "adaptive_transformation",
                "fallback": "string_processing"
            }
        }
    
    def get_module_config(self, module_id: str) -> Optional[ModuleAdaptiveConfig]:
        """Get configuration for a specific module."""
        return self.modules_config.get(module_id)
    
    def get_all_modules_config(self) -> Dict[str, ModuleAdaptiveConfig]:
        """Get configuration for all modules."""
        return self.modules_config
    
    def update_module_config(self, module_id: str, config: ModuleAdaptiveConfig):
        """Update configuration for a specific module."""
        if module_id in self.modules_config:
            self.modules_config[module_id] = config
    
    def get_modules_by_context(self, context: ContextDomain) -> List[str]:
        """Get modules that support a specific context domain."""
        return [
            module_id for module_id, config in self.modules_config.items()
            if context in config.context_domains
        ]
    
    def get_modules_by_data_structure(self, data_structure: DataStructureType) -> List[str]:
        """Get modules that support a specific data structure."""
        return [
            module_id for module_id, config in self.modules_config.items()
            if data_structure in config.data_structures
        ]
    
    def detect_context_domain(self, text: str) -> ContextDomain:
        """Detect context domain from text content."""
        text_lower = text.lower()
        
        for domain, keywords in self.adaptive_config.context_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return domain
        
        return ContextDomain.GENERAL
    
    def detect_data_structure(self, data: Union[str, Dict[str, Any]]) -> DataStructureType:
        """Detect data structure type."""
        if isinstance(data, str):
            return DataStructureType.STRING
        elif isinstance(data, dict):
            return DataStructureType.DICT
        else:
            return DataStructureType.MIXED
    
    def get_adaptive_config(self) -> AdaptiveDataConfig:
        """Get adaptive data configuration."""
        return self.adaptive_config
    
    def get_data_structure_handler(self, data_structure: DataStructureType) -> Dict[str, Any]:
        """Get data structure handler configuration."""
        return self.data_structure_handlers.get(data_structure, {})
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "modules_config": {
                module_id: {
                    "enabled": config.enabled,
                    "context_domains": [domain.value for domain in config.context_domains],
                    "data_structures": [struct.value for struct in config.data_structures],
                    "auto_adapt": config.auto_adapt,
                    "confidence_threshold": config.confidence_threshold,
                    "fallback_strategy": config.fallback_strategy,
                    "interactive_features": config.interactive_features,
                    "tooltips_enabled": config.tooltips_enabled,
                    "charts_enabled": config.charts_enabled,
                    "custom_styles": config.custom_styles,
                    "data_sources": config.data_sources,
                    "confidence_scores": config.confidence_scores
                }
                for module_id, config in self.modules_config.items()
            },
            "adaptive_config": {
                "supported_structures": [struct.value for struct in self.adaptive_config.supported_structures],
                "auto_detect_structure": self.adaptive_config.auto_detect_structure,
                "fallback_to_string": self.adaptive_config.fallback_to_string,
                "data_validation": self.adaptive_config.data_validation,
                "structure_mapping": self.adaptive_config.structure_mapping,
                "context_keywords": {
                    domain.value: keywords for domain, keywords in self.adaptive_config.context_keywords.items()
                }
            },
            "context_mapping": {
                module_id: domain.value for module_id, domain in self.context_mapping.items()
            },
            "data_structure_handlers": self.data_structure_handlers
        }
    
    def from_dict(self, config_dict: Dict[str, Any]):
        """Load configuration from dictionary."""
        # Implementation for loading from dictionary
        pass
    
    def save_config(self, file_path: str):
        """Save configuration to file."""
        with open(file_path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    def load_config(self, file_path: str):
        """Load configuration from file."""
        with open(file_path, 'r') as f:
            config_dict = json.load(f)
            self.from_dict(config_dict)


# Global configuration instance
modular_report_modules_config = ModularReportModulesConfig()
