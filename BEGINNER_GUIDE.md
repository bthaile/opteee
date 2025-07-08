# 🚀 Beginner's Guide to Running Python Scripts

## 📋 **You Don't Need to Configure Anything!**

**Good news:** Your system is already set up! You have:
- ✅ Python 3.9.6 installed
- ✅ Virtual environment created (`venv/`)
- ✅ All required packages installed
- ✅ Project ready to use

## 🖥️ **How to Open Terminal (Mac)**

**Method 1: Spotlight Search**
1. Press `Cmd + Space` (Command + Spacebar)
2. Type "terminal"
3. Press Enter

**Method 2: Finder**
1. Open Finder
2. Go to Applications → Utilities → Terminal
3. Double-click Terminal

**Method 3: Right-click in Project Folder**
1. Open Finder
2. Navigate to `/Users/bthaile/gitrepos/opteee`
3. Right-click in the folder → Services → New Terminal at Folder

## 🏃‍♂️ **How to Run Python Scripts (Step-by-Step)**

### **Step 1: Open Terminal and Navigate**
```bash
# Open Terminal (using any method above)
# Then navigate to your project:
cd /Users/bthaile/gitrepos/opteee
```

### **Step 2: Activate the Virtual Environment**
```bash
# This loads all the required Python packages
source venv/bin/activate

# You should see (venv) at the beginning of your prompt:
# (venv) [bthaile@mbp:~/gitrepos/opteee]$
```

### **Step 3: Run Your Python Script**
```bash
# Now you can run any Python script:
python3 whisper_transcribe.py

# Or the pipeline:
python3 run_pipeline.py --step transcripts
```

## 🔄 **Complete Example Session**

Here's exactly what you'll type in Terminal:

```bash
# 1. Navigate to project
cd /Users/bthaile/gitrepos/opteee

# 2. Activate virtual environment
source venv/bin/activate

# 3. Run the transcription script
python3 whisper_transcribe.py
```

**What you'll see:**
```
[bthaile@mbp:~]$ cd /Users/bthaile/gitrepos/opteee
[bthaile@mbp:~/gitrepos/opteee]$ source venv/bin/activate
(venv) [bthaile@mbp:~/gitrepos/opteee]$ python3 whisper_transcribe.py
🎵 Starting Whisper transcription...
📁 Scanning audio_files/ for MP3 files...
✅ Found 3 new MP3 files to process
🔄 Processing oOyjSHIJSPs.mp3...
```

## 🎯 **Your Workflow for Processing Downloaded MP3s**

### **Every time you download MP3 files:**

1. **Open Terminal**
2. **Copy and paste these commands one by one:**
   ```bash
   cd /Users/bthaile/gitrepos/opteee
   source venv/bin/activate
   python3 whisper_transcribe.py
   ```

**That's it!** The system will automatically:
- Find your new MP3 files
- Process them with AI
- Create transcript files
- Update progress

## 📁 **File Organization**

```
opteee/
├── audio_files/           # ← PUT YOUR MP3 FILES HERE
│   ├── oOyjSHIJSPs.mp3   # ← Downloaded MP3 files
│   └── cbMpZUz22cQ.mp3   # ← More MP3 files
├── transcripts/          # ← TRANSCRIPTS APPEAR HERE
│   ├── oOyjSHIJSPs.txt   # ← Generated transcripts
│   └── cbMpZUz22cQ.txt   # ← More transcripts
├── venv/                 # ← Python environment (don't touch)
├── whisper_transcribe.py # ← Script you run
└── download_tracker.html # ← Download tracker
```

## 🚨 **Understanding .note.txt Files**

**You currently have 502 `.note.txt` files in your `audio_files/` directory.** These are **error logs** that tell you which videos failed to download automatically.

### **What's in your audio_files/ directory right now:**
```
audio_files/
├── _bB29g2ofI0.mp3      # ← DUMMY file (20KB, not real audio)
├── _bB29g2ofI0.note.txt # ← ERROR LOG for this video
├── _HnN44SoAP8.mp3      # ← DUMMY file (20KB, not real audio) 
├── _HnN44SoAP8.note.txt # ← ERROR LOG for this video
└── ... (500 more pairs)
```

