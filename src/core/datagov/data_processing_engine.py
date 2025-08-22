"""
Data Processing Engine for Data.gov API Integration
Phase 2 Implementation - Data Processing & Validation
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional, Union
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from dataclasses import dataclass, field
from enum import Enum

from src.core.models import DataType, ProcessingStatus
from src.core.vector_db import VectorDBManager
from src.core.knowledge_graph_integration import KnowledgeGraphService
from src.config.datagov_config import DataGovConfig

logger = logging.getLogger(__name__)


class DataQualityLevel(Enum):
    """Data quality assessment levels."""
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    UNUSABLE = "unusable"


@dataclass
class DataValidationResult:
    """Result of data validation process."""
    is_valid: bool
    quality_level: DataQualityLevel
    issues: List[str] = field(default_factory=list)
    missing_fields: List[str] = field(default_factory=list)
    outlier_count: int = 0
    duplicate_count: int = 0
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class ProcessedData:
    """Container for processed data."""
    raw_data: Dict[str, Any]
    processed_data: Dict[str, Any]
    validation_result: DataValidationResult
    embeddings: Optional[List[float]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    processing_timestamp: datetime = field(default_factory=datetime.utcnow)


class DataProcessingEngine:
    """
    Core data processing engine for Data.gov integration.
    Handles data cleaning, validation, transformation, and storage.
    """
    
    def __init__(self):
        self.config = DataGovConfig()
        self.vector_db = VectorDBManager()
        self.knowledge_graph = KnowledgeGraphService()
        self.logger = logging.getLogger(__name__)
        
        # Data quality thresholds
        self.quality_thresholds = {
            'missing_data_threshold': 0.1,  # 10% missing data allowed
            'outlier_threshold': 0.05,      # 5% outliers allowed
            'duplicate_threshold': 0.02,    # 2% duplicates allowed
        }
    
    async def process_trade_data(self, raw_data: Dict[str, Any]) -> ProcessedData:
        """
        Process trade data from Census and USITC APIs.
        
        Args:
            raw_data: Raw trade data from APIs
            
        Returns:
            ProcessedData: Cleaned and validated trade data
        """
        try:
            self.logger.info("Processing trade data...")
            
            # Validate input data
            validation_result = await self._validate_trade_data(raw_data)
            
            if not validation_result.is_valid:
                self.logger.warning(f"Trade data validation failed: {validation_result.issues}")
                return ProcessedData(
                    raw_data=raw_data,
                    processed_data={},
                    validation_result=validation_result
                )
            
            # Clean and transform data
            processed_data = await self._clean_trade_data(raw_data)
            
            # Generate embeddings
            embeddings = await self._generate_trade_embeddings(processed_data)
            
            # Create knowledge graph relationships
            await self._create_trade_relationships(processed_data)
            
            return ProcessedData(
                raw_data=raw_data,
                processed_data=processed_data,
                validation_result=validation_result,
                embeddings=embeddings,
                metadata={
                    "data_type": "trade_data",
                    "source_apis": list(raw_data.keys()),
                    "record_count": len(processed_data.get('records', [])),
                    "processing_version": "2.0"
                }
            )
            
        except Exception as e:
            self.logger.error(f"Error processing trade data: {e}")
            raise
    
    async def process_macroeconomic_data(self, raw_data: Dict[str, Any]) -> ProcessedData:
        """
        Process macroeconomic data from USDA APIs.
        
        Args:
            raw_data: Raw macroeconomic data from APIs
            
        Returns:
            ProcessedData: Cleaned and validated macroeconomic data
        """
        try:
            self.logger.info("Processing macroeconomic data...")
            
            # Validate input data
            validation_result = await self._validate_macroeconomic_data(raw_data)
            
            if not validation_result.is_valid:
                self.logger.warning(f"Macroeconomic data validation failed: {validation_result.issues}")
                return ProcessedData(
                    raw_data=raw_data,
                    processed_data={},
                    validation_result=validation_result
                )
            
            # Clean and transform data
            processed_data = await self._clean_macroeconomic_data(raw_data)
            
            # Generate embeddings
            embeddings = await self._generate_macroeconomic_embeddings(processed_data)
            
            # Create knowledge graph relationships
            await self._create_macroeconomic_relationships(processed_data)
            
            return ProcessedData(
                raw_data=raw_data,
                processed_data=processed_data,
                validation_result=validation_result,
                embeddings=embeddings,
                metadata={
                    "data_type": "macroeconomic_data",
                    "source_apis": list(raw_data.keys()),
                    "record_count": len(processed_data.get('records', [])),
                    "processing_version": "2.0"
                }
            )
            
        except Exception as e:
            self.logger.error(f"Error processing macroeconomic data: {e}")
            raise
    
    async def process_environmental_data(self, raw_data: Dict[str, Any]) -> ProcessedData:
        """
        Process environmental data from EPI APIs.
        
        Args:
            raw_data: Raw environmental data from APIs
            
        Returns:
            ProcessedData: Cleaned and validated environmental data
        """
        try:
            self.logger.info("Processing environmental data...")
            
            # Validate input data
            validation_result = await self._validate_environmental_data(raw_data)
            
            if not validation_result.is_valid:
                self.logger.warning(f"Environmental data validation failed: {validation_result.issues}")
                return ProcessedData(
                    raw_data=raw_data,
                    processed_data={},
                    validation_result=validation_result
                )
            
            # Clean and transform data
            processed_data = await self._clean_environmental_data(raw_data)
            
            # Generate embeddings
            embeddings = await self._generate_environmental_embeddings(processed_data)
            
            # Create knowledge graph relationships
            await self._create_environmental_relationships(processed_data)
            
            return ProcessedData(
                raw_data=raw_data,
                processed_data=processed_data,
                validation_result=validation_result,
                embeddings=embeddings,
                metadata={
                    "data_type": "environmental_data",
                    "source_apis": list(raw_data.keys()),
                    "record_count": len(processed_data.get('records', [])),
                    "processing_version": "2.0"
                }
            )
            
        except Exception as e:
            self.logger.error(f"Error processing environmental data: {e}")
            raise
    
    async def _validate_trade_data(self, data: Dict[str, Any]) -> DataValidationResult:
        """Validate trade data quality and completeness."""
        issues = []
        missing_fields = []
        outlier_count = 0
        duplicate_count = 0
        
        # Check for required fields
        required_fields = ['country_code', 'trade_value', 'date', 'commodity_code']
        
        for record in data.get('records', []):
            for field in required_fields:
                if field not in record or record[field] is None:
                    missing_fields.append(field)
            
            # Check for outliers in trade values
            if 'trade_value' in record and record['trade_value'] is not None:
                if record['trade_value'] < 0 or record['trade_value'] > 1e12:  # $1 trillion threshold
                    outlier_count += 1
        
        # Check for duplicates
        seen_records = set()
        for record in data.get('records', []):
            record_key = f"{record.get('country_code')}_{record.get('date')}_{record.get('commodity_code')}"
            if record_key in seen_records:
                duplicate_count += 1
            else:
                seen_records.add(record_key)
        
        # Assess quality level
        total_records = len(data.get('records', []))
        if total_records == 0:
            quality_level = DataQualityLevel.UNUSABLE
            issues.append("No records found in data")
        else:
            missing_ratio = len(missing_fields) / (total_records * len(required_fields))
            outlier_ratio = outlier_count / total_records
            duplicate_ratio = duplicate_count / total_records
            
            if (missing_ratio < 0.05 and outlier_ratio < 0.02 and duplicate_ratio < 0.01):
                quality_level = DataQualityLevel.EXCELLENT
            elif (missing_ratio < 0.1 and outlier_ratio < 0.05 and duplicate_ratio < 0.02):
                quality_level = DataQualityLevel.GOOD
            elif (missing_ratio < 0.2 and outlier_ratio < 0.1 and duplicate_ratio < 0.05):
                quality_level = DataQualityLevel.FAIR
            elif (missing_ratio < 0.5 and outlier_ratio < 0.2 and duplicate_ratio < 0.1):
                quality_level = DataQualityLevel.POOR
            else:
                quality_level = DataQualityLevel.UNUSABLE
        
        is_valid = quality_level in [DataQualityLevel.EXCELLENT, DataQualityLevel.GOOD, DataQualityLevel.FAIR]
        
        return DataValidationResult(
            is_valid=is_valid,
            quality_level=quality_level,
            issues=issues,
            missing_fields=list(set(missing_fields)),
            outlier_count=outlier_count,
            duplicate_count=duplicate_count
        )
    
    async def _validate_macroeconomic_data(self, data: Dict[str, Any]) -> DataValidationResult:
        """Validate macroeconomic data quality and completeness."""
        issues = []
        missing_fields = []
        outlier_count = 0
        duplicate_count = 0
        
        # Check for required fields
        required_fields = ['country_code', 'gdp', 'population', 'date']
        
        for record in data.get('records', []):
            for field in required_fields:
                if field not in record or record[field] is None:
                    missing_fields.append(field)
            
            # Check for outliers in GDP and population
            if 'gdp' in record and record['gdp'] is not None:
                if record['gdp'] < 0 or record['gdp'] > 1e15:  # $1 quadrillion threshold
                    outlier_count += 1
            
            if 'population' in record and record['population'] is not None:
                if record['population'] < 0 or record['population'] > 2e10:  # 20 billion threshold
                    outlier_count += 1
        
        # Check for duplicates
        seen_records = set()
        for record in data.get('records', []):
            record_key = f"{record.get('country_code')}_{record.get('date')}"
            if record_key in seen_records:
                duplicate_count += 1
            else:
                seen_records.add(record_key)
        
        # Assess quality level
        total_records = len(data.get('records', []))
        if total_records == 0:
            quality_level = DataQualityLevel.UNUSABLE
            issues.append("No records found in data")
        else:
            missing_ratio = len(missing_fields) / (total_records * len(required_fields))
            outlier_ratio = outlier_count / total_records
            duplicate_ratio = duplicate_count / total_records
            
            if (missing_ratio < 0.05 and outlier_ratio < 0.02 and duplicate_ratio < 0.01):
                quality_level = DataQualityLevel.EXCELLENT
            elif (missing_ratio < 0.1 and outlier_ratio < 0.05 and duplicate_ratio < 0.02):
                quality_level = DataQualityLevel.GOOD
            elif (missing_ratio < 0.2 and outlier_ratio < 0.1 and duplicate_ratio < 0.05):
                quality_level = DataQualityLevel.FAIR
            elif (missing_ratio < 0.5 and outlier_ratio < 0.2 and duplicate_ratio < 0.1):
                quality_level = DataQualityLevel.POOR
            else:
                quality_level = DataQualityLevel.UNUSABLE
        
        is_valid = quality_level in [DataQualityLevel.EXCELLENT, DataQualityLevel.GOOD, DataQualityLevel.FAIR]
        
        return DataValidationResult(
            is_valid=is_valid,
            quality_level=quality_level,
            issues=issues,
            missing_fields=list(set(missing_fields)),
            outlier_count=outlier_count,
            duplicate_count=duplicate_count
        )
    
    async def _validate_environmental_data(self, data: Dict[str, Any]) -> DataValidationResult:
        """Validate environmental data quality and completeness."""
        issues = []
        missing_fields = []
        outlier_count = 0
        duplicate_count = 0
        
        # Check for required fields
        required_fields = ['country_code', 'epi_score', 'date']
        
        for record in data.get('records', []):
            for field in required_fields:
                if field not in record or record[field] is None:
                    missing_fields.append(field)
            
            # Check for outliers in EPI scores
            if 'epi_score' in record and record['epi_score'] is not None:
                if record['epi_score'] < 0 or record['epi_score'] > 100:
                    outlier_count += 1
        
        # Check for duplicates
        seen_records = set()
        for record in data.get('records', []):
            record_key = f"{record.get('country_code')}_{record.get('date')}"
            if record_key in seen_records:
                duplicate_count += 1
            else:
                seen_records.add(record_key)
        
        # Assess quality level
        total_records = len(data.get('records', []))
        if total_records == 0:
            quality_level = DataQualityLevel.UNUSABLE
            issues.append("No records found in data")
        else:
            missing_ratio = len(missing_fields) / (total_records * len(required_fields))
            outlier_ratio = outlier_count / total_records
            duplicate_ratio = duplicate_count / total_records
            
            if (missing_ratio < 0.05 and outlier_ratio < 0.02 and duplicate_ratio < 0.01):
                quality_level = DataQualityLevel.EXCELLENT
            elif (missing_ratio < 0.1 and outlier_ratio < 0.05 and duplicate_ratio < 0.02):
                quality_level = DataQualityLevel.GOOD
            elif (missing_ratio < 0.2 and outlier_ratio < 0.1 and duplicate_ratio < 0.05):
                quality_level = DataQualityLevel.FAIR
            elif (missing_ratio < 0.5 and outlier_ratio < 0.2 and duplicate_ratio < 0.1):
                quality_level = DataQualityLevel.POOR
            else:
                quality_level = DataQualityLevel.UNUSABLE
        
        is_valid = quality_level in [DataQualityLevel.EXCELLENT, DataQualityLevel.GOOD, DataQualityLevel.FAIR]
        
        return DataValidationResult(
            is_valid=is_valid,
            quality_level=quality_level,
            issues=issues,
            missing_fields=list(set(missing_fields)),
            outlier_count=outlier_count,
            duplicate_count=duplicate_count
        )
    
    async def _clean_trade_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Clean and transform trade data."""
        cleaned_data = {
            'records': [],
            'summary': {},
            'metadata': {}
        }
        
        # Clean individual records
        for record in data.get('records', []):
            cleaned_record = {
                'country_code': str(record.get('country_code', '')).strip().upper(),
                'trade_value': float(record.get('trade_value', 0)) if record.get('trade_value') is not None else 0,
                'date': self._parse_date(record.get('date')),
                'commodity_code': str(record.get('commodity_code', '')).strip(),
                'trade_type': str(record.get('trade_type', 'import')).strip().lower(),
                'currency': str(record.get('currency', 'USD')).strip().upper()
            }
            
            # Remove records with invalid data
            if (cleaned_record['country_code'] and 
                cleaned_record['trade_value'] > 0 and 
                cleaned_record['date']):
                cleaned_data['records'].append(cleaned_record)
        
        # Generate summary statistics
        if cleaned_data['records']:
            df = pd.DataFrame(cleaned_data['records'])
            cleaned_data['summary'] = {
                'total_records': len(cleaned_data['records']),
                'total_trade_value': df['trade_value'].sum(),
                'avg_trade_value': df['trade_value'].mean(),
                'countries': df['country_code'].unique().tolist(),
                'date_range': {
                    'start': df['date'].min().isoformat(),
                    'end': df['date'].max().isoformat()
                }
            }
        
        cleaned_data['metadata'] = {
            'cleaning_timestamp': datetime.utcnow().isoformat(),
            'original_record_count': len(data.get('records', [])),
            'cleaned_record_count': len(cleaned_data['records']),
            'cleaning_version': '2.0'
        }
        
        return cleaned_data
    
    async def _clean_macroeconomic_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Clean and transform macroeconomic data."""
        cleaned_data = {
            'records': [],
            'summary': {},
            'metadata': {}
        }
        
        # Clean individual records
        for record in data.get('records', []):
            cleaned_record = {
                'country_code': str(record.get('country_code', '')).strip().upper(),
                'gdp': float(record.get('gdp', 0)) if record.get('gdp') is not None else 0,
                'population': float(record.get('population', 0)) if record.get('population') is not None else 0,
                'date': self._parse_date(record.get('date')),
                'gdp_per_capita': float(record.get('gdp_per_capita', 0)) if record.get('gdp_per_capita') is not None else 0,
                'currency': str(record.get('currency', 'USD')).strip().upper()
            }
            
            # Calculate GDP per capita if not provided
            if cleaned_record['gdp_per_capita'] == 0 and cleaned_record['population'] > 0:
                cleaned_record['gdp_per_capita'] = cleaned_record['gdp'] / cleaned_record['population']
            
            # Remove records with invalid data
            if (cleaned_record['country_code'] and 
                cleaned_record['gdp'] > 0 and 
                cleaned_record['population'] > 0 and 
                cleaned_record['date']):
                cleaned_data['records'].append(cleaned_record)
        
        # Generate summary statistics
        if cleaned_data['records']:
            df = pd.DataFrame(cleaned_data['records'])
            cleaned_data['summary'] = {
                'total_records': len(cleaned_data['records']),
                'total_gdp': df['gdp'].sum(),
                'total_population': df['population'].sum(),
                'avg_gdp_per_capita': df['gdp_per_capita'].mean(),
                'countries': df['country_code'].unique().tolist(),
                'date_range': {
                    'start': df['date'].min().isoformat(),
                    'end': df['date'].max().isoformat()
                }
            }
        
        cleaned_data['metadata'] = {
            'cleaning_timestamp': datetime.utcnow().isoformat(),
            'original_record_count': len(data.get('records', [])),
            'cleaned_record_count': len(cleaned_data['records']),
            'cleaning_version': '2.0'
        }
        
        return cleaned_data
    
    async def _clean_environmental_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Clean and transform environmental data."""
        cleaned_data = {
            'records': [],
            'summary': {},
            'metadata': {}
        }
        
        # Clean individual records
        for record in data.get('records', []):
            cleaned_record = {
                'country_code': str(record.get('country_code', '')).strip().upper(),
                'epi_score': float(record.get('epi_score', 0)) if record.get('epi_score') is not None else 0,
                'date': self._parse_date(record.get('date')),
                'air_quality': float(record.get('air_quality', 0)) if record.get('air_quality') is not None else 0,
                'water_quality': float(record.get('water_quality', 0)) if record.get('water_quality') is not None else 0,
                'biodiversity': float(record.get('biodiversity', 0)) if record.get('biodiversity') is not None else 0
            }
            
            # Remove records with invalid data
            if (cleaned_record['country_code'] and 
                cleaned_record['epi_score'] > 0 and 
                cleaned_record['date']):
                cleaned_data['records'].append(cleaned_record)
        
        # Generate summary statistics
        if cleaned_data['records']:
            df = pd.DataFrame(cleaned_data['records'])
            cleaned_data['summary'] = {
                'total_records': len(cleaned_data['records']),
                'avg_epi_score': df['epi_score'].mean(),
                'avg_air_quality': df['air_quality'].mean(),
                'avg_water_quality': df['water_quality'].mean(),
                'avg_biodiversity': df['biodiversity'].mean(),
                'countries': df['country_code'].unique().tolist(),
                'date_range': {
                    'start': df['date'].min().isoformat(),
                    'end': df['date'].max().isoformat()
                }
            }
        
        cleaned_data['metadata'] = {
            'cleaning_timestamp': datetime.utcnow().isoformat(),
            'original_record_count': len(data.get('records', [])),
            'cleaned_record_count': len(cleaned_data['records']),
            'cleaning_version': '2.0'
        }
        
        return cleaned_data
    
    async def _generate_trade_embeddings(self, data: Dict[str, Any]) -> List[float]:
        """Generate embeddings for trade data."""
        try:
            # Create text representation for embedding
            text_content = []
            
            for record in data.get('records', []):
                text_content.append(
                    f"Trade data for {record.get('country_code')} "
                    f"on {record.get('date')} with value {record.get('trade_value')} "
                    f"for commodity {record.get('commodity_code')}"
                )
            
            if text_content:
                combined_text = " ".join(text_content)
                embeddings = await self.vector_db.generate_embeddings(combined_text)
                return embeddings
            
            return []
            
        except Exception as e:
            self.logger.error(f"Error generating trade embeddings: {e}")
            return []
    
    async def _generate_macroeconomic_embeddings(self, data: Dict[str, Any]) -> List[float]:
        """Generate embeddings for macroeconomic data."""
        try:
            # Create text representation for embedding
            text_content = []
            
            for record in data.get('records', []):
                text_content.append(
                    f"Economic data for {record.get('country_code')} "
                    f"on {record.get('date')} with GDP {record.get('gdp')} "
                    f"and population {record.get('population')}"
                )
            
            if text_content:
                combined_text = " ".join(text_content)
                embeddings = await self.vector_db.generate_embeddings(combined_text)
                return embeddings
            
            return []
            
        except Exception as e:
            self.logger.error(f"Error generating macroeconomic embeddings: {e}")
            return []
    
    async def _generate_environmental_embeddings(self, data: Dict[str, Any]) -> List[float]:
        """Generate embeddings for environmental data."""
        try:
            # Create text representation for embedding
            text_content = []
            
            for record in data.get('records', []):
                text_content.append(
                    f"Environmental data for {record.get('country_code')} "
                    f"on {record.get('date')} with EPI score {record.get('epi_score')} "
                    f"air quality {record.get('air_quality')} water quality {record.get('water_quality')}"
                )
            
            if text_content:
                combined_text = " ".join(text_content)
                embeddings = await self.vector_db.generate_embeddings(combined_text)
                return embeddings
            
            return []
            
        except Exception as e:
            self.logger.error(f"Error generating environmental embeddings: {e}")
            return []
    
    async def _create_trade_relationships(self, data: Dict[str, Any]):
        """Create knowledge graph relationships for trade data."""
        try:
            for record in data.get('records', []):
                # Create country node
                await self.knowledge_graph.create_node(
                    label="Country",
                    properties={
                        "code": record.get('country_code'),
                        "name": record.get('country_code')  # Could be enhanced with country names
                    }
                )
                
                # Create trade relationship
                await self.knowledge_graph.create_relationship(
                    from_label="Country",
                    from_properties={"code": record.get('country_code')},
                    to_label="TradeData",
                    to_properties={
                        "date": record.get('date').isoformat(),
                        "value": record.get('trade_value'),
                        "commodity": record.get('commodity_code'),
                        "type": record.get('trade_type')
                    },
                    relationship_type="HAS_TRADE_DATA"
                )
                
        except Exception as e:
            self.logger.error(f"Error creating trade relationships: {e}")
    
    async def _create_macroeconomic_relationships(self, data: Dict[str, Any]):
        """Create knowledge graph relationships for macroeconomic data."""
        try:
            for record in data.get('records', []):
                # Create country node
                await self.knowledge_graph.create_node(
                    label="Country",
                    properties={
                        "code": record.get('country_code'),
                        "name": record.get('country_code')  # Could be enhanced with country names
                    }
                )
                
                # Create economic relationship
                await self.knowledge_graph.create_relationship(
                    from_label="Country",
                    from_properties={"code": record.get('country_code')},
                    to_label="EconomicData",
                    to_properties={
                        "date": record.get('date').isoformat(),
                        "gdp": record.get('gdp'),
                        "population": record.get('population'),
                        "gdp_per_capita": record.get('gdp_per_capita')
                    },
                    relationship_type="HAS_ECONOMIC_DATA"
                )
                
        except Exception as e:
            self.logger.error(f"Error creating macroeconomic relationships: {e}")
    
    async def _create_environmental_relationships(self, data: Dict[str, Any]):
        """Create knowledge graph relationships for environmental data."""
        try:
            for record in data.get('records', []):
                # Create country node
                await self.knowledge_graph.create_node(
                    label="Country",
                    properties={
                        "code": record.get('country_code'),
                        "name": record.get('country_code')  # Could be enhanced with country names
                    }
                )
                
                # Create environmental relationship
                await self.knowledge_graph.create_relationship(
                    from_label="Country",
                    from_properties={"code": record.get('country_code')},
                    to_label="EnvironmentalData",
                    to_properties={
                        "date": record.get('date').isoformat(),
                        "epi_score": record.get('epi_score'),
                        "air_quality": record.get('air_quality'),
                        "water_quality": record.get('water_quality'),
                        "biodiversity": record.get('biodiversity')
                    },
                    relationship_type="HAS_ENVIRONMENTAL_DATA"
                )
                
        except Exception as e:
            self.logger.error(f"Error creating environmental relationships: {e}")
    
    def _parse_date(self, date_value: Any) -> Optional[datetime]:
        """Parse date value into datetime object."""
        if date_value is None:
            return None
        
        try:
            if isinstance(date_value, str):
                # Try different date formats
                for fmt in ['%Y-%m-%d', '%Y-%m', '%Y', '%m/%d/%Y', '%d/%m/%Y']:
                    try:
                        return datetime.strptime(date_value, fmt)
                    except ValueError:
                        continue
            elif isinstance(date_value, datetime):
                return date_value
            
            return None
            
        except Exception:
            return None
    
    async def store_processed_data(self, processed_data: ProcessedData) -> bool:
        """Store processed data in vector database and knowledge graph."""
        try:
            # Store embeddings in vector database
            if processed_data.embeddings:
                await self.vector_db.store_datagov_embeddings({
                    'embeddings': processed_data.embeddings,
                    'metadata': processed_data.metadata,
                    'data_type': processed_data.metadata.get('data_type', 'unknown')
                })
            
            # Store in knowledge graph (relationships already created during processing)
            self.logger.info(f"Successfully stored processed {processed_data.metadata.get('data_type', 'unknown')} data")
            return True
            
        except Exception as e:
            self.logger.error(f"Error storing processed data: {e}")
            return False
    
    async def get_data_quality_report(self, processed_data: ProcessedData) -> Dict[str, Any]:
        """Generate comprehensive data quality report."""
        return {
            'validation_result': {
                'is_valid': processed_data.validation_result.is_valid,
                'quality_level': processed_data.validation_result.quality_level.value,
                'issues': processed_data.validation_result.issues,
                'missing_fields': processed_data.validation_result.missing_fields,
                'outlier_count': processed_data.validation_result.outlier_count,
                'duplicate_count': processed_data.validation_result.duplicate_count
            },
            'processing_metadata': processed_data.metadata,
            'processing_timestamp': processed_data.processing_timestamp.isoformat(),
            'embeddings_generated': len(processed_data.embeddings) if processed_data.embeddings else 0,
            'record_count': processed_data.metadata.get('record_count', 0)
        }
