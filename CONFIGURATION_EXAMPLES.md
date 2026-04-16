# Configuration Examples for Backup Self-Purge
# These are example configurations for different backup scenarios

# ===========================================================================
# EXAMPLE 1: Conservative Backup Cleanup
# ===========================================================================
# Use this for critical backups where you want to keep plenty of free space

MINIMUM_FREE_SPACE_GB = 50          # Keep 50GB minimum free
MINIMUM_FREE_SPACE_PERCENT = 20     # OR 20% of total capacity (whichever is larger)
SAFETY_BUFFER_GB = 10               # Additional 10GB safety margin

DRY_RUN = True                      # Always preview first
ENABLE_CLEANUP = True


# ===========================================================================
# EXAMPLE 2: Aggressive Space Recovery
# ===========================================================================
# Use this for drives constantly running low on space

MINIMUM_FREE_SPACE_GB = 10          # Keep 10GB minimum free
MINIMUM_FREE_SPACE_PERCENT = 5      # OR 5% of total capacity
SAFETY_BUFFER_GB = 2                # Minimal 2GB buffer

DRY_RUN = False                     # Perform actual deletions
ENABLE_CLEANUP = True


# ===========================================================================
# EXAMPLE 3: Balanced Approach (RECOMMENDED for most users)
# ===========================================================================
# Good balance between space recovery and system performance

MINIMUM_FREE_SPACE_GB = 20          # Keep 20GB minimum free
MINIMUM_FREE_SPACE_PERCENT = 10     # OR 10% of total capacity
SAFETY_BUFFER_GB = 5                # 5GB additional buffer

DRY_RUN = True                      # Start with preview mode
ENABLE_CLEANUP = True


# ===========================================================================
# EXAMPLE 4: Large Capacity Drives (2TB+)
# ===========================================================================
# For very large backup drives where percentage makes more sense

MINIMUM_FREE_SPACE_GB = 100         # Keep 100GB minimum
MINIMUM_FREE_SPACE_PERCENT = 15     # OR 15% of total capacity (takes precedence on 2TB drives)
SAFETY_BUFFER_GB = 20               # Large safety buffer for performance

DRY_RUN = True
ENABLE_CLEANUP = True


# ===========================================================================
# EXAMPLE 5: Testing Configuration
# ===========================================================================
# Use this ONLY for testing/development on non-critical data

MINIMUM_FREE_SPACE_GB = 0.5         # Very low threshold for testing
MINIMUM_FREE_SPACE_PERCENT = 1      # 1% threshold
SAFETY_BUFFER_GB = 0.1              # Minimal buffer

DRY_RUN = True                      # MUST use dry-run for testing
ENABLE_CLEANUP = False              # Disable cleanup by default


# ===========================================================================
# RECOMMENDATIONS
# ===========================================================================

# 1. FIRST RUN
# - Use Example 3 (Balanced) with DRY_RUN = True
# - Review what would be deleted in the logs
# - Verify the oldest backups are truly expendable

# 2. SCHEDULED RUNS
# - Use Example 3 (Balanced) with DRY_RUN = False
# - Let it run automatically via Windows Task Scheduler
# - Monitor the log file regularly

# 3. VERY LOW SPACE EMERGENCY
# - Use Example 2 (Aggressive) temporarily
# - Revert to Example 3 after space is recovered

# 4. CRITICAL BACKUPS
# - Use Example 1 (Conservative)
# - Keep DRY_RUN = True for safety
# - Manually review and approve each cleanup session

# ===========================================================================
# DRIVE SIZE GUIDE FOR THRESHOLDS
# ===========================================================================

# 500GB Drive:
#   Conservative: 50GB free (10% of 500GB)
#   Balanced: 20GB free
#   Minimum: 10GB free

# 1TB Drive:
#   Conservative: 100GB free (10% of 1TB)
#   Balanced: 30GB free
#   Minimum: 15GB free

# 2TB Drive:
#   Conservative: 200GB free (10% of 2TB)
#   Balanced: 50GB free
#   Minimum: 25GB free

# 4TB Drive:
#   Conservative: 400GB free (10% of 4TB)
#   Balanced: 80GB free
#   Minimum: 40GB free

# ===========================================================================
# TOGGLING DRY_RUN AND ENABLE_CLEANUP
# ===========================================================================

# DRY_RUN = True
#   Result: Script shows what WOULD be deleted
#   Output: [DRY RUN] Would delete: filename.zip (50.23GB)
#   Safety: No actual deletions occur
#   Use: First run, testing, verification

# DRY_RUN = False
#   Result: Script ACTUALLY deletes files
#   Output: Deleted file: filename.zip (50.23GB)
#   Safety: Files are gone - ensure thresholds are correct!
#   Use: Trusted configurations, scheduled cleanup

# ENABLE_CLEANUP = True
#   Script will perform cleanup if space is below threshold

# ENABLE_CLEANUP = False
#   Script will only report status, NO cleanup performed
#   Use: Testing, monitoring without automatic cleanup
