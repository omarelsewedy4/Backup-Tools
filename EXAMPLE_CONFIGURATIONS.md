# EXAMPLE CONFIGURATIONS - WHITELIST & PRIORITY CLEANUP

## Configuration Templates for Real-World Scenarios

Copy and paste these examples into your `backup_self_purge.py` file to get started quickly!

---

## EXAMPLE 1: Home User - Protect Photos & Documents

Scenario: Personal backup drive with photos, documents, and old backups.
Goal: Clean oldest backups first, NEVER delete photo library or active projects.

```python
# WHITELIST: Items to NEVER delete
WHITELIST_NAMES = [
    "Family_Photos_Master",     # Most important - full resolution originals
    "Documents_2025",           # Current year documents
    "Active_Projects",          # Current work in progress
    "Encryption_Keys",          # Critical - can't recover if lost
    "README.txt",               # Personal backup notes
]

# PRIORITY_FOLDERS: Clean these FIRST
PRIORITY_FOLDERS = [
    "trash_old_files",          # Step 1: Obvious trash
    "failed_backups",           # Step 2: Failed attempts
    "_temp_storage",            # Step 3: Temporary staging
    "backups_2023",             # Step 4: Year-old backups
    "backups_old",              # Step 5: Old backups
]
```

**Behavior:**
- Protects: Photos, current documents, active projects, encryption keys
- Cleans first: Trash → failed attempts → temp → old 2023 backups → general old stuff
- Safe for: Running weekly with DRY_RUN = False

---

## EXAMPLE 2: Small Business - Database Backups

Scenario: Daily SQL database backups + incremental backups + test restores.
Goal: Keep current & monthly backups, clean test/staging first.

```python
# WHITELIST: Items to NEVER delete
WHITELIST_NAMES = [
    "Daily_Backup_Latest",      # Today's backup - absolutely critical
    "Monthly_Archive_2025-01",  # January monthly archive
    "Monthly_Archive_2025-02",  # February monthly archive
    "Monthly_Archive_2025-03",  # March monthly archive
    "Database_Schema",          # Schema documentation
    "Recovery_Instructions",    # How to restore
]

# PRIORITY_FOLDERS: Clean these FIRST
PRIORITY_FOLDERS = [
    "test_restores",            # Step 1: Test restore attempts (safe to delete)
    "staging_area",             # Step 2: Testing/staging area
    "restore_logs",             # Step 3: Restore attempt logs
    "incremental_old",          # Step 4: Old incremental backups
    "temporary_extracts",       # Step 5: Temporary extract files
]
```

**Behavior:**
- Protects: Today's backup + monthly archives + documentation
- Cleans first: Test attempts → staging → logs → old incremental → temp extracts
- Safe for: Running nightly as scheduled task

---

## EXAMPLE 3: Media Professional - Video Production

Scenario: Large video files, proxy files, rendered versions, originals.
Goal: Keep originals & finals, clean proxies and temp renders first.

```python
# WHITELIST: Items to NEVER delete
WHITELIST_NAMES = [
    "Original_Footage",         # Master originals - irreplaceable
    "Final_Deliverables",       # Client-delivered versions
    "Color_Grade_Masters",      # Color-corrected master files
    "Master_Audio",             # High-quality audio masters
    "Project_Archives_2025",    # Archived completed projects
]

# PRIORITY_FOLDERS: Clean these FIRST
PRIORITY_FOLDERS = [
    "proxy_files",              # Step 1: Low-res proxy for editing (recreatable)
    "render_cache",             # Step 2: Render cache files (recreatable)
    "temp_exports",             # Step 3: Temporary export attempts
    "old_renders",              # Step 4: Old render versions
    "project_working_copies",   # Step 5: Working copy projects (if desperate)
]
```

**Behavior:**
- Protects: Original footage, finals, masters, archives
- Cleans first: Proxies → render cache → temp exports → old renders → working copies
- Safe for: Running weekly, all cleaned items are recreatable

---

## EXAMPLE 4: System Administrator - Server Backups

Scenario: Multiple server backups, daily incrementals, verification logs.
Goal: Keep full backups and recent incrementals, clean old logs & test restores.

```python
# WHITELIST: Items to NEVER delete
WHITELIST_NAMES = [
    "Server_A_Full_Latest",     # Most recent full backup - Server A
    "Server_B_Full_Latest",     # Most recent full backup - Server B
    "Weekly_Full_Archive",      # Weekly consolidated backup
    "Compliance_Snapshots",     # For auditing/compliance
    "Backup_Verification_OK",   # Successfully verified backups
]

# PRIORITY_FOLDERS: Clean these FIRST
PRIORITY_FOLDERS = [
    "test_environment",         # Step 1: Test restoration environment
    "verification_logs",        # Step 2: Old verification logs
    "failed_backups",           # Step 3: Failed backup attempts
    "incremental_old",          # Step 4: Very old incremental backups
    "temporary_staging",        # Step 5: Temporary staging area
]
```

