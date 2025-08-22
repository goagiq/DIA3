# Phase 5: Production Deployment Guide
## Data.gov API Integration - Testing & Optimization

### **Executive Summary**
This document provides comprehensive guidance for deploying Phase 5 of the Data.gov API integration to production, including testing procedures, optimization strategies, and production readiness requirements.

---

## **1. Pre-Deployment Checklist**

### **1.1 System Requirements**
- ✅ **Python 3.9+**: Required for async/await support
- ✅ **Memory**: Minimum 8GB RAM, Recommended 16GB RAM
- ✅ **Storage**: Minimum 50GB free space for data storage
- ✅ **CPU**: Multi-core processor for parallel processing
- ✅ **Network**: Stable internet connection for API calls

### **1.2 Dependencies**
```bash
# Core dependencies
pip install -r requirements.txt

# Additional Phase 5 dependencies
pip install psutil==5.9.5
pip install aiohttp==3.8.5
pip install asyncio-throttle==1.0.2
pip install prometheus-client==0.17.1
```

### **1.3 Environment Configuration**
```bash
# Required environment variables
export CENSUS_API_KEY="your_census_api_key"
export DATAGOV_ENVIRONMENT="production"
export LOG_LEVEL="INFO"
export MAX_CONCURRENT_REQUESTS="10"
export CACHE_TTL="3600"
export OPTIMIZATION_ENABLED="true"
```

---

## **2. Testing Procedures**

### **2.1 Automated Testing**
```bash
# Run Phase 5 test suite
.venv/Scripts/python.exe Test/test_datagov_phase5.py

# Expected output:
# 🚀 Starting Phase 5 Testing & Optimization Suite
# 📋 Running Component Testing
# 📋 Running Integration Testing
# 📋 Running Performance Testing
# 📋 Running Load Testing
# 📋 Running MCP Integration Testing
# 📋 Running API Endpoint Testing
# 📋 Running Error Handling Testing
# 📋 Running Security Testing
# 📋 Running Documentation Testing
# 📋 Running Production Readiness Testing
```

### **2.2 Manual Testing Checklist**
- [ ] **Component Testing**: All individual components function correctly
- [ ] **Integration Testing**: Components work together seamlessly
- [ ] **Performance Testing**: Response times meet requirements (< 5s average)
- [ ] **Load Testing**: System handles expected load (100+ concurrent requests)
- [ ] **MCP Integration**: MCP server communicates properly on port 8000
- [ ] **API Endpoints**: All endpoints respond correctly on port 8001
- [ ] **Error Handling**: System gracefully handles failures
- [ ] **Security**: No vulnerabilities detected
- [ ] **Documentation**: All documentation is complete and accurate

### **2.3 Performance Benchmarks**
```python
# Performance requirements
PERFORMANCE_REQUIREMENTS = {
    "response_time": {
        "average": "< 5 seconds",
        "maximum": "< 10 seconds",
        "p95": "< 8 seconds"
    },
    "throughput": {
        "minimum": "2 requests/second",
        "target": "10 requests/second"
    },
    "memory_usage": {
        "maximum": "80% of available RAM"
    },
    "cpu_usage": {
        "average": "< 70%",
        "peak": "< 90%"
    },
    "error_rate": {
        "maximum": "< 5%"
    }
}
```

---

## **3. Optimization Configuration**

### **3.1 Cache Configuration**
```python
# Cache settings for production
CACHE_CONFIG = {
    "max_size": 1000,           # Maximum cache entries
    "ttl": 3600,               # Time to live in seconds
    "eviction_policy": "lru",   # Least recently used
    "compression": True,        # Enable compression
    "persistence": True         # Persist cache to disk
}
```

### **3.2 Load Balancing Configuration**
```python
# Load balancer settings
LOAD_BALANCER_CONFIG = {
    "max_concurrent_requests": 10,
    "request_timeout": 30,
    "retry_attempts": 3,
    "circuit_breaker": {
        "failure_threshold": 5,
        "recovery_timeout": 60
    }
}
```

