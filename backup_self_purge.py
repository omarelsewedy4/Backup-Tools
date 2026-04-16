"""
Intelligent Backup Storage Management System - Self-Purge (Interactive)
=========================================================================

This script monitors a backup drive's free space and automatically removes
the oldest backup files/folders when space falls below a defined threshold.

Features:
- Interactive GUI for folder selection
- Real-time free space monitoring
- Threshold-based automated cleanup
- Smart deletion (oldest files first)
- Dry-run mode for safe previewing
- Comprehensive logging
- Exception handling for file-in-use scenarios
- Safety buffer to maintain drive performance
- Dynamic drive letter detection
- User-friendly status messages

Author: Automated Backup Manager
Date: 2026
GitHub: Intelligent Backup Management System
"""

import os
import sys
import shutil
import logging
import time
import winreg
from pathlib import Path
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox
import psutil  # For disk usage information


# ============================================================================
# GLOBAL CONFIGURATION
# ============================================================================

# These can be modified through the GUI or set as defaults
BACKUP_DRIVE = None  # Will be auto-detected from selected folder
BACKUP_FOLDER = None  # Will be selected by user via GUI

# Space threshold settings (in GB and percentage)
MINIMUM_FREE_SPACE_GB = 25
MINIMUM_FREE_SPACE_PERCENT = 10
SAFETY_BUFFER_GB = 5

# Logging configuration
LOG_FILE = "backup_purge.log"
LOG_LEVEL = logging.INFO

# Operational settings - Easy to toggle
DRY_RUN = True  # Start with dry-run enabled for safety
ENABLE_CLEANUP = True

# Background loop settings
CHECK_INTERVAL_MINUTES = 60  # Check disk space every 60 minutes
RUN_IN_BACKGROUND = True  # Enable continuous background monitoring
ENABLE_STARTUP_PERSISTENCE = True  # Add to Windows startup on first run

# ============================================================================
# WHITELIST AND PRIORITY CLEANUP CONFIGURATION
# ============================================================================

# WHITELIST: Files/folders that NEVER get deleted
# Add exact names (case-sensitive) of items you want to protect
WHITELIST_NAMES = [
    # Examples (uncomment and customize as needed):
    # "Important_Archive",        # Folder name to protect
    # "Current_Backup.zip",       # Specific file to protect
    # "README.txt",               # Protect this file
]

# PRIORITY_FOLDERS: Folders to clean FIRST (oldest items first within each)
# Specify folder names within BACKUP_FOLDER that should be cleaned first
PRIORITY_FOLDERS = [
    # Examples (uncomment and customize as needed):
    # "_old_backups",             # Clean this folder first
    # "cache",                    # Then clean this folder
]

# How many items should be whitelisted (for logging)
WHITELIST_COUNT = len(WHITELIST_NAMES)


# ============================================================================
# LOGGING SETUP
# ============================================================================