### **What the .note.txt files contain:**
```
Failed to download audio for: https://www.youtube.com/watch?v=_bB29g2ofI0
Created dummy audio file on 2025-07-06 16:36:27.904863
This video has been flagged for manual processing.
```

### **What the dummy MP3 files are:**
- **Size:** About 20KB each
- **Content:** Not real audio, just placeholder files
- **Purpose:** System creates these to track failed downloads

## 🔄 **What You Need to Do**

### **Replace dummy files with real MP3 files:**

1. **Use the download tracker** (`download_tracker.html`) to download real MP3 files
2. **Save over the dummy files** with the same filename
3. **The .note.txt files will be automatically cleaned up** when processing succeeds

### **Example:**
```bash
# You have this dummy file:
audio_files/_bB29g2ofI0.mp3  (20KB dummy file)
audio_files/_bB29g2ofI0.note.txt  (error log)

# Download real audio from YouTube as MP3
# Save it as: audio_files/_bB29g2ofI0.mp3  (replaces dummy file)

# Run processing:
python3 whisper_transcribe.py

# System will:
# ✅ Process the real MP3 file
# ✅ Create transcripts/_bB29g2ofI0.txt
# ✅ Clean up the .note.txt file automatically
```

## 📋 **Summary of Current Situation**

- **502 videos** failed automatic download
- **502 .note.txt files** = error logs telling you which videos failed
- **502 dummy MP3 files** = 20KB placeholder files (not real audio)
- **You need to manually download** 502 real MP3 files to replace the dummies
- **Use `download_tracker.html`** to track your progress

## 🚨 **Common Issues and Solutions**

### **"Command not found"**
```bash
# If you get "command not found", check you're in the right directory:
pwd
# Should show: /Users/bthaile/gitrepos/opteee

# Navigate to correct directory:
cd /Users/bthaile/gitrepos/opteee
```

### **"No module named..."**
```bash
# If you get module errors, activate the virtual environment:
source venv/bin/activate

# You should see (venv) at the start of your prompt
```

### **"No files to process"**
```bash
# Check if your MP3 files are in the right place:
ls audio_files/

# Files should be named like: oOyjSHIJSPs.mp3
```

### **"Permission denied"**
```bash
# If you get permission errors, try:
chmod +x whisper_transcribe.py
```

## 🖱️ **Copy-Paste Commands**

**For quick access, here are the exact commands to copy:**

### **Process New MP3 Files:**
```bash
cd /Users/bthaile/gitrepos/opteee
source venv/bin/activate
python3 whisper_transcribe.py
```

### **Check What Files You Have:**
```bash
cd /Users/bthaile/gitrepos/opteee
ls audio_files/
ls transcripts/
```

### **Run Complete Pipeline:**
```bash
cd /Users/bthaile/gitrepos/opteee
source venv/bin/activate
python3 run_pipeline.py --step transcripts
```

## 🎓 **Terminal Basics**

### **Essential Commands:**
- `pwd` - Shows current directory
- `ls` - Lists files in current directory
- `cd` - Changes directory
- `cd ..` - Goes up one directory
- `clear` - Clears terminal screen

### **Keyboard Shortcuts:**
- `Cmd + C` - Copy text
- `Cmd + V` - Paste text
- `Cmd + T` - New terminal tab
- `Cmd + W` - Close terminal tab
- `↑` (Up arrow) - Previous command
- `Tab` - Auto-complete file/folder names

## 🔧 **When You Need Help**

### **Check if everything is working:**
```bash
cd /Users/bthaile/gitrepos/opteee
source venv/bin/activate
python3 --version
# Should show: Python 3.9.6 or similar
```

### **See what Python packages are installed:**
```bash
cd /Users/bthaile/gitrepos/opteee
source venv/bin/activate
pip list
# Shows all installed packages
```

### **If something breaks:**
```bash
cd /Users/bthaile/gitrepos/opteee
./setup.sh
# Re-runs the setup script
```

## 🎉 **Summary**

**You only need to remember 3 commands:**
1. `cd /Users/bthaile/gitrepos/opteee` - Go to project
2. `source venv/bin/activate` - Load Python packages
3. `python3 whisper_transcribe.py` - Process MP3 files

**Every time you download MP3 files, just run these 3 commands in Terminal!**

The system handles everything else automatically. No complex configuration needed! 