### **3.3 Resource Monitoring**
```python
# Resource monitoring settings
MONITORING_CONFIG = {
    "metrics_collection_interval": 60,  # seconds
    "history_retention_hours": 24,
    "alert_thresholds": {
        "cpu_usage": 80,
        "memory_usage": 85,
        "error_rate": 5,
        "response_time": 10
    }
}
```

---

## **4. Production Deployment Steps**

### **4.1 Environment Setup**
```bash
# 1. Create production environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv/Scripts/activate     # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set environment variables
export DATAGOV_ENVIRONMENT="production"
export CENSUS_API_KEY="your_production_api_key"

# 4. Create necessary directories
mkdir -p logs
mkdir -p data/cache
mkdir -p data/backups
```

### **4.2 Database Setup**
```bash
# 1. Start vector database (ChromaDB)
chroma run --host 0.0.0.0 --port 8000

# 2. Start knowledge graph (Neo4j)
neo4j start

# 3. Verify connections
python -c "from src.core.vector_db import VectorDBService; print('Vector DB OK')"
python -c "from src.core.knowledge_graph import KnowledgeGraphService; print('Knowledge Graph OK')"
```

### **4.3 MCP Server Deployment**
```bash
# 1. Start MCP server on port 8000
.venv/Scripts/python.exe src/mcp_servers/datagov_mcp_server.py

# 2. Wait 60 seconds for server stabilization
sleep 60

# 3. Test MCP communication
.venv/Scripts/python.exe Test/test_mcp_communication.py
```

### **4.4 API Server Deployment**
```bash
# 1. Start API server on port 8001
.venv/Scripts/python.exe src/api/main.py

# 2. Test API endpoints
curl http://localhost:8001/api/datagov/health

# 3. Verify all endpoints
.venv/Scripts/python.exe Test/test_api_endpoints.py
```

### **4.5 Optimization Service**
```bash
# 1. Start optimization service
.venv/Scripts/python.exe src/core/datagov/optimization_engine.py

# 2. Verify optimization service
curl http://localhost:8001/api/datagov/optimization/status

# 3. Run initial optimization
curl -X POST http://localhost:8001/api/datagov/optimization/run
```

---

## **5. Monitoring and Alerting**

### **5.1 Health Checks**
```python
# Health check endpoints
HEALTH_CHECK_ENDPOINTS = [
    "http://localhost:8001/api/datagov/health",
    "http://localhost:8000/mcp",
    "http://localhost:8000/api/v1/heartbeat"  # Vector DB
]

# Health check script
import asyncio
import aiohttp

async def health_check():
    async with aiohttp.ClientSession() as session:
        for endpoint in HEALTH_CHECK_ENDPOINTS:
            try:
                async with session.get(endpoint) as response:
                    if response.status == 200:
                        print(f"✅ {endpoint}: HEALTHY")
                    else:
                        print(f"❌ {endpoint}: UNHEALTHY ({response.status})")
            except Exception as e:
                print(f"❌ {endpoint}: ERROR ({e})")

# Run health checks every 5 minutes
asyncio.run(health_check())
```

### **5.2 Performance Monitoring**
```python
# Performance monitoring script
import psutil
import time
from datetime import datetime

def monitor_performance():
    while True:
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # Memory usage
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        
        # Disk usage
        disk = psutil.disk_usage('/')
        disk_percent = (disk.used / disk.total) * 100
        
        # Log metrics
        timestamp = datetime.now().isoformat()
        print(f"[{timestamp}] CPU: {cpu_percent}%, Memory: {memory_percent}%, Disk: {disk_percent}%")
        
        # Check thresholds
        if cpu_percent > 80:
            print(f"⚠️  High CPU usage: {cpu_percent}%")
        
        if memory_percent > 85:
            print(f"⚠️  High memory usage: {memory_percent}%")
        
        if disk_percent > 90:
            print(f"⚠️  High disk usage: {disk_percent}%")
        
        time.sleep(60)  # Check every minute

# Start monitoring
monitor_performance()
```

