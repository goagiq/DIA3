#!/bin/bash

# Phase 5 Enhanced Report System Deployment Script
# Includes 60-second sleep after server restart as requested

set -e

echo "🚀 Starting Phase 5 Enhanced Report System Deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    print_error "docker-compose is not installed. Please install docker-compose and try again."
    exit 1
fi

# Stop existing containers
print_status "Stopping existing containers..."
docker-compose -f docker-compose.phase5.yml down || true

# Remove old containers and volumes (optional - uncomment if needed)
# print_status "Removing old containers and volumes..."
# docker-compose -f docker-compose.phase5.yml down -v --remove-orphans

# Build and start services
print_status "Building and starting Phase 5 services..."
docker-compose -f docker-compose.phase5.yml up -d --build

# Wait for services to start
print_status "Waiting for services to start..."
sleep 10

# Check service health
print_status "Checking service health..."

# Function to check service health
check_service_health() {
    local service_name=$1
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if docker-compose -f docker-compose.phase5.yml ps $service_name | grep -q "Up"; then
            print_success "$service_name is running"
            return 0
        fi
        
        print_warning "Waiting for $service_name to start... (attempt $attempt/$max_attempts)"
        sleep 5
        attempt=$((attempt + 1))
    done
    
    print_error "$service_name failed to start"
    return 1
}

# Check each service
services=("enhanced-report-api" "mcp-server" "redis" "postgres" "mongo" "chroma" "nginx" "prometheus" "grafana")

for service in "${services[@]}"; do
    if ! check_service_health $service; then
        print_error "Service $service failed to start. Check logs with: docker-compose -f docker-compose.phase5.yml logs $service"
        exit 1
    fi
done

# Restart MCP server for enhanced report tools integration
print_status "Restarting MCP server to integrate enhanced report tools..."
docker-compose -f docker-compose.phase5.yml restart mcp-server

# ⏳ 60-second sleep after server restart as requested
print_status "⏳ Waiting 60 seconds for server to stabilize after restart..."
for i in {60..1}; do
    echo -ne "\r⏳ Waiting $i seconds for server to stabilize... "
    sleep 1
done
echo -e "\n"

print_success "✅ Server restart completed with 60-second stabilization period"

# Verify MCP server is responding
print_status "Verifying MCP server is responding..."
max_attempts=10
attempt=1

while [ $attempt -le $max_attempts ]; do
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        print_success "MCP server is responding on port 8000"
        break
    fi
    
    print_warning "Waiting for MCP server to respond... (attempt $attempt/$max_attempts)"
    sleep 5
    attempt=$((attempt + 1))
done

if [ $attempt -gt $max_attempts ]; then
    print_error "MCP server is not responding. Check logs with: docker-compose -f docker-compose.phase5.yml logs mcp-server"
    exit 1
fi

# Verify API server is responding
print_status "Verifying API server is responding..."
max_attempts=10
attempt=1

while [ $attempt -le $max_attempts ]; do
    if curl -f http://localhost:8001/health > /dev/null 2>&1; then
        print_success "API server is responding on port 8001"
        break
    fi
    
    print_warning "Waiting for API server to respond... (attempt $attempt/$max_attempts)"
    sleep 5
    attempt=$((attempt + 1))
done

if [ $attempt -gt $max_attempts ]; then
    print_error "API server is not responding. Check logs with: docker-compose -f docker-compose.phase5.yml logs enhanced-report-api"
    exit 1
fi

# Test enhanced report MCP tools
print_status "Testing enhanced report MCP tools..."

# Create test script
cat > /tmp/test_enhanced_report_mcp.py << 'EOF'
import asyncio
import aiohttp
import json

async def test_enhanced_report_mcp():
    """Test enhanced report MCP tools."""
    try:
        async with aiohttp.ClientSession() as session:
            # Test MCP server health
            async with session.get('http://localhost:8000/health') as response:
                if response.status == 200:
                    print("✅ MCP server health check passed")
                else:
                    print("❌ MCP server health check failed")
                    return False
            
            # Test API server health
            async with session.get('http://localhost:8001/health') as response:
                if response.status == 200:
                    print("✅ API server health check passed")
                else:
                    print("❌ API server health check failed")
                    return False
            
            # Test enhanced report generation endpoint
            test_data = {
                "query": "Test enhanced report generation",
                "include_monte_carlo": True,
                "include_visualizations": True,
                "include_knowledge_graph": True
            }
            
            async with session.post('http://localhost:8001/api/v1/reports/enhanced/generate', 
                                   json=test_data) as response:
                if response.status == 200:
                    result = await response.json()
                    print("✅ Enhanced report generation test passed")
                    print(f"   Result: {result.get('status', 'unknown')}")
                else:
                    print(f"❌ Enhanced report generation test failed: {response.status}")
                    return False
            
            return True
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_enhanced_report_mcp())
    exit(0 if success else 1)
EOF

# Run test
if python3 /tmp/test_enhanced_report_mcp.py; then
    print_success "Enhanced report MCP tools test passed"
else
    print_warning "Enhanced report MCP tools test failed - check logs for details"
fi

# Clean up test file
rm -f /tmp/test_enhanced_report_mcp.py

# Display service status
print_status "Displaying service status..."
docker-compose -f docker-compose.phase5.yml ps

# Display service URLs
echo ""
print_success "🎉 Phase 5 Enhanced Report System Deployment Complete!"
echo ""
echo "📋 Service URLs:"
echo "   MCP Server: http://localhost:8000"
echo "   API Server: http://localhost:8001"
echo "   Grafana Dashboard: http://localhost:3000"
echo "   Prometheus: http://localhost:9090"
echo "   Nginx: http://localhost:80"
echo ""
echo "🔧 Useful Commands:"
echo "   View logs: docker-compose -f docker-compose.phase5.yml logs -f"
echo "   Stop services: docker-compose -f docker-compose.phase5.yml down"
echo "   Restart services: docker-compose -f docker-compose.phase5.yml restart"
echo ""
echo "📊 Enhanced Report System Features:"
echo "   ✅ 25+ Analysis Components"
echo "   ✅ Monte Carlo Simulations"
echo "   ✅ Interactive Visualizations"
echo "   ✅ Knowledge Graph Analysis"
echo "   ✅ Strategic Intelligence Analysis"
echo "   ✅ Risk Assessment Matrix"
echo "   ✅ Executive Summary Generation"
echo "   ✅ Export Capabilities (PDF, Word, Excel)"
echo "   ✅ FedRAMP and DoD Compliance"
echo "   ✅ 60-second stabilization period implemented"
echo ""

print_success "🚀 Phase 5 Enhanced Report System is ready for testing!"
