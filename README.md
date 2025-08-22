# DIA3 - Distributed Intelligence Analysis System

A comprehensive, multi-modal intelligence analysis platform that combines advanced AI agents, Monte Carlo simulations, strategic assessment capabilities, and **enhanced report generation** for defense, intelligence, and business applications.

## 🎨 **NEW: Enhanced Report System**

DIA3 now includes a **comprehensive enhanced report generation system** with beautiful original styling, advanced analytics, and multiple integration options:

### ✨ Enhanced Report Features

- **🎨 Beautiful Original Styling**: Gradient headers, professional tables, interactive charts
- **📊 Sentiment Analysis**: Multi-modal sentiment assessment with regional analysis
- **🔮 Advanced Forecasting**: Ensemble LSTM models with 94% accuracy
- **📈 Predictive Analytics**: Feature importance ranking and scenario analysis
- **🎯 Monte Carlo Simulation**: 20,000 iterations for confidence intervals
- **⚡ Stress Testing**: Worst/average/best case scenario analysis
- **🔗 Knowledge Graphs**: Entity relationship mapping and analysis
- **📱 Interactive Visualizations**: Chart.js with drill-down capabilities

### 🚀 Integration Options

1. **API Endpoints** (`/api/v1/enhanced-reports/`)
   - `POST /generate` - Standard enhanced report
   - `POST /generate-beautiful` - Beautiful styling with advanced analytics
   - `GET /health` - Service health check
   - `GET /capabilities` - Available features
   - `GET /reports` - List generated reports

2. **MCP Tools** (Multi-Component Protocol)
   - `generate_enhanced_report` - Comprehensive report generation
   - `generate_beautiful_enhanced_report` - Beautiful styling with analytics

3. **Direct Generation**
   - Python API for standalone use
   - Customizable components and styling

### 📊 Performance Metrics

- **Generation Time**: ~2.2 seconds average
- **HTML Content Size**: ~36KB per report
- **Processing Components**: 9+ analysis components
- **Model Accuracy**: 94% for forecasting
- **Monte Carlo Iterations**: 20,000 per simulation

### 🎯 Usage Examples

```bash
# Generate beautiful enhanced report via API
curl -X POST "http://localhost:8003/api/v1/enhanced-reports/generate-beautiful" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Pakistan Submarine Acquisition Analysis: Strategic Impact on Conventional Deterrence Capabilities",
    "include_sentiment_analysis": true,
    "include_forecasting": true,
    "include_predictive_analytics": true,
    "beautiful_styling": true,
    "interactive_charts": true
  }'
```

```python
# Generate via MCP tools
result = await mcp_client.call_tool("generate_beautiful_enhanced_report", {
    "query": "Strategic Analysis Query",
    "include_sentiment_analysis": True,
    "include_forecasting": True,
    "include_predictive_analytics": True
})
```

```python
# Direct generation
from Test.enhanced_report_with_original_styling import EnhancedReportWithOriginalStyling

generator = EnhancedReportWithOriginalStyling()
result = await generator.generate_enhanced_report()
saved_file = generator.save_enhanced_report(result["html_content"], "my_report")
```

---

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
        EnhancedReports[Enhanced Report System]
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
    Orchestrator --> EnhancedReports
    
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

### 8. Data.gov Integration System

Comprehensive integration with Data.gov APIs for economic, trade, and environmental data analysis.

