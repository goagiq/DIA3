# DIA3 Deployment Architecture

## Overview

The DIA3 (Distributed Intelligence Analysis System) deployment architecture is designed for high availability, scalability, and production readiness. The system supports both Docker Compose and Kubernetes deployment models with comprehensive monitoring and security configurations.

## Deployment Architecture Diagram

```mermaid
graph TB
    %% External Access Layer
    subgraph "External Access"
        LB[Load Balancer<br/>Nginx Reverse Proxy<br/>Ports 80/443]
        SSL[SSL Termination<br/>TLS 1.3]
    end
    
    %% Application Layer
    subgraph "Application Services"
        MCP[MCP Server<br/>Port 8000<br/>Model Control Protocol]
        API[FastAPI Gateway<br/>Port 8003<br/>REST API + Health Checks]
        UI1[Streamlit Main UI<br/>Port 8501<br/>Primary Dashboard]
        UI2[Streamlit Landing<br/>Port 8502<br/>Landing Page]
    end
    
    %% Core Services Layer
    subgraph "Core Services"
        ORCH[Orchestrator<br/>Task Management<br/>Workflow Engine]
        AGENTS[AI Agent Swarm<br/>Multi-Modal Processing<br/>Strategic Analysis]
        ANALYTICS[Advanced Analytics<br/>ML + Monte Carlo<br/>Forecasting Engine]
    end
    
    %% Data Layer
    subgraph "Data Storage"
        CHROMA[(ChromaDB<br/>Vector Database<br/>Document Storage)]
        REDIS[(Redis Cache<br/>Session + Cache<br/>Port 6379)]
        FILE[File Storage<br/>Data + Results<br/>Persistent Volumes]
    end
    
    %% External AI Services
    subgraph "External AI Services"
        OLLAMA[Ollama<br/>Local LLM<br/>Port 11434]
        OPENAI[OpenAI API<br/>Cloud LLM<br/>Rate Limited]
        YOUTUBE[YouTube API<br/>Video Processing<br/>Quota Managed]
    end
    
    %% Monitoring & Observability
    subgraph "Monitoring Stack"
        PROM[Prometheus<br/>Metrics Collection<br/>Port 9090]
        GRAFANA[Grafana<br/>Visualization<br/>Port 3000]
        LOGS[Log Aggregation<br/>Structured Logging]
    end
    
    %% Infrastructure Layer
    subgraph "Infrastructure"
        K8S[Kubernetes Cluster<br/>Deployment + HPA<br/>ConfigMaps + Secrets]
        DOCKER[Docker Compose<br/>Development/Staging<br/>Service Discovery]
        VOLUMES[Persistent Volumes<br/>Data + Cache<br/>Backup Strategy]
    end
    
    %% Security Layer
    subgraph "Security"
        SECRETS[Secrets Management<br/>API Keys + Credentials<br/>Encrypted Storage]
        RBAC[RBAC + Network Policies<br/>Service Mesh Ready<br/>Zero Trust]
        AUDIT[Audit Logging<br/>Compliance + Monitoring<br/>Access Control]
    end
    
    %% Connection Flow
    LB --> SSL
    SSL --> MCP
    SSL --> API
    SSL --> UI1
    SSL --> UI2
    
    MCP --> ORCH
    API --> ORCH
    UI1 --> API
    UI2 --> API
    
    ORCH --> AGENTS
    ORCH --> ANALYTICS
    
    AGENTS --> CHROMA
    AGENTS --> REDIS
    ANALYTICS --> FILE
    
    AGENTS --> OLLAMA
    AGENTS --> OPENAI
    AGENTS --> YOUTUBE
    
    PROM --> API
    PROM --> MCP
    PROM --> UI1
    PROM --> UI2
    GRAFANA --> PROM
    LOGS --> PROM
    
    K8S --> API
    K8S --> MCP
    K8S --> UI1
    K8S --> UI2
    DOCKER --> API
    DOCKER --> MCP
    
    VOLUMES --> CHROMA
    VOLUMES --> REDIS
    VOLUMES --> FILE
    
    SECRETS --> API
    SECRETS --> MCP
    RBAC --> K8S
    AUDIT --> LOGS
    
    %% Styling
    classDef service fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef storage fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef monitoring fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px
    classDef security fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef infrastructure fill:#fce4ec,stroke:#880e4f,stroke-width:2px
    
    class MCP,API,UI1,UI2,ORCH,AGENTS,ANALYTICS,OLLAMA,OPENAI,YOUTUBE service
    class CHROMA,REDIS,FILE storage
    class PROM,GRAFANA,LOGS monitoring
    class SECRETS,RBAC,AUDIT security
    class K8S,DOCKER,VOLUMES,LB,SSL infrastructure
```

