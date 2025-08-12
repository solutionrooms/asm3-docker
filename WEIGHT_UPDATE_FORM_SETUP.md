# Animal Weight Update Form Setup Guide

This guide explains how to set up a web form that allows staff to update animal weights, with automatic weight change logging.

## 🎯 What This Achieves

- **Web Form**: Easy-to-use form for recording animal weights
- **Auto-Processing**: Automatically updates animal records when form is submitted
- **Weight History**: All weight changes are logged and tracked over time
- **Reports**: Access existing weight history and weight loss reports

## 📁 Files Created

1. **`/src/media/templates/weight_update_form.html`** - The weight update form template

## 🔧 Setup Instructions

### Step 1: Create the Online Form in ASM3

1. **Log into ASM3** with admin privileges
2. **Go to Settings → Online Forms**
3. **Click "New"** to create a new form
4. **Configure the form**:
   - **Name**: `weight_update`
   - **Description**: `Animal Weight Update Form`
   - **Auto-processing**: `Attach to animal by name` (option 1)
   - **Redirect URL After Submission**: `/static/pages/form_submitted.html`

### Step 2: Add Form Fields

Add the following fields in order:

#### Field 1: Animal Selection
- **Field Name**: `animalname`
- **Field Type**: `Shelter Animal` (Type 4)
- **Label**: `Select Animal`
- **Mandatory**: Yes
- **Display Index**: 1

#### Field 2: Weight Input
- **Field Name**: `weight`
- **Field Type**: `Number` (Type 20)
- **Label**: `Current Weight`
- **Mandatory**: Yes
- **Display Index**: 2

#### Field 3: Date of Weighing
- **Field Name**: `weighdate`
- **Field Type**: `Date` (Type 10)
- **Label**: `Date of Weighing`
- **Mandatory**: No
- **Display Index**: 3

#### Field 4: Recorded By
- **Field Name**: `recordedby`
- **Field Type**: `Text` (Type 1)
- **Label**: `Recorded By`
- **Mandatory**: No
- **Display Index**: 4

#### Field 5: Notes
- **Field Name**: `weighnotes`
- **Field Type**: `Long Text` (Type 2)
- **Label**: `Notes`
- **Mandatory**: No
- **Display Index**: 5

### Step 3: Configure Weight Change Logging

1. **Go to Settings → Options**
2. **Search for "weight"**
3. **Ensure these settings**:
   - `WeightChangeLog`: **Yes** (enabled)
   - `WeightChangeLogType`: **4** (Weight log type)
   - `show_weight_units_in_log`: **Yes** (optional, shows kg/lb in logs)

### Step 4: Access the Form

The form will be available at:
```
https://asm.fridaydigital.co.uk/onlineform/{form_id}/weight_update
```

Or use the generic form URL:
```
https://asm.fridaydigital.co.uk/onlineform/weight_update
```

### Step 5: Test the Form

1. **Submit a test weight** for an animal
2. **Check Results**:
   - Go to the animal record
   - Verify the weight field is updated
   - Check the animal's log for weight change entry
   - Run **Reports → Weight History** to see the logged weight

## 📊 Viewing Weight History

After submitting weight updates, you can view the history via:

### Built-in Reports
- **Reports → Weight History** - Individual animal weight over time
- **Reports → Weight History (Shelter Animals)** - All animals' weight history
- **Reports → Weight Chart** - Visual graph of weight changes
- **Reports → Weight Loss** - Identifies animals losing weight

### Animal Log
- Go to any animal record
- Click the **Log** tab
- Weight changes appear with Log Type "Weight"

## 🔒 Permissions Required

Users need these permissions to:
- **Submit forms**: No special permissions (public access possible)
- **Manage forms**: `VIEW_ONLINE_FORMS`, `CHANGE_ONLINE_FORMS`
- **Process submissions**: `VIEW_INCOMING_FORMS`, `ADD_MEDIA`

## ⚙️ Advanced Configuration

### Custom Form HTML
If you want to customize the form appearance, you can:
1. Edit `/src/media/templates/weight_update_form.html`
2. Update the `{DATABASE_ALIAS}` placeholder with your database name
3. Customize styling, add validation, etc.

### Manual Processing
If you prefer manual processing instead of auto-processing:
1. Set form auto-processing to "No auto-processing"
2. Staff process submissions via **Reports → View Incoming Forms**
3. Manually attach to animals and update weights

### Integration Options
The form can be:
- **Embedded** in your website using iframes
- **Linked** from your website
- **Used internally** by staff on tablets/phones
- **Customized** with your organization's branding

## 🐾 Weight Tracking Benefits

This system provides:
- **Complete audit trail** of all weight changes
- **Historical tracking** for health monitoring
- **Weight loss alerts** via built-in reports
- **Integration** with medical records and treatments
- **Automatic logging** with timestamps and user tracking

## 🚀 Next Steps

After setup, consider:
1. **Training staff** on the new form
2. **Setting up regular** weighing schedules
3. **Running weight reports** weekly/monthly
4. **Integrating with medical records** for health tracking
5. **Setting up alerts** for significant weight changes

The weight update form integrates seamlessly with ASM3's existing weight tracking and logging system, providing a professional solution for monitoring animal health over time.