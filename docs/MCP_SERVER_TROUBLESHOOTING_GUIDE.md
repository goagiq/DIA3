# MCP Server Troubleshooting Guide

## Common Issue: "MCP client cannot call mcp tools"

### Problem Description
The MCP server appears to be running (health checks pass) but MCP tools are not accessible via JSON-RPC calls. This typically manifests as:
- HTTP 404 errors for MCP endpoints (`/mcp`, `/mcp/`, `/mcp/initialize`, etc.)
- Empty responses from MCP JSON-RPC calls
- Tools not appearing in `tools/list` responses

### Root Cause
The most common cause is that the **standalone MCP server is not actually starting** - it's only being initialized. This happens when the `start_standalone_mcp_server` function in `main.py` only creates the server instance but doesn't call the `start()` method.

### The Fix (Applied 2025-08-15)

#### Before (Broken):
```python
def start_standalone_mcp_server(host: str = "localhost", port: int = 8000):
    """Start standalone MCP server for Strands integration."""
    try:
        from src.mcp_servers.standalone_mcp_server import StandaloneMCPServer
        
        # Initialize the standalone MCP server
        server = StandaloneMCPServer()
        print("✅ Standalone MCP server initialized")
        return server
    except Exception as e:
        print(f"⚠️ Warning: Could not initialize standalone MCP server: {e}")
        return None
```

#### After (Fixed):
```python
def start_standalone_mcp_server(host: str = "localhost", port: int = 8000):
    """Start standalone MCP server for Strands integration."""
    try:
        from src.mcp_servers.standalone_mcp_server import start_standalone_mcp_server as start_server
        
        # Start the standalone MCP server
        server = start_server(host, port)
        print("✅ Standalone MCP server started")
        return server
    except Exception as e:
        print(f"⚠️ Warning: Could not start standalone MCP server: {e}")
        return None
```

### Key Changes Made

1. **Import the correct function**: Import `start_standalone_mcp_server` from the standalone server module instead of just `StandaloneMCPServer`
2. **Actually start the server**: Call the imported function which properly starts the server on the specified port
3. **Update test scripts**: Change MCP base URL from `http://localhost:8003/mcp` to `http://localhost:8000`

### Verification Steps

1. **Check if standalone MCP server is running**:
   ```bash
   curl -s http://localhost:8000/health
   ```

2. **Test MCP initialize**:
   ```bash
   curl -s -X POST http://localhost:8000 -H "Content-Type: application/json" -d '{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test", "version": "1.0.0"}}}'
   ```

3. **Test tools/list**:
   ```bash
   curl -s -X POST http://localhost:8000 -H "Content-Type: application/json" -d '{"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}'
   ```

### Architecture Understanding

The system has **two separate MCP servers**:

1. **Standalone MCP Server** (Port 8000):
   - Runs independently for Strands integration
   - Handles direct JSON-RPC calls
   - Must be explicitly started with `start()` method

2. **Integrated MCP Server** (Port 8003/mcp):
   - Mounted within FastAPI for web integration
   - Handles HTTP routing through FastAPI
   - Used for web-based MCP interactions

### Prevention Checklist

- [ ] Ensure `start_standalone_mcp_server` calls the actual start function
- [ ] Verify standalone server is running on port 8000
- [ ] Test MCP tools are accessible via JSON-RPC
- [ ] Update test scripts to use correct MCP base URL
- [ ] Document any changes to MCP server configuration

### Related Files Modified

- `main.py`: Fixed standalone MCP server startup
- `Test/test_mcp_strategic_deception.py`: Updated MCP base URL
- `Test/test_mcp_simple_integration.py`: Updated MCP base URL (if exists)

### Testing Commands

```bash
# Test standalone MCP server
.venv/Scripts/python.exe Test/test_mcp_strategic_deception.py

# Test integrated MCP server
.venv/Scripts/python.exe Test/test_strategic_deception_simple.py
```

### When This Issue Occurs

This issue typically occurs when:
- New MCP tools are added to the system
- The standalone MCP server configuration is modified
- The server startup sequence is changed
- Test scripts are updated without corresponding server changes

### Quick Diagnostic Commands

```bash
# Check if standalone server is running
netstat -an | findstr :8000

# Check if integrated server is running
netstat -an | findstr :8003

# Test MCP health
curl -s http://localhost:8003/mcp-health
```

---

**Note**: This issue has occurred multiple times in the project history. Always verify that the standalone MCP server is actually starting, not just initializing, when adding new MCP tools or modifying server configuration.
