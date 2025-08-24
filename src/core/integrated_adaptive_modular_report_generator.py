"""
Integrated Adaptive Modular Report Generator

Integrated system that makes ALL existing modular report modules adaptive by
intelligently adapting data structures and handling any user query dynamically.
"""

from typing import Dict, Any, List, Optional

# Import the adaptive data adapter
from .adaptive_data_adapter import AdaptiveDataAdapter

# Import modular report generator
try:
    from .modular_report_generator import modular_report_generator
    MODULAR_REPORT_AVAILABLE = True
except ImportError as e:
    print(f"Modular report generator not available: {e}")
    MODULAR_REPORT_AVAILABLE = False


class IntegratedAdaptiveModularReportGenerator:
    """Integrated adaptive modular report generator that makes all modules adaptive."""
    
    def __init__(self):
        self.data_adapter = AdaptiveDataAdapter()
        
        # Define all available modules with categories (using actual module IDs)
        self.all_modules = {
            'executivesummarymodule': {
                'category': 'strategic', 'priority': 1, 'title': 'Executive Summary'
            },
            'geopoliticalimpactmodule': {
                'category': 'impact', 'priority': 2, 'title': 'Geopolitical Impact'
            },
            'tradeimpactmodule': {
                'category': 'impact', 'priority': 3, 'title': 'Trade Impact'
            },
            'balanceofpowermodule': {
                'category': 'assessment', 'priority': 4, 'title': 'Balance of Power'
            },
            'riskassessmentmodule': {
                'category': 'assessment', 'priority': 5, 'title': 'Risk Assessment'
            },
            'regionalsentimentmodule': {
                'category': 'visualization', 'priority': 6, 'title': 'Regional Sentiment'
            },
            'implementationtimelinemodule': {
                'category': 'operational', 'priority': 7, 'title': 'Implementation Timeline'
            },
            'acquisitionprogramsmodule': {
                'category': 'operational', 'priority': 8, 'title': 'Acquisition Programs'
            },
            'forecastingmodule': {
                'category': 'analytical', 'priority': 9, 'title': 'Forecasting'
            },
            'operationalconsiderationsmodule': {
                'category': 'operational', 'priority': 10, 
                'title': 'Operational Considerations'
            },
            'regionalsecuritymodule': {
                'category': 'impact', 'priority': 11, 'title': 'Regional Security'
            },
            'economicanalysismodule': {
                'category': 'impact', 'priority': 12, 'title': 'Economic Analysis'
            },
            'comparisonanalysismodule': {
                'category': 'assessment', 'priority': 13, 'title': 'Comparison Analysis'
            },
            'advancedforecastingmodule': {
                'category': 'analytical', 'priority': 14, 'title': 'Advanced Forecasting'
            },
            'modelperformancemodule': {
                'category': 'assessment', 'priority': 15, 'title': 'Model Performance'
            },
            'strategiccapabilitymodule': {
                'category': 'strategic', 'priority': 16, 'title': 'Strategic Capability'
            },
            'predictiveanalyticsmodule': {
                'category': 'analytical', 'priority': 17, 'title': 'Predictive Analytics'
            },
            'scenarioanalysismodule': {
                'category': 'analytical', 'priority': 18, 'title': 'Scenario Analysis'
            },
            'strategicrecommendationsmodule': {
                'category': 'strategic', 'priority': 19, 'title': 'Strategic Recommendations'
            },
            'strategicanalysismodule': {
                'category': 'strategic', 'priority': 20, 'title': 'Strategic Analysis'
            },
            'enhanceddataanalysismodule': {
                'category': 'analytical', 'priority': 21, 'title': 'Enhanced Data Analysis'
            },
            'interactivevisualizationsmodule': {
                'category': 'visualization', 'priority': 22, 
                'title': 'Interactive Visualizations'
            }
        }
        
        # Define module categories with actual module IDs
        self.module_categories = {
            'strategic': ['executivesummarymodule', 'strategicrecommendationsmodule', 'strategicanalysismodule', 'strategiccapabilitymodule'],
            'operational': ['operationalconsiderationsmodule', 'implementationtimelinemodule', 'acquisitionprogramsmodule'],
            'analytical': ['enhanceddataanalysismodule', 'predictiveanalyticsmodule', 'scenarioanalysismodule', 'forecastingmodule', 'advancedforecastingmodule'],
            'impact': ['geopoliticalimpactmodule', 'tradeimpactmodule', 'economicanalysismodule', 'regionalsecuritymodule'],
            'assessment': ['riskassessmentmodule', 'balanceofpowermodule', 'comparisonanalysismodule', 'modelperformancemodule'],
            'visualization': ['interactivevisualizationsmodule', 'regionalsentimentmodule']
        }
    
    async def generate_adaptive_report(
        self, 
        user_query: str, 
        data: Optional[Dict[str, Any]] = None,
        max_modules: Optional[int] = None,
        modules: Optional[List[str]] = None,
        module_categories: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Generate adaptive report with configurable module selection."""
        
        if data is None:
            data = {}
        
        print(f"🔍 Analyzing user query: {user_query}")
        
        # Clean the data
        clean_data = self.data_adapter.clean_data_structure(data)
        
        # Generate universal data structure
        universal_data = self.data_adapter.generate_universal_data(user_query, clean_data)
        
        print(f"📋 Generated universal data structure with {len(universal_data)} sections")
        
        # Select modules based on parameters
        selected_modules = self._select_modules(
            user_query=user_query,
            max_modules=max_modules,
            modules=modules,
            module_categories=module_categories
        )
        
        print(f"🎯 Selected {len(selected_modules)} modules: {', '.join(selected_modules)}")
        
        # Generate module configuration for selected modules
        module_config = self._generate_module_config(selected_modules)
        
        # Generate the report
        if MODULAR_REPORT_AVAILABLE:
            # Validate and adapt data structure early to ensure backend compatibility
            module_specific_data = self._validate_and_adapt_module_data(universal_data, selected_modules)
            
            result = await modular_report_generator.generate_modular_report(
                topic=user_query,
                data=module_specific_data,
                enabled_modules=selected_modules,
                report_title=f"Adaptive Analysis: {user_query}",
                custom_config=module_config
            )
        else:
            result = {
                'success': False,
                'file_path': '',
                'error': 'Modular report generator not available'
            }
        
        return {
            'success': result.get('success', False),
            'file_path': result.get('file_path', ''),
            'query': user_query,
            'universal_data_sections': len(universal_data),
            'integrated_adaptive_mode': True,
            'modules_generated': len(module_config),
            'selected_modules': selected_modules,
            'module_selection_method': self._get_selection_method(max_modules, modules, module_categories),
            'error': result.get('error', None)
        }
    
    def _select_modules(
        self,
        user_query: str,
        max_modules: Optional[int] = None,
        modules: Optional[List[str]] = None,
        module_categories: Optional[List[str]] = None
    ) -> List[str]:
        """Select modules based on parameters and query relevance."""
        
        # If specific modules are requested, use them
        if modules:
            valid_modules = [m for m in modules if m in self.all_modules]
            if not valid_modules:
                print(f"⚠️ No valid modules found in {modules}, using default selection")
                return self._get_default_modules(user_query, max_modules)
            return valid_modules
        
        # If categories are requested, get modules from those categories
        if module_categories:
            category_modules = []
            for category in module_categories:
                if category in self.module_categories:
                    category_modules.extend(self.module_categories[category])
                else:
                    print(f"⚠️ Unknown category: {category}")
            
            if category_modules:
                # Remove duplicates and limit if max_modules specified
                unique_modules = list(dict.fromkeys(category_modules))
                if max_modules:
                    return unique_modules[:max_modules]
                return unique_modules
        
        # If max_modules is specified, get the most relevant modules
        if max_modules:
            return self._get_default_modules(user_query, max_modules)
        
        # Default: return all modules (backward compatibility)
        return list(self.all_modules.keys())
    
    def _get_default_modules(self, user_query: str, max_modules: int) -> List[str]:
        """Get the most relevant modules based on query content."""
        query_lower = user_query.lower()
        
        # Score modules based on query relevance
        module_scores = {}
        for module_name, module_info in self.all_modules.items():
            score = 0
            
            # Base priority score (lower number = higher priority)
            score += (23 - module_info['priority']) * 10
            
            # Query relevance scoring
            if any(keyword in query_lower for keyword in ['executive', 'summary', 'overview']):
                if module_name == 'executive_summary':
                    score += 100
            
            if any(keyword in query_lower for keyword in ['geopolitical', 'political', 'diplomatic']):
                if module_name == 'geopolitical_impact':
                    score += 100
            
            if any(keyword in query_lower for keyword in ['trade', 'economic', 'financial']):
                if module_name in ['trade_impact', 'economic_analysis']:
                    score += 100
            
            if any(keyword in query_lower for keyword in ['military', 'defense', 'submarine', 'naval']):
                if module_name in ['balance_of_power', 'operational_considerations', 'acquisition_programs']:
                    score += 100
            
            if any(keyword in query_lower for keyword in ['risk', 'threat', 'vulnerability']):
                if module_name == 'risk_assessment':
                    score += 100
            
            if any(keyword in query_lower for keyword in ['strategic', 'strategy', 'planning']):
                if module_name in ['strategic_analysis', 'strategic_recommendations', 'strategic_capability']:
                    score += 100
            
            module_scores[module_name] = score
        
        # Sort by score and return top modules
        sorted_modules = sorted(module_scores.items(), key=lambda x: x[1], reverse=True)
        return [module for module, score in sorted_modules[:max_modules]]
    
    def _generate_module_config(self, selected_modules: List[str]) -> Dict[str, Any]:
        """Generate configuration for selected modules."""
        config = {}
        
        for i, module_name in enumerate(selected_modules, 1):
            if module_name in self.all_modules:
                module_info = self.all_modules[module_name]
                config[module_name] = {
                    'enabled': True,
                    'title': f"Adaptive {module_info['title']}",
                    'description': f"Intelligent {module_name} analysis that adapts to any data structure",
                    'order': i,
                    'category': module_info['category']
                }
        
        return config
    
    def _validate_and_adapt_module_data(self, universal_data: Dict[str, Any], selected_modules: List[str]) -> Dict[str, Any]:
        """
        Validate and adapt data structure early to ensure backend compatibility.
        This method ensures the data structure matches what each module expects.
        """
        print("🔍 Starting early data structure validation and adaptation...")
        
        # The modules are designed to receive the full universal_data and extract their specific section
        # So we just need to ensure the universal_data contains the required keys for each module
        validated_data = universal_data.copy()
        
        # Import module classes to get their required data keys
        try:
            from .modules.executive_summary_module import ExecutiveSummaryModule
            from .modules.geopolitical_impact_module import GeopoliticalImpactModule
            from .modules.trade_impact_module import TradeImpactModule
            from .modules.balance_of_power_module import BalanceOfPowerModule
            from .modules.risk_assessment_module import RiskAssessmentModule
            from .modules.regional_sentiment_module import RegionalSentimentModule
            from .modules.implementation_timeline_module import ImplementationTimelineModule
            from .modules.acquisition_programs_module import AcquisitionProgramsModule
            from .modules.forecasting_module import ForecastingModule
            from .modules.operational_considerations_module import OperationalConsiderationsModule
            from .modules.regional_security_module import RegionalSecurityModule
            from .modules.economic_analysis_module import EconomicAnalysisModule
            from .modules.comparison_analysis_module import ComparisonAnalysisModule
            from .modules.advanced_forecasting_module import AdvancedForecastingModule
            from .modules.model_performance_module import ModelPerformanceModule
            from .modules.strategic_capability_module import StrategicCapabilityModule
            from .modules.predictive_analytics_module import PredictiveAnalyticsModule
            from .modules.scenario_analysis_module import ScenarioAnalysisModule
            from .modules.strategic_recommendations_module import StrategicRecommendationsModule
            from .modules.strategic_analysis_module import StrategicAnalysisModule
            from .modules.enhanced_data_analysis_module import EnhancedDataAnalysisModule
            from .modules.interactive_visualizations_module import InteractiveVisualizationsModule
            
            # Module class mapping (using actual module IDs)
            module_classes = {
                'executivesummarymodule': ExecutiveSummaryModule,
                'geopoliticalimpactmodule': GeopoliticalImpactModule,
                'tradeimpactmodule': TradeImpactModule,
                'balanceofpowermodule': BalanceOfPowerModule,
                'riskassessmentmodule': RiskAssessmentModule,
                'regionalsentimentmodule': RegionalSentimentModule,
                'implementationtimelinemodule': ImplementationTimelineModule,
                'acquisitionprogramsmodule': AcquisitionProgramsModule,
                'forecastingmodule': ForecastingModule,
                'operationalconsiderationsmodule': OperationalConsiderationsModule,
                'regionalsecuritymodule': RegionalSecurityModule,
                'economicanalysismodule': EconomicAnalysisModule,
                'comparisonanalysismodule': ComparisonAnalysisModule,
                'advancedforecastingmodule': AdvancedForecastingModule,
                'modelperformancemodule': ModelPerformanceModule,
                'strategiccapabilitymodule': StrategicCapabilityModule,
                'predictiveanalyticsmodule': PredictiveAnalyticsModule,
                'scenarioanalysismodule': ScenarioAnalysisModule,
                'strategicrecommendationsmodule': StrategicRecommendationsModule,
                'strategicanalysismodule': StrategicAnalysisModule,
                'enhanceddataanalysismodule': EnhancedDataAnalysisModule,
                'interactivevisualizationsmodule': InteractiveVisualizationsModule
            }
        except ImportError as e:
            print(f"⚠️ Warning: Could not import module classes: {e}")
            # Fallback to the old method
            return self._extract_module_data_fallback(universal_data, selected_modules)
        
        for module_name in selected_modules:
            print(f"🔍 Validating data structure for module: {module_name}")
            
            if module_name not in module_classes:
                print(f"⚠️ Warning: No class found for module {module_name}")
                continue
            
            # Get the module class and its required data keys
            module_class = module_classes[module_name]
            module_instance = module_class()
            
            try:
                required_keys = module_instance.get_required_data_keys()
                print(f"📋 Module {module_name} requires keys: {required_keys}")
            except Exception as e:
                print(f"⚠️ Warning: Could not get required keys for {module_name}: {e}")
                required_keys = []
            
            # Ensure the required keys exist in the universal data
            for key in required_keys:
                if key not in validated_data:
                    print(f"⚠️ Missing required key: {key}, adding default data")
                    validated_data[key] = self._get_default_value(key, module_name)
                elif not isinstance(validated_data[key], dict):
                    print(f"⚠️ Invalid data type for {key}, converting to dict")
                    validated_data[key] = self._get_default_value(key, module_name)
            
            print(f"✅ Module {module_name} data validated")
        
        print(f"🎯 Total validated data keys: {len(validated_data)}")
        return validated_data
    
    def _adapt_data_for_module(
        self, 
        module_name: str, 
        module_data: Dict[str, Any], 
        required_keys: List[str], 
        universal_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Adapt data for a specific module to ensure all required keys are present
        with proper data types.
        """
        adapted_data = {}
        
        # Check each required key and extract from the nested module data
        for key in required_keys:
            if key in module_data:
                # The key exists at the top level of module_data
                value = module_data[key]
                if self._is_valid_data_type(key, value):
                    adapted_data[key] = value
                else:
                    print(f"⚠️ Invalid data type for {key}, providing default")
                    adapted_data[key] = self._get_default_value(key, module_name)
            else:
                # Key not found, provide default
                print(f"⚠️ Missing required key: {key}, providing default")
                adapted_data[key] = self._get_default_value(key, module_name)
        
        # Add any additional data from the module that might be useful
        for key, value in module_data.items():
            if key not in adapted_data:
                adapted_data[key] = value
        
        return adapted_data
    
    def _flatten_dict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Flatten a nested dictionary structure."""
        flattened = {}
        
        def flatten_recursive(d, prefix=''):
            for key, value in d.items():
                new_key = f"{prefix}{key}" if prefix else key
                
                if isinstance(value, dict):
                    flatten_recursive(value, f"{new_key}_")
                else:
                    flattened[new_key] = value
        
        if isinstance(data, dict):
            flatten_recursive(data)
        
        return flattened
    
    def _is_valid_data_type(self, key: str, value: Any) -> bool:
        """Check if the data type is valid for the given key."""
        # For keys that expect dictionaries, ensure they are dicts
        dict_keys = [
            'key_metrics', 'trend_analysis', 'strategic_insights', 'impact_assessment',
            'regional_analysis', 'economic_indicators', 'trade_flows', 'security_implications',
            'risk_factors', 'mitigation_strategies', 'capability_assessment', 'operational_requirements',
            'timeline_data', 'acquisition_details', 'forecast_data', 'scenario_data',
            'performance_metrics', 'recommendations', 'implementation_plan'
        ]
        
        if key in dict_keys:
            return isinstance(value, dict)
        
        # For other keys, any type is generally acceptable
        return True
    
    def _get_default_value(self, key: str, module_name: str) -> Any:
        """Get appropriate default value for a missing key."""
        # Always return dictionaries to avoid 'str' object has no attribute 'get' errors
        if 'metrics' in key:
            return {
                'current_value': 'Data not available',
                'trend': 'Stable',
                'projection': 'To be determined'
            }
        elif 'analysis' in key:
            return {
                'summary': f'Analysis for {module_name}',
                'key_findings': ['Data collection in progress'],
                'conclusions': 'Further analysis required'
            }
        elif 'assessment' in key:
            return {
                'level': 'Medium',
                'factors': ['Data pending'],
                'recommendations': ['Continue monitoring']
            }
        elif 'data' in key:
            return {
                'sources': ['Multiple sources'],
                'reliability': 'High',
                'last_updated': 'Current'
            }
        elif 'timeline' in key:
            return {
                'phases': ['Planning', 'Implementation', 'Evaluation'],
                'milestones': ['Phase 1 complete'],
                'dependencies': ['Resource allocation']
            }
        elif 'overview' in key:
            return {
                'summary': f'{key.replace("_", " ").title()} overview',
                'key_points': ['Analysis in progress'],
                'status': 'Under review'
            }
        elif 'insights' in key:
            return {
                'key_insights': ['Strategic insights being developed'],
                'implications': ['Implications under analysis'],
                'recommendations': ['Recommendations pending']
            }
        elif 'trends' in key:
            return {
                'current_trends': ['Trend analysis in progress'],
                'historical_trends': ['Historical data being compiled'],
                'future_projections': ['Projections under development']
            }
        elif 'security' in key:
            return {
                'security_overview': 'Security analysis in progress',
                'threat_assessment': 'Threat assessment ongoing',
                'vulnerability_analysis': 'Vulnerability analysis pending'
            }
        elif 'economic' in key:
            return {
                'economic_overview': 'Economic analysis in progress',
                'economic_indicators': ['Indicators being compiled'],
                'economic_impact': 'Impact assessment ongoing'
            }
        elif 'forecasting' in key:
            return {
                'forecasting_overview': 'Forecasting analysis in progress',
                'forecasting_methodology': 'Methodology under development',
                'forecasting_results': 'Results pending'
            }
        elif 'capability' in key:
            return {
                'capability_overview': 'Capability assessment in progress',
                'capability_gaps': ['Gap analysis ongoing'],
                'capability_improvements': ['Improvement strategies being developed']
            }
        elif 'recommendations' in key:
            return {
                'strategic_recommendations': ['Strategic recommendations being developed'],
                'implementation_plan': 'Implementation plan under development',
                'priority_actions': ['Priority actions being identified']
            }
        elif 'visualization' in key:
            return {
                'visualization_overview': 'Visualization development in progress',
                'chart_data': ['Chart data being compiled'],
                'interactive_features': ['Interactive features under development']
            }
        elif 'sentiment' in key:
            return {
                'sentiment_overview': 'Sentiment analysis in progress',
                'stakeholder_sentiment': ['Stakeholder sentiment being analyzed'],
                'sentiment_trends': ['Sentiment trends under analysis']
            }
        elif 'regional' in key:
            return {
                'regional_overview': 'Regional analysis in progress',
                'regional_dynamics': ['Regional dynamics being analyzed'],
                'regional_implications': ['Regional implications under assessment']
            }
        elif 'trade' in key:
            return {
                'trade_overview': 'Trade analysis in progress',
                'trade_flows': ['Trade flows being analyzed'],
                'trade_implications': ['Trade implications under assessment']
            }
        elif 'balance' in key:
            return {
                'balance_overview': 'Balance analysis in progress',
                'power_comparison': ['Power comparison being analyzed'],
                'strategic_implications': ['Strategic implications under assessment']
            }
        elif 'risk' in key:
            return {
                'risk_overview': 'Risk assessment in progress',
                'risk_factors': ['Risk factors being identified'],
                'mitigation_strategies': ['Mitigation strategies being developed']
            }
        elif 'implementation' in key:
            return {
                'implementation_overview': 'Implementation analysis in progress',
                'implementation_phases': ['Implementation phases being planned'],
                'implementation_timeline': 'Timeline under development'
            }
        elif 'acquisition' in key:
            return {
                'acquisition_overview': 'Acquisition analysis in progress',
                'acquisition_programs': ['Acquisition programs being analyzed'],
                'acquisition_timeline': 'Acquisition timeline under development'
            }
        elif 'operational' in key:
            return {
                'operational_overview': 'Operational analysis in progress',
                'operational_requirements': ['Operational requirements being analyzed'],
                'operational_considerations': ['Operational considerations under assessment']
            }
        elif 'scenario' in key:
            return {
                'scenario_overview': 'Scenario analysis in progress',
                'scenario_development': ['Scenario development ongoing'],
                'scenario_evaluation': 'Scenario evaluation in progress'
            }
        elif 'performance' in key:
            return {
                'performance_overview': 'Performance analysis in progress',
                'performance_metrics': ['Performance metrics being compiled'],
                'performance_evaluation': 'Performance evaluation ongoing'
            }
        elif 'predictive' in key:
            return {
                'predictive_overview': 'Predictive analysis in progress',
                'predictive_models': ['Predictive models being developed'],
                'predictive_results': 'Predictive results pending'
            }
        else:
            # Generic default for other keys - always return a dictionary
            return {
                'overview': f'{key.replace("_", " ").title()} analysis',
                'key_points': ['Analysis in progress'],
                'status': 'Under development',
                'data_available': False
            }
    
    def _extract_module_data_fallback(self, universal_data: Dict[str, Any], selected_modules: List[str]) -> Dict[str, Any]:
        """Fallback method for data extraction when module classes are not available."""
        print("⚠️ Using fallback data extraction method")
        module_data = {}
        
        for module_name in selected_modules:
            if module_name in universal_data:
                module_specific_data = universal_data[module_name]
                if isinstance(module_specific_data, dict):
                    for key, value in module_specific_data.items():
                        if isinstance(value, dict):
                            module_data.update(value)
                        else:
                            module_data[key] = value
                else:
                    print(f"⚠️ Warning: Module {module_name} data is not a dictionary")
            else:
                print(f"⚠️ Warning: No data found for module {module_name}")
        
        return module_data
    
    def _get_selection_method(
        self,
        max_modules: Optional[int],
        modules: Optional[List[str]],
        module_categories: Optional[List[str]]
    ) -> str:
        """Get the method used for module selection."""
        if modules:
            return f"specific_modules({len(modules)})"
        elif module_categories:
            return f"categories({', '.join(module_categories)})"
        elif max_modules:
            return f"top_{max_modules}_modules"
        else:
            return "all_22_modules"
    
    def get_available_modules(self) -> Dict[str, Any]:
        """Get information about all available modules."""
        return {
            'modules': self.all_modules,
            'categories': self.module_categories,
            'total_modules': len(self.all_modules)
        }
    
    async def generate_all_22_reports(self, user_query: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate all 22 modular reports by default."""
        return await self.generate_adaptive_report(user_query, data)


# Create global instance
integrated_adaptive_modular_report_generator = IntegratedAdaptiveModularReportGenerator()
