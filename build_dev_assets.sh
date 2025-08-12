#!/bin/bash

echo "🔧 Building Development Assets for ASM3 Live Development"
echo "========================================================"

# Check if npm dependencies are installed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing npm dependencies..."
    npm install
fi

# Generate JavaScript bundles
echo "🔄 Generating JavaScript bundles..."
make rollup

# Create minimal schema.js if it doesn't exist
if [ ! -f "src/static/js/bundle/schema.js" ]; then
    echo "📋 Creating minimal schema.js..."
    mkdir -p src/static/js/bundle
    cat > src/static/js/bundle/schema.js << 'EOF'
// Minimal schema.js for development
// This provides basic database schema information for ASM3
var SCHEMA = {
    "tables": {
        "animal": {
            "name": "animal",
            "fields": ["ID", "AnimalName", "ShelterCode", "SpeciesID", "AnimalTypeID", "BreedID", "Weight"]
        },
        "onlineform": {
            "name": "onlineform", 
            "fields": ["ID", "Name", "RedirectUrlAfterPOST", "SetOwnerFlags"]
        },
        "onlineformfield": {
            "name": "onlineformfield",
            "fields": ["ID", "OnlineFormID", "FieldName", "FieldType", "Label"]
        },
        "onlineformincoming": {
            "name": "onlineformincoming",
            "fields": ["CollationID", "FormName", "PostedDate", "Host", "Preview"]
        },
        "media": {
            "name": "media",
            "fields": ["ID", "MediaName", "MediaType", "MediaData", "LinkID", "LinkTypeID"]
        }
    },
    "version": "dev"
};

// Make it available globally for ASM3 components
if (typeof window !== "undefined") {
    window.SCHEMA = SCHEMA;
}
EOF
fi

# Ensure __version__.py exists
if [ ! -f "src/asm3/__version__.py" ]; then
    echo "📝 Creating __version__.py..."
    cat > src/asm3/__version__.py << 'EOF'
#!/usr/bin/env python3
VERSION = "50 [Live Development]"
BUILD = "dev"
EOF
fi

echo ""
echo "✅ Development assets built successfully!"
echo ""
echo "📁 Generated files:"
echo "   src/static/js/bundle/rollup.min.js"
echo "   src/static/js/bundle/rollup_compat.min.js" 
echo "   src/static/js/bundle/schema.js"
echo "   src/asm3/__version__.py"
echo ""
echo "🚀 Your live development environment is ready!"
echo "   Start with: docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d"
echo "   Access at:  http://localhost:8090"