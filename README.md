# DIA3 - Distributed Intelligence Analysis System

A comprehensive, multi-modal intelligence analysis platform that combines advanced AI agents, Monte Carlo simulations, and strategic assessment capabilities for defense, intelligence, and business applications.

## 🏗️ System Architecture

DIA3 is built on a modular, microservices-based architecture with the following core components:

### High-Level Architecture Overview

```mermaid
graph TB
    subgraph "Client Layer"
        UI[Web UI]
        API[API Clients]
        MCP[MCP Clients]
    end
    
    subgraph "API Gateway Layer"
        FastAPI[FastAPI Gateway]
        MCP_Server[MCP Server]
    end
    
    subgraph "Core Services Layer"
        Orchestrator[Orchestrator]
        MonteCarlo[Monte Carlo Engine]
        ForceProjection[Force Projection Engine]
        VectorDB[Vector Database]
    end
    
    subgraph "Agent Swarm Layer"
        TextAgent[Text Agent]
        VisionAgent[Vision Agent]
        AudioAgent[Audio Agent]
        WebAgent[Web Agent]
        KnowledgeGraph[Knowledge Graph Agent]
        StrategicAgent[Strategic Analysis Agent]
    end
    
    subgraph "Data Layer"
        ChromaDB[(ChromaDB)]
        Cache[(Redis Cache)]
        FileStorage[(File Storage)]
    end
    
    subgraph "External Integrations"
        Ollama[Ollama LLM]
        OpenAI[OpenAI API]
        YouTube[YouTube API]
        WebAPIs[Web APIs]
    end
    
    UI --> FastAPI
    API --> FastAPI
    MCP --> MCP_Server
    
    FastAPI --> Orchestrator
    MCP_Server --> Orchestrator
    
    Orchestrator --> TextAgent
    Orchestrator --> VisionAgent
    Orchestrator --> AudioAgent
    Orchestrator --> WebAgent
    Orchestrator --> KnowledgeGraph
    Orchestrator --> StrategicAgent
    
    Orchestrator --> MonteCarlo
    Orchestrator --> ForceProjection
    Orchestrator --> VectorDB
    
    MonteCarlo --> Cache
    ForceProjection --> Cache
    VectorDB --> ChromaDB
    
    TextAgent --> Ollama
    VisionAgent --> OpenAI
    AudioAgent --> WebAPIs
    WebAgent --> YouTube
    WebAgent --> WebAPIs
```

## 📋 Core Modules

### 1. Orchestrator Module

The central coordination hub that manages the agent swarm and routes requests.

```mermaid
graph TB
    subgraph "Orchestrator Core"
        MainOrch[Main Orchestrator]
        AgentRegistry[Agent Registry]
        RequestRouter[Request Router]
        CacheManager[Cache Manager]
    end
    
    subgraph "Agent Management"
        AgentLoader[Agent Loader]
        AgentMonitor[Agent Monitor]
        AgentHealth[Health Checker]
    end
    
    subgraph "Request Processing"
        RequestQueue[Request Queue]
        LoadBalancer[Load Balancer]
        ResultAggregator[Result Aggregator]
    end
    
    subgraph "Integration Layer"
        MCPClient[MCP Client]
        VectorDBClient[VectorDB Client]
        MonteCarloClient[Monte Carlo Client]
    end
    
    MainOrch --> AgentRegistry
    MainOrch --> RequestRouter
    MainOrch --> CacheManager
    
    RequestRouter --> RequestQueue
    RequestQueue --> LoadBalancer
    LoadBalancer --> AgentLoader
    AgentLoader --> AgentRegistry
    
    AgentMonitor --> AgentHealth
    AgentHealth --> AgentRegistry
    
    LoadBalancer --> ResultAggregator
    ResultAggregator --> CacheManager
    
    MainOrch --> MCPClient
    MainOrch --> VectorDBClient
    MainOrch --> MonteCarloClient
```

### 2. Monte Carlo Engine

Advanced simulation engine for probabilistic analysis and forecasting.

```mermaid
graph TB
    subgraph "Monte Carlo Core"
        MCEngine[Monte Carlo Engine]
        Config[Configuration]
        Cache[Result Cache]
    end
    
    subgraph "Simulation Components"
        Distributions[Distribution Library]
        Correlations[Correlation Engine]
        Scenarios[Scenario Generator]
        Analyzer[Result Analyzer]
    end
    
    subgraph "Performance Optimization"
        ProcessPool[Process Pool Executor]
        MemoryCache[Memory Cache]
        RedisCache[Redis Cache]
    end
    
    subgraph "Security & Compliance"
        AuditLog[Audit Logger]
        DataClassification[Data Classification]
        EventHandlers[Event Handlers]
    end
    
    MCEngine --> Config
    MCEngine --> Cache
    
    MCEngine --> Distributions
    MCEngine --> Correlations
    MCEngine --> Scenarios
    MCEngine --> Analyzer
    
    MCEngine --> ProcessPool
    ProcessPool --> MemoryCache
    MemoryCache --> RedisCache
    
    MCEngine --> AuditLog
    MCEngine --> DataClassification
    MCEngine --> EventHandlers
```

