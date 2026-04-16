# WHITELIST & PRIORITY CLEANUP CONFIGURATION GUIDE

## Overview

The updated backup self-purge system includes two powerful control features:

1. **WHITELIST** - Protect important files/folders from ever being deleted
2. **PRIORITY_FOLDERS** - Clean specific folders first before the rest

---

## WHITELIST Configuration

### What is a Whitelist?

A whitelist is a list of file or folder names that are **PROTECTED from deletion** regardless of how old they are or how low disk space gets.

### How to Configure

Edit `backup_self_purge.py` around line 58:

```python
WHITELIST_NAMES = [
    "Important_Archive",        # Folder name to protect
    "Current_Backup.zip",       # Specific file to protect
    "README.txt",               # Protect this file
    "Keep_Forever",             # Another protected folder
]
```

### Important Notes

- **Case Sensitive**: `Important` ≠ `important`
- **Exact Names Only**: Match the exact filename/foldername
- **Basename Matching**: The name of the file/folder, not the full path
- **Both Files and Folders**: Works on both individual files and entire folders
- **Protected ALWAYS**: Whitelisted items are NEVER deleted, no exceptions

### How It Works

1. Before deletion, script checks if item name is in WHITELIST_NAMES
2. If whitelisted → Item is SKIPPED entirely
3. If not whitelisted → Normal cleanup logic applies
4. Every whitelist skip is logged with `⊘ WHITELISTED (PROTECTED)` marker

### Example Configurations

**Example 1: Protect Critical Backups**
```python
WHITELIST_NAMES = [
    "System_State_Backup",      # Full system backup
    "Database_Archive",         # Critical database backup
    "Active_Project",           # Current working files
]
```

**Example 2: Protect Specific Files**
```python
WHITELIST_NAMES = [
    "Monthly_Full_Backup_2025.zip",
    "Encrypted_Archive.7z",
    "DO_NOT_DELETE.txt",
]
```

**Example 3: Mixed Files and Folders**
```python
WHITELIST_NAMES = [
    "Offsite_Backup",           # Entire folder protected
    "Recovery.iso",             # Single file protected
    "License_Keys_Backup",      # Another folder
]
```

### Logging Whitelist Events

Check `backup_purge.log` for whitelist activity:

```
2026-04-16 14:23:15 - INFO - ⊘ WHITELISTED (PROTECTED): Important_Archive
2026-04-16 14:23:16 - INFO - ⊘ WHITELISTED (PROTECTED): Current_Backup.zip
2026-04-16 14:23:17 - INFO - Skipped 2 whitelisted items during scan
```

---

## PRIORITY_FOLDERS Configuration

### What are Priority Folders?

Priority folders are cleaned **FIRST** before the rest of the backup directory. This allows you to:
- Clean expendable temporary files first
- Save critical folders for later
- Implement a staged cleanup strategy

### How to Configure

Edit `backup_self_purge.py` around line 66:

```python
PRIORITY_FOLDERS = [
    "_old_backups",             # Clean this folder first
    "cache",                    # Then clean this folder
    "temp_files",               # Then this folder
    "archived",                 # Finally this folder (if still needed)
]
```

### Important Notes

- **Folder Names Only**: Must be subfolders within your BACKUP_FOLDER
- **Order Matters**: Listed in order of cleanup priority
- **Respects Whitelist**: Items in PRIORITY_FOLDERS still respect WHITELIST_NAMES
- **Oldest First**: Within each priority folder, oldest items deleted first

### How It Works

**Cleanup Process:**

```
Step 1: Check PRIORITY_FOLDERS
├─ For each priority folder (in order):
│  ├─ Get all items in that folder
│  ├─ Skip whitelisted items
│  └─ Delete oldest items first until space is OK

Step 2: If space still low, clean other folders
├─ Get all items from root backup folder
├─ Exclude items already in priority folders
├─ Skip whitelisted items
└─ Delete oldest items first until space is OK

Step 3: Stop when space threshold is reached
```

### Example Configurations

**Example 1: Clean Temp Files First**
```python
PRIORITY_FOLDERS = [
    "temp_files",               # 1st priority: temporary data
    "cache",                    # 2nd priority: cached data
    "old_metadata",             # 3rd priority: old metadata
]
```

**Example 2: Clean Old Backups First**
```python
PRIORITY_FOLDERS = [
    "_old_backups",             # 1st: outdated complete backups
    "_incremental_old",         # 2nd: old incremental backups
    "_compressed_archive",      # 3rd: compressed archives
]
```

