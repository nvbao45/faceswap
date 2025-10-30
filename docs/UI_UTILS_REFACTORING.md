# UI and Utils Refactoring Documentation

## Overview
This document describes the UI and utility modules that have been extracted from the main application for better code organization and maintainability.

## UI Module (`src/ui/`)

### Structure
```
src/ui/
├── __init__.py       # Package exports
├── styles.py         # Styling constants and theme
└── components.py     # Reusable UI components
```

### styles.py
Contains all styling constants, color schemes, and theme configurations.

#### Classes

**Colors**
- Background colors: `BG_MAIN`, `BG_PANEL`, `BG_DARK`, `BG_STATUS`
- Accent colors: `ACCENT`, `ACCENT_HOVER`
- Text colors: `TEXT_PRIMARY`, `TEXT_SECONDARY`
- Status colors: `SUCCESS`, `WARNING`, `ERROR`, `INFO`
- Button colors: `BTN_PRIMARY`, `BTN_SUCCESS`, `BTN_WARNING`, `BTN_DANGER`, `BTN_SECONDARY`, `BTN_DISABLED`
- Separator: `SEPARATOR`, `SEPARATOR_LIGHT`

**Fonts**
- Font families: `FAMILY` (Segoe UI), `FAMILY_MONO` (Consolas)
- Font sizes: `SIZE_HEADER`, `SIZE_SUBTITLE`, `SIZE_SECTION`, `SIZE_BUTTON`, `SIZE_BUTTON_SMALL`, `SIZE_OUTPUT`, `SIZE_STATUS`
- Font weights: `WEIGHT_BOLD`, `WEIGHT_NORMAL`

**Layout**
- Padding: `PAD_MAIN`, `PAD_SECTION`, `PAD_BUTTON_H`, `PAD_BUTTON_V`, etc.
- Spacing: `SPACE_SECTION`, `SPACE_BUTTON`, `SPACE_SEPARATOR`
- Panel spacing: `PANEL_GAP`
- Preview: `PREVIEW_MAX_SIZE`

**ButtonStyle**
Static methods for button styles:
- `primary()` - Primary action buttons
- `success()` - Success/confirmation buttons
- `warning()` - Warning buttons
- `danger()` - Dangerous actions (delete, exit)
- `secondary()` - Secondary actions
- `special()` - Special actions (resume from crash)
- `utility()` - Utility buttons (toggle preview)

**TextTags**
Text widget tag configurations for colored output:
- `ERROR` - Red error messages
- `SUCCESS` - Green success messages
- `WARNING` - Orange warning messages
- `INFO` - Blue info messages
- `SEPARATOR` - Gray separators

**Icons**
Emoji icons used throughout the UI:
- App icons: `APP`, `SETTINGS`, `CPU`
- File icons: `IMAGE`, `FOLDER`, `FACE`, `VIDEO`
- Action icons: `PROCESSING`, `SWAP`, `PAUSE`, `PLAY`, `SAVE`, `MERGE`
- UI icons: `LOG`, `PREVIEW`, `HIDE`, `SHOW`, `EXIT`
- Status icons: `SUCCESS`, `ERROR`, `WARNING`, `SOUND`

### components.py
Contains reusable UI components built on tkinter widgets.

#### Components

**StyledButton**
Styled button with consistent appearance.
```python
button = StyledButton(parent, "Click Me", style="primary", size="normal")
```
- Styles: `primary`, `success`, `warning`, `danger`, `secondary`, `special`, `utility`
- Sizes: `normal`, `small`

**StyledLabel**
Styled label with consistent appearance.
```python
label = StyledLabel(parent, "Label Text", size="header", bold=True)
```
- Sizes: `header`, `section`, `subtitle`, `normal`
- Optional bold and custom color

**StyledFrame**
Styled frame with consistent background.
```python
frame = StyledFrame(parent, bg_type="panel")
```
- Background types: `panel`, `main`

