# Quick Start Guide - Pause/Resume Features

## 🚀 Quick Overview

Your Face Swap Tool app now has **Pause/Resume** and **Crash Recovery** features!

## 📋 What's New?

### 3 New Buttons
1. **Pause Swap** - Pause face swapping (appears when swapping)
2. **Resume Swap** - Resume after pause (appears when paused)
3. **Resume from Crash** - Continue after app crash/close

## 🎯 Common Scenarios

### Scenario 1: Need to Take a Break
```
1. Click "Swap Face" to start
2. Let it process for a while
3. Click "Pause Swap" when you need a break
4. Do whatever you need to do
5. Click "Resume Swap" to continue
6. All done!
```

### Scenario 2: App Crashed / Computer Restarted
```
1. Restart the app
2. You'll see a message: "PREVIOUS PROGRESS DETECTED!"
3. Click "Resume from Crash"
4. It continues where it left off
5. No need to re-process completed frames!
```

### Scenario 3: Want to Start Fresh (Despite Previous Progress)
```
1. If you see "PREVIOUS PROGRESS DETECTED!" message
2. Just click "Swap Face" instead of "Resume from Crash"
3. It will start fresh from the beginning
4. Old progress is automatically replaced
```

## 💡 Tips

### ✅ DO:
- Pause whenever you need to free up CPU/GPU
- Let the app finish the current frame before pause completes
- Use "Resume from Crash" if you closed the app mid-swap
- Trust the progress system - it saves after EVERY frame

### ❌ DON'T:
- Don't manually delete `progress.json` while swapping
- Don't click buttons rapidly - give each action time
- Don't worry if pausing takes a few seconds

## 🔍 Troubleshooting

### "No progress found to resume"
- This means there's no saved progress file
- Start a new swap with "Swap Face" button

### Progress seems stuck
- The app completes the current frame before pausing
- If processing a large frame, this might take time
- Check the output window for status messages

### Want to clear old progress manually?
- Delete the file `progress.json` in the app folder
- Or just click "Swap Face" to start fresh

## 📊 Understanding the Output Messages

| Message | Meaning |
|---------|---------|
| "PREVIOUS PROGRESS DETECTED!" | Found incomplete work from before |
| "Pausing face swap..." | Pause requested, will pause after current frame |
| "Resuming face swap..." | Continuing from where you paused |
| "Resuming from frame X/Y" | Starting from frame X out of Y total |
| "Progress has been saved" | Safe to close app, can resume later |
| "Finished swapping faces" | All done! Progress auto-cleared |

## 🎬 Example Workflow

### Long Video Processing (500 frames)
```
Day 1:
- Start swap (Frame 1-200)
- Pause for dinner
- Resume (Frame 201-300)
- Close app for the night

Day 2:
- Open app
- See "Last processed: 300/500 frames"
- Click "Resume from Crash"
- Continue (Frame 301-500)
- Done!
```

## 🛡️ Safety Features

1. **Auto-save**: Progress saved after each frame
2. **Error handling**: If error occurs, progress is preserved
3. **Smart detection**: Old progress (>7 days) still works
4. **Clean completion**: Progress auto-deleted when finished

## 📝 Technical Notes

### Where is progress saved?
- File: `progress.json` in the app directory
- Format: JSON (human-readable)
- Updates: After each frame

### What's saved?
- Current frame number
- Total frames
- Face and video paths
- Processing settings (CPU/GPU, Single/Model)
- Timestamp

### Button behavior:
- Buttons enable/disable based on app state
- Can't click same action twice
- Visual feedback in output window

## 🎓 Advanced Usage

### Checking Progress Manually
Open `progress.json` in any text editor to see:
```json
{
    "current_index": 150,
    "total_files": 500,
    "input_face": "path/to/face.jpg",
    "input_video": "path/to/video.mp4",
    "input_type": "Single Image",
    "processing_unit": "CPU",
    "timestamp": 1730000000.0
}
```

### Multiple Incomplete Tasks
The system keeps only ONE progress file. Starting a new swap overwrites the old progress.

### Recovery Time
Progress detection runs 1 second after app starts, giving the UI time to load.

## ❓ FAQ

**Q: Can I pause, close the app, and resume later?**  
A: Yes! Just use "Resume from Crash" when you restart.

**Q: Will it re-process frames I already did?**  
A: No! It skips completed frames and continues from where you left off.

**Q: What if I change my mind about the face/video?**  
A: Click "Swap Face" to start fresh with new inputs.

**Q: How long can I pause?**  
A: As long as you want! There's no time limit.

**Q: Is progress saved if my computer crashes?**  
A: Yes! Progress is written to disk after every frame.

**Q: Can I see how many frames are left?**  
A: Yes! Check the output window: "Finished image X of Y"

## 🎉 Enjoy!

No more losing hours of progress due to crashes or interruptions!
Face swap at your own pace, pause when needed, and resume whenever ready.
