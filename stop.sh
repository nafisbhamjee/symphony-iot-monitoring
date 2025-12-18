#!/bin/bash

##############################################
# Symphony IoT Monitoring - Stop Script
##############################################

echo "🛑 Stopping Symphony IoT Monitoring System..."
docker-compose down

echo ""
echo "✅ All services stopped!"
echo ""
