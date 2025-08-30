# Network Analysis Tool

## Overview
The Network Analysis tool provides comprehensive capabilities for analyzing network structures, graph theory applications, social network analysis, and complex network modeling to support network intelligence and relationship analysis across various domains.

## Purpose
To analyze network structures, relationships, and connectivity patterns in complex systems, enabling social network analysis, graph theory applications, network optimization, and relationship intelligence for business, research, and operational decision-making.

## Required Libraries

### Core Libraries
- **pandas** (>=2.0.0) - Data manipulation and analysis
- **numpy** (>=1.24.0) - Numerical computing and statistical analysis
- **matplotlib** (>=3.7.0) - Data visualization and charting
- **seaborn** (>=0.12.0) - Statistical data visualization

### Optional Libraries
- **networkx** (>=3.1.0) - Network analysis and graph theory
- **igraph** (>=0.10.0) - Network analysis and visualization
- **plotly** (>=5.15.0) - Interactive visualizations
- **scipy** (>=1.11.0) - Scientific computing and sparse matrices
- **scikit-learn** (>=1.3.0) - Machine learning for network analysis
- **community** (>=0.15.0) - Community detection algorithms
- **pyvis** (>=0.3.0) - Interactive network visualizations
- **bokeh** (>=3.0.0) - Interactive plotting for networks
- **dash** (>=2.14.0) - Interactive dashboards
- **streamlit** (>=1.28.0) - Web application framework
- **graphviz** (>=0.20.0) - Graph visualization
- **pydot** (>=1.4.0) - Graph layout algorithms

## Input Schema
```json
{
  "type": "object",
  "properties": {
    "network_data": {
      "type": "object",
      "properties": {
        "nodes": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "id": {"type": "string"},
              "label": {"type": "string"},
              "attributes": {
                "type": "object",
                "additionalProperties": true
              }
            }
          }
        },
        "edges": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "source": {"type": "string"},
              "target": {"type": "string"},
              "weight": {"type": "number"},
              "attributes": {
                "type": "object",
                "additionalProperties": true
              }
            }
          }
        },
        "directed": {"type": "boolean"},
        "weighted": {"type": "boolean"}
      }
    },
    "analysis_config": {
      "type": "object",
      "properties": {
        "analysis_type": {
          "type": "string",
          "enum": ["centrality_analysis", "community_detection", "path_analysis", "network_metrics", "influence_analysis", "network_evolution", "link_prediction", "network_visualization"]
        },
        "network_parameters": {
          "type": "object",
          "properties": {
            "centrality_measures": {
              "type": "array",
              "items": {
                "type": "string",
                "enum": ["degree", "betweenness", "closeness", "eigenvector", "pagerank", "katz"]
              }
            },
            "community_algorithm": {
              "type": "string",
              "enum": ["louvain", "girvan_newman", "label_propagation", "spectral_clustering"]
            },
            "path_analysis_type": {
              "type": "string",
              "enum": ["shortest_path", "all_paths", "k_shortest_paths"]
            }
          }
        },
        "visualization_config": {
          "type": "object",
          "properties": {
            "layout_algorithm": {
              "type": "string",
              "enum": ["spring", "circular", "random", "kamada_kawai", "fruchterman_reingold"]
            },
            "node_size_attribute": {"type": "string"},
            "edge_weight_attribute": {"type": "string"},
            "color_scheme": {"type": "string"}
          }
        }
      }
    }
  },
  "required": ["network_data", "analysis_config"]
}
```

