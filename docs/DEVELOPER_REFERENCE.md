# Developer Quick Reference

## 🚀 Quick Start

### Run the Application
```powershell
# New modular version (recommended)
python .\app.py

# Legacy version (still works)
python .\main.py
```

### Install Dependencies
```powershell
python .\install.py
```

## 📁 Project Structure

```
src/
├── core/           # Business logic - Don't touch UI here
├── ui/             # UI components - Don't add business logic here
└── utils/          # Helper functions - Keep stateless
```

## 🎨 UI Components Cheat Sheet

### Import Components
```python
from src.ui import (
    StyledButton, StyledLabel, StyledFrame,
    Panel, ScrollableText, StatusBar,
    Colors, Fonts, Layout, Icons
)
```

### Create Buttons
```python
# Primary action (blue)
btn = StyledButton(parent, "Click Me", style="primary")

# Success (green)
btn = StyledButton(parent, "Save", style="success")

# Warning (orange)
btn = StyledButton(parent, "Delete", style="warning")

# Danger (dark red)
btn = StyledButton(parent, "Exit", style="danger")

# Secondary (gray)
btn = StyledButton(parent, "Cancel", style="secondary")

# Small button
btn = StyledButton(parent, "OK", size="small")
```

### Create Labels
```python
# Header
lbl = StyledLabel(parent, "Title", size="header", bold=True)

# Section
lbl = StyledLabel(parent, "Section", size="section", bold=True)

# Normal
lbl = StyledLabel(parent, "Text", size="normal")

# Colored
lbl = StyledLabel(parent, "Error", color=Colors.ERROR)
```

### Create Panels
```python
# Panel with title
panel = Panel(parent, "My Panel", icon=Icons.SETTINGS)
content = panel.get_content()
# Add widgets to content
```

### Create Scrollable Output
```python
# Text with scrollbar
output = ScrollableText(parent)
output.append("Message\n", tag="success")
output.append("Error\n", tag="error")
output.clear()
```

### Status Bar
```python
status = StatusBar(parent)
status.set_status("Processing...", Colors.WARNING)
status.set_status("Done!", Colors.SUCCESS)
```

## 🎨 Colors Reference

```python
# Backgrounds
Colors.BG_MAIN       # #1e1e1e (main background)
Colors.BG_PANEL      # #2d2d2d (panel background)
Colors.BG_DARK       # #1a1a1a (dark areas)
Colors.BG_STATUS     # #252525 (status bar)

# Text
Colors.TEXT_PRIMARY    # #ffffff (white)
Colors.TEXT_SECONDARY  # #cccccc (gray)

# Status
Colors.SUCCESS  # #4ec9b0 (green)
Colors.WARNING  # #ce9178 (orange)
Colors.ERROR    # #f48771 (red)
Colors.INFO     # #569cd6 (blue)

# Accent
Colors.ACCENT       # #007acc (primary blue)
Colors.ACCENT_HOVER # #005a9e (darker blue)
```

## 📐 Layout Reference

```python
# Padding
Layout.PAD_MAIN      # 20 (main container)
Layout.PAD_SECTION   # 15 (sections)
Layout.PAD_BUTTON_H  # 20 (button horizontal)
Layout.PAD_BUTTON_V  # 10 (button vertical)

# Spacing
Layout.SPACE_SECTION  # 15 (between sections)
Layout.SPACE_BUTTON   # 2  (between buttons)

# Window
Layout.WINDOW_WIDTH   # 1200
Layout.WINDOW_HEIGHT  # 990
```

## 🎭 Icons Reference

```python
Icons.APP       # 🎬
Icons.SETTINGS  # ⚙️
Icons.CPU       # 🖥️
Icons.IMAGE     # 📷
Icons.FOLDER    # 📁
Icons.FACE      # 👤
Icons.VIDEO     # 🎥
Icons.PROCESSING # ⚡
Icons.SCISSORS  # ✂️
Icons.SWAP      # 🔄
Icons.PAUSE     # ⏸️
Icons.PLAY      # ▶️
Icons.SAVE      # 💾
Icons.MERGE     # 🎬
Icons.LOG       # 📋
Icons.PREVIEW   # 🖼️
Icons.HIDE      # 🙈
Icons.SHOW      # 👁️
Icons.EXIT      # 🚪
Icons.SUCCESS   # ✓
Icons.ERROR     # ❌
Icons.WARNING   # ⚠️
Icons.SOUND     # 🔊
```

## 🛠️ Utility Functions

### File Operations
```python
from src.utils import (
    ensure_directory,
    list_files,
    list_image_files,
    list_video_files,
    clear_directory,
    get_latest_file
)

# Create directory
ensure_directory("output/frames")

# List files
images = list_image_files("input_faces/")
videos = list_video_files("input_videos/")

# Clear directory
count = clear_directory("temp/")

# Get latest file
latest = get_latest_file("output/", ".mp4")
```