### 3. Force Projection Engine

Military capability assessment and strategic threat evaluation system.

```mermaid
graph TB
    subgraph "Force Projection Core"
        FPEngine[Force Projection Engine]
        CapabilityParams[Capability Parameters]
        ReadinessFactors[Readiness Factors]
        EnvironmentalFactors[Environmental Factors]
    end
    
    subgraph "Analysis Components"
        AdversaryTypes[Adversary Type Analysis]
        DomainAnalysis[Domain Analysis]
        CapabilityAssessment[Capability Assessment]
        ThreatEvaluation[Threat Evaluation]
    end
    
    subgraph "Simulation Engine"
        MonteCarlo[Monte Carlo Integration]
        LogNormalDist[Log-Normal Distributions]
        ConfidenceIntervals[Confidence Intervals]
    end
    
    subgraph "Output Generation"
        Reports[Report Generator]
        Visualizations[Visualization Engine]
        Recommendations[Recommendation Engine]
    end
    
    FPEngine --> CapabilityParams
    FPEngine --> ReadinessFactors
    FPEngine --> EnvironmentalFactors
    
    FPEngine --> AdversaryTypes
    FPEngine --> DomainAnalysis
    FPEngine --> CapabilityAssessment
    FPEngine --> ThreatEvaluation
    
    FPEngine --> MonteCarlo
    MonteCarlo --> LogNormalDist
    LogNormalDist --> ConfidenceIntervals
    
    FPEngine --> Reports
    FPEngine --> Visualizations
    FPEngine --> Recommendations
```

### 4. Agent Swarm System

Multi-modal AI agents for different types of content analysis.

```mermaid
graph TB
    subgraph "Agent Swarm Core"
        SwarmManager[Swarm Manager]
        AgentRegistry[Agent Registry]
        TaskDistributor[Task Distributor]
    end
    
    subgraph "Specialized Agents"
        TextAgent[Text Analysis Agent]
        VisionAgent[Vision Analysis Agent]
        AudioAgent[Audio Analysis Agent]
        WebAgent[Web Content Agent]
        KnowledgeGraph[Knowledge Graph Agent]
        StrategicAgent[Strategic Analysis Agent]
    end
    
    subgraph "Agent Capabilities"
        LLMIntegration[LLM Integration]
        ModelManagement[Model Management]
        CacheSystem[Cache System]
        ErrorHandling[Error Handling]
    end
    
    subgraph "Communication"
        MCPProtocol[MCP Protocol]
        AsyncProcessing[Async Processing]
        ResultAggregation[Result Aggregation]
    end
    
    SwarmManager --> AgentRegistry
    SwarmManager --> TaskDistributor
    
    TaskDistributor --> TextAgent
    TaskDistributor --> VisionAgent
    TaskDistributor --> AudioAgent
    TaskDistributor --> WebAgent
    TaskDistributor --> KnowledgeGraph
    TaskDistributor --> StrategicAgent
    
    TextAgent --> LLMIntegration
    VisionAgent --> LLMIntegration
    AudioAgent --> LLMIntegration
    WebAgent --> LLMIntegration
    KnowledgeGraph --> LLMIntegration
    StrategicAgent --> LLMIntegration
    
    LLMIntegration --> ModelManagement
    ModelManagement --> CacheSystem
    CacheSystem --> ErrorHandling
    
    SwarmManager --> MCPProtocol
    MCPProtocol --> AsyncProcessing
    AsyncProcessing --> ResultAggregation
```

### 5. MCP Server System

Model Context Protocol server for external tool integration.

```mermaid
graph TB
    subgraph "MCP Server Core"
        UnifiedServer[Unified MCP Server]
        ToolRegistry[Tool Registry]
        SessionManager[Session Manager]
    end
    
    subgraph "Tool Categories"
        MonteCarloTools[Monte Carlo Tools]
        ForceProjectionTools[Force Projection Tools]
        StrategicIntelligenceTools[Strategic Intelligence Tools]
        VisualizationTools[Visualization Tools]
        MultiDomainTools[Multi-Domain Tools]
        MarkdownExportTools[Markdown Export Tools]
    end
    
    subgraph "Dynamic Management"
        DynamicToolManager[Dynamic Tool Manager]
        ToolLoader[Tool Loader]
        ToolValidator[Tool Validator]
    end
    
    subgraph "Integration Layer"
        HTTPMCP[HTTP MCP Server]
        StreamableHTTP[Streamable HTTP]
        ClientWrapper[Client Wrapper]
    end
    
    UnifiedServer --> ToolRegistry
    UnifiedServer --> SessionManager
    
    ToolRegistry --> MonteCarloTools
    ToolRegistry --> ForceProjectionTools
    ToolRegistry --> StrategicIntelligenceTools
    ToolRegistry --> VisualizationTools
    ToolRegistry --> MultiDomainTools
    ToolRegistry --> MarkdownExportTools
    
    UnifiedServer --> DynamicToolManager
    DynamicToolManager --> ToolLoader
    ToolLoader --> ToolValidator
    
    UnifiedServer --> HTTPMCP
    HTTPMCP --> StreamableHTTP
    StreamableHTTP --> ClientWrapper
```