## Output Schema
```json
{
  "type": "object",
  "properties": {
    "network_analysis_results": {
      "type": "object",
      "properties": {
        "centrality_analysis": {
          "type": "object",
          "properties": {
            "degree_centrality": {
              "type": "object",
              "additionalProperties": {"type": "number"}
            },
            "betweenness_centrality": {
              "type": "object",
              "additionalProperties": {"type": "number"}
            },
            "closeness_centrality": {
              "type": "object",
              "additionalProperties": {"type": "number"}
            },
            "eigenvector_centrality": {
              "type": "object",
              "additionalProperties": {"type": "number"}
            },
            "pagerank": {
              "type": "object",
              "additionalProperties": {"type": "number"}
            }
          }
        },
        "community_detection": {
          "type": "object",
          "properties": {
            "communities": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "community_id": {"type": "integer"},
                  "nodes": {
                    "type": "array",
                    "items": {"type": "string"}
                  },
                  "size": {"type": "integer"},
                  "modularity": {"type": "number"}
                }
              }
            },
            "modularity_score": {"type": "number"},
            "number_of_communities": {"type": "integer"}
          }
        },
        "path_analysis": {
          "type": "object",
          "properties": {
            "shortest_paths": {
              "type": "object",
              "additionalProperties": {
                "type": "object",
                "additionalProperties": {
                  "type": "array",
                  "items": {"type": "string"}
                }
              }
            },
            "average_path_length": {"type": "number"},
            "diameter": {"type": "number"},
            "connectivity": {"type": "number"}
          }
        },
        "network_metrics": {
          "type": "object",
          "properties": {
            "density": {"type": "number"},
            "clustering_coefficient": {"type": "number"},
            "average_degree": {"type": "number"},
            "degree_distribution": {
              "type": "object",
              "additionalProperties": {"type": "integer"}
            },
            "assortativity": {"type": "number"}
          }
        }
      }
    },
    "influence_analysis": {
      "type": "object",
      "properties": {
        "influential_nodes": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "node_id": {"type": "string"},
              "influence_score": {"type": "number"},
              "influence_type": {"type": "string"}
            }
          }
        },
        "influence_spread": {
          "type": "object",
          "properties": {
            "spread_simulation": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "iteration": {"type": "integer"},
                  "infected_nodes": {
                    "type": "array",
                    "items": {"type": "string"}
                  },
                  "spread_rate": {"type": "number"}
                }
              }
            }
          }
        }
      }
    },
    "network_evolution": {
      "type": "object",
      "properties": {
        "temporal_metrics": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "timestamp": {"type": "string"},
              "metrics": {
                "type": "object",
                "properties": {
                  "density": {"type": "number"},
                  "clustering_coefficient": {"type": "number"},
                  "average_degree": {"type": "number"}
                }
              }
            }
          }
        }
      }
    },
    "link_prediction": {
      "type": "object",
      "properties": {
        "predicted_links": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "source": {"type": "string"},
              "target": {"type": "string"},
              "probability": {"type": "number"},
              "confidence": {"type": "number"}
            }
          }
        },
        "prediction_metrics": {
          "type": "object",
          "properties": {
            "precision": {"type": "number"},
            "recall": {"type": "number"},
            "f1_score": {"type": "number"},
            "auc": {"type": "number"}
          }
        }
      }
    },
    "visualizations": {
      "type": "object",
      "properties": {
        "network_graph": {"type": "string"},
        "centrality_heatmap": {"type": "string"},
        "community_visualization": {"type": "string"},
        "path_analysis_chart": {"type": "string"},
        "interactive_network": {"type": "string"}
      }
    },
    "network_insights": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "insight": {"type": "string"},
          "node_id": {"type": "string"},
          "metric": {"type": "string"},
          "value": {"type": "number"},
          "significance": {"type": "string"}
        }
      }
    },
    "processing_time": {
      "type": "number",
      "description": "Time taken for network analysis in seconds"
    }
  }
}
```

## Intended Use
- **Centrality Analysis**: Identify key nodes and influencers in networks
- **Community Detection**: Discover clusters and communities within networks
- **Path Analysis**: Analyze connectivity and routing in networks
- **Network Metrics**: Calculate fundamental network properties
- **Influence Analysis**: Model information spread and influence propagation
- **Network Evolution**: Track changes in network structure over time
- **Link Prediction**: Predict missing or future connections
- **Network Visualization**: Create interactive network visualizations

## Limitations
- Analysis complexity increases with network size
- Some algorithms may not scale to very large networks
- Network analysis results may be sensitive to data quality
- Dynamic network analysis requires temporal data

## Safety
- Validate network data quality and completeness
- Consider privacy implications of network analysis
- Handle sensitive relationship data appropriately
- Ensure network analysis methods are appropriate for the data

## Runbook