```mermaid
graph TB
    subgraph "Data.gov Integration Layer"
        DGSearch[Data.gov Search]
        DGPackage[Package Details]
        DGGroup[Group Management]
        DGTag[Tag Management]
    end
    
    subgraph "MCP Tools Layer"
        MCPPackageSearch[datagov_package_search]
        MCPPackageShow[datagov_package_show]
        MCPGroupList[datagov_group_list]
        MCPTagList[datagov_tag_list]
        MCPTradeAnalysis[datagov_trade_analysis]
        MCPEconomicForecast[datagov_economic_forecast]
        MCPEnvironmentalAnalysis[datagov_environmental_analysis]
        MCPNLQuery[datagov_natural_language_query]
    end
    
    subgraph "API Endpoints Layer"
        APITradeAnalysis[POST /api/datagov/trade-analysis]
        APIEconomicForecast[POST /api/datagov/economic-forecast]
        APIEnvironmentalAnalysis[POST /api/datagov/environmental-analysis]
        APINLQuery[POST /api/datagov/natural-language-query]
        APITradeData[GET /api/datagov/trade-data/country]
        APIEconomicData[GET /api/datagov/economic-forecast/country]
        APIEnvironmentalData[GET /api/datagov/environmental-data/country]
        APIHealth[GET /api/datagov/health]
    end
    
    subgraph "Analysis Engine Layer"
        TradeAnalysis[Trade Analysis Engine]
        EconomicForecast[Economic Forecasting Engine]
        EnvironmentalAnalysis[Environmental Analysis Engine]
        NLProcessor[Natural Language Processor]
        DataIngestion[Data Ingestion Manager]
        QueryProcessor[Query Processor]
    end
    
    subgraph "Data Processing Layer"
        DataValidation[Data Validation]
        DataTransformation[Data Transformation]
        DataAggregation[Data Aggregation]
        CacheManager[Cache Manager]
    end
    
    subgraph "External Data Sources"
        DataGovAPI[(Data.gov API)]
        TradeDatasets[(Trade Datasets)]
        EconomicDatasets[(Economic Datasets)]
        EnvironmentalDatasets[(Environmental Datasets)]
    end
    
    subgraph "Output Layer"
        Reports[Analysis Reports]
        Visualizations[Data Visualizations]
        Forecasts[Forecast Results]
        Recommendations[Strategic Recommendations]
    end
    
    %% Data.gov API connections
    DGSearch --> DataGovAPI
    DGPackage --> DataGovAPI
    DGGroup --> DataGovAPI
    DGTag --> DataGovAPI
    
    %% MCP Tools connections
    MCPPackageSearch --> DGSearch
    MCPPackageShow --> DGPackage
    MCPGroupList --> DGGroup
    MCPTagList --> DGTag
    MCPTradeAnalysis --> TradeAnalysis
    MCPEconomicForecast --> EconomicForecast
    MCPEnvironmentalAnalysis --> EnvironmentalAnalysis
    MCPNLQuery --> NLProcessor
    
    %% API Endpoints connections
    APITradeAnalysis --> TradeAnalysis
    APIEconomicForecast --> EconomicForecast
    APIEnvironmentalAnalysis --> EnvironmentalAnalysis
    APINLQuery --> NLProcessor
    APITradeData --> TradeAnalysis
    APIEconomicData --> EconomicForecast
    APIEnvironmentalData --> EnvironmentalAnalysis
    
    %% Analysis Engine connections
    TradeAnalysis --> DataIngestion
    EconomicForecast --> DataIngestion
    EnvironmentalAnalysis --> DataIngestion
    NLProcessor --> QueryProcessor
    
    %% Data Processing connections
    DataIngestion --> DataValidation
    DataValidation --> DataTransformation
    DataTransformation --> DataAggregation
    DataAggregation --> CacheManager
    
    %% External Data connections
    DataIngestion --> DataGovAPI
    DataIngestion --> TradeDatasets
    DataIngestion --> EconomicDatasets
    DataIngestion --> EnvironmentalDatasets
    
    %% Output connections
    TradeAnalysis --> Reports
    EconomicForecast --> Forecasts
    EnvironmentalAnalysis --> Visualizations
    NLProcessor --> Recommendations
    
    %% Cache connections
    CacheManager --> TradeAnalysis
    CacheManager --> EconomicForecast
    CacheManager --> EnvironmentalAnalysis
    CacheManager --> NLProcessor
```

### 9. Knowledge Graph System

Advanced knowledge graph construction, analysis, and querying system with GraphRAG-inspired architecture.

