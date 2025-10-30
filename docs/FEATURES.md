# New Features: Pause/Resume and Crash Recovery

## Overview
The Face Swap Tool application now includes pause/resume functionality and automatic crash recovery to make the face swapping process more flexible and reliable.

## Features

### 1. Pause/Resume During Face Swapping
You can now pause and resume the face swapping process at any time:

- **Pause Button**: Click "Pause Swap" during face swapping to pause the process
  - The process will pause after completing the current frame
  - Progress is automatically saved
  
- **Resume Button**: Click "Resume Swap" to continue from where you paused
  - All settings are preserved
  - No frames are re-processed

### 2. Crash Recovery
If the application crashes or is closed during face swapping, your progress is automatically saved:

- **Automatic Progress Tracking**: Every processed frame is saved to a progress file (`progress.json`)
- **Resume from Crash Button**: Click this button to continue from where the app stopped
- **Progress Detection**: On startup, the app checks for previous incomplete tasks and notifies you
- **Smart Resume**: Only processes remaining frames, skipping already completed ones

### 3. Progress Information
The progress file stores:
- Current frame index
- Total number of frames
- Input face and video paths
- Processing settings (CPU/GPU, Single Image/Face Model)
- Timestamp of last update

## How to Use

### Normal Workflow (No Changes)
1. Choose Face
2. Choose Video
3. Split Video Into Frames
4. Swap Face
5. Merge Frames Into Video

### Using Pause/Resume
1. Start face swapping with "Swap Face"
2. Click "Pause Swap" at any time to pause
3. Click "Resume Swap" to continue
4. Or close the app and use "Resume from Crash" later

### Recovering from a Crash
1. Restart the application
2. If previous progress is detected, you'll see a notification in the output
3. Click "Resume from Crash" to continue from the last processed frame
4. The app will restore all settings and continue processing

## Technical Details

### Progress File Location
The progress is saved in `progress.json` in the application directory.

### Progress File Format
```json
{
    "current_index": 150,
    "total_files": 500,
    "input_face": "path/to/face.jpg",
    "input_video": "path/to/video.mp4",
    "input_type": "Single Image",
    "processing_unit": "CPU",
    "timestamp": 1234567890.123
}
```

### Button States
- **Swap Face**: Available when not swapping
- **Pause Swap**: Available during swapping
- **Resume Swap**: Available when paused
- **Resume from Crash**: Available when not swapping (disabled during swapping)

## Benefits

1. **Flexibility**: Take breaks during long face swapping processes
2. **Reliability**: Never lose progress due to crashes or interruptions
3. **Efficiency**: Resume exactly where you left off without re-processing frames
4. **Peace of Mind**: Progress is saved after every frame
5. **Resource Management**: Pause to free up system resources temporarily

## Notes

- Progress files older than 7 days are still loaded but you'll be notified
- The progress file is automatically deleted upon successful completion
- You can manually delete `progress.json` to start fresh
- Pausing happens after the current frame completes (not instant)