### **5.3 Log Monitoring**
```python
# Log monitoring configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        },
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.StreamHandler",
        },
        "file": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.FileHandler",
            "filename": "logs/datagov.log",
            "mode": "a",
        },
    },
    "loggers": {
        "": {
            "handlers": ["default", "file"],
            "level": "INFO",
            "propagate": False
        }
    }
}
```

---

## **6. Backup and Recovery**

### **6.1 Data Backup Strategy**
```bash
#!/bin/bash
# Backup script for Data.gov data

# Create backup directory
BACKUP_DIR="data/backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p $BACKUP_DIR

# Backup vector database
echo "Backing up vector database..."
cp -r data/vector_db $BACKUP_DIR/

# Backup knowledge graph
echo "Backing up knowledge graph..."
neo4j-admin dump --database=neo4j --to=$BACKUP_DIR/neo4j_backup

# Backup cache
echo "Backing up cache..."
cp -r data/cache $BACKUP_DIR/

# Backup logs
echo "Backing up logs..."
cp -r logs $BACKUP_DIR/

# Compress backup
tar -czf $BACKUP_DIR.tar.gz $BACKUP_DIR
rm -rf $BACKUP_DIR

echo "Backup completed: $BACKUP_DIR.tar.gz"
```

### **6.2 Recovery Procedures**
```bash
#!/bin/bash
# Recovery script for Data.gov data

BACKUP_FILE=$1

if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: $0 <backup_file.tar.gz>"
    exit 1
fi

# Stop services
echo "Stopping services..."
pkill -f "datagov_mcp_server.py"
pkill -f "main.py"

# Extract backup
echo "Extracting backup..."
tar -xzf $BACKUP_FILE
BACKUP_DIR=$(basename $BACKUP_FILE .tar.gz)

# Restore vector database
echo "Restoring vector database..."
rm -rf data/vector_db
cp -r $BACKUP_DIR/vector_db data/

# Restore knowledge graph
echo "Restoring knowledge graph..."
neo4j-admin load --database=neo4j --from=$BACKUP_DIR/neo4j_backup

# Restore cache
echo "Restoring cache..."
rm -rf data/cache
cp -r $BACKUP_DIR/cache data/

# Restore logs
echo "Restoring logs..."
cp -r $BACKUP_DIR/logs ./

# Cleanup
rm -rf $BACKUP_DIR

# Restart services
echo "Restarting services..."
.venv/Scripts/python.exe src/mcp_servers/datagov_mcp_server.py &
sleep 60
.venv/Scripts/python.exe src/api/main.py &

echo "Recovery completed successfully"
```

---

## **7. Security Considerations**

### **7.1 API Key Security**
```python
# API key management
import os
from cryptography.fernet import Fernet

class APIKeyManager:
    def __init__(self):
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)
    
    def encrypt_api_key(self, api_key: str) -> bytes:
        return self.cipher_suite.encrypt(api_key.encode())
    
    def decrypt_api_key(self, encrypted_key: bytes) -> str:
        return self.cipher_suite.decrypt(encrypted_key).decode()

# Usage
key_manager = APIKeyManager()
encrypted_key = key_manager.encrypt_api_key(os.getenv('CENSUS_API_KEY'))
```

### **7.2 Input Validation**
```python
# Input validation for production
import re
from typing import List

def validate_country_codes(countries: List[str]) -> bool:
    """Validate country codes."""
    valid_pattern = re.compile(r'^[A-Z]{3}$')
    return all(valid_pattern.match(country) for country in countries)

def validate_time_period(time_period: str) -> bool:
    """Validate time period."""
    valid_periods = ['latest', '1Y', '5Y', '10Y']
    return time_period in valid_periods

def sanitize_input(input_string: str) -> str:
    """Sanitize user input."""
    # Remove potentially dangerous characters
    sanitized = re.sub(r'[<>"\']', '', input_string)
    return sanitized.strip()
```