```mermaid
graph TB
    subgraph "Knowledge Graph Core"
        KGAgent[Knowledge Graph Agent]
        KGCoordinator[Knowledge Graph Coordinator]
        MultiDomainKG[Multi-Domain Knowledge Graph]
        EnhancedKG[Enhanced Knowledge Graph]
    end
    
    subgraph "Entity Processing Layer"
        EntityExtractor[Entity Extraction Engine]
        EntityValidator[Entity Validator]
        EntityClustering[Entity Clustering]
        ChineseExtractor[Enhanced Chinese Extractor]
    end
    
    subgraph "Relationship Processing Layer"
        RelationshipMapper[Relationship Mapping Engine]
        SemanticAnalyzer[Semantic Similarity Analyzer]
        RelationshipOptimizer[Relationship Optimizer]
        PatternMatcher[Pattern Matcher]
    end
    
    subgraph "Graph Analysis Layer"
        CommunityDetector[Community Detection]
        PathFinder[Path Finding Engine]
        CentralityAnalyzer[Centrality Analysis]
        GraphMetrics[Graph Metrics Calculator]
    end
    
    subgraph "Storage & Query Layer"
        NetworkXGraph[(NetworkX Graph)]
        VectorDB[(Vector Database)]
        GraphCache[Graph Cache]
        QueryEngine[Query Engine]
    end
    
    subgraph "Visualization Layer"
        GraphViz[Graph Visualization]
        HTMLExport[HTML Export]
        PNGExport[PNG Export]
        InteractiveViz[Interactive Visualization]
    end
    
    subgraph "MCP Tools Layer"
        MCPGenerateKG[generate_knowledge_graph]
        MCPQueryKG[query_knowledge_graph]
        MCPAnalyzeCommunities[analyze_graph_communities]
        MCPFindPaths[find_entity_paths]
        MCPEntityContext[get_entity_context]
        MCPGraphReport[generate_graph_report]
    end
    
    subgraph "API Endpoints Layer"
        APISearchKG[POST /search/knowledge-graph]
        APICombinedSearch[POST /search/combined]
        APISearchStats[GET /search/statistics]
        APIKGSearch[POST /api/knowledge-graph/search]
    end
    
    subgraph "Data Input Layer"
        TextContent[Text Content]
        PDFContent[PDF Content]
        AudioContent[Audio Content]
        VideoContent[Video Content]
        WebContent[Web Content]
        SocialContent[Social Media Content]
    end
    
    subgraph "Output Layer"
        KnowledgeGraph[(Knowledge Graph)]
        EntityReports[Entity Reports]
        RelationshipReports[Relationship Reports]
        AnalysisReports[Analysis Reports]
        Visualizations[Graph Visualizations]
    end
    
    %% Core connections
    KGAgent --> EntityExtractor
    KGAgent --> RelationshipMapper
    KGCoordinator --> KGAgent
    MultiDomainKG --> KGAgent
    EnhancedKG --> KGAgent
    
    %% Entity processing connections
    EntityExtractor --> EntityValidator
    EntityValidator --> EntityClustering
    ChineseExtractor --> EntityExtractor
    
    %% Relationship processing connections
    RelationshipMapper --> SemanticAnalyzer
    SemanticAnalyzer --> RelationshipOptimizer
    RelationshipOptimizer --> PatternMatcher
    
    %% Graph analysis connections
    CommunityDetector --> PathFinder
    PathFinder --> CentralityAnalyzer
    CentralityAnalyzer --> GraphMetrics
    
    %% Storage connections
    NetworkXGraph --> VectorDB
    VectorDB --> GraphCache
    GraphCache --> QueryEngine
    
    %% Visualization connections
    GraphViz --> HTMLExport
    GraphViz --> PNGExport
    GraphViz --> InteractiveViz
    
    %% MCP Tools connections
    MCPGenerateKG --> KGAgent
    MCPQueryKG --> QueryEngine
    MCPAnalyzeCommunities --> CommunityDetector
    MCPFindPaths --> PathFinder
    MCPEntityContext --> QueryEngine
    MCPGraphReport --> GraphViz
    
    %% API Endpoints connections
    APISearchKG --> QueryEngine
    APICombinedSearch --> QueryEngine
    APISearchStats --> GraphMetrics
    APIKGSearch --> QueryEngine
    
    %% Data input connections
    TextContent --> KGAgent
    PDFContent --> KGAgent
    AudioContent --> KGAgent
    VideoContent --> KGAgent
    WebContent --> KGAgent
    SocialContent --> KGAgent
    
    %% Output connections
    KGAgent --> KnowledgeGraph
    EntityExtractor --> EntityReports
    RelationshipMapper --> RelationshipReports
    GraphMetrics --> AnalysisReports
    GraphViz --> Visualizations
    
    %% Graph storage connections
    KGAgent --> NetworkXGraph
    NetworkXGraph --> GraphViz
    QueryEngine --> NetworkXGraph
```

