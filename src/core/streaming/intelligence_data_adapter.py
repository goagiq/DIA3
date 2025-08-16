"""
Phase 3: Intelligence Data Adapter
Adapter for real-time intelligence data streams.
"""

import asyncio
import json
import numpy as np
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from datetime import datetime, timedelta
from loguru import logger

from .data_stream_processor import EnhancedDataStreamProcessor


@dataclass
class StreamData:
    """Intelligence stream data structure."""
    stream_id: str
    data_type: str  # 'sigint', 'humint', 'osint', 'geospatial', 'cyber'
    raw_data: Dict[str, Any]
    processed_data: Dict[str, Any]
    timestamp: datetime
    confidence_score: float
    source_reliability: float
    metadata: Dict[str, Any]


@dataclass
class StreamConnection:
    """Stream connection configuration."""
    connection_id: str
    stream_type: str
    connection_params: Dict[str, Any]
    is_connected: bool
    last_heartbeat: datetime
    data_count: int
    error_count: int


class SIGINTStreamAdapter:
    """Signals Intelligence stream adapter."""
    
    def __init__(self):
        self.connection = None
        self.data_buffer = []
        self.max_buffer_size = 1000
        
    async def connect(self, connection_params: Dict[str, Any]) -> bool:
        """Connect to SIGINT stream."""
        try:
            # Simulate connection to SIGINT data source
            self.connection = StreamConnection(
                connection_id=f"sigint_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                stream_type="sigint",
                connection_params=connection_params,
                is_connected=True,
                last_heartbeat=datetime.now(),
                data_count=0,
                error_count=0
            )
            logger.info("✅ SIGINT stream connected")
            return True
        except Exception as e:
            logger.error(f"Error connecting to SIGINT stream: {e}")
            return False
    
    async def process_data(self, raw_data: Dict[str, Any]) -> StreamData:
        """Process SIGINT data."""
        try:
            # Process signals intelligence data
            processed_data = {
                'signal_type': raw_data.get('signal_type', 'unknown'),
                'frequency': raw_data.get('frequency', 0.0),
                'strength': raw_data.get('strength', 0.0),
                'location': raw_data.get('location', {}),
                'encryption_level': raw_data.get('encryption_level', 'unknown'),
                'threat_level': self._calculate_threat_level(raw_data),
                'source_confidence': raw_data.get('source_confidence', 0.5)
            }
            
            stream_data = StreamData(
                stream_id=f"sigint_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                data_type="sigint",
                raw_data=raw_data,
                processed_data=processed_data,
                timestamp=datetime.now(),
                confidence_score=processed_data['source_confidence'],
                source_reliability=0.8,
                metadata={'stream_type': 'sigint'}
            )
            
            # Add to buffer
            self.data_buffer.append(stream_data)
            if len(self.data_buffer) > self.max_buffer_size:
                self.data_buffer.pop(0)
            
            return stream_data
            
        except Exception as e:
            logger.error(f"Error processing SIGINT data: {e}")
            raise
    
    def _calculate_threat_level(self, raw_data: Dict[str, Any]) -> str:
        """Calculate threat level from SIGINT data."""
        strength = raw_data.get('strength', 0.0)
        encryption = raw_data.get('encryption_level', 'low')
        
        if strength > 0.8 and encryption in ['high', 'military']:
            return 'high'
        elif strength > 0.5 or encryption in ['medium', 'high']:
            return 'medium'
        else:
            return 'low'


