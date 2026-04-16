# INSTALLATION & SETUP GUIDE

## Prerequisites

- **Python 3.6+** (Download from https://www.python.org/)
- **Windows 7 or later** (or Linux/Mac with Python)
- **pip** (comes with Python)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/backup-self-purge.git
cd backup-self-purge
```

Or download as ZIP and extract.

### 2. Install Dependencies

**Option A: Using requirements.txt (Recommended)**
```bash
pip install -r requirements.txt
```

**Option B: Manual install**
```bash
pip install psutil
```

### 3. Verify Installation

```bash
python -c "import psutil; print('✓ psutil installed successfully')"
```

---

## Running the Script

### Method 1: Batch File (Windows Only) - Easiest
```bash
double-click run.bat
```
or from command prompt:
```bash
run.bat
```

### Method 2: Command Line
```bash
python backup_self_purge.py
```

### Method 3: PowerShell (Windows)
```powershell
python backup_self_purge.py
```

### Method 4: Python IDE
- Open `backup_self_purge.py` in your IDE
- Click "Run" button

---

## Troubleshooting Installation

### "Python is not recognized"

**Windows:**
1. Install Python from https://www.python.org/
2. **CHECK THE BOX: "Add Python to PATH"** during installation
3. Restart your computer
4. Try again

**OR manually add to PATH:**
1. Find your Python installation: `python -c "import sys; print(sys.executable)"`
2. Copy the folder path (e.g., `C:\Users\YourName\AppData\Local\Programs\Python\Python39`)
3. Windows → Settings → Environment Variables
4. Add the path to your PATH variable
5. Restart command prompt

### "psutil is not installed"

```bash
pip install --upgrade pip
pip install psutil
```

If still failing:
```bash
python -m pip install psutil
```

### "No module named tkinter"

tkinter should come with Python. If missing:

**Windows:**
- Repair Python installation from "Add/Remove Programs"
- Make sure to select "tcl/tk and IDLE" in components

**Linux:**
```bash
sudo apt-get install python3-tk
```

**macOS:**
```bash
brew install python-tk@3.9  # or your Python version
```

### Permission Denied Error

**Windows:**
- Right-click `run.bat` → Run as Administrator

**Linux/Mac:**
```bash
chmod +x backup_self_purge.py
./backup_self_purge.py
```

---

## System Requirements

| Component | Requirement | Check Command |
|-----------|-------------|----------------|
| Python | 3.6+ | `python --version` |
| psutil | Latest | `pip show psutil` |
| tkinter | Included | `python -m tkinter` |
| RAM | 100MB minimum | - |
| Disk Space | 50MB minimum | - |

---

## Virtual Environment (Optional but Recommended)

Using a virtual environment isolates dependencies:

### Create Virtual Environment

**Windows:**
```bash
python -m venv BackupEnv
BackupEnv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv BackupEnv
source BackupEnv/bin/activate
```

### Install in Virtual Environment

```bash
pip install -r requirements.txt
```

### Run Script

```bash
python backup_self_purge.py
```

### Deactivate Virtual Environment

```bash
deactivate
```

---

## Docker (Advanced)

If you prefer containerized deployment:

### Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY backup_self_purge.py .

# Note: tkinter GUI won't work in containerized environment
# This is suitable for headless/scheduled operation only
```

### Build and Run
```bash
docker build -t backup-self-purge .
docker run -it -v /path/to/backups:/mnt/backups backup-self-purge
```

---

## Development Setup

If you want to contribute or modify the code:

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/backup-self-purge.git
cd backup-self-purge
```

### 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# OR
source venv/bin/activate  # Linux/Mac
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
pip install pylint pytest  # Optional: for code quality
```

### 4. Run Tests (if available)
```bash
pytest
```

### 5. Run Code Quality Check
```bash
pylint backup_self_purge.py
```

---

## Post-Installation Configuration

1. **Edit Settings:**
   - Open `backup_self_purge.py` in your text editor
   - Look for "GLOBAL CONFIGURATION" section (around line 33)
   - Adjust thresholds as needed (see CONFIGURATION_EXAMPLES.md)

2. **Test with Dry-Run:**
   - Keep `DRY_RUN = True`
   - Run script and verify output
   - Review `backup_purge.log`

3. **Enable Production:**
   - Change `DRY_RUN = False`
   - Schedule with Task Scheduler (Windows) or cron (Linux)

4. **Monitor:**
   - Check `backup_purge.log` regularly
   - Verify cleanup is happening as expected

---

## First Run Checklist

- [ ] Python installed and in PATH
- [ ] psutil installed (`pip install psutil`)
- [ ] Script runs without errors
- [ ] GUI folder selection dialog appears
- [ ] Dry-run mode generates log file
- [ ] Log file shows expected items to delete
- [ ] Ready to enable actual deletions

---

## Getting Help

- **README.md** - Full documentation
- **QUICK_START.md** - Quick reference guide
- **CONFIGURATION_EXAMPLES.md** - Example configurations
- **backup_purge.log** - Operation logs
- **GitHub Issues** - Report problems

---

## Uninstallation

### Remove from Computer

**Windows:**
1. Delete the folder where you extracted the files
2. (Optional) Remove Python if not needed:
   - Settings → Apps → Uninstall
   - Find "Python x.x.x"

**Linux/Mac:**
```bash
rm -rf /path/to/backup-self-purge
# Optional: pip uninstall psutil
```

### Remove Task Scheduler Jobs (Windows)
1. Task Scheduler → Find "Backup Cleanup"
2. Right-click → Delete

### Remove Cron Jobs (Linux/Mac)
```bash
crontab -e
# Then delete the backup-self-purge line
```

---

**Ready to go? Check QUICK_START.md for next steps!**
