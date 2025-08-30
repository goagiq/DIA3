# Geospatial Analysis Tool

## Overview
The Geospatial Analysis tool provides comprehensive capabilities for analyzing spatial data, creating maps, performing location-based analysis, and supporting geographic information system (GIS) operations for spatial intelligence and location-based decision-making.

## Purpose
To analyze spatial relationships, patterns, and distributions in geographic data, enabling location-based insights, spatial modeling, and geographic intelligence for business, research, and operational decision-making.

## Required Libraries

### Core Libraries
- **pandas** (>=2.0.0) - Data manipulation and analysis
- **numpy** (>=1.24.0) - Numerical computing and statistical analysis
- **matplotlib** (>=3.7.0) - Data visualization and charting
- **seaborn** (>=0.12.0) - Statistical data visualization

### Optional Libraries
- **geopandas** (>=0.13.0) - Geospatial data manipulation
- **folium** (>=0.14.0) - Interactive mapping
- **plotly** (>=5.15.0) - Interactive visualizations
- **shapely** (>=2.0.0) - Geometric operations
- **pyproj** (>=3.5.0) - Coordinate system transformations
- **rasterio** (>=1.3.0) - Raster data processing
- **fiona** (>=1.9.0) - Vector data I/O
- **contextily** (>=1.3.0) - Web map tiles
- **geopy** (>=2.3.0) - Geocoding and distance calculations
- **scipy** (>=1.11.0) - Scientific computing and spatial statistics
- **scikit-learn** (>=1.3.0) - Machine learning for spatial analysis
- **networkx** (>=3.1.0) - Network analysis for spatial networks

## Input Schema
```json
{
  "type": "object",
  "properties": {
    "spatial_data": {
      "type": "object",
      "properties": {
        "vector_data": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "geometry": {
                "type": "object",
                "properties": {
                  "type": {"type": "string"},
                  "coordinates": {"type": "array"}
                }
              },
              "properties": {
                "type": "object",
                "additionalProperties": true
              }
            }
          }
        },
        "raster_data": {
          "type": "object",
          "properties": {
            "data": {"type": "array"},
            "transform": {"type": "array"},
            "crs": {"type": "string"}
          }
        },
        "point_data": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "latitude": {"type": "number"},
              "longitude": {"type": "number"},
              "attributes": {
                "type": "object",
                "additionalProperties": true
              }
            }
          }
        }
      }
    },
    "analysis_config": {
      "type": "object",
      "properties": {
        "analysis_type": {
          "type": "string",
          "enum": ["spatial_clustering", "hotspot_analysis", "spatial_interpolation", "buffer_analysis", "overlay_analysis", "network_analysis", "spatial_regression", "geostatistics"]
        },
        "coordinate_system": {
          "type": "object",
          "properties": {
            "input_crs": {"type": "string"},
            "output_crs": {"type": "string"}
          }
        },
        "spatial_parameters": {
          "type": "object",
          "properties": {
            "buffer_distance": {"type": "number"},
            "clustering_radius": {"type": "number"},
            "interpolation_method": {"type": "string"},
            "neighborhood_size": {"type": "integer"}
          }
        }
      }
    },
    "visualization_config": {
      "type": "object",
      "properties": {
        "map_type": {
          "type": "string",
          "enum": ["choropleth", "heatmap", "point_map", "flow_map", "3d_surface"]
        },
        "color_scheme": {"type": "string"},
        "basemap": {"type": "string"},
        "interactive": {"type": "boolean"}
      }
    }
  },
  "required": ["spatial_data", "analysis_config"]
}
```

## Output Schema
```json
{
  "type": "object",
  "properties": {
    "spatial_analysis_results": {
      "type": "object",
      "properties": {
        "clustering_results": {
          "type": "object",
          "properties": {
            "clusters": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "cluster_id": {"type": "integer"},
                  "centroid": {
                    "type": "object",
                    "properties": {
                      "latitude": {"type": "number"},
                      "longitude": {"type": "number"}
                    }
                  },
                  "points": {
                    "type": "array",
                    "items": {
                      "type": "object",
                      "properties": {
                        "latitude": {"type": "number"},
                        "longitude": {"type": "number"}
                      }
                    }
                  }
                }
              }
            }
          }
        },
        "hotspot_analysis": {
          "type": "object",
          "properties": {
            "hotspots": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "location": {
                    "type": "object",
                    "properties": {
                      "latitude": {"type": "number"},
                      "longitude": {"type": "number"}
                    }
                  },
                  "intensity": {"type": "number"},
                  "significance": {"type": "number"}
                }
              }
            }
          }
        },
        "spatial_statistics": {
          "type": "object",
          "properties": {
            "moran_i": {"type": "number"},
            "geary_c": {"type": "number"},
            "spatial_autocorrelation": {"type": "string"},
            "spatial_pattern": {"type": "string"}
          }
        }
      }
    },
    "interpolation_results": {
      "type": "object",
      "properties": {
        "interpolated_surface": {
          "type": "object",
          "properties": {
            "grid": {
              "type": "array",
              "items": {
                "type": "array",
                "items": {"type": "number"}
              }
            },
            "coordinates": {
              "type": "object",
              "properties": {
                "x_coords": {"type": "array"},
                "y_coords": {"type": "array"}
              }
            }
          }
        },
        "interpolation_metrics": {
          "type": "object",
          "properties": {
            "rmse": {"type": "number"},
            "mae": {"type": "number"},
            "r_squared": {"type": "number"}
          }
        }
      }
    },
    "buffer_analysis": {
      "type": "object",
      "properties": {
        "buffers": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "original_feature": {"type": "object"},
              "buffer_geometry": {"type": "object"},
              "area": {"type": "number"},
              "intersecting_features": {
                "type": "array",
                "items": {"type": "object"}
              }
            }
          }
        }
      }
    },
    "visualizations": {
      "type": "object",
      "properties": {
        "interactive_map": {"type": "string"},
        "static_map": {"type": "string"},
        "spatial_charts": {"type": "string"},
        "3d_visualization": {"type": "string"}
      }
    },
    "spatial_insights": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "insight": {"type": "string"},
          "location": {
            "type": "object",
            "properties": {
              "latitude": {"type": "number"},
              "longitude": {"type": "number"}
            }
          },
          "confidence": {"type": "number"},
          "significance": {"type": "string"}
        }
      }
    },
    "processing_time": {
      "type": "number",
      "description": "Time taken for geospatial analysis in seconds"
    }
  }
}
```