**Example 3: Staged Cleanup Strategy**
```python
PRIORITY_FOLDERS = [
    "staging_area",             # 1st: incomplete/test backups
    "duplicates",               # 2nd: known duplicate backups
    "pre_2024",                 # 3rd: older than 2024
    "daily_backups",            # 4th: daily incremental backups (if desperate)
]
```

### Logging Priority Folder Activity

Check `backup_purge.log` to see priority cleanup in action:

```
2026-04-16 14:25:00 - INFO - Priority Folders: ['temp_files', 'cache']
2026-04-16 14:25:01 - INFO - STEP 1: Cleaning priority folders: ['temp_files', 'cache']
2026-04-16 14:25:01 - INFO - Scanning priority folder: temp_files
2026-04-16 14:25:02 - INFO - Found 5 items in priority folders
2026-04-16 14:25:03 - INFO - Processing (PRIORITY): old_temp_data.zip (Created: 2026-03-01, Size: 8.50GB)
2026-04-16 14:25:04 - INFO - Deleted file: old_temp_data.zip (8.50GB)
2026-04-16 14:25:05 - INFO - Target space reached during priority cleanup: 25.00GB free
2026-04-16 14:25:05 - INFO - STEP 2: Cleaning regular items (excluding priority folders)
```

---

## Combined Usage Examples

### Example 1: Protect Active Backups, Clean Old Temp Files First

```python
WHITELIST_NAMES = [
    "Current_Full_Backup",      # Never delete current backup
    "Active_Database",          # Never delete active database
    "Production_Files",         # Never delete production data
]

PRIORITY_FOLDERS = [
    "temp_staging",             # Clean temporary files first
    "_old_daily",               # Then old daily backups
]
```

**Behavior:**
1. First deletes oldest files from `temp_staging` folder
2. Then deletes oldest files from `_old_daily` folder
3. If still low, deletes oldest from other folders
4. NEVER touches `Current_Full_Backup`, `Active_Database`, or `Production_Files`

### Example 2: Clean Metadata First, Protect All 2025 Backups

```python
WHITELIST_NAMES = [
    "2025-01-Full.zip",
    "2025-02-Full.zip",
    "2025-03-Full.zip",
    "Security_Keys_Backup",
]

PRIORITY_FOLDERS = [
    "metadata",                 # Clean metadata first
    "logs",                     # Then logs
]
```

**Behavior:**
1. Prioritizes deletion from `metadata` and `logs` folders
2. Protects all 2025 backups and security keys from deletion
3. Implements tiered cleanup: metadata → logs → everything else

### Example 3: Aggressive Cleanup with Safeguards

```python
WHITELIST_NAMES = [
    "CRITICAL_BACKUP",          # Absolutely protect
    "License_Info",             # Protect license info
]

PRIORITY_FOLDERS = [
    "temp",
    "cache",
    "old_2024",
    "offline_copies",
]
```

**Behavior:**
1. Aggressively cleans temporary and cached data first
2. Progresses through priority folders in order
3. Only protects 2 critical items
4. Good for drives that are frequently tight on space

---

## Best Practices

### DO:
✅ Use WHITELIST for truly critical data  
✅ Use PRIORITY_FOLDERS for temp/cache locations  
✅ Test with DRY_RUN = True first  
✅ Review the log file after each run  
✅ Keep backup copies of whitelisted data elsewhere  
✅ Document WHY items are whitelisted  
✅ Update lists as your backup strategy changes  

