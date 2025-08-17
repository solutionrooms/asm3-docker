# 🎯 Complete Live Development Guide - No Rebuilds Required!

## 🔥 **QUICK START: JavaScript Development**

**🎯 FASTEST WORKFLOW - Development Mode:**
```bash
# 1. Enable development mode (one-time)
./dev-js.sh dev

# 2. Edit JavaScript files
vim src/static/js/animal_weight_log.js

# 3. Refresh browser - changes appear INSTANTLY!
# Ctrl+F5 (or Cmd+Shift+R on Mac)

# 4. When done, switch back:
./dev-js.sh prod
```

**✅ Your Weight Log version should now appear in browser console!**

---

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
- **Service endpoints** (`src/asm3/service.py`, `src/main.py`)
- **Form processing** (`src/asm3/onlineform.py`)
- **JavaScript modules** (`src/static/js/*.js`) - restart picks up changes
- **Email templates** - create via ASM3 interface or restart after file changes

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
docker compose up -d

# Edit files in src/ - changes are immediate
vim src/static/pages/form_submitted.html
vim src/static/js/onlineform_extra.js
vim src/media/templates/hedgehog_care_form.html

# Refresh browser - see changes instantly!
```

### **🎯 JavaScript Development - SIMPLE WORKFLOW:**

#### **Option 1: Development Mode (Recommended)**
```bash
# Enable development mode (one-time setup)
./dev-js.sh dev

# Edit JavaScript files - changes appear INSTANTLY!
vim src/static/js/animal_weight_log.js
vim src/static/js/animal.js

# Just refresh browser - NO BUILD NEEDED!
# Ctrl+F5 (or Cmd+Shift+R)

# When done developing, switch back to production mode:
./dev-js.sh prod
```

#### **Option 2: Production Mode (Build After Changes)**
```bash
# Edit JavaScript files
vim src/static/js/animal_weight_log.js

# Rebuild bundle (takes ~10 seconds)
./dev-js.sh build

# Refresh browser to see changes
# Ctrl+F5 (or Cmd+Shift+R)
```

#### **Manual Commands (if script not available):**
```bash
# Enable development mode manually:
sed -i 's/rollup_js = true/rollup_js = false/' asm3.conf
docker compose restart asm3

# Or rebuild bundle manually:
docker compose exec asm3 sh -c "cd /app && npm install && make rollup"
```

### **For Python Changes:**
```bash
# Edit Python files
vim src/asm3/onlineform.py
vim src/asm3/service.py
vim src/main.py

# Restart container (much faster than rebuild)
docker compose restart asm3

# Check logs if needed
docker compose logs asm3 --tail 20 -f
```

### **For Email Templates:**
```bash
# Create/edit templates in ASM3 interface:
# Settings > Publishing > Document Templates
# Set "Show" field to "Emails" for email dropdowns

# Or edit template files:
vim src/media/templates/receipt_email.html
docker compose restart asm3
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

### **404 Errors on Endpoints:**
```bash
# Check if animal exists
curl http://localhost:8090/animal?id=2

# Test endpoint directly
curl http://localhost:8090/animal_weight_log?id=2

# Check permissions and login status
http://localhost:8090/login
```

### **JavaScript Module Issues (Weight Log, etc.):**
```bash
# Check browser console for errors
# F12 -> Console tab

# Clear browser cache completely
Ctrl+F5 (or Cmd+Shift+R on Mac)

# Check if files are loading
# F12 -> Network tab -> refresh page

# Restart to reload JavaScript bundles
docker compose restart asm3
```

### **Page Content Disappears:**
```bash
# This usually indicates JavaScript errors
# Check browser console for errors
# Common fixes:

# 1. Clear browser cache
Ctrl+F5

# 2. Check for JavaScript syntax errors
docker compose logs asm3 | grep -i error

# 3. Restart ASM3
docker compose restart asm3
```

### **Email Templates Not Showing:**
```bash
# Templates must have "Show" field set to "Emails"
# In ASM3: Document Templates -> Select template -> Show button
# Set to "Emails" for email dropdown appearance

# Check template exists
ls -la src/media/templates/
```

### **Container Won't Start:**
```bash
# Check logs
docker compose logs asm3

# Common fixes:
docker compose restart asm3
./build_dev_assets.sh  # Regenerate assets

# Nuclear option - rebuild everything
docker compose down -v
docker compose up --build -d
```

### **Changes Not Appearing:**
```bash
# Verify volume mounts
docker compose exec asm3 ls -la /app/src/static/pages/

# Force browser refresh
Ctrl+F5 (or Cmd+Shift+R on Mac)

# Check file exists locally
ls -la src/static/pages/form_submitted.html

# For JavaScript changes, restart:
docker compose restart asm3
```

### **Python Import Errors:**
```bash
# Regenerate __version__.py
./build_dev_assets.sh

# Restart container
docker compose restart asm3

# Check Python path
docker compose exec asm3 python3 -c "import asm3; print('OK')"
```

### **Database Issues:**
```bash
# Check database connectivity
docker compose exec asm3 python3 -c "import asm3.db; print('DB OK')"

# Visit database setup page
http://localhost:8090/database

# Reset database (WARNING: loses data)
docker compose down -v
docker compose up -d
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
# Install npm dependencies in container
docker compose exec asm3 npm install

# Check what make targets are available
docker compose exec asm3 make

# Run available targets
docker compose exec asm3 make compile  # Code quality checks
docker compose exec asm3 make test     # Start dev server (port 5000)

# Restart containers
docker compose restart asm3
```

### **Debugging JavaScript Issues:**
```bash
# Check if JavaScript files are loading
curl http://localhost:8090/static/js/animal_weight_log.js

# Check bundled JavaScript
curl http://localhost:8090/static/js/bundle/rollup.min.js | head

# Test specific endpoints
curl "http://localhost:8090/animal_weight_log?id=2&json=true"

# Check browser console:
# F12 -> Console -> Look for errors
# F12 -> Network -> Check failed requests
```

## 🎉 **You're Ready!**

The live development environment is now **fully functional**:

1. ✅ **All JavaScript errors resolved**
2. ✅ **Live file mounting working**  
3. ✅ **ASM3 login page loads correctly**
4. ✅ **Form development ready**
5. ✅ **No rebuild workflow established**
6. ✅ **Weight Log fixes applied**
7. ✅ **Email template system working**

## 🐛 **Common Development Tasks**

### **Fix JavaScript Module Issues:**
1. Edit the JavaScript file: `vim src/static/js/animal_weight_log.js`
2. Add error handling: `try { ... } catch(err) { console.error(...) }`
3. Restart ASM3: `docker compose restart asm3`
4. Clear browser cache: `Ctrl+F5`
5. Test functionality

### **Create Email Templates:**
1. Go to Settings > Publishing > Document Templates
2. Create new template or upload HTML file
3. Set "Show" field to "Emails"
4. Template appears in email dropdown
5. Use tokens like `{ANIMALNAME}` for dynamic content

### **Debug 404 Errors:**
1. Check endpoint exists: `grep -r "class animal_weight_log" src/`
2. Test direct URL: `curl http://localhost:8090/animal_weight_log?id=2`
3. Check permissions and login status
4. Restart if needed: `docker compose restart asm3`

### **Add Read-Only Form Fields:**
1. Edit form generation code: `src/asm3/onlineform.py`
2. Add readonly logic for specific fields
3. Restart: `docker compose restart asm3`
4. Test form behavior

**Start developing your hedgehog care forms with instant feedback!** 🦔⚡