# Knowledge Graph .pkl Storage Update

## 🎯 **Objective Achieved**

Successfully updated the code to store knowledge graph .pkl files in the `Results\knowledge_graphs` directory, ensuring consistent and organized storage of knowledge graph data.

## 📋 **What Was Updated**

### ✅ **1. Enhanced Process Content Agent**
- **File**: `src/agents/enhanced_process_content_agent.py`
- **Updated Methods**:
  - `create_knowledge_graph()` - Added .pkl file saving functionality
  - `_process_ctext_content()` - Added .pkl file saving for ctext.org content
  - `_process_openlibrary_content()` - Added .pkl file saving for Open Library content

### ✅ **2. Knowledge Graph Coordinator**
- **File**: `src/agents/knowledge_graph_coordinator.py`
- **Updated**: Graph storage path to use settings-based configuration

### ✅ **3. Settings Configuration**
- **File**: `src/config/settings.py`
- **Verified**: Knowledge graphs directory is properly configured as `Results\knowledge_graphs`

## 🔧 **Implementation Details**

### **Storage Location**
All knowledge graph .pkl files are now stored in:
```
Results/knowledge_graphs/
```

### **File Naming Convention**
Files are saved with descriptive names including:
- Content type prefix (e.g., `ctext_`, `openlibrary_`, `knowledge_graph_`)
- Safe title (sanitized for filesystem compatibility)
- Timestamp for uniqueness

**Example filenames**:
- `ctext_knowledge_graph_Sun_Tzu_Art_of_War_20250814_232500.pkl`
- `openlibrary_knowledge_graph_War_and_Peace_20250814_232500.pkl`
- `knowledge_graph_Content_20250814_232500.pkl`

### **Enhanced Return Data**
All knowledge graph creation methods now return additional metadata:
```python
{
    "success": True,
    "nodes": 3,
    "edges": 2,
    "entities_count": 5,
    "relationships_count": 3,
    "pkl_file_path": "Results/knowledge_graphs/knowledge_graph_Content_20250814_232500.pkl",
    "storage_location": "Results/knowledge_graphs"
}
```

## 🧪 **Testing**

### **Test Script**: `Test/test_knowledge_graph_pkl_storage.py`
Comprehensive test suite that verifies:
- ✅ Settings configuration is correct
- ✅ Directory creation and management
- ✅ Knowledge graph creation and .pkl file saving
- ✅ File validation (existence, size, content)
- ✅ File loading and verification

### **Test Results**
```
✅ Knowledge graphs directory ensured: Results\knowledge_graphs
✅ Test knowledge graph saved to: Results\knowledge_graphs\test_knowledge_graph_20250814_232500.pkl
✅ PKL file exists at: Results\knowledge_graphs\test_knowledge_graph_20250814_232500.pkl
✅ PKL file has content (706 bytes)
✅ PKL file loaded successfully with 3 nodes and 2 edges
```

## 📁 **Directory Structure**

The updated structure ensures organized storage:
```
Results/
├── knowledge_graphs/          # Knowledge graph .pkl files
│   ├── ctext_knowledge_graph_*.pkl
│   ├── openlibrary_knowledge_graph_*.pkl
│   ├── knowledge_graph_*.pkl
│   └── test_knowledge_graph_*.pkl
├── reports/                   # Generated reports
└── ...
```

## 🔄 **Integration Points**

### **Enhanced Process Content Agent**
- **Tool Method**: `create_knowledge_graph()` - Saves .pkl files directly
- **Bulk Import**: Automatically saves .pkl files for each processed URL
- **Content Types**: Supports ctext.org, Open Library, and general content

### **MCP Servers**
- **Unified MCP Server**: Inherits .pkl saving functionality
- **Enhanced Unified MCP Server**: Inherits .pkl saving functionality
- **Process Content Agent**: Provides .pkl saving through tool interface

### **Settings Integration**
- **Path Configuration**: Uses `settings.paths.knowledge_graphs_dir`
- **Directory Management**: Automatic directory creation
- **Consistent Storage**: All agents use the same storage location

## 📊 **Benefits**

### **1. Organized Storage**
- All knowledge graph files in one location
- Consistent naming convention
- Easy to find and manage

### **2. Persistent Storage**
- Knowledge graphs are saved as .pkl files
- Can be loaded and reused later
- Maintains graph structure and metadata

### **3. Traceability**
- Each file includes timestamp and content information
- Easy to track when graphs were created
- Clear identification of content source

### **4. Scalability**
- Supports multiple knowledge graphs
- No file conflicts due to timestamped naming
- Easy to manage large numbers of graphs

## 🚀 **Usage Examples**

### **Via Enhanced Process Content Agent**
```python
agent = EnhancedProcessContentAgent()
result = await agent.create_knowledge_graph(
    content="Sample content about Sun Tzu",
    title="Sun Tzu Analysis"
)

# Result includes pkl file path
pkl_path = result.get("pkl_file_path")
print(f"Knowledge graph saved to: {pkl_path}")
```

### **Via Bulk Import**
```python
# Process URLs and automatically save .pkl files
bulk_content = """
add the following to vector and knowledge graph db @https://ctext.org/art-of-war
"""
result = await agent.process_content(bulk_content)
```

### **Loading Saved Knowledge Graphs**
```python
import pickle
from pathlib import Path

# Load a saved knowledge graph
pkl_path = "Results/knowledge_graphs/knowledge_graph_Content_20250814_232500.pkl"
with open(pkl_path, 'rb') as f:
    graph = pickle.load(f)

print(f"Loaded graph with {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges")
```

## 📝 **Maintenance Notes**

- **File Management**: Old .pkl files can be safely deleted if no longer needed
- **Storage Space**: Monitor disk usage as .pkl files can grow large
- **Backup**: Consider backing up important knowledge graph files
- **Versioning**: Timestamped filenames provide natural versioning

## 🎯 **Next Steps**

The knowledge graph .pkl storage system is now fully implemented and tested. Future enhancements could include:

1. **Graph Merging**: Combine multiple .pkl files into larger graphs
2. **Graph Versioning**: Track changes and versions of knowledge graphs
3. **Graph Compression**: Optimize storage for large graphs
4. **Graph Indexing**: Create searchable indexes of graph content
5. **Graph Visualization**: Generate visual representations of saved graphs

---

**Update Completed**: Knowledge Graph .pkl Storage
**Storage Location**: `Results\knowledge_graphs`
**File Format**: Pickle (.pkl)
**Naming**: Descriptive with timestamps
**Testing**: Comprehensive test suite passed