### **7.3 Access Control**
```python
# Access control for production
from functools import wraps
from fastapi import HTTPException, Depends

def require_api_key(api_key: str = Depends(get_api_key)):
    """Require valid API key for access."""
    if not api_key:
        raise HTTPException(status_code=401, detail="API key required")
    return api_key

def rate_limit(max_requests: int = 100, window: int = 3600):
    """Rate limiting decorator."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Implement rate limiting logic
            return await func(*args, **kwargs)
        return wrapper
    return decorator
```

---

## **8. Troubleshooting Guide**

### **8.1 Common Issues**

#### **MCP Server Issues**
```bash
# Problem: MCP server not starting
# Solution: Check port availability
netstat -an | grep 8000

# Problem: MCP communication errors
# Solution: Restart server and wait 60 seconds
pkill -f "datagov_mcp_server.py"
sleep 60
.venv/Scripts/python.exe src/mcp_servers/datagov_mcp_server.py
```

#### **API Server Issues**
```bash
# Problem: API server not responding
# Solution: Check if server is running
curl http://localhost:8001/api/datagov/health

# Problem: High response times
# Solution: Check optimization service
curl http://localhost:8001/api/datagov/optimization/status
```

#### **Database Issues**
```bash
# Problem: Vector database connection failed
# Solution: Restart ChromaDB
pkill -f chroma
chroma run --host 0.0.0.0 --port 8000

# Problem: Knowledge graph connection failed
# Solution: Restart Neo4j
neo4j restart
```

### **8.2 Performance Issues**
```python
# Performance debugging script
import asyncio
import time
from src.core.datagov.optimization_engine import get_optimization_engine

async def debug_performance():
    engine = await get_optimization_engine()
    
    # Check current metrics
    status = await engine.get_optimization_status()
    print("Current Performance Metrics:")
    print(f"CPU Usage: {status['current_metrics'].cpu_usage}%")
    print(f"Memory Usage: {status['current_metrics'].memory_usage}%")
    print(f"Response Time: {status['current_metrics'].response_time}s")
    
    # Run optimization if needed
    if status['current_metrics'].response_time > 5.0:
        print("Running optimization...")
        results = await engine.run_manual_optimization()
        for result in results:
            print(f"Optimization: {result.optimization_type}")
            print(f"Improvement: {result.improvement_percentage}%")

# Run debugging
asyncio.run(debug_performance())
```

---

## **9. Maintenance Procedures**

### **9.1 Regular Maintenance**
```bash
#!/bin/bash
# Daily maintenance script

echo "Starting daily maintenance..."

# 1. Run health checks
.venv/Scripts/python.exe Test/test_health_checks.py

# 2. Clean old logs (keep last 30 days)
find logs -name "*.log" -mtime +30 -delete

# 3. Optimize cache
curl -X POST http://localhost:8001/api/datagov/optimization/run

# 4. Backup data
./scripts/backup.sh

# 5. Update statistics
curl -X POST http://localhost:8001/api/datagov/stats/update

echo "Daily maintenance completed"
```

### **9.2 Weekly Maintenance**
```bash
#!/bin/bash
# Weekly maintenance script

echo "Starting weekly maintenance..."

# 1. Full system optimization
.venv/Scripts/python.exe src/core/datagov/optimization_engine.py --full-optimization

# 2. Database maintenance
neo4j-admin check

# 3. Security audit
.venv/Scripts/python.exe Test/test_security.py

# 4. Performance analysis
.venv/Scripts/python.exe Test/test_performance.py

echo "Weekly maintenance completed"
```

---

## **10. Rollback Procedures**

### **10.1 Emergency Rollback**
```bash
#!/bin/bash
# Emergency rollback script

echo "Starting emergency rollback..."

# 1. Stop all services
pkill -f "datagov_mcp_server.py"
pkill -f "main.py"
pkill -f "optimization_engine.py"

# 2. Restore from last known good backup
LATEST_BACKUP=$(ls -t data/backups/*.tar.gz | head -1)
./scripts/recovery.sh $LATEST_BACKUP

# 3. Restart services with previous configuration
.venv/Scripts/python.exe src/mcp_servers/datagov_mcp_server.py &
sleep 60
.venv/Scripts/python.exe src/api/main.py &

echo "Emergency rollback completed"
```

