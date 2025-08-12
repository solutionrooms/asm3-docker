# Hedgehog Daily Care Form Setup Guide

This guide explains how to set up a mobile-friendly form for hedgehog volunteers to record daily weights and upload photos. The hedgehog name comes from the URL parameter, making it easy to create individual links for each hedgehog.

## 🎯 What This Achieves

- **Mobile-Optimized Form**: Easy-to-use form designed for phones and tablets
- **URL-Based Animal Selection**: Hedgehog name comes from URL parameter (no dropdown needed)
- **Daily Photos**: Upload photos with automatic resizing and storage
- **Weight Tracking**: Record weights in grams with automatic conversion
- **Auto-Processing**: Automatically updates hedgehog records when form is submitted
- **Volunteer Tracking**: Records who performed the care

## 📁 Files Created

1. **`/src/media/templates/hedgehog_care_form.html`** - The hedgehog care form template

## 🔧 Setup Instructions

### Step 1: Create the Online Form in ASM3

1. **Log into ASM3** with admin privileges
2. **Go to Settings → Online Forms**
3. **Click "New"** to create a new form
4. **Configure the form**:
   - **Name**: `hedgehog_care`
   - **Description**: `Hedgehog Daily Care Form`
   - **Auto-processing**: `Attach to animal by name` (option 1)
   - **Redirect URL After Submission**: `/static/pages/form_submitted.html`

### Step 2: Add Form Fields

Add the following fields in order:

#### Field 1: Hedgehog Name (from URL)
- **Field Name**: `animalname`
- **Field Type**: `Text` (Type 1)
- **Label**: `Hedgehog`
- **Mandatory**: Yes
- **Display Index**: 1

#### Field 2: Weight Input (grams)
- **Field Name**: `weight`
- **Field Type**: `Number` (Type 20)
- **Label**: `Current Weight`
- **Mandatory**: Yes
- **Display Index**: 2

#### Field 3: Date and Time of Care
- **Field Name**: `caretime`
- **Field Type**: `Date` (Type 10)
- **Label**: `Date & Time of Care`
- **Mandatory**: No
- **Display Index**: 3

#### Field 4: Daily Photo
- **Field Name**: `careimage`
- **Field Type**: `Image` (Type 17)
- **Label**: `Daily Photo`
- **Mandatory**: Yes
- **Display Index**: 4

#### Field 5: Volunteer Name
- **Field Name**: `volunteer`
- **Field Type**: `Text` (Type 1)
- **Label**: `Your Name`
- **Mandatory**: No
- **Display Index**: 5

#### Field 6: Care Notes
- **Field Name**: `carenotes`
- **Field Type**: `Text` (Type 1)
- **Label**: `Notes`
- **Mandatory**: No
- **Display Index**: 6

### Step 3: Configure Weight Units

1. **Go to Settings → Options**
2. **Search for "weight"**
3. **Set weight units**:
   - If using metric: `WeightDisplayUnits`: **kg**
   - The form will convert grams to kg automatically (divide by 1000)
   - `WeightChangeLog`: **Yes** (enabled for tracking)

### Step 4: Access the Form

The form requires a hedgehog name in the URL. Examples:

**Individual hedgehog URLs:**
```
https://asm.fridaydigital.co.uk/onlineform/hedgehog_care?hedgehog=Spike
https://asm.fridaydigital.co.uk/onlineform/hedgehog_care?animal=Luna
https://asm.fridaydigital.co.uk/onlineform/hedgehog_care?name=Hazel
```

**Alternative parameter names supported:**
- `?hedgehog=NAME` (recommended)
- `?animal=NAME`
- `?name=NAME` 
- `?animalname=NAME`

**Important:** The form will not work without a hedgehog name parameter. It will show an error and disable submission.

### Step 5: Generate URLs for Each Hedgehog

Create individual URLs for each hedgehog in your care:

**Method 1: Manual URL Creation**
1. **List all hedgehogs** in ASM3 (Animals → Find Animals)
2. **Note the exact names** (case-sensitive)
3. **Create URLs** using format: `https://your-domain/onlineform/hedgehog_care?hedgehog=NAME`

**Method 2: Use ASM3 Reports (Advanced)**
Create a custom report to generate URLs automatically:
```sql
SELECT 
    AnimalName,
    'https://asm.fridaydigital.co.uk/onlineform/hedgehog_care?hedgehog=' || 
    REPLACE(AnimalName, ' ', '%20') AS CareFormURL
FROM animal 
WHERE SpeciesID = (SELECT ID FROM species WHERE SpeciesName = 'Hedgehog')
    AND Archived = 0
ORDER BY AnimalName
```

