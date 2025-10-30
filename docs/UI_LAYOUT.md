# Face Swap Tool - New UI Layout

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│                      🎬 Face Swap Tool                                   │
│                Easy Face Swapping with Pause & Resume                   │
│                                                                         │
├────────────────────────────────┬────────────────────────────────────────┤
│                                │                                        │
│  ⚙️ Settings                   │  📋 Output Log                         │
│  ┌──────────────────────────┐  │  ┌──────────────────────────────────┐ │
│  │ 🖥️ CPU                   │  │  │ Welcome to Face Swap Tool!       │ │
│  └──────────────────────────┘  │  │ ✓ Pause/Resume enabled           │ │
│  ┌──────────────────────────┐  │  │ ✓ Crash recovery enabled         │ │
│  │ 📷 Single Image          │  │  │                                  │ │
│  └──────────────────────────┘  │  │ Quick Start:                     │ │
│  ────────────────────────────  │  │ 1. Choose Face                   │ │
│                                │  │ 2. Choose Video                  │ │
│  📁 Input Files                │  │ 3. Split Video Into Frames       │ │
│  ┌──────────────────────────┐  │  │ 4. Swap Face                     │ │
│  │ 👤 Choose Face           │  │  │ 5. Merge Frames Into Video       │ │
│  └──────────────────────────┘  │  │                                  │ │
│  ┌──────────────────────────┐  │  │ Ready to begin!                  │ │
│  │ 🎥 Choose Video          │  │  │                                  │ │
│  └──────────────────────────┘  │  │ ✓ Selected face: myface.jpg      │ │
│  ────────────────────────────  │  │ ✓ Selected video: myvideo.mp4    │ │
│                                │  │ ✂️ Splitting video...            │ │
│  ⚡ Processing                 │  │ ✓ Frame 150/500 (30.0%)          │ │
│  ┌──────────────────────────┐  │  │ ⏸️ Pausing...                    │ │
│  │ ✂️ Split Video           │  │  │ ▶️ Resuming...                   │ │
│  └──────────────────────────┘  │  │ ✓ Finished swapping faces        │ │
│  ┌──────────────────────────┐  │  │ 🎬 Creating video...             │ │
│  │ 🔄 Swap Face             │  │  │ ✓ Finished creating video!       │ │
│  └──────────────────────────┘  │  │ 📁 Saved to: finished_videos/... │ │
│  ┌────────────┬─────────────┐  │  │                                  │ │
│  │⏸️ Pause    │▶️ Resume    │  │  │                                  │ │
│  └────────────┴─────────────┘  │  │                                  │ │
│  ┌──────────────────────────┐  │  │                                  │ │
│  │ 💾 Resume from Crash     │  │  └──────────────────────────────────┘ │
│  └──────────────────────────┘  │                                   ▲    │
│  ┌──────────────────────────┐  │                                   │    │
│  │ 🎬 Merge Frames          │  │                              Scrollbar │
│  └──────────────────────────┘  │                                   │    │
│                                │                                   ▼    │
├────────────────────────────────┴────────────────────────────────────────┤
│ ✓ Ready                                                                 │
└─────────────────────────────────────────────────────────────────────────┘
```

## Color Guide

### Buttons
- **Blue** (#007acc): Primary input actions (Choose Face, Choose Video)
- **Green** (#4ec9b0): Main action (Swap Face)
- **Orange** (#ce9178): Pause button
- **Teal** (#4ec9b0): Resume button
- **Purple** (#5a4a7a): Resume from Crash
- **Gray** (#3c3c3c): Secondary actions

### Output Log Colors
- **Green** (#4ec9b0): Success messages (✓)
- **Blue** (#569cd6): Info messages
- **Orange** (#ce9178): Warnings (⚠️)
- **Red** (#f48771): Errors (❌)
- **Gray** (#858585): Separators (===)
- **White** (#e0e0e0): Normal text

### Background Colors
- **Main BG**: #1e1e1e (very dark gray)
- **Panel BG**: #2d2d2d (dark gray)
- **Output BG**: #1a1a1a (nearly black)
- **Status Bar**: #252525 (dark gray)

## Layout Proportions

```
Total Width: 1000px
├─ Left Panel: ~400px (40%)
│  ├─ Padding: 15px
│  ├─ Settings: 2 buttons
│  ├─ Input: 2 buttons
│  └─ Processing: 6 buttons/controls
│
└─ Right Panel: ~600px (60%)
   ├─ Padding: 15px
   ├─ Header: "📋 Output Log"
   └─ Output: Expandable with scrollbar

