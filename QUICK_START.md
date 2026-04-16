# QUICK START GUIDE

## 30-Second Setup

### Step 1: Install Dependency
```bash
pip install psutil
```

### Step 2: Run the Script
```bash
python backup_self_purge.py
```

### Step 3: Select Your Backup Folder
- Click "Browse" in the GUI dialog
- Select your backup folder (e.g., `D:\Backups`)
- Drive letter is **automatically detected**

### Step 4: Review & Confirm
- Check disk status displayed
- Confirm to proceed with cleanup
- Results shown in popup and console

---

## First Time - Safe Testing

**IMPORTANT:** Always test with dry-run first!

1. Edit `backup_self_purge.py`
2. Verify these settings (around line 50):
   ```python
   DRY_RUN = True              # ✓ Enabled - SAFE to test
   ENABLE_CLEANUP = True       # Cleanup enabled
   ```
3. Run the script
4. Review what would be deleted in the log file
5. Change to `DRY_RUN = False` only when satisfied

---

## What Gets Deleted?

- **Oldest files/folders first** (by creation date)
- **One by one** until space threshold is reached
- **Deleted items:**
  - Individual backup files (*.zip, *.tar, etc.)
  - Backup folders (entire directories)
- **NOT deleted:**
  - Files currently in use (skipped with error)
  - Read-only files (skipped with warning)
  - System/hidden files (treated normally)

---

## GUI Interactions

### 1. Folder Selection Dialog
- Opens when script starts
- Select your backup folder
- Drive is auto-detected from path

### 2. Status Messages
- **Green (Info/Success)**: Operation succeeded
- **Yellow (Warning)**: Issues encountered, check log
- **Red (Error)**: Operation failed, please fix issue

### 3. Confirmation Dialog
- Shows before cleanup starts
- Review thresholds and dry-run status
- Click Yes to proceed, No to cancel

---

## Checking Logs

After each run, review the log file:

```bash
cat backup_purge.log    # Linux/Mac
type backup_purge.log   # Windows
```

**Look for:**
- What was deleted (or would be deleted)
- Any errors/warnings
- Final space status

---

## Scheduling (Optional)

### Windows Task Scheduler
1. Open Task Scheduler
2. Create Basic Task
3. Name: "Daily Backup Cleanup"
4. Trigger: Daily at 2:00 AM
5. Action: Run `python C:\path\to\backup_self_purge.py`
6. Set `DRY_RUN = False` in script

### Run As Administrator:
In Task Scheduler, go to task properties → General → Check "Run with highest privileges"

---

## Common Questions

**Q: Can the script run on multiple drives?**  
A: Run the script once per backup folder (GUI asks you each time)

**Q: What if a file is locked/in use?**  
A: Script skips it and tries the next oldest file. No crash!

**Q: How do I disable cleanup?**  
A: Set `ENABLE_CLEANUP = False` to run in status-only mode

**Q: Can I stop the cleanup mid-process?**  
A: Press Ctrl+C to stop (some deletions may have already occurred)

**Q: Where are deleted files stored?**  
A: They're permanently deleted. The log shows what was removed.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "psutil not found" | Run `pip install psutil` |
| GUI doesn't appear | Ensure tkinter is installed (`pip install tk`) |
| Can't access drive | Check drive letter and permissions |
| Files keep getting skipped | Files may be in use; try restarting services |
| Folder not found error | Verify path exists before running script |

---

## Safety Checklist

- [ ] Tested with `DRY_RUN = True` first
- [ ] Reviewed log file for deleted items
- [ ] Confirmed oldest backups are truly expendable
- [ ] Set reasonable thresholds (don't be too aggressive)
- [ ] Scheduled appropriate time (outside backup windows)
- [ ] Have backup of important data elsewhere
- [ ] Monitored log file after first automated run

---

## Example Run

```
=======================================================
Intelligent Backup Storage Management System
Interactive Mode - GitHub Ready
=======================================================

Opening folder selection dialog...

[User selects D:\Backups]

Disk Status:
  Backup Folder: D:\Backups
  Drive: D:
  Current Free Space: 18.50 GB
  Required Threshold: 20.00 GB
  Status: ⚠️ BELOW THRESHOLD

[User clicks "Yes" to proceed]

Processing: backup_2024_01.zip (Created: 2024-01-15, Size: 15.32GB)
Deleted file: backup_2024_01.zip (15.32GB)

Target space reached: 23.45GB free (Target: 25.00GB)

Cleanup Summary:
  Items Deleted: 1
  Items Skipped: 0
  Space Freed: 15.32 GB
  Status: ✅ SUCCESS

Check 'backup_purge.log' for detailed operation logs
=======================================================
```

---

## Next Steps

1. ✓ Install psutil
2. ✓ Run script once with dry-run
3. ✓ Review logs and confirm changes look good
4. ✓ Toggle `DRY_RUN = False` for production use
5. ✓ Schedule in Task Scheduler for automated runs
6. ✓ Monitor logs periodically

---

**Questions? Check README.md for detailed documentation**
