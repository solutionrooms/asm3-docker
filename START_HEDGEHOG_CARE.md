# 🚀 Start Hedgehog Care System (No Rebuild Required!)

This is a **complete standalone solution** that works immediately without needing to rebuild ASM3 or modify any existing systems.

## ⚡ **Quick Start (30 seconds)**

### **Step 1: Start the Server**
```bash
# In your ASM3 directory:
python3 hedgehog_data_server.py
```

You'll see:
```
🦔 Starting Hedgehog Care Data Server...
📁 Data will be saved to: /path/to/hedgehog_care_data
🌐 Server starting on http://localhost:8080
```

### **Step 2: Use the Form**

**Open in browser:**
```
http://localhost:8080/hedgehog_care_standalone.html?hedgehog=Spike
```

**Or use the URL generator** (if you forget the hedgehog name):
```
http://localhost:8080/hedgehog_care_standalone.html
```

## 📱 **Creating Mobile Links**

### **For Each Hedgehog:**

1. **Replace "Spike" with actual hedgehog names:**
   ```
   http://localhost:8080/hedgehog_care_standalone.html?hedgehog=Spike
   http://localhost:8080/hedgehog_care_standalone.html?hedgehog=Luna
   http://localhost:8080/hedgehog_care_standalone.html?hedgehog=Hazel
   ```

2. **Share these URLs** with volunteers via:
   - Text message
   - Email
   - QR codes
   - WhatsApp

3. **Volunteers bookmark on phones:**
   - Open URL on phone
   - Add to Home Screen
   - Gets app-like icon

## 📊 **Viewing Collected Data**

### **All Care Records:**
```
http://localhost:8080/api/care_records
```

### **Specific Hedgehog:**
```
http://localhost:8080/api/hedgehog/Spike
```

### **Data Files:**
All data is saved to `hedgehog_care_data/` folder as JSON files:
```
hedgehog_care_data/
├── care_Spike_20241201_143022.json
├── care_Luna_20241201_151234.json
└── care_Hazel_20241201_162045.json
```

## 🌐 **Making It Accessible to Volunteers**

### **Option 1: Local Network (Same WiFi)**
```bash
# Find your local IP address
# On Mac/Linux:
ifconfig | grep "inet " | grep -v 127.0.0.1

# Share URLs like:
http://192.168.1.100:8080/hedgehog_care_standalone.html?hedgehog=Spike
```

### **Option 2: Internet Access (Advanced)**
```bash
# Using ngrok (install from ngrok.com):
ngrok http 8080

# You'll get a public URL like:
https://abc123.ngrok.io/hedgehog_care_standalone.html?hedgehog=Spike
```

### **Option 3: Copy to Web Server**
Copy `hedgehog_care_standalone.html` to any web server and use URL parameters.

## 🔧 **Features**

### **✅ What Works Right Now:**
- ✅ Mobile-optimized form
- ✅ Camera integration for photos
- ✅ Weight tracking in grams
- ✅ Date/time recording
- ✅ Volunteer name tracking
- ✅ Notes collection
- ✅ Data export (JSON format)
- ✅ Per-hedgehog URL links
- ✅ No rebuild required
- ✅ Works offline (after initial load)

### **📋 What Gets Collected:**
```json
{
  "hedgehog": "Spike",
  "weight": "450",
  "date": "2024-12-01T14:30:00",
  "volunteer": "Sarah",
  "notes": "Very active today, ate well",
  "photo": "IMG_1234.jpg",
  "timestamp": "2024-12-01T14:30:22.123Z",
  "server_timestamp": "2024-12-01T14:30:22",
  "submission_id": "20241201_143022"
}
```

## 🔄 **Integration with ASM3 (Optional)**

Later, you can:

1. **Import the JSON data** into ASM3 using scripts
2. **Add weight data** to animal records  
3. **Upload photos** to media galleries
4. **Create log entries** for care activities

## 🛠️ **Customization**

### **Add More Hedgehogs:**
Just use different names in URLs - no configuration needed:
```
?hedgehog=Sonic
?hedgehog=Prickles
?hedgehog=Rosie%20Mae  (for names with spaces)
```

### **Change Server Port:**
```bash
# Edit hedgehog_data_server.py, change:
PORT = 8080  # to whatever you want
```

### **Customize Form:**
Edit `hedgehog_care_standalone.html` - changes take effect immediately (no restart needed).

## ⚠️ **Important Notes**

1. **Data Security**: Data is stored locally in JSON files
2. **Backup**: Copy `hedgehog_care_data/` folder to backup data  
3. **Access**: Only accessible while server is running
4. **Photos**: Photo filenames are recorded, actual photos need separate handling

## 🎯 **Why This Approach?**

### **✅ Advantages:**
- **No rebuilds** - works immediately
- **No ASM3 modifications** - runs alongside  
- **Mobile-friendly** - designed for phones
- **Simple URLs** - easy to share
- **Lightweight** - minimal requirements
- **Flexible** - easy to customize

### **🔄 Migration Path:**
1. **Start with this** for immediate use
2. **Collect data** and test workflow
3. **Later integrate** with ASM3 if desired
4. **Import historical data** from JSON files

## 🆘 **Troubleshooting**

### **Server won't start:**
```bash
# Check if port is in use:
lsof -i :8080

# Use different port:
# Edit PORT = 8080 in hedgehog_data_server.py
```

### **Form doesn't load:**
```bash
# Make sure you're in the right directory:
ls hedgehog_care_standalone.html

# Check server output for errors
```

### **Data not saving:**
```bash
# Check permissions:
ls -la hedgehog_care_data/

# Check server logs for error messages
```

This solution gives you **immediate hedgehog care tracking** without waiting for ASM3 rebuilds or complex integrations! 🦔