**Behavior:**
- Protects: Latest full backups from each server, weekly archive, compliance data
- Cleans first: Test env → old logs → failed attempts → old incrementals → staging
- Safe for: Automated daily/weekly cleanup with alerts on errors

---

## EXAMPLE 5: Developer - Git/Code Backups

Scenario: GitHub repos backup, build artifacts, dependency caches, old releases.
Goal: Keep latest code backups, clean build artifacts & old releases first.

```python
# WHITELIST: Items to NEVER delete
WHITELIST_NAMES = [
    "repositories_master",      # Active repositories
    "current_stable_release",   # Current stable version
    "release_2025.Q1",          # Q1 2025 release
    "SOURCE_CONTROL_BACKUP",    # Git backup manifest
]

# PRIORITY_FOLDERS: Clean these FIRST
PRIORITY_FOLDERS = [
    "build_artifacts",          # Step 1: Can be rebuilt from source
    "node_modules_backup",      # Step 2: Can be reinstalled
    "pip_cache",                # Step 3: Can be redownloaded
    "old_releases_2024",        # Step 4: superseded by 2025 releases
    "beta_versions",            # Step 5: Non-production versions
]
```

**Behavior:**
- Protects: Active repositories, current & Q1 releases, source control backup
- Cleans first: Build artifacts → modules → cache → 2024 releases → beta versions
- Safe for: Running daily, all temp items are recreatable

---

## EXAMPLE 6: Conservative Approach - Maximum Protection

Scenario: Critical data that's harder to replace.
Goal: Minimize risk of accidental deletion.

```python
# WHITELIST: Items to NEVER delete (Very protective)
WHITELIST_NAMES = [
    "CRITICAL_SYSTEM_BACKUP",
    "Insurance_Documents",
    "Financial_Records",
    "Medical_Records",
    "Legal_Documents",
    "Irreplaceable_Photos",
    "Family_Videos_Master",
    "Encryption_Keys",
    "Password_Backup",
    "Important_Contracts",
]

# PRIORITY_FOLDERS: Clean these FIRST (Very aggressive on temp)
PRIORITY_FOLDERS = [
    "_temp_staging",            # Step 1: Temporary staging
    "_cache_files",             # Step 2: Cache files
    "downloads_old",            # Step 3: Old downloads
    "working_copies",           # Step 4: Working copies
    "previews",                 # Step 5: Preview versions
]
```

**Behavior:**
- Protects: 10 critical categories
- Cleans first: Temp staging → cache → old downloads → working copies → previews
- Safe for: Drives with mission-critical data, very conservative

---

## EXAMPLE 7: Aggressive Approach - Space Recovery

Scenario: Drive running critically low on space.
Goal: Free up space fast, but protect essentials.

```python
# WHITELIST: Items to NEVER delete (Minimal - only essentials)
WHITELIST_NAMES = [
    "Current_Database",         # Current database in use
    "License",                  # Can't replace license file
]

# PRIORITY_FOLDERS: Clean these FIRST (Aggressive - many temp folders)
PRIORITY_FOLDERS = [
    "temp",
    "cache",
    "downloads",
    "staging",
    "test_data",
    "logs",
    "old_backups",
    "archive",
    "obsolete",
]
```

**Behavior:**
- Protects: Only 2 essential items
- Cleans first: 9 priority folders in order
- Aggressive: Deletes lots when space is truly critical
- Safe for: Emergency space recovery (use with DRY_RUN first!)

---

## EXAMPLE 8: Tiered Backup Strategy

Scenario: Implementing backup tiers - daily, weekly, monthly, yearly.
Goal: Keep recent & milestone backups, clean intermediate tiers first.

```python
# WHITELIST: Items to NEVER delete
WHITELIST_NAMES = [
    "Daily_Latest",             # Today's backup
    "Weekly_Latest",            # This week's backup
    "Monthly_2025_03",          # March monthly archive
    "Yearly_2025",              # 2025 yearly archive
    "Recovery_Master",          # Master recovery/configuration
]

# PRIORITY_FOLDERS: Clean these FIRST (Oldest tiers first)
PRIORITY_FOLDERS = [
    "daily_old_2wks",           # Step 1: 2+ week old daily backups
    "daily_old_1month",         # Step 2: 1+ month old daily backups
    "weekly_old_1month",        # Step 3: 1+ month old weekly backups
    "weekly_old_3months",       # Step 4: 3+ month old weekly backups
    "monthly_old_6months",      # Step 5: 6+ month old monthly backups
]
```