## Intended Use
- **Spatial Clustering**: Identify spatial clusters and patterns
- **Hotspot Analysis**: Detect areas of high activity or concentration
- **Spatial Interpolation**: Estimate values at unmeasured locations
- **Buffer Analysis**: Analyze areas within specified distances
- **Overlay Analysis**: Combine multiple spatial datasets
- **Network Analysis**: Analyze spatial networks and connectivity
- **Spatial Regression**: Model relationships with spatial components
- **Geostatistics**: Apply statistical methods to spatial data

## Limitations
- Analysis quality depends on spatial data accuracy and resolution
- Coordinate system transformations may introduce errors
- Large spatial datasets may require significant computational resources
- Spatial analysis results may be sensitive to parameter choices

## Safety
- Validate spatial data quality and coordinate systems
- Consider privacy implications of location-based analysis
- Handle sensitive geographic information appropriately
- Ensure spatial analysis methods are appropriate for the data

## Runbook

### Setup
1. **Install Dependencies**:
   ```bash
   pip install pandas numpy matplotlib seaborn geopandas folium plotly shapely pyproj
   ```

2. **Verify Installation**:
   ```python
   import pandas as pd
   import numpy as np
   import matplotlib.pyplot as plt
   import geopandas as gpd
   import folium
   import plotly.express as px
   from shapely.geometry import Point, Polygon
   ```

### Usage

#### Spatial Clustering Analysis
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
import geopandas as gpd
from shapely.geometry import Point

def perform_spatial_clustering(point_data, eps=0.01, min_samples=5):
    """Perform spatial clustering using DBSCAN"""
    
    # Convert to DataFrame
    df = pd.DataFrame(point_data)
    
    # Create geometry column
    geometry = [Point(xy) for xy in zip(df['longitude'], df['latitude'])]
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")
    
    # Perform clustering
    coords = np.column_stack([df['longitude'], df['latitude']])
    clustering = DBSCAN(eps=eps, min_samples=min_samples).fit(coords)
    
    # Add cluster labels
    gdf['cluster'] = clustering.labels_
    
    return gdf, clustering

def visualize_spatial_clusters(gdf):
    """Visualize spatial clusters"""
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Plot clusters
    for cluster_id in gdf['cluster'].unique():
        if cluster_id == -1:  # Noise points
            cluster_data = gdf[gdf['cluster'] == cluster_id]
            ax.scatter(cluster_data['longitude'], cluster_data['latitude'], 
                      c='black', s=20, alpha=0.6, label='Noise')
        else:
            cluster_data = gdf[gdf['cluster'] == cluster_id]
            ax.scatter(cluster_data['longitude'], cluster_data['latitude'], 
                      s=50, alpha=0.7, label=f'Cluster {cluster_id}')
    
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_title('Spatial Clustering Results')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('spatial_clustering.png', dpi=300, bbox_inches='tight')
    plt.close()

# Usage example
point_data = [
    {'latitude': 40.7128, 'longitude': -74.0060, 'value': 100},
    {'latitude': 40.7589, 'longitude': -73.9851, 'value': 150},
    {'latitude': 40.7505, 'longitude': -73.9934, 'value': 120},
    {'latitude': 40.7484, 'longitude': -73.9857, 'value': 180},
    {'latitude': 40.7527, 'longitude': -73.9772, 'value': 90},
    {'latitude': 40.7589, 'longitude': -73.9851, 'value': 160},
    {'latitude': 40.7505, 'longitude': -73.9934, 'value': 140},
    {'latitude': 40.7484, 'longitude': -73.9857, 'value': 200}
]

gdf, clustering = perform_spatial_clustering(point_data)
visualize_spatial_clusters(gdf)