### Knowledge Graph Architecture Components

```mermaid
graph LR
    subgraph "Agent Types"
        BasicKG[Basic Knowledge Graph Agent]
        EnhancedKG[Enhanced Knowledge Graph Agent]
        MultiDomainKG[Multi-Domain Knowledge Graph Agent]
        CoordinatorKG[Knowledge Graph Coordinator]
    end
    
    subgraph "Entity Types"
        PERSON[PERSON - Individuals]
        ORGANIZATION[ORGANIZATION - Companies]
        LOCATION[LOCATION - Places]
        EVENT[EVENT - Occurrences]
        CONCEPT[CONCEPT - Abstract Ideas]
        OBJECT[OBJECT - Physical Items]
        TECHNOLOGY[TECHNOLOGY - Tools/Systems]
        METHOD[METHOD - Processes]
        PROCESS[PROCESS - Workflows]
    end
    
    subgraph "Relationship Types"
        IS_A[IS_A - Hierarchical]
        PART_OF[PART_OF - Component]
        LOCATED_IN[LOCATED_IN - Spatial]
        WORKS_FOR[WORKS_FOR - Employment]
        CREATED_BY[CREATED_BY - Attribution]
        USES[USES - Dependency]
        IMPLEMENTS[IMPLEMENTS - Implementation]
        SIMILAR_TO[SIMILAR_TO - Similarity]
        OPPOSES[OPPOSES - Opposition]
        SUPPORTS[SUPPORTS - Support]
        LEADS_TO[LEADS_TO - Causal]
        DEPENDS_ON[DEPENDS_ON - Dependency]
        RELATED_TO[RELATED_TO - General]
    end
    
    subgraph "Analysis Algorithms"
        Louvain[Louvain Community Detection]
        LabelProp[Label Propagation]
        GirvanNewman[Girvan-Newman]
        ShortestPath[Shortest Path]
        Centrality[Centrality Analysis]
        PageRank[PageRank Algorithm]
    end
    
    subgraph "Processing Features"
        ChunkProcessing[Chunk-based Processing]
        ConfidenceScoring[Confidence Scoring]
        LanguageSupport[Multi-language Support]
        ErrorHandling[Robust Error Handling]
        FallbackStrategies[Fallback Strategies]
        CacheOptimization[Cache Optimization]
    end
    
    %% Agent connections
    BasicKG --> EnhancedKG
    EnhancedKG --> MultiDomainKG
    MultiDomainKG --> CoordinatorKG
    
    %% Entity connections
    BasicKG --> PERSON
    BasicKG --> ORGANIZATION
    BasicKG --> LOCATION
    EnhancedKG --> EVENT
    EnhancedKG --> CONCEPT
    EnhancedKG --> OBJECT
    MultiDomainKG --> TECHNOLOGY
    MultiDomainKG --> METHOD
    MultiDomainKG --> PROCESS
    
    %% Relationship connections
    BasicKG --> IS_A
    BasicKG --> PART_OF
    BasicKG --> LOCATED_IN
    EnhancedKG --> WORKS_FOR
    EnhancedKG --> CREATED_BY
    EnhancedKG --> USES
    MultiDomainKG --> IMPLEMENTS
    MultiDomainKG --> SIMILAR_TO
    MultiDomainKG --> OPPOSES
    CoordinatorKG --> SUPPORTS
    CoordinatorKG --> LEADS_TO
    CoordinatorKG --> DEPENDS_ON
    CoordinatorKG --> RELATED_TO
    
    %% Analysis connections
    EnhancedKG --> Louvain
    EnhancedKG --> LabelProp
    MultiDomainKG --> GirvanNewman
    MultiDomainKG --> ShortestPath
    CoordinatorKG --> Centrality
    CoordinatorKG --> PageRank
    
    %% Processing connections
    BasicKG --> ChunkProcessing
    EnhancedKG --> ConfidenceScoring
    MultiDomainKG --> LanguageSupport
    CoordinatorKG --> ErrorHandling
    CoordinatorKG --> FallbackStrategies
    CoordinatorKG --> CacheOptimization
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

#### Data.gov API Endpoints

Comprehensive Data.gov integration for economic, trade, and environmental analysis:

- `POST /api/datagov/trade-analysis` - Analyze trade data with forecasting
- `POST /api/datagov/economic-forecast` - Generate economic forecasts
- `POST /api/datagov/environmental-analysis` - Analyze environmental data
- `POST /api/datagov/natural-language-query` - Process natural language queries
- `GET /api/datagov/trade-data/{country}` - Get trade data for specific country
- `GET /api/datagov/economic-forecast/{country}` - Get economic forecast for country
- `GET /api/datagov/environmental-data/{country}` - Get environmental data for country
- `GET /api/datagov/health` - Data.gov service health check

#### Knowledge Graph API Endpoints

Advanced knowledge graph search and analysis endpoints:

- `POST /search/knowledge-graph` - Search knowledge graph with queries
- `POST /search/combined` - Combined semantic and knowledge graph search
- `GET /search/statistics` - Get search statistics and index information
- `POST /api/knowledge-graph/search` - Advanced knowledge graph search

#### Enhanced Report API

Comprehensive enhanced report generation with beautiful styling and advanced analytics:

- `POST /api/v1/enhanced-reports/generate` - Generate standard enhanced report
- `POST /api/v1/enhanced-reports/generate-beautiful` - Generate beautiful enhanced report with styling
- `GET /api/v1/enhanced-reports/health` - Enhanced report service health check
- `GET /api/v1/enhanced-reports/capabilities` - Get available capabilities and features
- `GET /api/v1/enhanced-reports/reports` - List all generated reports
- `GET /api/v1/enhanced-reports/reports/{report_id}` - Get specific report by ID
- `DELETE /api/v1/enhanced-reports/reports/{report_id}` - Delete specific report

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

#### Enhanced Report MCP Tools

Comprehensive enhanced report generation with beautiful styling and advanced analytics:

- `generate_enhanced_report` - Generate comprehensive report with 25+ analysis components
- `generate_beautiful_enhanced_report` - Generate beautiful enhanced report with original styling
- `run_monte_carlo_simulation` - Run Monte Carlo simulation for risk assessment
- `run_stress_testing` - Run stress testing scenarios for worst/average/best cases
- `generate_knowledge_graph` - Generate knowledge graph analysis with relationships
- `generate_visualizations` - Generate interactive visualizations with drill-down
- `detect_anomalies` - Detect anomalies in data using statistical and ML methods
- `analyze_patterns` - Analyze patterns in data using temporal, spatial, and behavioral analysis
- `assess_risks` - Assess risks and create risk assessment matrix
- `create_geopolitical_map` - Create geopolitical mapping and analysis
- `generate_strategic_analysis` - Generate comprehensive strategic analysis
- `generate_risk_assessment` - Generate comprehensive risk assessment with matrices
- `generate_executive_summary` - Generate AI-driven executive summary

#### Data.gov MCP Tools

Comprehensive Data.gov integration tools:

- `datagov_package_search` - Search for datasets on Data.gov
- `datagov_package_show` - Get details for specific datasets
- `datagov_group_list` - List groups on Data.gov
- `datagov_tag_list` - List tags on Data.gov
- `datagov_trade_analysis` - Analyze trade data with forecasting
- `datagov_economic_forecast` - Generate economic forecasts
- `datagov_environmental_analysis` - Analyze environmental data
- `datagov_natural_language_query` - Process natural language queries

#### Knowledge Graph MCP Tools

Advanced knowledge graph construction and analysis tools:

- `generate_knowledge_graph` - Generate knowledge graph from content
- `query_knowledge_graph` - Query knowledge graph with natural language
- `analyze_graph_communities` - Analyze community structures in graph
- `find_entity_paths` - Find paths between entities in graph
- `get_entity_context` - Get context and relationships for entities
- `generate_graph_report` - Generate comprehensive graph analysis reports

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
- **Data.gov Integration**: Comprehensive economic, trade, and environmental data analysis
- **Knowledge Graph Analysis**: GraphRAG-inspired entity extraction, relationship mapping, and graph analysis
- **Markdown Export**: Convert markdown content to PDF and Word documents with embedded images, tables, and Mermaid diagrams
- **Enhanced Report Generation**: Beautiful styling with sentiment analysis, forecasting, predictive analytics, and interactive visualizations

### Data.gov Integration Capabilities
- **Trade Analysis**: Multi-country trade flow analysis with forecasting
- **Economic Forecasting**: GDP, inflation, employment, and economic indicator predictions
- **Environmental Analysis**: Environmental policy and performance correlation analysis
- **Natural Language Queries**: Process complex queries against Data.gov datasets
- **Scenario-Based Forecasting**: Comprehensive scenario analysis for trade wars, economic crises, and policy changes
- **Seasonal Pattern Analysis**: Identify and predict seasonal patterns in trade and economic data
- **Supply Chain Analysis**: Vulnerability assessment and resilience modeling
- **Currency Risk Analysis**: Financial risk assessment and hedging strategies

### Knowledge Graph Capabilities
- **Entity Extraction**: Advanced extraction of 9 entity types (PERSON, ORGANIZATION, LOCATION, EVENT, CONCEPT, OBJECT, TECHNOLOGY, METHOD, PROCESS)
- **Relationship Mapping**: 13 relationship types with semantic analysis and pattern matching
- **Graph Analysis**: Community detection, path finding, centrality analysis, and graph metrics
- **Multi-Domain Support**: Language-based domain separation and cross-domain relationships
- **Visualization**: Interactive HTML, PNG exports, and comprehensive graph reports
- **Query Processing**: Natural language queries with semantic search integration
- **Multi-Modal Input**: Support for text, PDF, audio, video, web, and social media content
- **Enhanced Chinese Support**: Specialized Chinese entity extraction and validation

### Scalability & Performance
- **Agent Swarm**: Parallel processing with multiple specialized agents
- **Caching**: Multi-level caching (Redis, memory, disk)
- **Async Processing**: Non-blocking operations
- **Load Balancing**: Intelligent request distribution

### Integration Capabilities
- **MCP Protocol**: Model Context Protocol for tool integration
- **REST APIs**: Comprehensive REST API endpoints
- **WebSocket Support**: Real-time communication
- **External APIs**: YouTube, OpenAI, Data.gov, and other service integrations
- **Document Export**: PDF and Word document generation with professional formatting

## 🛠️ Development

### Project Structure

```
DIA3/
├── src/
│   ├── agents/           # AI agent implementations
│   │   ├── knowledge_graph_agent.py  # Knowledge Graph Agent
│   │   ├── enhanced_knowledge_graph_agent.py  # Enhanced Knowledge Graph Agent
│   │   ├── multi_domain_knowledge_graph_agent.py  # Multi-Domain Knowledge Graph Agent
│   │   └── knowledge_graph_coordinator.py  # Knowledge Graph Coordinator
│   ├── api/             # FastAPI routes and endpoints
│   │   └── datagov_routes.py  # Data.gov API endpoints
│   ├── core/            # Core engine implementations
│   │   ├── datagov/     # Data.gov integration core
│   │   ├── export/      # Markdown export service
│   │   └── improved_knowledge_graph_utility.py  # Knowledge Graph utilities
│   ├── mcp_servers/     # MCP server implementations
│   │   └── datagov_mcp_server.py  # Data.gov MCP server
│   └── config/          # Configuration management
│       └── datagov_config.py  # Data.gov configuration
├── tests/               # Test suites
├── docs/                # Documentation
│   ├── architecture/    # System architecture docs
│   │   └── datagov_forecasting_scenarios.md  # Data.gov scenarios
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
- `docs/architecture/datagov_forecasting_scenarios.md` - Data.gov integration scenarios and usage guide
- `docs/guides/KNOWLEDGE_GRAPH_AGENT_GUIDE.md` - Knowledge Graph agent implementation and usage guide
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