### Step 6: Create Mobile Bookmarks

**For volunteers using phones:**
1. **Open each hedgehog's URL** in your phone's browser
2. **Add to Home Screen** (iOS) or **Add to Home screen** (Android)
3. **Give it a specific name** like "Spike Care" or "Luna Daily"
4. Each hedgehog will have its own app icon for instant access

## 📱 Mobile Features

### Optimized for Touch
- Large, touch-friendly buttons and inputs
- Camera integration for easy photo capture
- Drag and drop photo upload
- Auto-focus on first field
- Current date/time pre-filled

### Photo Handling
- **Camera access**: Direct camera capture on mobile devices
- **Automatic resizing**: Photos are scaled to 640x640 pixels max
- **Format conversion**: All images converted to JPEG
- **Size limit**: Maximum 375KB per image
- **Drag & drop**: Desktop users can drag photos onto upload area

### Weight Input
- **Grams only**: Simple numeric input for hedgehog weights
- **Automatic validation**: Only accepts numbers
- **Range checking**: 0-2000 grams (typical hedgehog range)

## 🔧 Testing the Form

### Test Workflow
1. **Open form** on mobile device
2. **Select a hedgehog** from the dropdown
3. **Enter weight** in grams (e.g., 450)
4. **Take photo** using camera or upload existing image
5. **Fill in volunteer name** and notes
6. **Submit form**

### Verify Results
1. **Check animal record**: Weight should be updated
2. **Check media tab**: Photo should appear in animal's gallery
3. **Check log**: Weight change should be logged
4. **View online forms**: Submission should appear in incoming forms

## 📊 Data Flow

```
Volunteer fills form → ASM3 processes submission → Updates:
├── Animal weight field (converted from grams to system units)
├── Adds photo to animal's media gallery
├── Creates weight change log entry
└── Records submission in online forms log
```

## 🔒 Permissions

### For Volunteers (Form Access)
- No special ASM3 permissions needed
- Can be accessed via public URL
- Consider password protection for security

### For Staff (Form Management)
- `VIEW_ONLINE_FORMS`: View form submissions
- `CHANGE_ONLINE_FORMS`: Modify form settings
- `ADD_MEDIA`: Allow photo attachments
- `VIEW_INCOMING_FORMS`: Process submissions

## 📈 Monitoring & Reports

### Built-in Reports
- **Reports → Online Form Inbox**: View all submissions
- **Reports → Weight History**: Track individual hedgehog weights over time
- **Animal Records → Log tab**: See weight change history
- **Animal Records → Media tab**: View daily photos chronologically

### Custom Reports
You can create custom reports to track:
- Daily care completion rates
- Weight trends per hedgehog
- Photo submission frequency
- Volunteer participation

## 🚀 Advanced Features

### Integration Options
- **Embed in website**: Use iframe to embed in volunteer portal
- **QR Code access**: Generate QR codes for easy mobile access
- **Custom branding**: Modify HTML template with organization colors/logo
- **Automated alerts**: Set up weight change notifications

### Data Export
- Form submissions can be exported to CSV
- Weight data integrates with ASM3's reporting system
- Photos are stored in ASM3's media system

## 🛠️ Troubleshooting

### Common Issues
1. **Photos too large**: Form automatically resizes, but very large images may fail
2. **Camera not working**: Ensure browser has camera permissions
3. **Form not submitting**: Check all required fields are filled
4. **Weight not updating**: Verify auto-processing is enabled

### Mobile Browser Tips
- **iOS Safari**: Works best for camera integration
- **Android Chrome**: Good camera support and drag/drop
- **Older browsers**: May need fallback to file selection only

## 🔄 Maintenance

### Regular Tasks
1. **Monitor submissions**: Check online form inbox daily
2. **Process failures**: Handle any failed auto-processing
3. **Clean up**: Archive old form submissions periodically
4. **Update form**: Adjust fields based on volunteer feedback

### Weight Unit Conversion
If your ASM3 system uses:
- **Kilograms**: Form automatically divides gram input by 1000
- **Pounds**: You may need to modify the form to convert grams to pounds (divide by 453.592)

## 📋 Volunteer Instructions

Create simple instructions for volunteers:

1. **Open the hedgehog care form** (provide bookmark/QR code)
2. **Select the hedgehog** you're caring for
3. **Weigh the hedgehog** and enter weight in grams
4. **Take a photo** of the hedgehog
5. **Add your name** and any notes
6. **Submit the form**

The form is designed to be intuitive and mobile-friendly, requiring minimal training for volunteers.