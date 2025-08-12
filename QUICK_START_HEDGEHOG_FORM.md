# 🦔 Quick Start: Hedgehog Care Form

## 🚀 **Immediate Use Options**

### **Option 1: Simple Demo Form (Works Right Now)**

I've created `simple_hedgehog_form.html` that you can use immediately:

1. **Open the file** in a web browser
2. **Add hedgehog name to URL**: `simple_hedgehog_form.html?hedgehog=Spike`
3. **Test the form** - it collects all the data but doesn't save to ASM3 yet

**Test URLs:**
- `simple_hedgehog_form.html?hedgehog=Spike`
- `simple_hedgehog_form.html?animal=Luna`
- `simple_hedgehog_form.html?name=Hazel`

### **Option 2: Full ASM3 Integration (Production Ready)**

For the complete solution that actually saves data to ASM3:

## 📋 **Step-by-Step ASM3 Setup**

### **1. Create Online Form in ASM3**

1. **Log into ASM3** → **Settings** → **Online Forms**
2. **Click "New"**
3. **Fill in form details**:
   - **Name**: `hedgehog_care`
   - **Description**: `Hedgehog Daily Care Form`
   - **Auto-processing**: `Attach to animal by name`

### **2. Add Form Fields**

Click **"Form Fields"** and add these fields in order:

| Field Name | Type | Label | Required |
|------------|------|-------|----------|
| `animalname` | Text | Hedgehog | Yes |
| `weight` | Number | Weight (grams) | Yes |
| `caretime` | Date | Date & Time | No |
| `careimage` | Image | Photo | Yes |
| `volunteer` | Text | Your Name | No |
| `carenotes` | Text | Notes | No |

### **3. Get Your Form URL**

After creating the form, ASM3 will give you a form ID. Your URL will be:
```
https://asm.fridaydigital.co.uk/service?method=online_form_html&formid=YOUR_ID
```

### **4. Add Hedgehog Parameter**

Add the hedgehog name to any URL:
```
https://asm.fridaydigital.co.uk/service?method=online_form_html&formid=123&hedgehog=Spike
```

## 📱 **Creating Mobile Links**

### **For Each Hedgehog:**

1. **List your hedgehogs** in ASM3
2. **Create individual URLs**:
   ```
   https://your-asm3-domain/service?method=online_form_html&formid=123&hedgehog=Spike
   https://your-asm3-domain/service?method=online_form_html&formid=123&hedgehog=Luna
   https://your-asm3-domain/service?method=online_form_html&formid=123&hedgehog=Hazel
   ```

3. **Share with volunteers** or create QR codes

### **Mobile Bookmarks:**

Volunteers can:
1. **Open their hedgehog's URL** on their phone
2. **Add to Home Screen** (creates app-like icon)
3. **Tap icon** for instant access to that hedgehog's form

## 🔧 **Which Approach to Use?**

### **Use Simple Form If:**
- You want to test the concept first
- You need something working immediately
- You're evaluating the workflow

### **Use Full ASM3 Integration If:**
- You want data automatically saved to animal records
- You need weight tracking and photo storage
- You want production-ready solution

## 🎯 **URL Parameter Examples**

Both forms support these URL formats:

```bash
# Using 'hedgehog' parameter (recommended)
?hedgehog=Spike

# Using 'animal' parameter  
?animal=Luna

# Using 'name' parameter
?name=Hazel

# Handling spaces in names
?hedgehog=Rosie%20Mae

# Multiple parameters (hedgehog takes priority)
?hedgehog=Spike&volunteer=Sarah
```

## 🚨 **Important Notes**

1. **URL Parameter Required**: Both forms **require** a hedgehog name in the URL
2. **Case Sensitive**: Hedgehog names must match exactly as they appear in ASM3
3. **Mobile Optimized**: Both forms work well on phones and tablets
4. **Photo Capture**: Uses device camera on mobile browsers

## 🔄 **Next Steps**

1. **Try the simple form** first to test the workflow
2. **Set up ASM3 integration** when ready for production
3. **Create individual URLs** for each hedgehog
4. **Train volunteers** on using their specific URLs/bookmarks

The simple form shows exactly how it will work, then the ASM3 integration makes it save data automatically! 🦔