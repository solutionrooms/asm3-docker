#!/bin/bash

# Test script for ASM3 Cron + Weight Monitor Integration
# This script helps verify that the weight monitor is properly integrated
# into the asm3_cron service

echo "ASM3 Cron Integration Test"
echo "========================="

# Check if required files exist
echo "Checking required files..."

if [ ! -f "weight_monitor.py" ]; then
    echo "❌ weight_monitor.py not found"
    exit 1
fi
echo "✅ weight_monitor.py found"

if [ ! -f "asm3.conf" ]; then
    echo "❌ asm3.conf not found"
    exit 1
fi
echo "✅ asm3.conf found"

if [ ! -f "docker-compose.yml" ]; then
    echo "❌ docker-compose.yml not found"
    exit 1
fi
echo "✅ docker-compose.yml found"

# Check if weight_monitor.py is mounted in docker-compose.yml
echo ""
echo "Checking Docker configuration..."

if grep -q "weight_monitor.py:/app/weight_monitor.py:ro" docker-compose.yml; then
    echo "✅ weight_monitor.py is mounted in asm3_cron service"
else
    echo "❌ weight_monitor.py mount not found in docker-compose.yml"
    exit 1
fi

if grep -q "python3 /app/weight_monitor.py &" docker-compose.yml; then
    echo "✅ weight_monitor.py is started in asm3_cron service"
else
    echo "❌ weight_monitor.py startup command not found in docker-compose.yml"
    exit 1
fi

echo ""
echo "Testing weight monitor syntax..."
if python3 -m py_compile weight_monitor.py; then
    echo "✅ weight_monitor.py syntax is valid"
else
    echo "❌ weight_monitor.py has syntax errors"
    exit 1
fi

echo ""
echo "Integration test passed! ✅"
echo ""
echo "To start the integrated services:"
echo "  docker compose up -d"
echo ""
echo "To view logs:"
echo "  docker compose logs -f asm3_cron"
echo ""
echo "To test weight monitor only:"
echo "  docker compose exec asm3_cron python3 /app/weight_monitor.py --once"