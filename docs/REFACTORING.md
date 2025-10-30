# Project Refactoring - Face Swap Tool

## New Project Structure

```
face2video/
├── app.py                          # New main entry point
├── main.py                         # Legacy entry point (keep for compatibility)
│
├── src/                            # Source code modules
│   ├── __init__.py
│   │
│   ├── core/                       # Core business logic
│   │   ├── __init__.py
│   │   ├── api_handler.py         # Automatic1111 API client
│   │   ├── video_processor.py     # Video frame extraction/merging
│   │   ├── progress_manager.py    # Progress tracking
│   │   └── face_swap_processor.py # Face swap orchestration
│   │
│   ├── ui/                         # User interface
│   │   ├── __init__.py
│   │   ├── main_window.py         # Main application window (TO CREATE)
│   │   ├── components.py          # Reusable UI components (TO CREATE)
│   │   └── styles.py              # UI styling constants (TO CREATE)
│   │
│   └── utils/                      # Utility functions
│       ├── __init__.py
│       └── file_utils.py          # File operations (TO CREATE)
│
├── docs/                           # Documentation
│   ├── FEATURES.md
│   ├── QUICK_START.md
│   ├── UI_IMPROVEMENTS.md
│   ├── UI_LAYOUT.md
│   ├── UI_REDESIGN_SUMMARY.md
│   ├── FLOW_DIAGRAMS.md
│   └── CHANGELOG.md
│
├── input_faces/                    # Input face images
├── input_faces_models/             # Input face models
├── input_videos/                   # Input videos
├── extracted_frames/               # Temporary extracted frames
├── finished_frames/                # Processed frames
├── finished_videos/                # Final output videos
│
├── automatic1111_api.py           # Legacy API (keep for compatibility)
├── get_frames_from_video.py       # Legacy (keep for compatibility)
├── turn_frames_into_video.py      # Legacy (keep for compatibility)
├── copy_sound_from_video.py       # Legacy (keep for compatibility)
│
├── install.py                      # Installation script
├── test_progress.py                # Progress testing
├── progress.json                   # Progress tracking file
├── .gitignore
├── LICENSE
└── README.md
```

## Modules Created

### 1. `src/core/api_handler.py`
- **Class**: `Automatic1111API`
- **Purpose**: Handle Reactor API communication
- **Methods**:
  - `swap_face()` - Perform face swap via API

### 2. `src/core/video_processor.py`
- **Class**: `VideoProcessor`
- **Purpose**: Video frame extraction and merging
- **Methods**:
  - `extract_frames()` - Extract frames from video
  - `create_video_from_frames()` - Create video from frames
  - `add_audio()` - Add audio to video

### 3. `src/core/progress_manager.py`
- **Class**: `ProgressManager`
- **Purpose**: Track and manage progress for crash recovery
- **Methods**:
  - `save()` - Save progress
  - `load()` - Load progress
  - `clear()` - Clear progress
  - `is_recent()` - Check if progress is recent

### 4. `src/core/face_swap_processor.py`
- **Class**: `FaceSwapProcessor`
- **Purpose**: Orchestrate face swapping process
- **Methods**:
  - `process_frames()` - Main processing loop with callbacks
  - `pause()` - Pause processing
  - `resume()` - Resume processing
  - `stop()` - Stop processing

### 5. `app.py`
- **Purpose**: New main entry point
- **Benefits**: Clean separation, uses modular structure

## Benefits of Refactored Structure

### 1. **Separation of Concerns**
- UI code separate from business logic
- Core functionality independent of UI framework
- Easy to test individual components

### 2. **Maintainability**
- Clear module boundaries
- Easy to locate and fix bugs
- Smaller, focused files

### 3. **Reusability**
- Core modules can be used without UI
- Can create CLI version easily
- API can be used in other projects

### 4. **Testability**
- Each module can be unit tested
- Mock dependencies easily
- Clear interfaces between modules

### 5. **Scalability**
- Easy to add new features
- Can extend without modifying existing code
- Plugin architecture possible

### 6. **Documentation**
- All docs moved to `docs/` folder
- Cleaner root directory
- Better organization

## Migration Path

### Phase 1: Core Modules (✅ COMPLETE)
- Created `src/core/` modules
- Refactored business logic
- Maintained backward compatibility

### Phase 2: UI Modules (PENDING)
- Extract UI from `main.py` to `src/ui/main_window.py`
- Create reusable components
- Separate styling constants

### Phase 3: Utilities (PENDING)
- Create file utilities
- Add logging utilities
- Configuration management

### Phase 4: Testing (PENDING)
- Add unit tests
- Integration tests
- End-to-end tests

### Phase 5: Documentation (PENDING)
- Update all documentation
- Add API documentation
- Create developer guide

## How to Use Refactored Code

### Option 1: Use New Entry Point
```powershell
python app.py
```

### Option 2: Use Legacy Entry Point
```powershell
python main.py  # Still works with old structure
```

### Option 3: Import Modules Directly
```python
from src.core import FaceSwapProcessor, VideoProcessor

# Extract frames
processor = VideoProcessor()
processor.extract_frames("input.mp4")

# Swap faces
swapper = FaceSwapProcessor()
swapper.process_frames(...)
```

## Next Steps

1. **Complete UI Refactoring**: Move UI code to `src/ui/`
2. **Add Utilities**: Create helper functions in `src/utils/`
3. **Add Tests**: Create test suite
4. **Update Documentation**: Reflect new structure
5. **Add Configuration**: Config file support
6. **Add Logging**: Proper logging system

## Backward Compatibility

- Old entry point (`main.py`) still works
- Legacy modules (`automatic1111_api.py`, etc.) kept
- Gradual migration possible
- No breaking changes for existing users