### 6. API Gateway System

FastAPI-based REST API for external integrations.

```mermaid
graph TB
    subgraph "API Gateway Core"
        FastAPIMain[FastAPI Main]
        RouteManager[Route Manager]
        Middleware[Middleware Stack]
    end
    
    subgraph "Route Categories"
        AnalyticsRoutes[Advanced Analytics Routes]
        StrategicRoutes[Strategic Analysis Routes]
        ForceProjectionRoutes[Force Projection Routes]
        MLForecastingRoutes[ML Forecasting Routes]
        MonitoringRoutes[Monitoring Routes]
        MarkdownExportRoutes[Markdown Export Routes]
    end
    
    subgraph "Request Processing"
        RequestValidator[Request Validator]
        RateLimiter[Rate Limiter]
        Authentication[Authentication]
        ResponseFormatter[Response Formatter]
    end
    
    subgraph "Integration Points"
        OrchestratorAPI[Orchestrator API]
        MCPIntegration[MCP Integration]
        DatabaseConnector[Database Connector]
        ExportService[Export Service]
    end
    
    FastAPIMain --> RouteManager
    FastAPIMain --> Middleware
    
    RouteManager --> AnalyticsRoutes
    RouteManager --> StrategicRoutes
    RouteManager --> ForceProjectionRoutes
    RouteManager --> MLForecastingRoutes
    RouteManager --> MonitoringRoutes
    RouteManager --> MarkdownExportRoutes
    
    Middleware --> RequestValidator
    RequestValidator --> RateLimiter
    RateLimiter --> Authentication
    Authentication --> ResponseFormatter
    
    FastAPIMain --> OrchestratorAPI
    FastAPIMain --> MCPIntegration
    FastAPIMain --> DatabaseConnector
    MarkdownExportRoutes --> ExportService
```

### 7. Vector Database System

ChromaDB-based vector storage and retrieval system.

```mermaid
graph TB
    subgraph "Vector DB Core"
        VectorDB[Vector Database]
        EmbeddingEngine[Embedding Engine]
        IndexManager[Index Manager]
    end
    
    subgraph "Storage Components"
        ChromaDB[(ChromaDB)]
        MetadataStore[Metadata Store]
        CacheLayer[Cache Layer]
    end
    
    subgraph "Query Processing"
        QueryParser[Query Parser]
        SimilaritySearch[Similarity Search]
        ResultRanker[Result Ranker]
    end
    
    subgraph "Integration"
        MCPClient[MCP Client]
        APIEndpoints[API Endpoints]
        Monitoring[Monitoring]
    end
    
    VectorDB --> EmbeddingEngine
    VectorDB --> IndexManager
    
    VectorDB --> ChromaDB
    ChromaDB --> MetadataStore
    MetadataStore --> CacheLayer
    
    VectorDB --> QueryParser
    QueryParser --> SimilaritySearch
    SimilaritySearch --> ResultRanker
    
    VectorDB --> MCPClient
    VectorDB --> APIEndpoints
    VectorDB --> Monitoring
```

## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- UV package manager
- Redis (optional, for caching)
- Ollama (for local LLM inference)
- Mermaid CLI (for diagram rendering in markdown export)

### Installation

```bash
# Clone the repository
git clone https://github.com/goagiq/DIA3.git
cd DIA3

# Create virtual environment
uv venv --python 3.13

# Activate environment
source .venv/Scripts/activate  # Windows: .venv\Scripts\activate

# Install dependencies
uv sync

# Install Mermaid CLI for diagram rendering (optional)
npm install -g @mermaid-js/mermaid-cli

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration
```

### Running the System

**Quick Start:**
```bash
# Start the complete system
python main.py
```

**Individual Components:**
```bash
# Start API server only
python -m src.api.main

# Start MCP server only
python -m src.mcp_servers.unified_mcp_server

# Start strategic intelligence system
python start_strategic_intelligence_system.py
```

### API Endpoints

The system exposes REST APIs at `http://localhost:8000`:

