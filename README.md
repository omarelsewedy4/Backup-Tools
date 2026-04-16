# Intelligent Backup Storage Management System

**Self-Purge** - An automated, intelligent backup drive cleanup utility with GUI integration and safety features.

## Overview

This Python script monitors your backup drive's free space and automatically removes the oldest backup files/folders when storage falls below a defined threshold. It's designed to maintain disk health and prevent performance degradation from running out of space.

## Features

✅ **Interactive GUI** - Folder selection dialog with user-friendly interface  
✅ **Smart Cleanup** - Deletes oldest files/folders first (creation date-based)  
✅ **Dry-Run Mode** - Preview deletions without actually removing files  
✅ **Exception Handling** - Gracefully handles file-in-use and permission errors  
✅ **Comprehensive Logging** - Full audit trail of all operations  
✅ **Safety Buffer** - Maintains extra free space to prevent disk thrashing  
✅ **Dynamic Drive Detection** - Automatically extracts drive letter from selected path  
✅ **User Feedback** - Real-time status messages and operation results  

## Requirements

- Python 3.6+
- `psutil` library (for disk usage monitoring)
- tkinter (usually included with Python)

## Installation

1. Clone or download this repository:
```bash
git clone <your-repo-url>
cd backup-self-purge
```

2. Install required dependency:
```bash
pip install psutil
```

## Configuration

Edit the top section of `backup_self_purge.py` to customize thresholds:

```python
# Space threshold settings (in GB and percentage)
MINIMUM_FREE_SPACE_GB = 20          # Fixed threshold
MINIMUM_FREE_SPACE_PERCENT = 10     # Percentage-based threshold (whichever is larger)
SAFETY_BUFFER_GB = 5                # Extra buffer to maintain

# Operational settings - Easy to toggle
DRY_RUN = True                      # True = Preview only, False = Actually delete
ENABLE_CLEANUP = True               # Master on/off switch
```

## Usage

### Manual Execution

```bash
python backup_self_purge.py
```

**Flow:**
1. GUI folder selection dialog opens
2. Drive letter automatically detected
3. Current disk status displayed
4. User confirmation before cleanup
5. Results shown with operation summary

### Schedule Automated Runs (Windows Task Scheduler)

1. Open **Task Scheduler**
2. Create Basic Task → "Backup Cleanup"
3. Trigger: Daily at 2:00 AM (or your preferred time)
4. Action: Start program `python` with arguments `C:\path\to\backup_self_purge.py`
5. Set `DRY_RUN = False` if you want automatic deletions

### Linux Cron Job

Add to crontab (`crontab -e`):
```bash
# Run backup cleanup daily at 2 AM
0 2 * * * /usr/bin/python3 /path/to/backup_self_purge.py
```

## How It Works

### 1. Folder Selection
- Opens GUI dialog for user to select backup folder
- Automatically extracts drive letter (e.g., "D:" from "D:\Backups")

### 2. Space Monitoring
- Checks current free space against threshold
- Uses larger value: fixed GB threshold OR percentage-based threshold
- Includes safety buffer calculation

### 3. Smart Cleanup (if triggered)
- Lists all items in backup folder
- Sorts by creation date (oldest first)
- Iteratively deletes oldest items until threshold + buffer is reached
- Handles file-in-use errors gracefully

### 4. Logging & Reporting
- All operations logged to `backup_purge.log`
- Console output for real-time monitoring
- GUI messages for user feedback

## Dry-Run Mode

**Before running actual deletions, always test with Dry-Run mode enabled:**

```python
DRY_RUN = True  # Preview what would be deleted
```

Output will show: `[DRY RUN] Would delete: backup_2024_01.zip (15.32GB)`

## Log File

Operations are logged to `backup_purge.log` with timestamp and detail level:

```
2026-04-16 02:15:33 - INFO - Backup self-purge system started (Interactive Mode)
2026-04-16 02:15:34 - INFO - User selected backup folder: D:\Backups
2026-04-16 02:15:34 - INFO - Detected drive letter: D:
2026-04-16 02:15:35 - INFO - Disk Status: 18.50GB free (12.1%) | Threshold: 20.00GB
2026-04-16 02:15:36 - INFO - Deleted file: backup_2024_01.zip (15.32GB)
2026-04-16 02:15:40 - INFO - Target space reached: 23.45GB free (Target: 25.00GB)
```

## Error Handling

The script handles common issues gracefully:

- **File in use** → Skipped with warning, continues to next item
- **Permission denied** → Logged and skipped
- **Drive not accessible** → Error message shown, operation halts
- **Invalid path** → Validation with user feedback

## Safety Features

✅ **Dry-Run Mode** - See exactly what will be deleted first  
✅ **Safety Buffer** - Prevents aggressive space recovery  
✅ **Threshold Filtering** - Respects both GB and percentage minimums  
✅ **Exception Handling** - Won't crash if a file is locked  
✅ **Full Logging** - Complete audit trail of all actions  
✅ **User Confirmation** - Asks for approval before deleting  

## Troubleshooting

### "psutil module not found"
```bash
pip install psutil
```

### Script doesn't start on Windows
Ensure Python is in your PATH:
```bash
python --version  # Should display version
```

### Drive letter not detected
- Ensure you're selecting a valid Windows path (not UNC network paths)
- The path must be on a mounted drive (C:, D:, E:, etc.)

### Permission denied errors
- Run as Administrator if needed
- Ensure the backup folder is not locked by another process
- Check file/folder permissions

## Development

### Code Structure

```
backup_self_purge.py
├── Configuration
├── Logging Setup
├── GUI Functions
│   ├── extract_drive_letter()
│   ├── select_backup_folder()
│   └── show_status_message()
├── Disk Monitoring
│   ├── get_disk_usage()
│   └── check_space_threshold()
├── Backup Management
│   ├── get_backup_items()
│   └── delete_item()
├── Cleanup Orchestration
│   └── perform_cleanup()
└── Main Execution
    └── main()
```

### Contributing

Feel free to submit issues and enhancement requests!

### Future Enhancements

- [ ] Configuration file support (.ini/.json)
- [ ] Email notifications on cleanup completion
- [ ] Filtering options (exclude certain file types)
- [ ] Scheduling integration
- [ ] Web dashboard for monitoring
- [ ] Multi-drive support

## License

MIT License - feel free to use and modify for your needs

## Author

Automated Backup Manager System  
Created: April 2026

---

**Note:** Always test in dry-run mode first before enabling automatic deletions!