**Behavior:**
- Protects: Latest daily/weekly + milestones (monthly/yearly)
- Cleans first: Old daily → older daily → old weekly → older weekly → old monthly
- Preserves: Tiered backup architecture, cleans most expendable first
- Safe for: Sophisticated backup rotation strategies

---

## EXAMPLE 9: Cloud Storage Sync - Keep Recent, Clean Sync Cache

Scenario: Cloud storage backup with sync caches and temporary files.
Goal: Keep recent backups, clean sync artifacts & temp files.

```python
# WHITELIST: Items to NEVER delete
WHITELIST_NAMES = [
    "Cloud_Sync_Master",        # Master copy of synced data
    "Last_Successful_Sync",     # Last known good sync
    "Sync_Configuration",       # Sync settings/configuration
    "Encryption_Keys_Cloud",    # Cloud encryption keys
]

# PRIORITY_FOLDERS: Clean these FIRST
PRIORITY_FOLDERS = [
    ".sync_cache",              # Step 1: Sync cache (recreated automatically)
    ".temp_uploads",            # Step 2: Temporary upload area
    ".failed_syncs",            # Step 3: Failed sync attempts
    "old_sync_versions",        # Step 4: Old sync versions
    "conflicted_copies",        # Step 5: Sync conflict copies
]
```

**Behavior:**
- Protects: Master data, last good sync, config, encryption keys
- Cleans first: Cache → temp uploads → failed syncs → old versions → conflicts
- Safe for: Cloud sync backup systems

---

## EXAMPLE 10: Empty Configuration - Full Auto Mode

Scenario: Want automation but no special protection or priorities.
Goal: Simple auto-cleanup of everything by age.

```python
# WHITELIST: No special protection
WHITELIST_NAMES = [
    # Nothing - everything can be deleted
]

# PRIORITY_FOLDERS: No special priorities
PRIORITY_FOLDERS = [
    # Nothing - delete by creation date everywhere
]
```

**Behavior:**
- Protects: Nothing (use only if all backups are permanent)
- Cleans: Everything by creation date (oldest first)
- Safe for: Non-critical backup directories only

---

## How to Use These Examples

### Step 1: Choose Your Scenario
Find the example that matches your situation best (or combine elements from multiple).

### Step 2: Copy to Your Script
Open `backup_self_purge.py` and replace the WHITELIST_NAMES and PRIORITY_FOLDERS sections.

### Step 3: Customize Names
Replace example folder/file names with YOUR actual names:

```python
# WRONG (from example):
WHITELIST_NAMES = ["Family_Photos_Master"]

# CORRECT (your actual folder):
WHITELIST_NAMES = ["My_Backup_Folder"]
```

### Step 4: Test with DRY_RUN
Set `DRY_RUN = True` and run once to preview:

```python
DRY_RUN = True  # Preview mode
```

### Step 5: Review Logs
Check `backup_purge.log` to verify behavior matches expectations.

### Step 6: Enable Production
When satisfied:

```python
DRY_RUN = False  # Actually delete files
```

---

## Mixing Scenarios

You can combine elements from different examples:

**Example: Home User + Small Business**
```python
WHITELIST_NAMES = [
    "Family_Photos_Master",     # From Example 1
    "Daily_Backup_Latest",      # From Example 2
    "Documents_2025",           # From Example 1
]

PRIORITY_FOLDERS = [
    "test_restores",            # From Example 2
    "temp_staging",             # From Example 1
]
```

---

## Testing Your Configuration

```bash
# Step 1: Set dry-run mode
# Edit backup_self_purge.py and set: DRY_RUN = True

# Step 2: Run the script
python backup_self_purge.py

# Step 3: Select your backup folder (GUI)

# Step 4: Review output
# - Check console messages
# - Check backup_purge.log for:
#   - WHITELISTED items (should see expected items)
#   - PRIORITY folders being processed
#   - Total items protected by whitelist

# Step 5: Verify results looked correct

# Step 6: If satisfied, enable production
# Edit backup_self_purge.py and set: DRY_RUN = False
```

---

## Troubleshooting Configuration

| Issue | Solution |
|-------|----------|
| Whitelist not working | Check exact spelling (case-sensitive) |
| Priority folders not cleaned first | Verify folder names exist in your backup |
| Too many items protected | Remove unnecessary items from WHITELIST |
| Not enough space freed | Add more folders to PRIORITY_FOLDERS |
| Unsure what to protect | Default: Current + Monthly + Critical data |

---

## Next Steps

1. **Choose an example** that matches your situation
2. **Customize** the file/folder names to match your backup structure
3. **Test** with `DRY_RUN = True`
4. **Review** logs to confirm behavior
5. **Enable** production with `DRY_RUN = False`
6. **Schedule** the script for automated runs

For detailed explanations, see **WHITELIST_PRIORITY_GUIDE.md**