Status Bar: Full width (100%)
```

## Button Sizes

```
Settings Buttons:
  Height: ~40px
  Width: Fill panel
  Padding: 10px vertical

Input Buttons:
  Height: ~40px
  Width: Fill panel
  Padding: 10px vertical
  Bold font

Main Action (Swap Face):
  Height: ~44px
  Width: Fill panel
  Padding: 12px vertical
  Bold font

Control Buttons (Pause/Resume):
  Height: ~36px
  Width: Half panel each
  Padding: 8px vertical

Secondary Buttons:
  Height: ~40px
  Width: Fill panel
  Padding: 10px vertical
```

## Spacing System

```
Vertical Spacing:
├─ Header margin: 20px bottom
├─ Section headers: 10-15px top, 10px bottom
├─ Section separators: 10px top/bottom
├─ Button spacing: 2px between buttons
└─ Status bar: 10px top margin

Horizontal Spacing:
├─ Main container: 20px padding
├─ Panel gap: 10px
├─ Section padding: 15px
└─ Button padding: 20px horizontal
```

## Responsive Behavior

### Minimum Size (900x650)
```
┌──────────────────┬─────────────────┐
│   Controls       │   Output Log    │
│   (360px)        │   (520px)       │
└──────────────────┴─────────────────┘
```

### Large Size (1400x900)
```
┌────────────────────────┬──────────────────────────────┐
│      Controls          │        Output Log            │
│      (540px)           │        (840px)               │
└────────────────────────┴──────────────────────────────┘
```

## State Indicators

### Button State Colors

**Enabled State:**
```
Primary (Blue):   #007acc
Success (Green):  #4ec9b0
Warning (Orange): #ce9178
Secondary (Gray): #3c3c3c
```

**Disabled State:**
```
Primary:   #3a4a5a (dark blue-gray)
Success:   #3a5a4a (dark teal)
Warning:   #4a3a3a (dark brown)
Secondary: #2a2a2a (darker gray)
```

**Hover State (Active Buttons):**
```
Primary:   #005a9e (darker blue)
Success:   #3da88a (darker teal)
Warning:   #b87a5e (darker orange)
Secondary: #4a4a4a (lighter gray)
```

## Font Specifications

```
Header Title:
  Font: Segoe UI
  Size: 24pt
  Weight: Bold
  Color: #007acc

Subtitle:
  Font: Segoe UI
  Size: 10pt
  Weight: Normal
  Color: #cccccc

Section Headers:
  Font: Segoe UI
  Size: 12pt
  Weight: Bold
  Color: #ffffff

Buttons:
  Font: Segoe UI
  Size: 10pt
  Weight: Bold (primary), Normal (secondary)
  Color: #ffffff or #000000 (on green/orange)

Output Log:
  Font: Consolas (monospace)
  Size: 10pt
  Weight: Normal (bold for errors)
  Color: Various (see color guide)

Status Bar:
  Font: Segoe UI
  Size: 9pt
  Weight: Normal
  Color: #cccccc or status color
```

## Icon Usage

```
🎬 - Video/Film related
👤 - Face/Person
🖥️ - Processing unit
📷 - Camera/Image
📁 - Files/Folders
⚙️ - Settings
⚡ - Processing/Power
✂️ - Split/Cut
🔄 - Swap/Exchange
⏸️ - Pause
▶️ - Play/Resume
💾 - Save/Storage
📋 - Log/List
✓ - Success/Complete
❌ - Error/Fail
⚠️ - Warning/Caution
🔊 - Sound/Audio
```

## Workflow Visual Flow

```
START
  ↓
┌─────────────────┐
│ Choose Face     │ ← Click blue button
└────────┬────────┘
         ↓
┌─────────────────┐
│ Choose Video    │ ← Click blue button
└────────┬────────┘
         ↓
┌─────────────────┐
│ Split Video     │ ← Click gray button
└────────┬────────┘   (Watch output log)
         ↓
┌─────────────────┐
│ Swap Face       │ ← Click green button
└────────┬────────┘   (Main processing)
         │
         ├→ [Pause] ← Orange button (optional)
         │     ↓
         ├→ [Resume] ← Teal button
         │     ↓
         ↓
┌─────────────────┐
│ Merge Frames    │ ← Click gray button
└────────┬────────┘   (Final step)
         ↓
       DONE!
  (Video saved)
```

## Interactive Elements

### Clickable
- All enabled buttons
- Setting toggles
- File choosers

### Visual Feedback
- Button hover effects
- Status bar updates
- Output log scrolling
- Progress percentages

### Dynamic Updates
- Button enable/disable
- Color changes
- Status messages
- Progress counting