### Setup
1. **Install Dependencies**:
   ```bash
   pip install pandas numpy matplotlib seaborn networkx plotly scipy scikit-learn
   ```

2. **Verify Installation**:
   ```python
   import pandas as pd
   import numpy as np
   import matplotlib.pyplot as plt
   import networkx as nx
   import plotly.graph_objects as go
   from scipy import sparse
   ```

### Usage

#### Network Creation and Basic Analysis
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import seaborn as sns

def create_network_from_data(nodes_data, edges_data):
    """Create network from nodes and edges data"""
    
    # Create graph
    if edges_data[0].get('weight'):
        G = nx.Graph()
        for edge in edges_data:
            G.add_edge(edge['source'], edge['target'], weight=edge['weight'])
    else:
        G = nx.Graph()
        for edge in edges_data:
            G.add_edge(edge['source'], edge['target'])
    
    # Add node attributes
    for node in nodes_data:
        if 'id' in node:
            G.nodes[node['id']].update(node.get('attributes', {}))
    
    return G

def analyze_network_metrics(G):
    """Analyze basic network metrics"""
    
    metrics = {
        'number_of_nodes': G.number_of_nodes(),
        'number_of_edges': G.number_of_edges(),
        'density': nx.density(G),
        'average_degree': sum(dict(G.degree()).values()) / G.number_of_nodes(),
        'clustering_coefficient': nx.average_clustering(G),
        'average_shortest_path_length': nx.average_shortest_path_length(G) if nx.is_connected(G) else None,
        'diameter': nx.diameter(G) if nx.is_connected(G) else None,
        'is_connected': nx.is_connected(G),
        'number_of_connected_components': nx.number_connected_components(G)
    }
    
    return metrics

def calculate_centrality_measures(G):
    """Calculate various centrality measures"""
    
    centrality_measures = {
        'degree_centrality': nx.degree_centrality(G),
        'betweenness_centrality': nx.betweenness_centrality(G),
        'closeness_centrality': nx.closeness_centrality(G),
        'eigenvector_centrality': nx.eigenvector_centrality(G, max_iter=1000),
        'pagerank': nx.pagerank(G)
    }
    
    return centrality_measures

