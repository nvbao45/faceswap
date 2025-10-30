# New Project Structure - Visual Guide

## Directory Tree

```
face2video/
│
├── 📄 app.py                       ⭐ NEW: Main entry point (modular)
├── 📄 main.py                      📌 Legacy entry point (still works)
├── 📄 README.md                    📝 Updated with new structure
├── 📄 REFACTORING.md              📚 Refactoring guide
├── 📄 REFACTORING_SUMMARY.md      📚 Quick summary
│
├── 📁 src/                         ⭐ NEW: Source code modules
│   ├── 📄 __init__.py
│   ├── 📄 compat.py               🔗 Compatibility layer
│   │
│   ├── 📁 core/                    💼 Core business logic
│   │   ├── 📄 __init__.py
│   │   ├── 📄 api_handler.py      🔌 API client (OOP)
│   │   ├── 📄 video_processor.py  🎬 Video operations
│   │   ├── 📄 progress_manager.py 💾 Progress tracking
│   │   └── 📄 face_swap_processor.py 🔄 Main orchestration
│   │
│   ├── 📁 ui/                      🎨 User interface (future)
│   │   └── 📄 __init__.py
│   │
│   └── 📁 utils/                   🛠️ Utilities (future)
│       └── 📄 __init__.py
│
├── 📁 docs/                        ⭐ NEW: Documentation folder
│   ├── 📄 FEATURES.md             ✨ Feature documentation
│   ├── 📄 QUICK_START.md          🚀 Quick start guide
│   ├── 📄 UI_IMPROVEMENTS.md      🎨 UI documentation
│   ├── 📄 UI_LAYOUT.md            📐 UI layout guide
│   ├── 📄 UI_REDESIGN_SUMMARY.md  📋 UI summary
│   ├── 📄 FLOW_DIAGRAMS.md        📊 Flow diagrams
│   └── 📄 CHANGELOG.md            📝 Change log
│
├── 📁 input_faces/                 📷 Input face images
├── 📁 input_faces_models/          🎭 Input face models
├── 📁 input_videos/                🎥 Input videos
├── 📁 extracted_frames/            🖼️ Temporary frames
├── 📁 finished_frames/             ✅ Processed frames
├── 📁 finished_videos/             🎬 Final videos
│
├── 📄 automatic1111_api.py        📌 Legacy API (keep)
├── 📄 get_frames_from_video.py    📌 Legacy (keep)
├── 📄 turn_frames_into_video.py   📌 Legacy (keep)
├── 📄 copy_sound_from_video.py    📌 Legacy (keep)
│
├── 📄 install.py                   ⚙️ Installation script
├── 📄 test_progress.py             🧪 Progress tests
├── 📄 progress.json                💾 Progress tracking
├── 📄 .gitignore
└── 📄 LICENSE
```

## Module Dependencies

```
┌─────────────────────────────────────────────┐
│              app.py (New)                   │
│         Main Application Entry              │
└──────────────────┬──────────────────────────┘
                   │
                   ├─► ui.main_window (Future)
                   │
        ┌──────────┴──────────┐
        │                     │
        ▼                     ▼
┌──────────────┐    ┌──────────────────┐
│  UI Layer    │    │   Core Layer     │
│  (Future)    │◄───┤  (Implemented)   │
└──────────────┘    └────────┬─────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│ api_handler  │   │video_processor│   │progress_mgr  │
│              │   │               │   │              │
│ • swap_face()│   │ • extract()   │   │ • save()     │
│              │   │ • merge()     │   │ • load()     │
│              │   │ • add_audio() │   │ • clear()    │
└──────────────┘   └──────────────┘   └──────────────┘
        ▲                  ▲                  ▲
        │                  │                  │
        └──────────────────┴──────────────────┘
                           │
                ┌──────────┴──────────┐
                │ face_swap_processor │
                │                     │
                │ • process_frames()  │
                │ • pause()           │
                │ • resume()          │
                └─────────────────────┘
```

## Code Flow

### Old Flow (main.py)
```
main.py
  └─► All code in one file (744 lines)
       ├─ UI code
       ├─ Business logic
       ├─ Event handlers
       └─ Utility functions
```

### New Flow (app.py + modules)
```
app.py (20 lines)
  │
  └─► ui.main_window
       ├─► core.face_swap_processor
       │    ├─► core.api_handler
       │    ├─► core.video_processor
       │    └─► core.progress_manager
       │
       └─► ui.components
            └─► ui.styles
```

## Migration Map

### From → To

```
automatic1111_api.py
  └─► src/core/api_handler.py
       └─ Class: Automatic1111API
           └─ Method: swap_face()

get_frames_from_video.py
  └─► src/core/video_processor.py
       └─ Class: VideoProcessor
           └─ Method: extract_frames()

turn_frames_into_video.py
  └─► src/core/video_processor.py
       └─ Class: VideoProcessor
           └─ Method: create_video_from_frames()

copy_sound_from_video.py
  └─► src/core/video_processor.py
       └─ Class: VideoProcessor
           └─ Method: add_audio()

main.py (progress functions)
  └─► src/core/progress_manager.py
       └─ Class: ProgressManager
           ├─ Method: save()
           ├─ Method: load()
           └─ Method: clear()

main.py (face swap logic)
  └─► src/core/face_swap_processor.py
       └─ Class: FaceSwapProcessor
           ├─ Method: process_frames()
           ├─ Method: pause()
           └─ Method: resume()
```

## File Size Comparison

```
Before Refactoring:
  main.py: 744 lines ⚠️ (everything in one file)

After Refactoring:
  app.py: 20 lines ✅
  src/core/api_handler.py: 76 lines ✅
  src/core/video_processor.py: 124 lines ✅
  src/core/progress_manager.py: 73 lines ✅
  src/core/face_swap_processor.py: 118 lines ✅
  
  Total: ~411 lines (well organized)
  main.py: 744 lines (legacy, still works)
```

## Benefits Visualization

```
┌─────────────────────────────────────────────┐
│           Before Refactoring                │
├─────────────────────────────────────────────┤
│ ❌ One massive file                         │
│ ❌ Hard to maintain                         │
│ ❌ Difficult to test                        │
│ ❌ No code reuse                            │
│ ❌ Unclear dependencies                     │
└─────────────────────────────────────────────┘

                    ↓ REFACTOR ↓

┌─────────────────────────────────────────────┐
│           After Refactoring                 │
├─────────────────────────────────────────────┤
│ ✅ Small, focused modules                   │
│ ✅ Easy to maintain                         │
│ ✅ Testable components                      │
│ ✅ Reusable code                            │
│ ✅ Clear dependencies                       │
│ ✅ Better organization                      │
│ ✅ Backward compatible                      │
└─────────────────────────────────────────────┘
```

## Legend

📄 = File
📁 = Folder
⭐ = New/Changed
📌 = Legacy (kept for compatibility)
💼 = Business logic
🎨 = User interface
🛠️ = Utilities
📚 = Documentation
✅ = Completed
🔄 = In progress
📝 = Updated
