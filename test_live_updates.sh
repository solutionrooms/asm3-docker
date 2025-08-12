#!/bin/bash

echo "🔧 Testing Live Development Setup"
echo "================================="

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

echo "✅ Docker is running"

# Check if containers are up
if ! docker compose ps | grep -q "Up"; then
    echo "📦 Starting containers with live development setup..."
    docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d
    
    echo "⏳ Waiting for containers to start..."
    sleep 10
else
    echo "✅ Containers are already running"
fi

# Test basic connectivity
echo "🌐 Testing ASM3 connectivity..."
if curl -f -s http://localhost:8090/ > /dev/null; then
    echo "✅ ASM3 is responding on http://localhost:8090"
else
    echo "❌ ASM3 is not responding. Check logs with: docker compose logs asm3"
    exit 1
fi

# Check volume mounts
echo "📁 Checking volume mounts..."
if docker compose exec asm3 test -f /app/src/static/pages/form_submitted.html; then
    echo "✅ Static files are mounted correctly"
else
    echo "❌ Static files not found in container"
    exit 1
fi

# Test live file updates
echo "🔄 Testing live file updates..."
TIMESTAMP=$(date)
TEST_FILE="src/static/pages/test_live_update.html"

# Create a test file
cat > "$TEST_FILE" <<EOF
<!DOCTYPE html>
<html>
<head><title>Live Update Test</title></head>
<body>
    <h1>Live Update Test</h1>
    <p>Created at: $TIMESTAMP</p>
    <p>If you can see this, live updates are working! 🎉</p>
</body>
</html>
EOF

echo "📝 Created test file: $TEST_FILE"

# Check if file appears in container immediately
sleep 2
if docker compose exec asm3 test -f /app/$TEST_FILE; then
    echo "✅ Live file mounting is working!"
    
    # Test access via web
    if curl -f -s http://localhost:8090/static/pages/test_live_update.html | grep -q "$TIMESTAMP"; then
        echo "✅ File is accessible via web server"
    else
        echo "⚠️  File mounted but not accessible via web (this might be normal)"
    fi
else
    echo "❌ Live file mounting is not working"
    exit 1
fi

# Clean up test file
rm -f "$TEST_FILE"

echo ""
echo "🎉 Live Development Setup is working!"
echo ""
echo "📋 Next steps:"
echo "   1. Edit files in src/ directory"
echo "   2. Changes appear immediately in the container"
echo "   3. Refresh browser to see updates"
echo ""
echo "🦔 For hedgehog forms:"
echo "   - Edit: src/static/pages/form_submitted.html"
echo "   - Add forms to: src/media/templates/"
echo "   - Access at: http://localhost:8090/static/pages/..."
echo ""
echo "🔧 Useful commands:"
echo "   docker compose logs asm3              # View logs"
echo "   docker compose restart asm3          # Restart if needed"
echo "   docker compose exec asm3 bash        # Shell into container"