### DON'T:
❌ Whitelist everything (defeats cleanup purpose)  
❌ Use PRIORITY_FOLDERS for mission-critical data (that's what WHITELIST is for)  
❌ Set DRY_RUN = False without testing first  
❌ Ignore the log file  
❌ Keep whitelisted items only on this drive  
❌ Forget to update lists when backup structure changes  

---

## Monitoring & Debugging

### Check Whitelist Protection

In `backup_purge.log`, look for:
```
⊘ WHITELISTED (PROTECTED): <item_name>
```

This shows items being protected by the whitelist.

### Check Priority Cleanup

In `backup_purge.log`, look for:
```
Processing (PRIORITY): <item_name>
Processing (REGULAR): <item_name>
```

PRIORITY items are deleted first, then REGULAR items.

### Verify Settings at Startup

The log shows your configuration at startup:
```
2026-04-16 14:25:00 - INFO - Priority Folders: ['temp', 'cache']
2026-04-16 14:25:00 - INFO - Whitelisted Items: 3
```

### Disable Features Temporarily

To temporarily disable whitelist:
```python
WHITELIST_NAMES = []  # Empty list = no protection
```

To disable priority folders:
```python
PRIORITY_FOLDERS = []  # Empty list = no priority
```

---

## Troubleshooting

### Items Are Still Being Deleted (Not Protected)

**Problem:** A whitelisted item was deleted anyway

**Solutions:**
1. Check item NAME matches EXACTLY (case-sensitive)
2. Verify it's the basename, not full path
3. Check logs for typos in WHITELIST_NAMES
4. Ensure DRY_RUN = True to test changes

### Priority Folders Are Not Being Cleaned First

**Problem:** Regular items deleted before priority items

**Solutions:**
1. Verify priority folder NAMES match exactly
2. Ensure folders exist in your BACKUP_FOLDER
3. Check logs for "Priority folder not found" warnings
4. Verify path structure with DRY_RUN mode first

### Too Many Items Being Protected

**Problem:** Cleanup not freeing enough space

**Solutions:**
1. Review WHITELIST_NAMES - is everything really critical?
2. Move non-critical items from whitelist
3. Use PRIORITY_FOLDERS to clean temp/cache first
4. Increase MINIMUM_FREE_SPACE_GB if cleanup is too conservative

### Not Enough Items Being Cleaned

**Problem:** Priority folders empty or too small

**Solutions:**
1. Check if priority folder paths are correct
2. Verify items exist in those folders
3. Use DRY_RUN to preview what would be deleted
4. Check backup_purge.log for detailed cleanup steps

---

## Migration Guide

### Upgrading from Old Script

If you're upgrading from the basic version:

1. Add to your config (around line 58):
   ```python
   WHITELIST_NAMES = [
       # Add items here
   ]
   
   PRIORITY_FOLDERS = [
       # Add items here
   ]
   ```

2. Test with DRY_RUN = True first

3. Review logs to ensure behavior is as expected

4. Gradually enable actual cleanup (DRY_RUN = False)

---

## Real-World Scenarios

### Scenario 1: Home Backup Drive

```python
WHITELIST_NAMES = [
    "Active_Project_2025",
    "Family_Photos_Master",
    "Encrypted_Vault",
]

PRIORITY_FOLDERS = [
    "temp_staging",
    "failed_backups",
    "old_browser_cache",
]
```

Clean temp data → keep critical personal files

### Scenario 2: Business Backup Server

```python
WHITELIST_NAMES = [
    "Current_Daily_Backup",
    "Monthly_Archive_2025",
    "Database_Snapshot",
    "Compliance_Records",
]

PRIORITY_FOLDERS = [
    "temp_restores",
    "failed_attempts",
    "old_logs",
    "compressed_archives",
]
```

Protect current/compliance data → clean test/log files first

### Scenario 3: Media Archive

```python
WHITELIST_NAMES = [
    "Originals",
    "Mastered_Final",
    "License_Info",
]

PRIORITY_FOLDERS = [
    "working_copies",
    "rendered_preview",
    "proxy_files",
    "old_versions",
]
```

Protect originals → clean working/preview files first

---

## Advanced Configuration

### Dynamic Whitelist (Optional Enhancement)

You could create a separate file with whitelisted items:

```python
# whitelist.txt format (one item per line)
Current_Backup
Critical_Data
Important_Project
```

Then load it:
```python
with open('whitelist.txt', 'r') as f:
    WHITELIST_NAMES = [line.strip() for line in f if line.strip()]
```

### Weighted Priority (Optional Future Feature)

Consider adding numeric priorities to folders:

```python
# Future enhancement
PRIORITY_FOLDERS = [
    ("temp", 1),        # Highest priority (delete first)
    ("cache", 2),
    ("logs", 3),
    ("old_backups", 4), # Lowest priority (delete last)
]
```

---

## Summary

| Feature | Purpose | How to Use |
|---------|---------|-----------|
| WHITELIST_NAMES | Protect critical items | Add names to list |
| PRIORITY_FOLDERS | Clean specific folders first | Add folder names in order |
| DRY_RUN | Preview without deleting | Set to True for testing |
| Logging | Track all actions | Check backup_purge.log |

**Next Steps:**
1. Define what's critical (→ WHITELIST)
2. Identify temp/cache locations (→ PRIORITY_FOLDERS)
3. Test with DRY_RUN = True
4. Review logs and enable actual cleanup
5. Schedule automated runs

---

**Questions? Check the main README.md or review backup_purge.log for detailed operation logs.**
