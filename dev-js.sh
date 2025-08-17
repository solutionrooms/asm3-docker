#!/bin/bash
# ASM3 JavaScript Development Helper Script
# 
# This script helps manage JavaScript development workflow

echo "=== ASM3 JavaScript Development Helper ==="
echo

if [ "$1" = "dev" ]; then
    echo "🔧 Enabling DEVELOPMENT mode (individual JS files)..."
    sed -i 's/rollup_js = true/rollup_js = false  # Development mode: load individual JS files for instant changes/' asm3.conf
    docker compose restart asm3
    echo "✅ Development mode enabled!"
    echo "   → Edit files in src/static/js/"
    echo "   → Changes appear immediately on browser refresh"
    echo "   → Use 'dev-js.sh prod' when done developing"

elif [ "$1" = "prod" ]; then
    echo "🚀 Enabling PRODUCTION mode (bundled JS files)..."
    echo "   → Building JavaScript bundle..."
    docker compose exec asm3 sh -c "cd /app && npm install && make rollup"
    sed -i 's/rollup_js = false.*$/rollup_js = true/' asm3.conf
    docker compose restart asm3
    echo "✅ Production mode enabled!"
    echo "   → Application now uses optimized bundled JavaScript"

elif [ "$1" = "build" ]; then
    echo "🔨 Rebuilding JavaScript bundle (keeping current mode)..."
    docker compose exec asm3 sh -c "cd /app && npm install && make rollup"
    echo "✅ Bundle rebuilt! Refresh browser to see changes."

else
    echo "Usage:"
    echo "  ./dev-js.sh dev     # Enable development mode (individual files)"
    echo "  ./dev-js.sh prod    # Enable production mode (bundled files)"
    echo "  ./dev-js.sh build   # Rebuild bundle (keep current mode)"
    echo
    echo "Current status:"
    if grep -q "rollup_js = false" asm3.conf; then
        echo "  📝 DEVELOPMENT mode (individual files loaded)"
        echo "     JavaScript changes appear immediately on page refresh"
    else
        echo "  📦 PRODUCTION mode (bundled files loaded)"
        echo "     Run './dev-js.sh build' after JavaScript changes"
    fi
fi