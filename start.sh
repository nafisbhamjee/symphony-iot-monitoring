#!/bin/bash

###############################################################################
# Symphony IoT Monitoring System - One-Command Startup Script
# This script starts the entire stack: IoT Sim, Prometheus, Grafana, 
# Analysis Engine, and Alert Engine with Gmail notifications
###############################################################################

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Banner
echo ""
echo -e "${PURPLE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${PURPLE}║                                                              ║${NC}"
echo -e "${PURPLE}║          🚀 Symphony IoT Monitoring System 🚀               ║${NC}"
echo -e "${PURPLE}║                                                              ║${NC}"
echo -e "${PURPLE}║         Starting Complete Stack in One Command...           ║${NC}"
echo -e "${PURPLE}║                                                              ║${NC}"
echo -e "${PURPLE}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Function to print step
print_step() {
    echo -e "${CYAN}▶ $1${NC}"
}

# Function to print success
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

# Function to print warning
print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Function to print error
print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Function to check if Docker is running
check_docker() {
    print_step "Checking Docker..."
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running!"
        echo "Please start Docker Desktop and try again."
        exit 1
    fi
    print_success "Docker is running"
}

# Function to stop existing containers
stop_existing() {
    print_step "Stopping any existing Symphony containers..."
    docker-compose down > /dev/null 2>&1 || true
    print_success "Cleanup complete"
}

# Function to build images
build_images() {
    print_step "Building Docker images..."
    echo ""
    docker-compose build --no-cache
    echo ""
    print_success "All images built successfully"
}

# Function to start containers
start_containers() {
    print_step "Starting all containers..."
    echo ""
    docker-compose up -d
    echo ""
    print_success "All containers started"
}

# Function to wait for service
wait_for_service() {
    local service_name=$1
    local url=$2
    local max_attempts=30
    local attempt=0
    
    print_step "Waiting for $service_name to be ready..."
    
    while [ $attempt -lt $max_attempts ]; do
        if curl -s -f "$url" > /dev/null 2>&1; then
            print_success "$service_name is ready!"
            return 0
        fi
        attempt=$((attempt + 1))
        echo -n "."
        sleep 2
    done
    
    print_warning "$service_name took longer than expected, but continuing..."
    return 1
}

# Function to display status
display_status() {
    echo ""
    echo -e "${PURPLE}════════════════════════════════════════════════════════════${NC}"
    echo -e "${PURPLE}                    System Status                           ${NC}"
    echo -e "${PURPLE}════════════════════════════════════════════════════════════${NC}"
    echo ""
    
    docker-compose ps
    
    echo ""
}

# Function to display access URLs
display_urls() {
    echo ""
    echo -e "${PURPLE}════════════════════════════════════════════════════════════${NC}"
    echo -e "${PURPLE}                    Access URLs                             ${NC}"
    echo -e "${PURPLE}════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "${GREEN}🌡️  IoT Simulator:      ${NC}http://localhost:8080"
    echo -e "${GREEN}📊 Prometheus:         ${NC}http://localhost:9090"
    echo -e "${GREEN}📈 Grafana:            ${NC}http://localhost:3000 ${YELLOW}(admin/admin)${NC}"
    echo -e "${GREEN}🔬 Analysis Engine:    ${NC}http://localhost:8086"
    echo -e "${GREEN}🚨 Alert Engine:       ${NC}http://localhost:8087"
    echo ""
    echo -e "${CYAN}Alert Engine API Endpoints:${NC}"
    echo -e "  • http://localhost:8087/health       - Health check"
    echo -e "  • http://localhost:8087/alerts       - Current alerts"
    echo -e "  • http://localhost:8087/rules        - Alert rules"
    echo -e "  • http://localhost:8087/history      - Alert history"
    echo -e "  • http://localhost:8087/metrics      - Prometheus metrics"
    echo ""
}