### File Info
```python
from src.utils import (
    get_filename_without_ext,
    get_file_size,
    format_file_size,
    sanitize_filename
)

# Get name without extension
name = get_filename_without_ext("video.mp4")  # "video"

# Get and format size
size = get_file_size("video.mp4")
size_str = format_file_size(size)  # "1.5 MB"

# Sanitize filename
safe = sanitize_filename("my:file*.txt")  # "my_file_.txt"
```

### Logging
```python
from src.utils import log_info, log_error, log_warning

log_info("Processing started")
log_error("Failed to process frame")
log_warning("Low disk space")
```

## 🔧 Core Components

### API Handler
```python
from src.core import Automatic1111API

api = Automatic1111API()
api.swap_face(
    image_file="frame_001.jpg",
    source_image="face.jpg",
    model_name="",
    file_path="extracted_frames/frame_001.jpg",
    processing_unit="CPU",
    source_choice=0
)
```

### Video Processor
```python
from src.core import VideoProcessor

processor = VideoProcessor()

# Extract frames
processor.extract_frames("input.mp4")

# Create video
output_file = processor.create_video_from_frames("frames/")

# Add audio
processor.add_audio("input.mp4", output_file)
```

### Progress Manager
```python
from src.core import ProgressManager

pm = ProgressManager()

# Save progress
pm.save(
    current_index=42,
    total_files=100,
    input_face="face.jpg",
    input_video="video.mp4",
    input_type="Single Image",
    processing_unit="CPU"
)

# Load progress
progress = pm.load()
if progress and pm.is_recent(progress):
    start_from = progress['current_index']

# Clear progress
pm.clear()
```

## 🎯 Common Patterns

### Threading Pattern
```python
import threading

def long_running_task():
    # Do work
    result = process_something()
    
    # Update UI (thread-safe)
    root.after(0, lambda: update_ui(result))

# Start in thread
thread = threading.Thread(target=long_running_task)
thread.start()
```

### Callback Pattern
```python
def process_with_callback(progress_callback, finish_callback):
    for i in range(100):
        # Process
        result = process_item(i)
        
        # Callback for progress
        root.after(0, lambda r=result: progress_callback(r))
    
    # Callback when finished
    root.after(0, finish_callback)
```

### Error Handling Pattern
```python
try:
    # Risky operation
    result = do_something()
except Exception as e:
    # Log error
    from src.utils import log_error
    log_error(f"Operation failed: {e}")
    
    # Update UI
    self._append_output(f"{Icons.ERROR} Error: {str(e)}")
    self._update_status(f"Error: {str(e)}", Colors.ERROR)
```

## 📝 Code Style

### Naming Conventions
```python
# Classes: PascalCase
class FaceSwapApp:
    pass

# Functions/Methods: snake_case
def process_frame():
    pass

# Constants: UPPER_SNAKE_CASE
MAX_SIZE = 400

# Private methods: _leading_underscore
def _internal_method():
    pass
```

### Type Hints
```python
from typing import List, Optional

def process_files(files: List[str]) -> int:
    return len(files)

def get_file(path: str) -> Optional[str]:
    if os.path.exists(path):
        return path
    return None
```

### Docstrings
```python
def process_video(video_path: str, output_dir: str) -> bool:
    """
    Process a video file and extract frames
    
    Args:
        video_path: Path to input video file
        output_dir: Directory to save extracted frames
    
    Returns:
        True if successful, False otherwise
    """
    # Implementation
    pass
```

## 🐛 Debugging Tips

### Check Errors
```python
from src.core import get_errors
errors = get_errors()
```

### Enable Logging
```python
from src.utils import get_logger

logger = get_logger("MyModule", log_dir="logs/")
logger.debug("Detailed debug info")
logger.info("General information")
logger.warning("Warning message")
logger.error("Error occurred")
```

### Print to Output Log
```python
# In main_window.py
self._append_output(f"Debug: {variable_value}")
```

## 📚 Documentation

- **FEATURES.md** - What the app can do
- **QUICK_START.md** - How to use it
- **PROJECT_STRUCTURE.md** - Architecture overview
- **REFACTORING_COMPLETE.md** - Refactoring summary
- **UI_UTILS_REFACTORING.md** - UI/Utils details
- **DEVELOPMENT_SUMMARY.md** - Technical overview

## 🎓 Learning Path

1. **Start Here**: Read `README.md`
2. **Understand Features**: Read `docs/FEATURES.md`
3. **Learn Structure**: Read `docs/PROJECT_STRUCTURE.md`
4. **Explore UI**: Read `docs/UI_UTILS_REFACTORING.md`
5. **Deep Dive**: Read `docs/DEVELOPMENT_SUMMARY.md`

## 💡 Pro Tips

1. **Use Components**: Always use UI components, never raw tkinter widgets
2. **Thread Heavy Operations**: Keep UI responsive
3. **Use Callbacks**: For async UI updates
4. **Type Hints**: Help IDE and catch errors early
5. **Document Code**: Write clear docstrings
6. **Follow Patterns**: Look at existing code for examples
7. **Keep Modules Small**: Single responsibility principle
8. **Centralize Config**: Use Colors, Fonts, Layout classes
9. **Error Gracefully**: Always handle exceptions
10. **Test Changes**: Run app.py after modifications

---

**Happy Coding!** 🚀