print(f"Number of clusters: {len(set(clustering.labels_)) - (1 if -1 in clustering.labels_ else 0)}")
print(f"Number of noise points: {list(clustering.labels_).count(-1)}")
```

#### Interactive Mapping
```python
import folium
import pandas as pd
import numpy as np

def create_interactive_map(point_data, cluster_results=None):
    """Create interactive map with Folium"""
    
    # Calculate center point
    lats = [point['latitude'] for point in point_data]
    lons = [point['longitude'] for point in point_data]
    center_lat = np.mean(lats)
    center_lon = np.mean(lons)
    
    # Create map
    m = folium.Map(location=[center_lat, center_lon], zoom_start=12)
    
    # Add points to map
    for i, point in enumerate(point_data):
        popup_text = f"Value: {point.get('value', 'N/A')}"
        if cluster_results is not None:
            popup_text += f"<br>Cluster: {cluster_results[i]}"
        
        folium.CircleMarker(
            location=[point['latitude'], point['longitude']],
            radius=8,
            popup=popup_text,
            color='red',
            fill=True,
            fillColor='red',
            fillOpacity=0.7
        ).add_to(m)
    
    # Add heatmap
    heat_data = [[point['latitude'], point['longitude'], point.get('value', 1)] 
                 for point in point_data]
    folium.plugins.HeatMap(heat_data).add_to(m)
    
    return m

def create_choropleth_map(geojson_data, value_column):
    """Create choropleth map"""
    
    m = folium.Map()
    
    folium.Choropleth(
        geo_data=geojson_data,
        name="choropleth",
        data=geojson_data,
        columns=["id", value_column],
        key_on="feature.id",
        fill_color="YlOrRd",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=value_column
    ).add_to(m)
    
    folium.LayerControl().add_to(m)
    
    return m

# Usage example
interactive_map = create_interactive_map(point_data)
interactive_map.save('interactive_spatial_map.html')

print("Interactive map saved as 'interactive_spatial_map.html'")
```

#### Spatial Interpolation
```python
import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt

def perform_spatial_interpolation(point_data, grid_resolution=100):
    """Perform spatial interpolation using scipy"""
    
    # Extract coordinates and values
    x = np.array([point['longitude'] for point in point_data])
    y = np.array([point['latitude'] for point in point_data])
    z = np.array([point['value'] for point in point_data])
    
    # Create grid
    xi = np.linspace(x.min(), x.max(), grid_resolution)
    yi = np.linspace(y.min(), y.max(), grid_resolution)
    xi_grid, yi_grid = np.meshgrid(xi, yi)
    
    # Perform interpolation
    zi_grid = griddata((x, y), z, (xi_grid, yi_grid), method='cubic')
    
    return xi_grid, yi_grid, zi_grid

def visualize_interpolation(xi_grid, yi_grid, zi_grid, original_points):
    """Visualize interpolation results"""
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Interpolated surface
    contour = ax1.contourf(xi_grid, yi_grid, zi_grid, levels=20, cmap='viridis')
    ax1.scatter([p['longitude'] for p in original_points], 
                [p['latitude'] for p in original_points], 
                c='red', s=50, edgecolors='black')
    ax1.set_title('Spatial Interpolation Surface')
    ax1.set_xlabel('Longitude')
    ax1.set_ylabel('Latitude')
    plt.colorbar(contour, ax=ax1)
    
    # 3D surface
    ax2 = fig.add_subplot(122, projection='3d')
    surf = ax2.plot_surface(xi_grid, yi_grid, zi_grid, cmap='viridis', alpha=0.8)
    ax2.scatter([p['longitude'] for p in original_points], 
                [p['latitude'] for p in original_points], 
                [p['value'] for p in original_points], 
                c='red', s=50, edgecolors='black')
    ax2.set_title('3D Interpolation Surface')
    ax2.set_xlabel('Longitude')
    ax2.set_ylabel('Latitude')
    ax2.set_zlabel('Value')
    
    plt.tight_layout()
    plt.savefig('spatial_interpolation.png', dpi=300, bbox_inches='tight')
    plt.close()

# Usage example
xi_grid, yi_grid, zi_grid = perform_spatial_interpolation(point_data)
visualize_interpolation(xi_grid, yi_grid, zi_grid, point_data)
```

### Error Handling
- Validate spatial data coordinates and CRS
- Handle missing or invalid spatial data
- Manage coordinate system transformation errors
- Ensure spatial analysis parameters are appropriate

### Monitoring
- Track spatial analysis performance and accuracy
- Monitor spatial data quality and completeness
- Review spatial analysis results and insights
- Validate spatial model assumptions

### Best Practices
1. **Data Quality**: Ensure high-quality spatial data and coordinate systems
2. **CRS Management**: Use appropriate coordinate reference systems
3. **Spatial Scale**: Consider appropriate spatial scale for analysis
4. **Validation**: Validate spatial analysis results with ground truth
5. **Visualization**: Use appropriate maps and visualizations
6. **Documentation**: Document spatial analysis methods and assumptions
7. **Privacy**: Consider privacy implications of spatial data
8. **Performance**: Optimize spatial analysis for large datasets