# Function to display monitoring info
display_monitoring() {
    echo -e "${PURPLE}════════════════════════════════════════════════════════════${NC}"
    echo -e "${PURPLE}                 Email Alert Monitoring                     ${NC}"
    echo -e "${PURPLE}════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "${GREEN}📧 Gmail Alerts:       ${NC}ENABLED"
    echo -e "${GREEN}📬 Recipient:          ${NC}sathyacanchi@gmail.com"
    echo -e "${GREEN}🔄 Check Interval:     ${NC}30 seconds"
    echo -e "${GREEN}⏱️  Alert Cooldown:     ${NC}15 minutes"
    echo ""
    echo -e "${YELLOW}Active Alert Rules:${NC}"
    echo -e "  🔥 Critical Temperature  → > 35°C    (fires immediately)"
    echo -e "  🔋 Low Battery           → < 20%     (fires immediately)"
    echo -e "  💧 High Humidity         → > 80%     (fires immediately)"
    echo ""
}

# Function to check alerts
check_alerts() {
    print_step "Checking alert status..."
    sleep 5  # Wait a bit for first evaluation
    
    if curl -s http://localhost:8087/alerts > /dev/null 2>&1; then
        echo ""
        echo -e "${CYAN}Current Alert Status:${NC}"
        curl -s http://localhost:8087/alerts | python3 -m json.tool
        print_success "Alert engine is monitoring metrics!"
    else
        print_warning "Alert engine API not responding yet (this is normal)"
    fi
}

# Function to display useful commands
display_commands() {
    echo ""
    echo -e "${PURPLE}════════════════════════════════════════════════════════════${NC}"
    echo -e "${PURPLE}                 Useful Commands                            ${NC}"
    echo -e "${PURPLE}════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "${CYAN}View Logs:${NC}"
    echo -e "  docker-compose logs -f                    # All services"
    echo -e "  docker-compose logs -f alert-engine       # Alert engine only"
    echo -e "  docker-compose logs -f iot-sim            # IoT simulator only"
    echo ""
    echo -e "${CYAN}Check Status:${NC}"
    echo -e "  docker-compose ps                         # Container status"
    echo -e "  curl http://localhost:8087/alerts | jq    # Current alerts"
    echo -e "  curl http://localhost:8087/health | jq    # Health check"
    echo ""
    echo -e "${CYAN}Control Services:${NC}"
    echo -e "  docker-compose stop                       # Stop all"
    echo -e "  docker-compose restart alert-engine       # Restart alerts"
    echo -e "  docker-compose down                       # Stop and remove"
    echo ""
    echo -e "${CYAN}Send Test Email:${NC}"
    echo -e "  curl -X POST http://localhost:8087/test-email"
    echo ""
}

# Main execution
main() {
    cd "$(dirname "$0")"
    
    check_docker
    stop_existing
    build_images
    start_containers
    
    # Wait for critical services
    wait_for_service "IoT Simulator" "http://localhost:8080"
    wait_for_service "Prometheus" "http://localhost:9090"
    wait_for_service "Alert Engine" "http://localhost:8087/health"
    
    display_status
    display_urls
    display_monitoring
    check_alerts
    display_commands
    
    echo ""
    echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}   ✓ Symphony IoT Monitoring System is Running! ✓          ${NC}"
    echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "${YELLOW}📧 Email alerts will be sent to: sathyacanchi@gmail.com${NC}"
    echo -e "${YELLOW}🌡️  Temperature is currently being monitored${NC}"
    echo -e "${YELLOW}🔔 You'll receive an email if temperature > 35°C${NC}"
    echo ""
    echo -e "${CYAN}Press Ctrl+C to stop monitoring, then run:${NC}"
    echo -e "${CYAN}  docker-compose down${NC}"
    echo ""
    echo -e "${PURPLE}Tailing alert engine logs (Ctrl+C to exit)...${NC}"
    echo ""
    
    # Tail logs
    docker-compose logs -f alert-engine
}

# Run main function
main