## Deployment Models

### 1. Kubernetes Production Deployment

**Key Components:**
- **Deployment**: 3 replicas with rolling updates
- **Horizontal Pod Autoscaler**: CPU/Memory-based scaling
- **Resource Limits**: 2Gi memory, 1 CPU per pod
- **Health Checks**: Liveness and readiness probes
- **Security**: Non-root containers, RBAC, network policies

**Services:**
- MCP Server (Port 8000)
- FastAPI Gateway (Port 8003)
- Streamlit UIs (Ports 8501-8502)
- Monitoring (Ports 9090, 3000)

### 2. Docker Compose Development/Staging

**Key Components:**
- **Services**: 5 core services with resource limits
- **Networking**: Isolated network with service discovery
- **Volumes**: Persistent data and cache storage
- **Environment**: Production-like configuration

**Services:**
- Sentiment Analysis (Main Application)
- Ollama (Local LLM)
- Redis (Caching)
- Prometheus (Metrics)
- Grafana (Visualization)

## Infrastructure Requirements

### Compute Resources
- **Minimum**: 4 CPU cores, 8GB RAM
- **Recommended**: 8 CPU cores, 16GB RAM
- **Production**: 16+ CPU cores, 32GB+ RAM

### Storage Requirements
- **Data Storage**: 100GB+ SSD storage
- **Cache Storage**: 50GB+ fast storage
- **Log Storage**: 50GB+ with rotation

### Network Requirements
- **Bandwidth**: 100Mbps minimum, 1Gbps recommended
- **Latency**: <50ms for external API calls
- **Security**: HTTPS/TLS 1.3, VPN access

## Security Architecture

### Authentication & Authorization
- **API Keys**: Secure storage in Kubernetes secrets
- **RBAC**: Role-based access control
- **Network Policies**: Pod-to-pod communication control
- **Audit Logging**: Comprehensive access tracking

### Data Protection
- **Encryption**: Data at rest and in transit
- **Backup**: Automated backup strategies
- **Compliance**: GDPR, SOC2, HIPAA ready
- **Monitoring**: Security event detection

## Monitoring & Observability

### Metrics Collection
- **Prometheus**: Custom metrics and health checks
- **Grafana**: Real-time dashboards and alerts
- **Log Aggregation**: Structured logging with correlation IDs
- **Performance**: Response time and throughput monitoring

### Alerting
- **Health Checks**: Service availability monitoring
- **Resource Usage**: CPU, memory, disk space alerts
- **Error Rates**: API error rate monitoring
- **Business Metrics**: Custom KPI tracking

## Scaling Strategy

### Horizontal Scaling
- **Kubernetes HPA**: Automatic pod scaling based on metrics
- **Load Balancing**: Nginx reverse proxy with health checks
- **Database Scaling**: Read replicas and connection pooling
- **Cache Scaling**: Redis cluster for high availability

### Vertical Scaling
- **Resource Limits**: Configurable CPU and memory limits
- **Performance Tuning**: JVM and Python optimization
- **Database Optimization**: Query optimization and indexing
- **Caching Strategy**: Multi-level caching implementation

## Disaster Recovery

### Backup Strategy
- **Data Backup**: Daily automated backups
- **Configuration Backup**: Version-controlled configurations
- **Recovery Testing**: Regular disaster recovery drills
- **Multi-Region**: Cross-region deployment capability

### High Availability
- **Redundancy**: Multiple availability zones
- **Failover**: Automatic failover mechanisms
- **Monitoring**: Continuous health monitoring
- **Documentation**: Comprehensive runbooks and procedures