**StyledText**
Styled text widget for output log.
```python
text = StyledText(parent, wrap="word", height=20)
```

**StyledEntry**
Styled entry widget for user input.
```python
entry = StyledEntry(parent, width=30)
```

**Separator**
Horizontal separator line.
```python
sep = Separator(parent)
sep.pack(fill="x", pady=10)
```

**SectionHeader**
Section header with icon and title.
```python
header = SectionHeader(parent, "🎬", "Processing Options")
header.pack(fill="x", pady=10)
```

**StatusBar**
Status bar at the bottom of the window.
```python
status = StatusBar(parent)
status.set_status("Processing...", color=Colors.INFO)
```

**Panel**
Panel with title and content area.
```python
panel = Panel(parent, "Output Log", icon="📋")
content = panel.get_content()
# Add widgets to content
```

**ScrollableText**
Text widget with scrollbar.
```python
log = ScrollableText(parent)
log.append("Message\n", tag="success")
log_widget = log.get_text_widget()
```

**ToggleButton**
Button that toggles between two states.
```python
toggle = ToggleButton(
    parent,
    text_on="🙈 Hide Preview",
    text_off="👁️ Show Preview",
    command=lambda is_on: print(f"State: {is_on}")
)
```

**ImagePreview**
Image preview widget.
```python
preview = ImagePreview(parent, max_size=400)
preview.set_image(pil_image)
preview.clear()
```

## Utils Module (`src/utils/`)

### Structure
```
src/utils/
├── __init__.py       # Package exports
├── file_utils.py     # File and directory operations
└── logger.py         # Logging utilities
```

### file_utils.py
File and directory operation utilities.

#### Functions

**ensure_directory(path)**
Create directory if it doesn't exist.
```python
ensure_directory("output/frames")
```

**list_files(directory, extension=None)**
List files in directory with optional extension filter.
```python
files = list_files("input/", ".jpg")
```

**list_image_files(directory)**
List all image files (jpg, png, bmp, gif, webp).
```python
images = list_image_files("input_faces/")
```

**list_video_files(directory)**
List all video files (mp4, avi, mov, mkv, etc.).
```python
videos = list_video_files("input_videos/")
```

**clear_directory(directory, pattern=None)**
Clear files in directory with optional regex pattern.
```python
count = clear_directory("temp/", pattern=r"frame_\d+\.jpg")
```

**get_filename_without_ext(path)**
Get filename without extension.
```python
name = get_filename_without_ext("video.mp4")  # Returns "video"
```

**get_file_size(path)**
Get file size in bytes.
```python
size = get_file_size("video.mp4")
```

**format_file_size(size_bytes)**
Format size in human-readable format.
```python
size_str = format_file_size(1536000)  # Returns "1.5 MB"
```

**generate_timestamp_filename(prefix="", extension="")**
Generate filename with timestamp.
```python
filename = generate_timestamp_filename("output", ".mp4")
# Returns "output_20240101_123045.mp4"
```

**sanitize_filename(filename)**
Remove invalid characters from filename.
```python
safe_name = sanitize_filename("file:name?.txt")  # Returns "file_name_.txt"
```

**count_files(directory, extension=None)**
Count files in directory.
```python
count = count_files("frames/", ".jpg")
```

**get_latest_file(directory, extension=None)**
Get most recently modified file.
```python
latest = get_latest_file("output/", ".mp4")
```

### logger.py
Logging utilities for the application.

#### Classes

**AppLogger**
Application logger with file and console output.
```python
logger = AppLogger("FaceSwapTool", log_dir="logs/")
logger.info("Processing started")
logger.error("An error occurred")
```

Methods:
- `debug(message)` - Debug level
- `info(message)` - Info level
- `warning(message)` - Warning level
- `error(message)` - Error level
- `critical(message)` - Critical level

#### Quick Functions

