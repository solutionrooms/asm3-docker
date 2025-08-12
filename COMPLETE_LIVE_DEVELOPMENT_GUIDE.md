# 🎯 Complete Live Development Guide - No Rebuilds Required!

## 🚀 **One-Time Setup**

### **Step 1: Build Development Assets**
```bash
# Run the development build script (only needed once)
./build_dev_assets.sh
```

This generates:
- ✅ JavaScript bundles (`rollup.min.js`, `rollup_compat.min.js`)
- ✅ Database schema (`schema.js`)  
- ✅ Version file (`__version__.py`)

### **Step 2: Start Live Development**
```bash
# Start with live file mounting
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d

# Or use the updated main compose file:
docker compose up -d
```

## ✨ **Live Development Features**

### **✅ Instant Updates (No Restart):**
- **Static files** (`src/static/`) - HTML, CSS, JS
- **Form templates** (`src/media/templates/`)
- **Media files** (`src/media/`)
- **Configuration pages** (`src/static/pages/`)

### **🔄 Quick Restart (Much Faster Than Rebuild):**
- **Python code** (`src/asm3/*.py`) - `docker compose restart asm3`
- **Service endpoints** (`src/asm3/service.py`)
- **Form processing** (`src/asm3/onlineform.py`)

## 🦔 **Hedgehog Form Development Workflow**

### **1. Edit Forms Instantly:**
```bash
# Edit the form submission page - changes appear immediately
vim src/static/pages/form_submitted.html

# Edit JavaScript for forms - immediate updates
vim src/static/js/onlineform_extra.js

# Add new form templates - instantly available
cp hedgehog_care_standalone.html src/media/templates/
```

### **2. Test Immediately:**
```bash
# Open browser - no cache clear needed:
http://localhost:8090/static/pages/form_submitted.html
http://localhost:8090/login?target=main

# Changes appear instantly!
```

### **3. Add Hedgehog Forms:**
```bash
# Copy our hedgehog forms
cp hedgehog_care_standalone.html src/media/templates/
cp simple_hedgehog_form.html src/static/pages/

# Access immediately:
http://localhost:8090/static/pages/simple_hedgehog_form.html?hedgehog=Spike
http://localhost:8090/media/templates/hedgehog_care_standalone.html?hedgehog=Luna
```

## 🔧 **Development Workflow**

### **Daily Development:**
```bash
# Start development environment (once per day)
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d

# Edit files in src/ - changes are immediate
vim src/static/pages/form_submitted.html
vim src/static/js/onlineform_extra.js
vim src/media/templates/hedgehog_care_form.html

# Refresh browser - see changes instantly!
```

### **For Python Changes:**
```bash
# Edit Python files
vim src/asm3/onlineform.py
vim src/asm3/service.py

# Restart container (much faster than rebuild)
docker compose restart asm3

# Check logs if needed
docker compose logs asm3 --tail 20
```

## 📊 **Performance Comparison**

| Task | Before (Rebuild) | After (Live Mount) |
|------|------------------|-------------------|
| Edit HTML/CSS | 2-5 minutes | 0 seconds |
| Edit JavaScript | 2-5 minutes | 0 seconds |
| Edit Templates | 2-5 minutes | 0 seconds |
| Edit Python | 2-5 minutes | 30 seconds |

## 🔍 **Testing Your Changes**

### **Browser Testing:**
```bash
# Main ASM3 application
http://localhost:8090/login?target=main

# Static files
http://localhost:8090/static/pages/form_submitted.html

# Form templates
http://localhost:8090/media/templates/hedgehog_care_form.html

# API endpoints
http://localhost:8090/service?method=online_form_html&formid=1
```

### **Command Line Testing:**
```bash
# Test static file updates
curl http://localhost:8090/static/pages/form_submitted.html

# Test API availability
curl http://localhost:8090/service?method=online_form_html

# Check JavaScript bundles
curl http://localhost:8090/static/js/bundle/rollup.min.js | wc -c
```

## 🚨 **Troubleshooting**

### **JavaScript Errors in Browser:**
✅ **Fixed!** The bundles are now generated correctly.

### **Container Won't Start:**
```bash
# Check logs
docker compose logs asm3

# Common fixes:
docker compose restart asm3
./build_dev_assets.sh  # Regenerate assets
```

### **Changes Not Appearing:**
```bash
# Verify volume mounts
docker compose exec asm3 ls -la /app/src/static/pages/

# Force browser refresh
Ctrl+F5 (or Cmd+Shift+R on Mac)

# Check file exists locally
ls -la src/static/pages/form_submitted.html
```

### **Python Import Errors:**
```bash
# Regenerate __version__.py
./build_dev_assets.sh

# Restart container
docker compose restart asm3
```

## 📁 **File Organization for Hedgehog Forms**

```
src/
├── static/
│   ├── pages/
│   │   ├── form_submitted.html          # ✅ Edit directly (instant)
│   │   └── simple_hedgehog_form.html    # ✅ Add standalone forms
│   ├── js/
│   │   ├── onlineform_extra.js          # ✅ Form behavior (instant)
│   │   └── bundle/
│   │       ├── rollup.min.js            # ✅ Generated bundles
│   │       ├── rollup_compat.min.js     # ✅ Generated bundles
│   │       └── schema.js                # ✅ Generated schema
│   └── css/
│       └── asm.css                      # ✅ Styles (instant)
├── media/
│   └── templates/
│       ├── hedgehog_care_form.html      # ✅ ASM3 integrated forms
│       └── weight_update_form.html      # ✅ Existing templates
└── asm3/
    ├── onlineform.py                    # 🔄 Form processing (restart)
    ├── service.py                       # 🔄 API endpoints (restart)
    └── __version__.py                   # ✅ Generated version file
```

## 🎯 **Benefits Achieved**

- ✅ **No Docker rebuilds** for file changes
- ✅ **Instant feedback** during development  
- ✅ **Fast iteration** on hedgehog forms
- ✅ **Live debugging** capabilities
- ✅ **Multiple developers** can work simultaneously
- ✅ **Easy experimentation** with UI changes

## 🔄 **Maintenance**

### **Regenerate Assets (If Needed):**
```bash
# If JavaScript bundles get corrupted
./build_dev_assets.sh

# If you pull new code that changes JS structure
./build_dev_assets.sh && docker compose restart asm3
```

### **Update Dependencies:**
```bash
# If package.json changes
npm install
make rollup

# Restart containers
docker compose restart asm3
```

## 🎉 **You're Ready!**

The live development environment is now **fully functional**:

1. ✅ **All JavaScript errors resolved**
2. ✅ **Live file mounting working**  
3. ✅ **ASM3 login page loads correctly**
4. ✅ **Form development ready**
5. ✅ **No rebuild workflow established**

**Start developing your hedgehog care forms with instant feedback!** 🦔⚡