def setup_logging(log_file, level=logging.INFO):
    """
    Configure logging to both file and console.
    
    Args:
        log_file (str): Path to the log file
        level: Logging level (logging.DEBUG, logging.INFO, etc.)
    
    Returns:
        logging.Logger: Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(__name__)
    logger.setLevel(level)
    
    # Clear existing handlers to prevent duplicates
    logger.handlers.clear()
    
    # Create formatters
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler
    try:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        print(f"Warning: Could not create log file - {e}")
    
    # Console handler (only for non-.pyw files)
    # For .pyw files, this will be silently ignored
    try:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    except Exception as e:
        logger.error(f"Could not setup console handler: {e}")
    
    return logger


logger = setup_logging(LOG_FILE, LOG_LEVEL)


# ============================================================================
# WINDOWS STARTUP PERSISTENCE FUNCTIONS
# ============================================================================

def add_to_windows_startup():
    """
    Add the current script to Windows Startup (Run Key) for automatic execution at boot.
    
    Uses the script's real path to ensure it works regardless of installation location.
    This function should be called once on first execution.
    
    Returns:
        bool: True if successfully added to startup, False otherwise
    """
    try:
        # Get the absolute path to the current script
        script_path = os.path.realpath(sys.argv[0])
        
        if not os.path.exists(script_path):
            logger.error(f"Cannot find script path: {script_path}")
            return False
        
        logger.info(f"Adding script to Windows Startup: {script_path}")
        
        # Open the Windows Registry (HKCU\Software\Microsoft\Windows\CurrentVersion\Run)
        reg_key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_SET_VALUE
        )
        
        # Register the script with a descriptive name
        app_name = "BackupSelfPurge"
        
        # Set the value (run the script with pythonw.exe for .pyw files)
        winreg.SetValueEx(
            reg_key,
            app_name,
            0,
            winreg.REG_SZ,
            f'"{sys.executable}" "{script_path}"'
        )
        
        winreg.CloseKey(reg_key)
        
        logger.info(f"Successfully added '{app_name}' to Windows Startup")
        return True
        
    except PermissionError:
        logger.error("Permission denied: Cannot add to Windows Startup without admin rights")
        return False
    except OSError as e:
        logger.error(f"OS Error while adding to startup: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error adding to startup: {e}")
        return False


def is_in_startup():
    """
    Check if the script is already registered in Windows Startup.
    
    Returns:
        bool: True if script is in startup, False otherwise
    """
    try:
        script_path = os.path.realpath(sys.argv[0])
        reg_key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_READ
        )
        
        # Try to find the script in the registry
        try:
            value, _ = winreg.QueryValueEx(reg_key, "BackupSelfPurge")
            winreg.CloseKey(reg_key)
            return script_path in value
        except FileNotFoundError:
            winreg.CloseKey(reg_key)
            return False
            
    except Exception as e:
        logger.debug(f"Error checking startup status: {e}")
        return False


# ============================================================================
# GUI AND FOLDER SELECTION FUNCTIONS
# ============================================================================

def extract_drive_letter(folder_path):
    """
    Extract the drive letter from a folder path.
    
    Works on Windows paths like "C:\\Users", "D:\\Backups", etc.
    
    Args:
        folder_path (str): Full path to a folder
    
    Returns:
        str: Drive letter with colon (e.g., "D:") or None if extraction fails
    """
    try:
        path_obj = Path(folder_path)
        # On Windows, the drive attribute returns 'C:', 'D:', etc.
        if path_obj.drive:
            return path_obj.drive
        else:
            logger.warning(f"Could not extract drive from path: {folder_path}")
            return None
    except Exception as e:
        logger.error(f"Error extracting drive letter: {e}")
        return None


def select_backup_folder():
    """
    Open a tkinter folder selection dialog for the user to choose the backup folder.
    
    Returns:
        tuple: (backup_folder, drive_letter) or (None, None) if cancelled
    """
    try:
        # Create a hidden root window for tkinter
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        root.attributes('-topmost', True)  # Make dialog appear on top
        
        # Open folder selection dialog
        folder_path = filedialog.askdirectory(
            title="Select Your Backup Folder",
            initialdir=os.path.expanduser("~"),
        )
        
        root.destroy()
        
        if not folder_path:
            logger.info("User cancelled folder selection")
            return None, None
        
        # Extract drive letter from selected path
        drive_letter = extract_drive_letter(folder_path)
        
        if not drive_letter:
            messagebox.showerror(
                "Error",
                f"Could not extract drive letter from path:\n{folder_path}"
            )
            return None, None
        
        logger.info(f"User selected backup folder: {folder_path}")
        logger.info(f"Detected drive letter: {drive_letter}")
        
        return folder_path, drive_letter
    
    except Exception as e:
        logger.error(f"Error in folder selection: {e}")
        messagebox.showerror("Error", f"Error selecting folder:\n{str(e)}")
        return None, None


def show_status_message(title, message, status_type="info"):
    """
    Display a status message to the user using tkinter messagebox.
    Falls back to logging if GUI is not available (e.g., in .pyw mode).
    
    Args:
        title (str): Title of the message box
        message (str): Message content
        status_type (str): Type of message - "info", "success", "warning", or "error"
    """
    try:
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        
        if status_type == "error":
            messagebox.showerror(title, message)
        elif status_type == "warning":
            messagebox.showwarning(title, message)
        elif status_type == "success":
            messagebox.showinfo(title, message)
        else:  # info
            messagebox.showinfo(title, message)
        
        root.destroy()
    except Exception as e:
        # Fallback to logging if GUI fails (common in .pyw windowless mode)
        log_message = f"{title}: {message}"
        if status_type == "error":
            logger.error(log_message)
        elif status_type == "warning":
            logger.warning(log_message)
        else:
            logger.info(log_message)


# ============================================================================
# WHITELIST AND PRIORITY CLEANUP FUNCTIONS
# ============================================================================

def is_whitelisted(item_name):
    """
    Check if an item is in the whitelist and protected from deletion.
    
    Args:
        item_name (str): Name of the file or folder (basename only)
    
    Returns:
        bool: True if item is whitelisted, False otherwise
    """
    return item_name in WHITELIST_NAMES


def log_whitelist_skip(item_name, item_path):
    """
    Log when an item is skipped because it's in the whitelist.
    
    Args:
        item_name (str): Name of the file or folder
        item_path (str): Full path to the item
    """
    message = f"⊘ WHITELISTED (PROTECTED): {item_name}"
    logger.info(message)


def get_backup_items(backup_path, whitelist_enabled=True):
    """
    Get all items (files/folders) in the backup folder sorted by creation date.
    
    Args:
        backup_path (str): Path to the backup folder
        whitelist_enabled (bool): If True, exclude whitelisted items
    
    Returns:
        list: List of tuples (item_path, creation_time, item_size_gb)
              Sorted by creation date (oldest first), excluding whitelisted items
    """
    try:
        if not os.path.exists(backup_path):
            logger.error(f"Backup path does not exist: {backup_path}")
            return []
        
        items = []
        whitelisted_count = 0
        
        for item in os.listdir(backup_path):
            item_path = os.path.join(backup_path, item)
            
            # Check whitelist
            if whitelist_enabled and is_whitelisted(item):
                log_whitelist_skip(item, item_path)
                whitelisted_count += 1
                continue
            
            try:
                # Get creation time (most reliable cross-platform method)
                creation_time = os.path.getctime(item_path)
                creation_datetime = datetime.fromtimestamp(creation_time)
                
                # Get item size
                if os.path.isfile(item_path):
                    size_bytes = os.path.getsize(item_path)
                else:
                    # Calculate folder size recursively
                    size_bytes = sum(
                        os.path.getsize(os.path.join(dirpath, filename))
                        for dirpath, dirnames, filenames in os.walk(item_path)
                        for filename in filenames
                    )
                
                size_gb = size_bytes / (1024**3)
                items.append((item_path, creation_datetime, size_gb))
                
            except Exception as e:
                logger.warning(f"Could not process item {item}: {e}")
                continue
        
        # Sort by creation date (oldest first)
        items.sort(key=lambda x: x[1])
        
        if whitelisted_count > 0:
            logger.info(f"Skipped {whitelisted_count} whitelisted items during scan")
        
        return items
    
    except Exception as e:
        logger.error(f"Error reading backup folder: {e}")
        return []


def get_priority_items(backup_path, priority_folders, whitelist_enabled=True):
    """
    Get items from priority folders sorted by creation date.
    Priority items are cleaned before regular items.
    
    Args:
        backup_path (str): Path to the backup folder
        priority_folders (list): List of folder names to prioritize
        whitelist_enabled (bool): If True, exclude whitelisted items
    
    Returns:
        list: List of tuples (item_path, creation_time, item_size_gb)
              From priority folders only, sorted by creation date (oldest first)
    """
    priority_items = []
    
    try:
        for folder_name in priority_folders:
            folder_path = os.path.join(backup_path, folder_name)
            
            # Check if priority folder exists
            if not os.path.exists(folder_path):
                logger.warning(f"Priority folder not found: {folder_path}")
                continue
            
            if not os.path.isdir(folder_path):
                logger.warning(f"Priority item is not a folder: {folder_path}")
                continue
            
            # Check whitelist for the priority folder itself
            if whitelist_enabled and is_whitelisted(folder_name):
                log_whitelist_skip(folder_name, folder_path)
                continue
            
            logger.info(f"Scanning priority folder: {folder_name}")
            
            # Get items within the priority folder
            try:
                for item in os.listdir(folder_path):
                    item_path = os.path.join(folder_path, item)
                    
                    # Check whitelist
                    if whitelist_enabled and is_whitelisted(item):
                        log_whitelist_skip(item, item_path)
                        continue
                    
                    try:
                        # Get creation time
                        creation_time = os.path.getctime(item_path)
                        creation_datetime = datetime.fromtimestamp(creation_time)
                        
                        # Get item size
                        if os.path.isfile(item_path):
                            size_bytes = os.path.getsize(item_path)
                        else:
                            size_bytes = sum(
                                os.path.getsize(os.path.join(dirpath, filename))
                                for dirpath, dirnames, filenames in os.walk(item_path)
                                for filename in filenames
                            )
                        
                        size_gb = size_bytes / (1024**3)
                        priority_items.append((item_path, creation_datetime, size_gb))
                        
                    except Exception as e:
                        logger.warning(f"Could not process priority item {item}: {e}")
                        continue
            
            except Exception as e:
                logger.warning(f"Error reading priority folder {folder_path}: {e}")
                continue
    
    except Exception as e:
        logger.error(f"Error processing priority folders: {e}")
    
    # Sort by creation date (oldest first)
    priority_items.sort(key=lambda x: x[1])
    
    return priority_items


# ============================================================================
# DISK SPACE MONITORING FUNCTIONS
# ============================================================================

def get_disk_usage(drive_path):
    """
    Get disk usage statistics for a specific drive.
    
    Args:
        drive_path (str): Path to the drive (e.g., "D:")
    
    Returns:
        dict: Dictionary with total, used, and free space in GB and percentages
    """
    try:
        usage = psutil.disk_usage(drive_path)
        
        return {
            'total_gb': usage.total / (1024**3),
            'used_gb': usage.used / (1024**3),
            'free_gb': usage.free / (1024**3),
            'percent_used': usage.percent,
            'percent_free': 100 - usage.percent
        }
    except Exception as e:
        logger.error(f"Error getting disk usage for {drive_path}: {e}")
        return None


def check_space_threshold(drive_path, min_gb, min_percent):
    """
    Check if free space is below the defined threshold.
    
    Args:
        drive_path (str): Path to the drive
        min_gb (float): Minimum free space in GB
        min_percent (float): Minimum free space percentage
    
    Returns:
        tuple: (is_below_threshold, current_free_gb, required_space_gb)
    """
    usage = get_disk_usage(drive_path)
    
    if usage is None:
        return None, None, None
    
    # Calculate threshold based on percentage
    percent_threshold_gb = (usage['total_gb'] * min_percent) / 100
    
    # Use the larger threshold (percentage-based or fixed)
    effective_threshold = max(min_gb, percent_threshold_gb)
    
    is_below = usage['free_gb'] < effective_threshold
    
    logger.info(
        f"Disk Status: {usage['free_gb']:.2f}GB free "
        f"({usage['percent_free']:.1f}%) | "
        f"Threshold: {effective_threshold:.2f}GB"
    )
    
    return is_below, usage['free_gb'], effective_threshold


# ============================================================================
# ITEM DELETION FUNCTION
# ============================================================================

def delete_item(item_path, dry_run=False):
    """
    Delete a file or folder with comprehensive exception handling.
    
    Handles PermissionError, OSError, and other exceptions gracefully.
    
    Args:
        item_path (str): Path to the file or folder to delete
        dry_run (bool): If True, only simulate deletion
    
    Returns:
        tuple: (success, size_freed_gb, message)
    """
    try:
        if not os.path.exists(item_path):
            message = f"Item not found: {item_path}"
            logger.warning(message)
            return False, 0, message
        
        # Calculate size before deletion
        try:
            if os.path.isfile(item_path):
                size_bytes = os.path.getsize(item_path)
            else:
                # Calculate folder size recursively
                size_bytes = 0
                try:
                    for dirpath, dirnames, filenames in os.walk(item_path):
                        for filename in filenames:
                            try:
                                size_bytes += os.path.getsize(os.path.join(dirpath, filename))
                            except (OSError, PermissionError) as e:
                                logger.debug(f"Could not get size of {filename}: {e}")
                                continue
                except Exception as e:
                    logger.warning(f"Error calculating folder size for {item_path}: {e}")
        except (OSError, PermissionError) as e:
            logger.warning(f"Could not calculate size for {item_path}: {e}")
            size_bytes = 0
        
        size_gb = size_bytes / (1024**3) if size_bytes > 0 else 0
        
        if dry_run:
            message = f"[DRY RUN] Would delete: {os.path.basename(item_path)} ({size_gb:.2f}GB)"
            logger.info(message)
            return True, size_gb, message
        
        # Perform actual deletion with error handling
        try:
            if os.path.isfile(item_path):
                try:
                    os.remove(item_path)
                    message = f"Deleted file: {os.path.basename(item_path)} ({size_gb:.2f}GB)"
                except PermissionError:
                    message = f"Permission denied - cannot delete file: {os.path.basename(item_path)}"
                    logger.warning(message)
                    return False, 0, message
                except OSError as e:
                    message = f"OS Error deleting file {os.path.basename(item_path)}: {e}"
                    logger.warning(message)
                    return False, 0, message
            else:
                try:
                    shutil.rmtree(item_path)
                    message = f"Deleted folder: {os.path.basename(item_path)} ({size_gb:.2f}GB)"
                except PermissionError:
                    message = f"Permission denied - cannot delete folder: {os.path.basename(item_path)}"
                    logger.warning(message)
                    return False, 0, message
                except OSError as e:
                    message = f"OS Error deleting folder {os.path.basename(item_path)}: {e}"
                    logger.warning(message)
                    return False, 0, message
        
        except Exception as e:
            message = f"Unexpected error deleting {os.path.basename(item_path)}: {e}"
            logger.error(message)
            return False, 0, message
        
        logger.info(message)
        return True, size_gb, message
    
    except Exception as e:
        message = f"Critical error in delete_item for {item_path}: {e}"
        logger.error(message)
        return False, 0, message


# ============================================================================
# CLEANUP ORCHESTRATION
# ============================================================================


# ============================================================================
# CLEANUP ORCHESTRATION
# ============================================================================

def perform_cleanup(backup_path, drive_path, min_gb, min_percent, 
                    safety_buffer_gb, dry_run=False):
    """
    Execute the cleanup process with priority folder support.
    
    Process:
    1. Delete from PRIORITY_FOLDERS first (oldest items first)
    2. If space still below threshold, delete from other folders
    3. Respect WHITELIST_NAMES throughout the entire process
    
    Args:
        backup_path (str): Path to backup folder
        drive_path (str): Path to the drive
        min_gb (float): Minimum free space in GB
        min_percent (float): Minimum free space percentage
        safety_buffer_gb (float): Safety buffer to add to threshold
        dry_run (bool): If True, only simulate deletions
    
    Returns:
        dict: Cleanup statistics (items_deleted, space_freed_gb, etc.)
    """
    logger.info("=" * 70)
    logger.info(f"Starting cleanup process - DRY RUN: {dry_run}")
    logger.info(f"Priority Folders: {PRIORITY_FOLDERS if PRIORITY_FOLDERS else 'None'}")
    logger.info(f"Whitelisted Items: {WHITELIST_COUNT}")
    logger.info("=" * 70)
    
    stats = {
        'items_deleted': 0,
        'space_freed_gb': 0.0,
        'items_skipped': 0,
        'cleanup_successful': False,
        'whitelisted_protected': 0
    }
    
    # Check current space
    is_below, current_free, required = check_space_threshold(
        drive_path, min_gb, min_percent
    )
    
    if is_below is None:
        logger.error("Cannot determine disk usage")
        return stats
    
    logger.info(f"Free space: {current_free:.2f}GB | Required: {required:.2f}GB + {safety_buffer_gb:.2f}GB buffer")
    
    # Calculate target free space (threshold + safety buffer)
    target_free_space = required + safety_buffer_gb
    
    if not is_below:
        logger.info("Free space is above threshold - No cleanup needed")
        stats['cleanup_successful'] = True
        return stats
    
    logger.info(f"Space is below threshold - Starting cleanup")
    logger.info(f"Target free space: {target_free_space:.2f}GB")
    
    # STEP 1: Clean priority folders first
    if PRIORITY_FOLDERS:
        logger.info(f"STEP 1: Cleaning priority folders: {PRIORITY_FOLDERS}")
        priority_items = get_priority_items(backup_path, PRIORITY_FOLDERS, whitelist_enabled=True)
        
        if priority_items:
            logger.info(f"Found {len(priority_items)} items in priority folders")
            
            for item_path, creation_time, size_gb in priority_items:
                # Recheck disk space
                is_below, current_free, _ = check_space_threshold(
                    drive_path, min_gb, min_percent
                )
                
                if not is_below:
                    logger.info(
                        f"Target space reached during priority cleanup: {current_free:.2f}GB free "
                        f"(Target: {target_free_space:.2f}GB)"
                    )
                    stats['cleanup_successful'] = True
                    break
                
                # Delete the item
                item_name = os.path.basename(item_path)
                created = creation_time.strftime("%Y-%m-%d %H:%M:%S")
                
                logger.info(f"Processing (PRIORITY): {item_name} (Created: {created}, Size: {size_gb:.2f}GB)")
                
                success, freed, message = delete_item(item_path, dry_run=dry_run)
                
                if success:
                    stats['items_deleted'] += 1
                    stats['space_freed_gb'] += freed
                else:
                    stats['items_skipped'] += 1
                    logger.warning(f"Could not delete item: {message}")
    
    # STEP 2: If space still low, clean regular items (excluding priority folders)
    if is_below:
        logger.info("STEP 2: Cleaning regular items (excluding priority folders)")
        
        # Get all backup items
        all_items = get_backup_items(backup_path, whitelist_enabled=True)
        
        # Filter out items from priority folders
        regular_items = [
            item for item in all_items
            if not any(
                item[0].startswith(os.path.join(backup_path, pf))
                for pf in PRIORITY_FOLDERS
            )
        ]
        
        if regular_items:
            logger.info(f"Found {len(regular_items)} items in regular folders")
            
            for item_path, creation_time, size_gb in regular_items:
                # Recheck disk space
                is_below, current_free, _ = check_space_threshold(
                    drive_path, min_gb, min_percent
                )
                
                if not is_below:
                    logger.info(
                        f"Target space reached: {current_free:.2f}GB free "
                        f"(Target: {target_free_space:.2f}GB)"
                    )
                    stats['cleanup_successful'] = True
                    break
                
                # Delete the item
                item_name = os.path.basename(item_path)
                created = creation_time.strftime("%Y-%m-%d %H:%M:%S")
                
                logger.info(f"Processing (REGULAR): {item_name} (Created: {created}, Size: {size_gb:.2f}GB)")
                
                success, freed, message = delete_item(item_path, dry_run=dry_run)
                
                if success:
                    stats['items_deleted'] += 1
                    stats['space_freed_gb'] += freed
                else:
                    stats['items_skipped'] += 1
                    logger.warning(f"Could not delete item: {message}")
    
    # Final status report
    logger.info("=" * 70)
    logger.info("Cleanup Summary:")
    logger.info(f"  Items Deleted: {stats['items_deleted']}")
    logger.info(f"  Items Skipped: {stats['items_skipped']}")
    logger.info(f"  Space Freed: {stats['space_freed_gb']:.2f}GB")
    logger.info(f"  Whitelisted Items Protected: {WHITELIST_COUNT}")
    
    # Final disk check
    _, final_free, _ = check_space_threshold(drive_path, min_gb, min_percent)
    if final_free is not None:
        logger.info(f"  Final Free Space: {final_free:.2f}GB")
    
    logger.info(f"  Status: {'SUCCESS' if stats['cleanup_successful'] else 'TARGET NOT REACHED'}")
    logger.info("=" * 70)
    
    return stats


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def cleanup_cycle(backup_folder, drive_letter):
    """
    Execute a single cleanup cycle.
    
    Args:
        backup_folder (str): Path to backup folder
        drive_letter (str): Drive letter (e.g., "D:")
    
    Returns:
        bool: True if cleanup was performed, False otherwise
    """
    try:
        logger.info(f"Starting cleanup cycle at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Check if space is below threshold
        is_below_threshold, current_free, required = check_space_threshold(
            drive_letter,
            MINIMUM_FREE_SPACE_GB,
            MINIMUM_FREE_SPACE_PERCENT
        )
        
        if is_below_threshold is None:
            logger.error("Cannot determine disk usage")
            return False
        
        if not is_below_threshold:
            logger.info(f"Free space OK: {current_free:.2f}GB (Required: {required:.2f}GB)")
            return False
        
        # Space is below threshold - perform cleanup
        logger.warning(f"Free space below threshold: {current_free:.2f}GB (Required: {required:.2f}GB)")
        
        stats = perform_cleanup(
            backup_folder,
            drive_letter,
            MINIMUM_FREE_SPACE_GB,
            MINIMUM_FREE_SPACE_PERCENT,
            SAFETY_BUFFER_GB,
            dry_run=DRY_RUN
        )
        
        logger.info(f"Cleanup cycle completed: {stats['items_deleted']} deleted, {stats['items_skipped']} skipped")
        return stats['cleanup_successful']
        
    except Exception as e:
        logger.error(f"Error during cleanup cycle: {e}")
        return False


def background_loop(backup_folder, drive_letter):
    """
    Background monitoring loop that checks disk space at regular intervals.
    
    Args:
        backup_folder (str): Path to backup folder
        drive_letter (str): Drive letter (e.g., "D:")
    """
    logger.info(f"Starting background monitoring loop (interval: {CHECK_INTERVAL_MINUTES} minutes)")
    logger.info(f"Monitoring backup folder: {backup_folder}")
    logger.info(f"Monitoring drive: {drive_letter}")
    
    try:
        while True:
            try:
                # Execute cleanup cycle
                cleanup_cycle(backup_folder, drive_letter)
                
                # Sleep for the specified interval
                sleep_seconds = CHECK_INTERVAL_MINUTES * 60
                logger.debug(f"Sleeping for {CHECK_INTERVAL_MINUTES} minutes ({sleep_seconds} seconds)")
                time.sleep(sleep_seconds)
                
            except KeyboardInterrupt:
                logger.info("Background loop interrupted by user (Ctrl+C)")
                break
            except Exception as e:
                logger.error(f"Error in background loop iteration: {e}")
                # Sleep before retrying to avoid rapid error loops
                logger.info("Waiting 5 minutes before retrying...")
                time.sleep(5 * 60)
    
    except Exception as e:
        logger.error(f"Critical error in background loop: {e}")
    finally:
        logger.info("Background loop terminated")


def main():
    """
    Main entry point for the backup self-purge system.
    
    In interactive mode: Prompts for folder selection and performs single cleanup
    In background mode: Runs continuously, checking disk space every 60 minutes
    """
    try:
        logger.info("=" * 70)
        logger.info("Intelligent Backup Storage Management System - Self-Purge")
        logger.info(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"Script location: {os.path.realpath(sys.argv[0])}")
        logger.info(f"Dry-Run Mode: {DRY_RUN}")
        logger.info(f"Background Mode: {RUN_IN_BACKGROUND}")
        logger.info("=" * 70)
        
        # Add to Windows Startup on first run (if enabled)
        if ENABLE_STARTUP_PERSISTENCE and not is_in_startup():
            logger.info("First run detected - attempting to add to Windows Startup...")
            if add_to_windows_startup():
                logger.info("Successfully registered for Windows Startup")
            else:
                logger.warning("Could not add to Windows Startup (may require admin rights)")
        
        # Attempt interactive folder selection
        backup_folder, drive_letter = select_backup_folder()
        
        if not backup_folder or not drive_letter:
            error_msg = "No backup folder selected. Exiting."
            logger.warning(error_msg)
            return
        
        # Validate backup folder exists
        if not os.path.exists(backup_folder):
            error_msg = f"Backup folder not found: {backup_folder}"
            logger.error(error_msg)
            return
        
        # Check if drive is accessible
        try:
            disk_usage = psutil.disk_usage(drive_letter)
            logger.info(f"Drive {drive_letter} is accessible ({disk_usage.total / (1024**3):.2f}GB total)")
        except Exception as e:
            error_msg = f"Cannot access drive {drive_letter}: {e}"
            logger.error(error_msg)
            return
        
        logger.info(f"Backup folder: {backup_folder}")
        logger.info(f"Drive: {drive_letter}")
        logger.info(f"Minimum free space: {MINIMUM_FREE_SPACE_GB}GB or {MINIMUM_FREE_SPACE_PERCENT}%")
        logger.info(f"Safety buffer: {SAFETY_BUFFER_GB}GB")
        
        # Enter background loop if enabled
        if RUN_IN_BACKGROUND:
            logger.info("Entering background monitoring mode...")
            background_loop(backup_folder, drive_letter)
        else:
            logger.info("Running in single-cycle mode...")
            cleanup_cycle(backup_folder, drive_letter)
        
        logger.info("=" * 70)
        logger.info("Backup self-purge system terminated")
        logger.info("=" * 70)
        
    except Exception as e:
        logger.error(f"Critical error in main: {e}", exc_info=True)
    finally:
        logger.info("Program ended")


if __name__ == "__main__":
    main()