```python
from src.utils import log_info, log_error, log_warning

log_info("Process started")
log_error("Failed to process frame")
log_warning("Low disk space")
```

## Usage Examples

### Creating a Styled UI
```python
from src.ui import (
    StyledFrame, StyledButton, Panel, ScrollableText,
    SectionHeader, StatusBar, Colors, Icons
)

# Main window
root = tk.Tk()
root.configure(bg=Colors.BG_MAIN)

# Section header
header = SectionHeader(root, Icons.APP, "Face Swap Tool")
header.pack(fill="x", padx=20, pady=(20, 10))

# Panel with content
panel = Panel(root, "Controls", icon=Icons.SETTINGS)
panel.pack(fill="both", expand=True, padx=20, pady=10)

content = panel.get_content()

# Buttons in panel
btn = StyledButton(content, "Start Processing", style="success")
btn.pack(pady=5)

# Output log
log_panel = Panel(root, "Output Log", icon=Icons.LOG)
log_panel.pack(fill="both", expand=True, padx=20, pady=10)

log = ScrollableText(log_panel.get_content())
log.pack(fill="both", expand=True)

# Status bar
status = StatusBar(root)
status.pack(fill="x")
status.set_status("Ready", color=Colors.SUCCESS)
```

### Using File Utilities
```python
from src.utils import (
    ensure_directory, list_image_files, clear_directory,
    get_latest_file, format_file_size
)

# Setup directories
ensure_directory("output/frames")
ensure_directory("output/videos")

# List input files
faces = list_image_files("input_faces/")
print(f"Found {len(faces)} face images")

# Clear old frames
count = clear_directory("temp/frames")
print(f"Deleted {count} old frames")

# Get latest output
latest_video = get_latest_file("output/videos/", ".mp4")
if latest_video:
    size = get_file_size(latest_video)
    print(f"Latest video: {latest_video} ({format_file_size(size)})")
```

### Using Logger
```python
from src.utils import get_logger

# Create logger with file output
logger = get_logger("FaceSwapTool", log_dir="logs/")

logger.info("Application started")
logger.debug("Loading configuration...")

try:
    # Process something
    logger.info("Processing frame 1/100")
except Exception as e:
    logger.error(f"Error processing frame: {e}")

logger.info("Application finished")
```

## Migration Guide

### From main.py to New Modules

**Old Code (main.py)**
```python
# Define colors
bg_color = "#1e1e1e"
panel_bg = "#2d2d2d"
accent_color = "#007acc"

# Create button
button = tk.Button(
    parent,
    text="Click",
    font=("Segoe UI", 10),
    bg="#007acc",
    fg="#ffffff",
    activebackground="#005a9e",
    relief="flat",
    cursor="hand2"
)
```

**New Code (using UI modules)**
```python
from src.ui import StyledButton, Colors

button = StyledButton(parent, "Click", style="primary")
```

**Old Code (file operations)**
```python
import os

def list_images(directory):
    files = []
    for file in os.listdir(directory):
        if file.lower().endswith(('.jpg', '.png')):
            files.append(os.path.join(directory, file))
    return sorted(files)
```

**New Code (using file utils)**
```python
from src.utils import list_image_files

images = list_image_files(directory)
```

## Benefits

1. **Code Reusability**: UI components can be reused across different parts of the application
2. **Consistency**: Centralized styling ensures consistent look and feel
3. **Maintainability**: Changes to styles or utilities only need to be made in one place
4. **Testability**: Smaller, focused modules are easier to test
5. **Readability**: Main application code is cleaner and more focused on business logic
6. **Scalability**: Easy to add new components or utilities without cluttering main code

## Next Steps

The next phase will involve:
1. Creating `src/ui/main_window.py` - Main application window class
2. Migrating UI code from `main.py` to use the new components
3. Updating `app.py` to use the new main window class
4. Testing the refactored application
5. Deprecating old monolithic `main.py` in favor of modular structure