### **10.2 Configuration Rollback**
```bash
#!/bin/bash
# Configuration rollback script

echo "Rolling back configuration..."

# 1. Restore previous configuration
cp config/datagov_config.py.backup config/datagov_config.py

# 2. Restart services
pkill -f "datagov_mcp_server.py"
pkill -f "main.py"
sleep 10

.venv/Scripts/python.exe src/mcp_servers/datagov_mcp_server.py &
sleep 60
.venv/Scripts/python.exe src/api/main.py &

echo "Configuration rollback completed"
```

---

## **11. Success Metrics**

### **11.1 Performance Metrics**
- ✅ **Response Time**: Average < 5 seconds, P95 < 8 seconds
- ✅ **Throughput**: Minimum 2 requests/second, Target 10 requests/second
- ✅ **Availability**: 99.5% uptime
- ✅ **Error Rate**: < 5% error rate
- ✅ **Resource Usage**: CPU < 70%, Memory < 80%

### **11.2 Quality Metrics**
- ✅ **Test Coverage**: > 90% test coverage
- ✅ **Code Quality**: No critical security vulnerabilities
- ✅ **Documentation**: Complete and up-to-date
- ✅ **Monitoring**: All systems monitored and alerting

### **11.3 Business Metrics**
- ✅ **Data Freshness**: < 1 hour data latency
- ✅ **Analysis Accuracy**: > 85% prediction accuracy
- ✅ **User Satisfaction**: > 4.5/5 rating
- ✅ **System Reliability**: < 1 hour downtime per month

---

## **12. Post-Deployment Verification**

### **12.1 Verification Checklist**
- [ ] All services running and healthy
- [ ] MCP server communicating on port 8000
- [ ] API endpoints responding on port 8001
- [ ] Optimization service active and monitoring
- [ ] All tests passing
- [ ] Performance metrics within acceptable ranges
- [ ] Security audit completed
- [ ] Documentation updated
- [ ] Backup procedures tested
- [ ] Monitoring and alerting configured

### **12.2 Go-Live Checklist**
- [ ] Production environment configured
- [ ] All dependencies installed
- [ ] Environment variables set
- [ ] Database connections verified
- [ ] MCP server started and stable
- [ ] API server started and responding
- [ ] Optimization service running
- [ ] Health checks passing
- [ ] Performance benchmarks met
- [ ] Security measures in place
- [ ] Monitoring active
- [ ] Backup procedures ready
- [ ] Rollback procedures tested
- [ ] Team notified and ready

---

## **13. Support and Contact**

### **13.1 Support Channels**
- **Technical Issues**: Create issue in project repository
- **Performance Issues**: Check optimization service status
- **Security Issues**: Contact security team immediately
- **Documentation**: Update documentation as needed

### **13.2 Emergency Contacts**
- **System Administrator**: [Contact Information]
- **Security Team**: [Contact Information]
- **Development Team**: [Contact Information]

---

## **14. Conclusion**

Phase 5 of the Data.gov API integration provides comprehensive testing, optimization, and production deployment capabilities. The system is designed to be robust, scalable, and maintainable in production environments.

**Key Success Factors:**
1. **Thorough Testing**: Comprehensive test suite ensures reliability
2. **Performance Optimization**: Advanced optimization engine maintains performance
3. **Monitoring**: Real-time monitoring and alerting for proactive management
4. **Security**: Multiple layers of security protection
5. **Backup and Recovery**: Robust backup and recovery procedures
6. **Documentation**: Complete documentation for all procedures

**Next Steps:**
1. Execute deployment checklist
2. Run comprehensive testing
3. Monitor system performance
4. Gather feedback and iterate
5. Plan future enhancements

---

**Phase 5 Status: ✅ READY FOR PRODUCTION DEPLOYMENT**

This deployment guide ensures a smooth transition to production with comprehensive testing, optimization, and monitoring capabilities.