def visualize_network(G, centrality_measures=None, layout='spring'):
    """Visualize network with centrality measures"""
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Network Analysis', fontsize=16)
    
    # Choose layout
    if layout == 'spring':
        pos = nx.spring_layout(G, k=1, iterations=50)
    elif layout == 'circular':
        pos = nx.circular_layout(G)
    elif layout == 'random':
        pos = nx.random_layout(G)
    else:
        pos = nx.spring_layout(G)
    
    # Network visualization
    nx.draw(G, pos, ax=axes[0, 0], with_labels=True, node_color='lightblue', 
            node_size=500, font_size=8, font_weight='bold')
    axes[0, 0].set_title('Network Structure')
    
    # Degree centrality
    if centrality_measures:
        degree_cent = centrality_measures['degree_centrality']
        node_colors = [degree_cent[node] for node in G.nodes()]
        nx.draw(G, pos, ax=axes[0, 1], with_labels=True, node_color=node_colors, 
                cmap=plt.cm.Reds, node_size=500, font_size=8, font_weight='bold')
        axes[0, 1].set_title('Degree Centrality')
    
    # Betweenness centrality
    if centrality_measures:
        between_cent = centrality_measures['betweenness_centrality']
        node_colors = [between_cent[node] for node in G.nodes()]
        nx.draw(G, pos, ax=axes[1, 0], with_labels=True, node_color=node_colors, 
                cmap=plt.cm.Blues, node_size=500, font_size=8, font_weight='bold')
        axes[1, 0].set_title('Betweenness Centrality')
    
    # Closeness centrality
    if centrality_measures:
        close_cent = centrality_measures['closeness_centrality']
        node_colors = [close_cent[node] for node in G.nodes()]
        nx.draw(G, pos, ax=axes[1, 1], with_labels=True, node_color=node_colors, 
                cmap=plt.cm.Greens, node_size=500, font_size=8, font_weight='bold')
        axes[1, 1].set_title('Closeness Centrality')
    
    plt.tight_layout()
    plt.savefig('network_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

# Usage example
nodes_data = [
    {'id': 'A', 'attributes': {'label': 'Alice', 'group': 1}},
    {'id': 'B', 'attributes': {'label': 'Bob', 'group': 1}},
    {'id': 'C', 'attributes': {'label': 'Charlie', 'group': 2}},
    {'id': 'D', 'attributes': {'label': 'David', 'group': 2}},
    {'id': 'E', 'attributes': {'label': 'Eve', 'group': 3}},
    {'id': 'F', 'attributes': {'label': 'Frank', 'group': 3}}
]

edges_data = [
    {'source': 'A', 'target': 'B', 'weight': 1.0},
    {'source': 'A', 'target': 'C', 'weight': 0.8},
    {'source': 'B', 'target': 'C', 'weight': 0.9},
    {'source': 'C', 'target': 'D', 'weight': 0.7},
    {'source': 'D', 'target': 'E', 'weight': 0.6},
    {'source': 'E', 'target': 'F', 'weight': 0.5},
    {'source': 'F', 'target': 'A', 'weight': 0.4}
]

G = create_network_from_data(nodes_data, edges_data)
metrics = analyze_network_metrics(G)
centrality_measures = calculate_centrality_measures(G)
visualize_network(G, centrality_measures)

print("Network Metrics:")
for key, value in metrics.items():
    print(f"{key}: {value}")
```

#### Community Detection
```python
import community
from sklearn.cluster import SpectralClustering
import numpy as np

def detect_communities(G, algorithm='louvain'):
    """Detect communities in the network"""
    
    if algorithm == 'louvain':
        # Louvain method
        partition = community.best_partition(G)
        communities = {}
        for node, community_id in partition.items():
            if community_id not in communities:
                communities[community_id] = []
            communities[community_id].append(node)
        
        return communities, partition
    
    elif algorithm == 'spectral':
        # Spectral clustering
        adjacency_matrix = nx.adjacency_matrix(G).toarray()
        n_clusters = min(3, len(G.nodes()) // 2)  # Determine number of clusters
        
        clustering = SpectralClustering(n_clusters=n_clusters, 
                                       affinity='precomputed', 
                                       random_state=42)
        labels = clustering.fit_predict(adjacency_matrix)
        
        communities = {}
        for i, label in enumerate(labels):
            if label not in communities:
                communities[label] = []
            communities[label].append(list(G.nodes())[i])
        
        return communities, dict(zip(G.nodes(), labels))
    
    elif algorithm == 'girvan_newman':
        # Girvan-Newman algorithm (simplified)
        components = list(nx.connected_components(G))
        communities = {i: list(comp) for i, comp in enumerate(components)}
        return communities, {node: i for i, comp in enumerate(components) for node in comp}

def analyze_communities(G, communities):
    """Analyze detected communities"""
    
    analysis = {
        'number_of_communities': len(communities),
        'community_sizes': [len(comm) for comm in communities.values()],
        'modularity': community.modularity(community.best_partition(G), G),
        'communities': {}
    }
    
    for comm_id, nodes in communities.items():
        subgraph = G.subgraph(nodes)
        analysis['communities'][comm_id] = {
            'nodes': nodes,
            'size': len(nodes),
            'density': nx.density(subgraph),
            'average_degree': sum(dict(subgraph.degree()).values()) / len(nodes) if nodes else 0
        }
    
    return analysis

def visualize_communities(G, communities):
    """Visualize network with community colors"""
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Network with community colors
    pos = nx.spring_layout(G, k=1, iterations=50)
    
    # Color nodes by community
    colors = plt.cm.Set3(np.linspace(0, 1, len(communities)))
    node_colors = []
    
    for node in G.nodes():
        for comm_id, comm_nodes in communities.items():
            if node in comm_nodes:
                node_colors.append(colors[comm_id])
                break
    
    nx.draw(G, pos, ax=ax1, with_labels=True, node_color=node_colors, 
            node_size=500, font_size=8, font_weight='bold')
    ax1.set_title('Network with Communities')
    
    # Community size distribution
    community_sizes = [len(comm) for comm in communities.values()]
    ax2.bar(range(len(community_sizes)), community_sizes, color=colors[:len(community_sizes)])
    ax2.set_title('Community Size Distribution')
    ax2.set_xlabel('Community ID')
    ax2.set_ylabel('Number of Nodes')
    
    plt.tight_layout()
    plt.savefig('community_detection.png', dpi=300, bbox_inches='tight')
    plt.close()

# Usage example
communities, partition = detect_communities(G, algorithm='louvain')
community_analysis = analyze_communities(G, communities)
visualize_communities(G, communities)

print("Community Analysis:")
print(f"Number of communities: {community_analysis['number_of_communities']}")
print(f"Modularity: {community_analysis['modularity']:.4f}")
print(f"Community sizes: {community_analysis['community_sizes']}")
```

#### Interactive Network Visualization
```python
import plotly.graph_objects as go
import plotly.express as px

def create_interactive_network(G, centrality_measures=None, communities=None):
    """Create interactive network visualization with Plotly"""
    
    # Get node positions
    pos = nx.spring_layout(G, k=1, iterations=50)
    
    # Prepare node data
    node_x = [pos[node][0] for node in G.nodes()]
    node_y = [pos[node][1] for node in G.nodes()]
    node_text = [f"Node: {node}<br>Degree: {G.degree(node)}" for node in G.nodes()]
    
    # Node colors based on centrality
    if centrality_measures:
        node_colors = [centrality_measures['degree_centrality'][node] for node in G.nodes()]
    else:
        node_colors = [1] * len(G.nodes())
    
    # Node sizes based on degree
    node_sizes = [G.degree(node) * 10 + 10 for node in G.nodes()]
    
    # Prepare edge data
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
    
    # Create edge trace
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')
    
    # Create node trace
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        text=node_text,
        textposition="top center",
        marker=dict(
            size=node_sizes,
            color=node_colors,
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Centrality"),
            line=dict(width=2, color='white')))
    
    # Create layout
    layout = go.Layout(
        title='Interactive Network Visualization',
        showlegend=False,
        hovermode='closest',
        margin=dict(b=20,l=5,r=5,t=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
    
    # Create figure
    fig = go.Figure(data=[edge_trace, node_trace], layout=layout)
    
    return fig

def create_centrality_comparison(centrality_measures):
    """Create comparison chart of centrality measures"""
    
    # Prepare data
    nodes = list(centrality_measures['degree_centrality'].keys())
    measures = ['degree_centrality', 'betweenness_centrality', 'closeness_centrality']
    
    data = []
    for node in nodes:
        for measure in measures:
            data.append({
                'Node': node,
                'Centrality Type': measure.replace('_', ' ').title(),
                'Value': centrality_measures[measure][node]
            })
    
    df = pd.DataFrame(data)
    
    # Create heatmap
    pivot_df = df.pivot(index='Node', columns='Centrality Type', values='Value')
    
    fig = px.imshow(pivot_df, 
                    title='Centrality Measures Comparison',
                    color_continuous_scale='Viridis',
                    aspect='auto')
    
    return fig

# Usage example
interactive_network = create_interactive_network(G, centrality_measures, communities)
interactive_network.write_html('interactive_network.html')

centrality_comparison = create_centrality_comparison(centrality_measures)
centrality_comparison.write_html('centrality_comparison.html')

print("Interactive visualizations saved as HTML files")
```

### Error Handling
- Validate network data structure and connectivity
- Handle disconnected networks and isolated nodes
- Manage computational complexity for large networks
- Ensure network analysis parameters are appropriate

### Monitoring
- Track network analysis performance and accuracy
- Monitor network evolution and changes over time
- Review community detection quality and stability
- Validate centrality measures and their interpretation

### Best Practices
1. **Data Quality**: Ensure high-quality network data and relationship accuracy
2. **Network Size**: Consider computational complexity for large networks
3. **Algorithm Selection**: Choose appropriate algorithms for the network type
4. **Interpretation**: Interpret network metrics in domain context
5. **Visualization**: Use appropriate visualizations for different analysis types
6. **Validation**: Validate network analysis results with domain knowledge
7. **Documentation**: Document network analysis methods and assumptions
8. **Privacy**: Consider privacy implications of network analysis
