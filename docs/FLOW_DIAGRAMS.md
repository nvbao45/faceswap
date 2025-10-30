# Feature Flow Diagrams

## Pause/Resume Flow

```
┌─────────────────────┐
│   Start Face Swap   │
│   (Swap Face btn)   │
└──────────┬──────────┘
           │
           v
┌─────────────────────┐
│  Processing Frame   │◄──────────────┐
│   (Loop through)    │               │
└──────────┬──────────┘               │
           │                          │
           v                          │
    ┌──────────────┐                 │
    │ Save Progress│                 │
    │ after frame  │                 │
    └──────┬───────┘                 │
           │                          │
           v                          │
    ┌──────────────┐     NO          │
    │  User paused?├─────────────────┘
    └──────┬───────┘
           │ YES
           v
    ┌──────────────┐
    │ Wait in loop │
    │ (check pause)│
    └──────┬───────┘
           │
           v
    ┌──────────────┐
    │ User resumed?│
    └──────┬───────┘
           │ YES
           v
    [Continue processing]
```

## Crash Recovery Flow

```
┌─────────────────────┐
│   App Starts        │
└──────────┬──────────┘
           │
           v
┌─────────────────────┐
│ Check for progress  │
│   file (1s delay)   │
└──────────┬──────────┘
           │
           v
    ┌──────────────┐
    │Progress file │
    │  exists?     │
    └──────┬───────┘
           │
      ┌────┴────┐
      │         │
     YES       NO
      │         │
      v         v
┌─────────┐   [Normal
│ Display │    Start]
│ Notice  │
└─────┬───┘
      │
      v
┌─────────────────────┐
│  User clicks        │
│ Resume from Crash   │
└──────────┬──────────┘
           │
           v
┌─────────────────────┐
│  Load settings from │
│   progress file     │
└──────────┬──────────┘
           │
           v
┌─────────────────────┐
│  Skip processed     │
│  frames, continue   │
│  from last index    │
└──────────┬──────────┘
           │
           v
    [Normal processing]
```

## Progress File Lifecycle

```
Event                    Action                     Progress File
─────────────────────────────────────────────────────────────────
App Start                Check for file             Read if exists
                                                    ↓
User clicks              Clear old progress         Delete file
"Swap Face"                                         ↓
(fresh start)                                       
                                                    
Frame 1 processed        Save progress              Create/Write
                         (index: 1)                 ↓
                                                    
Frame 2 processed        Save progress              Update
                         (index: 2)                 ↓
                                                    
...                      ...                        ...
                                                    ↓
User pauses              Save progress              Update
                         (current index)            ↓
                                                    
User resumes             Read progress              Read
                         (continue from index)      ↓
                                                    
...                      ...                        ...
                                                    ↓
All frames done          Clear progress             Delete file
                                                    
─────────────────────────────────────────────────────────────────
If crash occurs:         Progress remains           File persists
App restart              Display notice             ↓
User clicks              Read and continue          Read, then
"Resume from Crash"      from saved index          continue updating
```

## Button State Transitions

```
                    ┌──────────────┐
                    │     IDLE     │
                    │              │
                    │ [Swap Face]  │
                    │ [Resume Crash]│
                    └──────┬───────┘
                           │
                    Click Swap Face
                    or Resume Crash
                           │
                           v
                    ┌──────────────┐
                    │   RUNNING    │
                    │              │
                    │ [Pause Swap] │
                    └──────┬───────┘
                           │
                    Click Pause Swap
                           │
                           v
                    ┌──────────────┐
                    │    PAUSED    │
                    │              │
                    │[Resume Swap] │
                    └──────┬───────┘
                           │
                    Click Resume Swap
                           │
                           v
                    ┌──────────────┐
                    │   RUNNING    │
                    │              │
                    │ [Pause Swap] │
                    └──────┬───────┘
                           │
                    All frames done
                    or error occurs
                           │
                           v
                    ┌──────────────┐
                    │     IDLE     │
                    │              │
                    │ [Swap Face]  │
                    │ [Resume Crash]│
                    └──────────────┘
```

## Key Implementation Details

### Thread Safety
- Main processing runs in separate thread
- GUI updates use `root.after()` for thread safety
- State variables (`is_paused`, `is_running`) checked in loop

### Progress Persistence
- JSON format for human readability
- Saved after EVERY frame (not just on pause)
- Includes timestamp for freshness check (7 days)

### Resume Logic
```python
for index, file in enumerate(files):
    # Skip already processed frames
    if index < start_index:
        continue
    
    # Process current frame
    # ...
```

### Pause Check
```python
# Check if paused
while self.is_paused and self.is_running:
    time.sleep(0.1)  # Small sleep to prevent CPU spinning
```

This allows:
- Responsive pause (checks every 0.1 seconds)
- Low CPU usage during pause
- Clean resume without missing frames
