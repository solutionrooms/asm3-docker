# 🔧 Troubleshooting Form Access Issues

## 🚨 **The Issue You're Seeing**

You're getting "This site can't be reached" when accessing `static/pages/form_submitted.html` directly. This is **normal** and **expected**.

## ✅ **Why This Happens**

### **1. Static Files Need Web Server**
- ASM3 files must be accessed through the **ASM3 web server**
- Direct file access (`file://` or `static/pages/...`) won't work
- Need proper HTTP server running

### **2. Correct Access Methods**

**❌ WRONG:**
```
static/pages/form_submitted.html
file:///path/to/form_submitted.html
```

**✅ CORRECT:**
```
http://localhost:5000/static/pages/form_submitted.html
https://asm.fridaydigital.co.uk/static/pages/form_submitted.html
```

## 🔧 **Solutions**

### **Option 1: Start ASM3 Development Server**

```bash
# In your ASM3 directory
make test

# Then access via:
# http://localhost:5000/static/pages/form_submitted.html
```

### **Option 2: Test Forms Independently**

Use the standalone files I created:

```bash
# Open these files directly in browser:
simple_hedgehog_form.html?hedgehog=Spike
test_hedgehog_form.html
```

### **Option 3: Production ASM3 Server**

Access through your live ASM3 installation:
```
https://asm.fridaydigital.co.uk/static/pages/form_submitted.html
```

## 🦔 **Testing the Hedgehog Form**

### **Development Testing:**
1. **Start ASM3**: `make test` 
2. **Access form**: `http://localhost:5000/service?method=online_form_html&formid=X&hedgehog=Spike`
3. **After submission**: Automatically redirects to form_submitted.html

### **Standalone Testing:**
1. **Open**: `simple_hedgehog_form.html?hedgehog=Spike`
2. **Fill form**: Enter weight, take photo, add notes
3. **Submit**: Shows demo confirmation (doesn't save to ASM3)

## 🔍 **Debugging Steps**

### **1. Check ASM3 Server Status**
```bash
# Is ASM3 running?
curl http://localhost:5000/
# Should return ASM3 login page HTML
```

### **2. Check Form ID**
```bash
# List online forms in ASM3
# Settings → Online Forms → Check ID number
```

### **3. Check Form URL**
```bash
# Correct format:
https://your-domain/service?method=online_form_html&formid=123&hedgehog=Spike
```

### **4. Check File Permissions**
```bash
# Make sure files are readable
ls -la src/static/pages/form_submitted.html
```

## 📱 **Mobile Testing**

### **For Volunteers:**
1. **Use production URLs** (not localhost)
2. **Test on actual mobile devices**
3. **Check camera permissions**
4. **Verify bookmark creation**

### **Mobile-Specific URLs:**
```
https://asm.fridaydigital.co.uk/service?method=online_form_html&formid=123&hedgehog=Spike
```

## 🔄 **Workflow Summary**

### **Development:**
```
1. Start ASM3 server (make test)
2. Create online form in ASM3 UI
3. Test form via service URL
4. Check form submission processing
```

### **Production:**
```
1. Deploy to production server
2. Create online form in production ASM3
3. Generate individual hedgehog URLs
4. Share with volunteers
```

## 🚀 **Quick Test Commands**

```bash
# Test ASM3 server
curl http://localhost:5000/static/pages/form_submitted.html

# Test standalone form (any browser)
open simple_hedgehog_form.html?hedgehog=TestSpike

# Check ASM3 service endpoint
curl "http://localhost:5000/service?method=online_form_html&formid=1"
```

## 🎯 **Next Steps**

1. **Start ASM3 server** if testing development
2. **Use production URL** if testing live system  
3. **Try standalone form** for immediate testing
4. **Check setup documentation** for complete ASM3 integration

The form submission page is now **much better** and will work properly when accessed through the correct ASM3 URLs! 🦔✅