- `POST /analyze` - Multi-modal content analysis
- `POST /strategic-analysis` - Strategic assessment
- `POST /force-projection` - Military capability analysis
- `POST /monte-carlo` - Monte Carlo simulations
- `GET /health` - System health check

#### Markdown Export API

Export markdown content to PDF and Word documents:

- `POST /api/v1/markdown-export/export` - Export markdown content to PDF/Word
- `POST /api/v1/markdown-export/export-file` - Export markdown file to PDF/Word
- `GET /api/v1/markdown-export/download/{filename}` - Download exported files
- `GET /api/v1/markdown-export/files` - List exported files
- `DELETE /api/v1/markdown-export/files/{filename}` - Delete exported files
- `GET /api/v1/markdown-export/health` - Export service health check

### MCP Tools

Available MCP tools for external integration:

- `monte_carlo_simulation` - Run Monte Carlo simulations
- `force_projection_analysis` - Analyze military capabilities
- `strategic_intelligence_forecast` - Strategic forecasting
- `multi_domain_analysis` - Multi-domain Monte Carlo analysis
- `visualization_generator` - Generate analysis visualizations

#### Markdown Export MCP Tools

Export markdown content to various formats:

- `markdown_export_to_pdf` - Export markdown content to PDF
- `markdown_export_to_word` - Export markdown content to Word document
- `markdown_export_batch` - Batch export multiple markdown files
- `markdown_export_list_files` - List exported files
- `markdown_export_get_file_info` - Get file information
- `markdown_export_delete_file` - Delete exported files
- `markdown_export_cleanup` - Clean up exported files

## 📊 Key Features

### Multi-Modal Analysis
- **Text Analysis**: Document processing, sentiment analysis, entity extraction
- **Vision Analysis**: Image and video content analysis
- **Audio Analysis**: Speech recognition and audio content analysis
- **Web Content**: Web scraping and content extraction

### Advanced Analytics
- **Monte Carlo Simulations**: Probabilistic modeling and forecasting
- **Force Projection**: Military capability assessment
- **Strategic Intelligence**: Threat evaluation and forecasting
- **Multi-Domain Analysis**: Cross-domain correlation analysis
- **Markdown Export**: Convert markdown content to PDF and Word documents with embedded images, tables, and Mermaid diagrams

### Scalability & Performance
- **Agent Swarm**: Parallel processing with multiple specialized agents
- **Caching**: Multi-level caching (Redis, memory, disk)
- **Async Processing**: Non-blocking operations
- **Load Balancing**: Intelligent request distribution

### Integration Capabilities
- **MCP Protocol**: Model Context Protocol for tool integration
- **REST APIs**: Comprehensive REST API endpoints
- **WebSocket Support**: Real-time communication
- **External APIs**: YouTube, OpenAI, and other service integrations
- **Document Export**: PDF and Word document generation with professional formatting

## 🛠️ Development

### Project Structure

```
DIA3/
├── src/
│   ├── agents/           # AI agent implementations
│   ├── api/             # FastAPI routes and endpoints
│   ├── core/            # Core engine implementations
│   │   └── export/      # Markdown export service
│   ├── mcp_servers/     # MCP server implementations
│   └── config/          # Configuration management
├── tests/               # Test suites
├── docs/                # Documentation
│   └── white_papers/    # Whitepapers and exported documents
├── examples/            # Usage examples
├── scripts/             # Utility scripts
└── Results/             # Analysis results and reports
```

### Testing

```bash
# Run all tests
uv run pytest

# Run specific test categories
uv run pytest tests/performance/
uv run pytest tests/integration/
uv run pytest tests/mcp/
```

### Code Quality

```bash
# Format code
uv run black src/ tests/

# Type checking
uv run mypy src/

# Linting
uv run flake8 src/
```

## 📈 Performance Monitoring

The system includes comprehensive monitoring capabilities:

- **Health Checks**: System and component health monitoring
- **Performance Metrics**: Response times, throughput, resource usage
- **Error Tracking**: Comprehensive error logging and analysis
- **Audit Logging**: Security and compliance audit trails

## 🔒 Security & Compliance

- **Data Classification**: Support for classified data handling
- **Audit Logging**: Comprehensive audit trails
- **Access Control**: Role-based access control
- **Encryption**: Data encryption in transit and at rest

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📚 Documentation

Additional documentation is available in the `docs/` directory:

- `docs/MARKDOWN_EXPORT_GUIDE.md` - Comprehensive guide for markdown export functionality
- `docs/white_papers/` - Whitepapers and exported documents
- `docs/guides/` - Implementation and usage guides
- `docs/plans/` - Development and integration plans

## 🆘 Support

For support and questions:

- Create an issue on GitHub
- Check the documentation in the `docs/` directory
- Review the examples in the `examples/` directory

---

**DIA3** - Distributed Intelligence Analysis System  
*Advanced AI-powered intelligence analysis for defense, intelligence, and business applications*
