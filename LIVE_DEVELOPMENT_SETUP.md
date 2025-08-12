# 🔥 Live Development Setup - No More Rebuilds!

This setup lets you make changes to ASM3 files and see them **immediately** without Docker rebuilds.

## 🚀 **Quick Start**

### **Option 1: Use Development Override (Recommended)**
```bash
# Start with live file mounting
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d

# Your changes are now live! No rebuilds needed.
```

### **Option 2: Use Modified docker-compose.yml**
```bash
# The main docker-compose.yml now includes volume mounts
docker compose up -d

# Changes to these directories are immediately reflected:
# - src/
# - src/static/
# - src/media/
```

## 📁 **What Gets Live-Mounted**

### **✅ These changes are immediate:**
- **Python code** (`src/asm3/*.py`) - may need container restart for some changes
- **Static files** (`src/static/`) - immediate
- **HTML templates** (`src/media/templates/`) - immediate
- **CSS/JS files** (`src/static/css/`, `src/static/js/`) - immediate  
- **Form templates** (`src/media/templates/`) - immediate
- **Localization files** (`src/asm3/locales/`) - immediate

### **🔄 These may need restart:**
- **Configuration changes** - restart container
- **Major Python module changes** - restart container
- **Database schema changes** - run migrations

## 🦔 **Hedgehog Form Development**

### **Add your hedgehog form:**
```bash
# 1. Add the form file (immediate)
cp hedgehog_care_standalone.html src/media/templates/

# 2. Access immediately at:
# http://localhost:8090/static/pages/hedgehog_care_standalone.html?hedgehog=Spike

# 3. Make changes to the file - they appear instantly!
```

### **Update form_submitted.html:**
```bash
# Updates are immediate - no rebuild needed
vim src/static/pages/form_submitted.html

# Changes visible immediately at:
# http://localhost:8090/static/pages/form_submitted.html
```

## 🔧 **Development Workflow**

### **1. Start Development Environment:**
```bash
# Start with live mounting
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d

# Check it's running
docker compose ps
```

### **2. Make Changes:**
```bash
# Edit any file in src/
vim src/static/pages/form_submitted.html
vim src/media/templates/hedgehog_care_form.html
vim src/asm3/onlineform.py

# Changes are immediately available!
```

### **3. Test Changes:**
```bash
# No rebuild needed - just refresh browser
curl http://localhost:8090/static/pages/form_submitted.html

# Or open in browser:
open http://localhost:8090/static/pages/form_submitted.html
```

### **4. Restart Container (if needed):**
```bash
# Only needed for major Python changes
docker compose restart asm3

# Much faster than full rebuild!
```

## 📊 **What's Different**

### **❌ Before (slow):**
```bash
# Make change
vim src/static/pages/form.html

# Rebuild container (slow!)
docker compose build asm3

# Restart services  
docker compose up -d

# Total time: 2-5 minutes
```

### **✅ After (instant):**
```bash
# Make change
vim src/static/pages/form.html

# Refresh browser - change is live!
# Total time: 0 seconds
```

## 🗂️ **File Location Guide**

```
src/
├── static/
│   ├── pages/
│   │   ├── form_submitted.html          # ← Edit this directly
│   │   └── hedgehog_care_standalone.html # ← Add hedgehog form here
│   ├── js/
│   │   └── onlineform_extra.js          # ← Form JavaScript  
│   └── css/
│       └── asm.css                      # ← Styles
├── media/
│   └── templates/
│       ├── hedgehog_care_form.html      # ← ASM3 integrated form
│       └── weight_update_form.html      # ← Existing weight form
└── asm3/
    ├── onlineform.py                    # ← Form processing logic
    └── service.py                       # ← API endpoints
```

## 🔍 **Testing Your Changes**

### **Static Files:**
```bash
# Direct access to static files
http://localhost:8090/static/pages/form_submitted.html
http://localhost:8090/static/js/onlineform_extra.js
http://localhost:8090/static/css/asm.css
```

### **Templates via ASM3:**
```bash
# Access through ASM3 service
http://localhost:8090/service?method=online_form_html&formid=1
```

### **API Endpoints:**
```bash
# Test API changes
curl http://localhost:8090/service?method=online_form_html&formid=1
```

## 🚨 **Troubleshooting**

### **Changes not appearing:**
```bash
# Check volume mounts
docker compose exec asm3 ls -la /app/src/static/pages/

# Verify file permissions  
ls -la src/static/pages/form_submitted.html

# Force refresh browser (Ctrl+F5)
```

### **Python changes not working:**
```bash
# Restart container for Python module changes
docker compose restart asm3

# Check logs
docker compose logs asm3
```

### **Container won't start:**
```bash
# Check for syntax errors
docker compose logs asm3

# Verify volume paths exist
ls -la src/
```

## 🎯 **Benefits**

- ✅ **Instant feedback** - see changes immediately
- ✅ **Faster development** - no build wait times  
- ✅ **Live debugging** - modify files while testing
- ✅ **Multiple developers** - everyone sees changes instantly
- ✅ **Easy experimentation** - quick iterations

## 🔄 **Migration from Old Setup**

### **If you have existing containers:**
```bash
# Stop current containers
docker compose down

# Start with new live mounting
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d

# Your changes are now live!
```

### **No data loss:**
- Database data is preserved (uses volumes)
- Media files are preserved  
- Only the container file mounting changes

Now you can develop the hedgehog forms with **instant feedback**! 🦔⚡