class HUMINTStreamAdapter:
    """Human Intelligence stream adapter."""
    
    def __init__(self):
        self.connection = None
        self.data_buffer = []
        self.max_buffer_size = 1000
        
    async def connect(self, connection_params: Dict[str, Any]) -> bool:
        """Connect to HUMINT stream."""
        try:
            # Simulate connection to HUMINT data source
            self.connection = StreamConnection(
                connection_id=f"humint_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                stream_type="humint",
                connection_params=connection_params,
                is_connected=True,
                last_heartbeat=datetime.now(),
                data_count=0,
                error_count=0
            )
            logger.info("✅ HUMINT stream connected")
            return True
        except Exception as e:
            logger.error(f"Error connecting to HUMINT stream: {e}")
            return False
    
    async def process_data(self, raw_data: Dict[str, Any]) -> StreamData:
        """Process HUMINT data."""
        try:
            # Process human intelligence data
            processed_data = {
                'source_type': raw_data.get('source_type', 'unknown'),
                'reliability_score': raw_data.get('reliability_score', 0.5),
                'information_type': raw_data.get('information_type', 'general'),
                'location': raw_data.get('location', {}),
                'urgency_level': raw_data.get('urgency_level', 'normal'),
                'verification_status': raw_data.get('verification_status', 'pending'),
                'threat_assessment': self._assess_humint_threat(raw_data)
            }
            
            stream_data = StreamData(
                stream_id=f"humint_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                data_type="humint",
                raw_data=raw_data,
                processed_data=processed_data,
                timestamp=datetime.now(),
                confidence_score=processed_data['reliability_score'],
                source_reliability=processed_data['reliability_score'],
                metadata={'stream_type': 'humint'}
            )
            
            # Add to buffer
            self.data_buffer.append(stream_data)
            if len(self.data_buffer) > self.max_buffer_size:
                self.data_buffer.pop(0)
            
            return stream_data
            
        except Exception as e:
            logger.error(f"Error processing HUMINT data: {e}")
            raise
    
    def _assess_humint_threat(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess threat from HUMINT data."""
        reliability = raw_data.get('reliability_score', 0.5)
        urgency = raw_data.get('urgency_level', 'normal')
        
        threat_level = 'low'
        if reliability > 0.7 and urgency in ['high', 'critical']:
            threat_level = 'high'
        elif reliability > 0.5 or urgency == 'high':
            threat_level = 'medium'
        
        return {
            'threat_level': threat_level,
            'confidence': reliability,
            'urgency': urgency
        }


class OSINTStreamAdapter:
    """Open Source Intelligence stream adapter."""
    
    def __init__(self):
        self.connection = None
        self.data_buffer = []
        self.max_buffer_size = 1000
        
    async def connect(self, connection_params: Dict[str, Any]) -> bool:
        """Connect to OSINT stream."""
        try:
            # Simulate connection to OSINT data source
            self.connection = StreamConnection(
                connection_id=f"osint_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                stream_type="osint",
                connection_params=connection_params,
                is_connected=True,
                last_heartbeat=datetime.now(),
                data_count=0,
                error_count=0
            )
            logger.info("✅ OSINT stream connected")
            return True
        except Exception as e:
            logger.error(f"Error connecting to OSINT stream: {e}")
            return False
    
    async def process_data(self, raw_data: Dict[str, Any]) -> StreamData:
        """Process OSINT data."""
        try:
            # Process open source intelligence data
            processed_data = {
                'source_type': raw_data.get('source_type', 'unknown'),
                'content_type': raw_data.get('content_type', 'text'),
                'sentiment_score': raw_data.get('sentiment_score', 0.0),
                'geographic_location': raw_data.get('geographic_location', {}),
                'temporal_context': raw_data.get('temporal_context', {}),
                'credibility_score': raw_data.get('credibility_score', 0.5),
                'trend_analysis': self._analyze_osint_trends(raw_data)
            }
            
            stream_data = StreamData(
                stream_id=f"osint_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                data_type="osint",
                raw_data=raw_data,
                processed_data=processed_data,
                timestamp=datetime.now(),
                confidence_score=processed_data['credibility_score'],
                source_reliability=0.6,
                metadata={'stream_type': 'osint'}
            )
            
            # Add to buffer
            self.data_buffer.append(stream_data)
            if len(self.data_buffer) > self.max_buffer_size:
                self.data_buffer.pop(0)
            
            return stream_data
            
        except Exception as e:
            logger.error(f"Error processing OSINT data: {e}")
            raise
    
    def _analyze_osint_trends(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze trends in OSINT data."""
        sentiment = raw_data.get('sentiment_score', 0.0)
        content = raw_data.get('content', '')
        
        # Simple trend analysis
        trend_direction = 'neutral'
        if sentiment > 0.3:
            trend_direction = 'positive'
        elif sentiment < -0.3:
            trend_direction = 'negative'
        
        return {
            'trend_direction': trend_direction,
            'sentiment_trend': sentiment,
            'content_length': len(content),
            'keyword_density': self._calculate_keyword_density(content)
        }
    
    def _calculate_keyword_density(self, content: str) -> Dict[str, float]:
        """Calculate keyword density in content."""
        keywords = ['threat', 'attack', 'military', 'conflict', 'security']
        density = {}
        
        content_lower = content.lower()
        total_words = len(content_lower.split())
        
        for keyword in keywords:
            count = content_lower.count(keyword)
            density[keyword] = count / max(total_words, 1)
        
        return density


class GeospatialStreamAdapter:
    """Geospatial intelligence stream adapter."""
    
    def __init__(self):
        self.connection = None
        self.data_buffer = []
        self.max_buffer_size = 1000
        
    async def connect(self, connection_params: Dict[str, Any]) -> bool:
        """Connect to geospatial stream."""
        try:
            # Simulate connection to geospatial data source
            self.connection = StreamConnection(
                connection_id=f"geospatial_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                stream_type="geospatial",
                connection_params=connection_params,
                is_connected=True,
                last_heartbeat=datetime.now(),
                data_count=0,
                error_count=0
            )
            logger.info("✅ Geospatial stream connected")
            return True
        except Exception as e:
            logger.error(f"Error connecting to geospatial stream: {e}")
            return False
    
    async def process_data(self, raw_data: Dict[str, Any]) -> StreamData:
        """Process geospatial data."""
        try:
            # Process geospatial intelligence data
            processed_data = {
                'coordinates': raw_data.get('coordinates', {}),
                'elevation': raw_data.get('elevation', 0.0),
                'terrain_type': raw_data.get('terrain_type', 'unknown'),
                'weather_conditions': raw_data.get('weather_conditions', {}),
                'movement_detected': raw_data.get('movement_detected', False),
                'threat_assessment': self._assess_geospatial_threat(raw_data)
            }
            
            stream_data = StreamData(
                stream_id=f"geospatial_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                data_type="geospatial",
                raw_data=raw_data,
                processed_data=processed_data,
                timestamp=datetime.now(),
                confidence_score=0.9,  # Geospatial data is typically high confidence
                source_reliability=0.9,
                metadata={'stream_type': 'geospatial'}
            )
            
            # Add to buffer
            self.data_buffer.append(stream_data)
            if len(self.data_buffer) > self.max_buffer_size:
                self.data_buffer.pop(0)
            
            return stream_data
            
        except Exception as e:
            logger.error(f"Error processing geospatial data: {e}")
            raise
    
    def _assess_geospatial_threat(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess threat from geospatial data."""
        movement = raw_data.get('movement_detected', False)
        coordinates = raw_data.get('coordinates', {})
        
        threat_level = 'low'
        if movement:
            threat_level = 'medium'
            # Additional logic for high threat assessment
            if coordinates.get('proximity_to_critical', False):
                threat_level = 'high'
        
        return {
            'threat_level': threat_level,
            'movement_detected': movement,
            'location_risk': coordinates.get('risk_level', 'low')
        }


class CyberThreatStreamAdapter:
    """Cyber threat intelligence stream adapter."""
    
    def __init__(self):
        self.connection = None
        self.data_buffer = []
        self.max_buffer_size = 1000
        
    async def connect(self, connection_params: Dict[str, Any]) -> bool:
        """Connect to cyber threat stream."""
        try:
            # Simulate connection to cyber threat data source
            self.connection = StreamConnection(
                connection_id=f"cyber_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                stream_type="cyber",
                connection_params=connection_params,
                is_connected=True,
                last_heartbeat=datetime.now(),
                data_count=0,
                error_count=0
            )
            logger.info("✅ Cyber threat stream connected")
            return True
        except Exception as e:
            logger.error(f"Error connecting to cyber threat stream: {e}")
            return False
    
    async def process_data(self, raw_data: Dict[str, Any]) -> StreamData:
        """Process cyber threat data."""
        try:
            # Process cyber threat intelligence data
            processed_data = {
                'threat_type': raw_data.get('threat_type', 'unknown'),
                'severity_level': raw_data.get('severity_level', 'low'),
                'target_system': raw_data.get('target_system', 'unknown'),
                'attack_vector': raw_data.get('attack_vector', 'unknown'),
                'malware_family': raw_data.get('malware_family', 'unknown'),
                'threat_actor': raw_data.get('threat_actor', 'unknown'),
                'threat_assessment': self._assess_cyber_threat(raw_data)
            }
            
            stream_data = StreamData(
                stream_id=f"cyber_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                data_type="cyber",
                raw_data=raw_data,
                processed_data=processed_data,
                timestamp=datetime.now(),
                confidence_score=0.8,
                source_reliability=0.8,
                metadata={'stream_type': 'cyber'}
            )
            
            # Add to buffer
            self.data_buffer.append(stream_data)
            if len(self.data_buffer) > self.max_buffer_size:
                self.data_buffer.pop(0)
            
            return stream_data
            
        except Exception as e:
            logger.error(f"Error processing cyber threat data: {e}")
            raise
    
    def _assess_cyber_threat(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess cyber threat level."""
        severity = raw_data.get('severity_level', 'low')
        threat_type = raw_data.get('threat_type', 'unknown')
        
        threat_level = 'low'
        if severity in ['high', 'critical']:
            threat_level = 'high'
        elif severity == 'medium':
            threat_level = 'medium'
        
        # Adjust based on threat type
        if threat_type in ['apt', 'ransomware', 'zero_day']:
            threat_level = 'high'
        
        return {
            'threat_level': threat_level,
            'severity': severity,
            'threat_type': threat_type,
            'response_urgency': 'immediate' if threat_level == 'high' else 'normal'
        }


class IntelligenceDataAdapter:
    """Adapter for real-time intelligence data streams."""
    
    def __init__(self):
        self.adapters = {
            'sigint_stream': SIGINTStreamAdapter(),
            'humint_stream': HUMINTStreamAdapter(),
            'osint_stream': OSINTStreamAdapter(),
            'geospatial_stream': GeospatialStreamAdapter(),
            'cyber_stream': CyberThreatStreamAdapter()
        }
        self.stream_processor = EnhancedDataStreamProcessor()
        self.active_connections = {}
        self.data_callbacks = []
        
        logger.info("✅ Intelligence Data Adapter initialized")
    
    async def connect_to_stream(self, stream_type: str, connection_params: Dict[str, Any]) -> bool:
        """Connect to intelligence data stream."""
        try:
            if stream_type not in self.adapters:
                raise ValueError(f"Unsupported stream type: {stream_type}")
            
            adapter = self.adapters[stream_type]
            success = await adapter.connect(connection_params)
            
            if success:
                self.active_connections[stream_type] = adapter.connection
                logger.info(f"✅ Connected to {stream_type}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error connecting to {stream_type} stream: {e}")
            return False
    
    async def process_stream_data(self, raw_data: Dict[str, Any]) -> StreamData:
        """Process incoming stream data."""
        try:
            stream_type = raw_data.get('stream_type', 'unknown')
            
            if stream_type not in self.adapters:
                raise ValueError(f"Unsupported stream type: {stream_type}")
            
            adapter = self.adapters[stream_type]
            processed_data = await adapter.process_data(raw_data)
            
            # Trigger real-time analysis
            await self.trigger_real_time_analysis(processed_data)
            
            return processed_data
            
        except Exception as e:
            logger.error(f"Error processing stream data: {e}")
            raise
    
    async def trigger_real_time_analysis(self, processed_data: StreamData):
        """Trigger real-time analysis based on stream data."""
        try:
            # Process data through stream processor
            analysis_result = await self.stream_processor.process_data(processed_data)
            
            # Execute callbacks
            for callback in self.data_callbacks:
                try:
                    await callback(processed_data, analysis_result)
                except Exception as e:
                    logger.warning(f"Error in data callback: {e}")
            
            logger.info(f"✅ Real-time analysis triggered for {processed_data.data_type}")
            
        except Exception as e:
            logger.error(f"Error triggering real-time analysis: {e}")
    
    def register_data_callback(self, callback: Callable):
        """Register a callback for data processing."""
        self.data_callbacks.append(callback)
        logger.info("✅ Data callback registered")
    
    async def get_stream_status(self) -> Dict[str, Any]:
        """Get status of all streams."""
        status = {}
        
        for stream_type, adapter in self.adapters.items():
            if adapter.connection:
                status[stream_type] = {
                    'connected': adapter.connection.is_connected,
                    'last_heartbeat': adapter.connection.last_heartbeat,
                    'data_count': adapter.connection.data_count,
                    'error_count': adapter.connection.error_count,
                    'buffer_size': len(adapter.data_buffer)
                }
            else:
                status[stream_type] = {
                    'connected': False,
                    'last_heartbeat': None,
                    'data_count': 0,
                    'error_count': 0,
                    'buffer_size': 0
                }
        
        return status
    
    async def disconnect_stream(self, stream_type: str) -> bool:
        """Disconnect from a stream."""
        try:
            if stream_type in self.adapters:
                adapter = self.adapters[stream_type]
                if adapter.connection:
                    adapter.connection.is_connected = False
                    adapter.connection = None
                    if stream_type in self.active_connections:
                        del self.active_connections[stream_type]
                    logger.info(f"✅ Disconnected from {stream_type}")
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error disconnecting from {stream_type}: {e}")
            return False
    
    async def get_intelligence_adapter_status(self) -> Dict[str, Any]:
        """Get intelligence adapter status."""
        return {
            'status': 'operational',
            'supported_stream_types': list(self.adapters.keys()),
            'active_connections': len(self.active_connections),
            'total_callbacks': len(self.data_callbacks),
            'stream_status': await self.get_stream_status()
        }
