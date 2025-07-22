# Manual Audio Download Instructions

## 📁 **Project Directory Structure**

**Important: All commands must be run from the project root directory:**

```bash
# Your project location
/Users/bthaile/gitrepos/opteee/

# Directory structure:
opteee/
├── audio_files/           # ← PUT YOUR MP3 FILES HERE
├── transcripts/           # ← TRANSCRIPTS CREATED HERE
├── whisper_transcribe.py  # ← SCRIPT TO PROCESS FILES
├── run_pipeline.py        # ← MAIN PIPELINE SCRIPT
├── download_tracker.html  # ← INTERACTIVE TRACKER
└── manual_download_instructions.md  # ← THIS FILE
```

### **How to Navigate to the Project Directory:**

**Option 1: Using Terminal (Mac/Linux):**
```bash
# Open Terminal and navigate to project
cd /Users/bthaile/gitrepos/opteee

# Verify you're in the right directory
pwd
# Should show: /Users/bthaile/gitrepos/opteee

# List files to confirm
ls
# Should show: whisper_transcribe.py, run_pipeline.py, audio_files/, etc.
```

**Option 2: Using Finder (Mac):**
1. Open Finder
2. Navigate to `/Users/bthaile/gitrepos/opteee`
3. Right-click in the folder → "Services" → "New Terminal at Folder"

## 🎯 **What You Need to Download**

**502 videos failed automatic download** and need manual processing. Use the interactive tracker page: `download_tracker.html`

## 📁 **Where to Store Downloaded Audio Files**

### **Audio File Storage Location:**
```bash
audio_files/
```

### **Required File Naming Convention:**
```bash
audio_files/{VIDEO_ID}.mp3
```

**Example:**
- Video ID: `oOyjSHIJSPs`
- Save as: `audio_files/oOyjSHIJSPs.mp3`

### **Important: You Already Have Dummy Files**

**Your `audio_files/` directory currently contains:**
- **502 dummy MP3 files** (20KB each) - placeholders, not real audio
- **502 .note.txt files** - error logs showing which videos failed to download

```
audio_files/
├── _bB29g2ofI0.mp3      # ← DUMMY file (replace with real MP3)
├── _bB29g2ofI0.note.txt # ← Error log (will be cleaned up automatically)
├── _HnN44SoAP8.mp3      # ← DUMMY file (replace with real MP3)
├── _HnN44SoAP8.note.txt # ← Error log (will be cleaned up automatically)
└── ... (500 more pairs)
```

**What you need to do:**
1. **Download real MP3 files** from YouTube
2. **Save them with the same filename** to replace the dummy files
3. **The .note.txt files will be automatically removed** when processing succeeds

## 🔗 **Easiest Download Method: Use the Tracker**

**Open `download_tracker.html` in your browser for the easiest experience:**

1. **Click "📥 Download" buttons** → Opens y2mate directly
2. **Download as MP3** → Use y2mate's download options  
3. **Click video ID** → Copies ID to clipboard (e.g., `cbMpZUz22cQ`)
4. **Rename file** → Use copied ID: `cbMpZUz22cQ.mp3`
5. **Save to** → `audio_files/cbMpZUz22cQ.mp3`
6. **Check the box** → Track your progress

## 🛠️ **Alternative Download Tools**

### **Option 1: yt-dlp (Recommended for Batch)**
```bash
# Install yt-dlp
pip install yt-dlp

# Download audio only in MP3 format
yt-dlp --extract-audio --audio-format mp3 --output "audio_files/%(id)s.%(ext)s" "https://www.youtube.com/watch?v=VIDEO_ID"
```

### **Option 2: Browser Extensions**
- 4K Video Downloader
- Video DownloadHelper
- Any YouTube audio downloader extension

### **Option 3: Online Services**
- y2mate.com (linked directly in tracker)
- savefrom.net
- Convert2mp3.net

## 📋 **Complete Workflow**

### **Step 1: Download Audio Files**
For each video you want to process:

1. **Open the tracker:** `download_tracker.html`
2. **Click "📥 Download"** → Opens y2mate
3. **Download as MP3** → Save to your Downloads folder
4. **Click video ID** → Copies ID to clipboard
5. **Rename & move file:** 
   ```bash
   # Move from Downloads to audio_files with correct name
   mv ~/Downloads/video_file.mp3 audio_files/{VIDEO_ID}.mp3
   ```

### **Step 2: Process Your Downloaded Files**

**🎯 After downloading MP3 files, run ONE of these commands:**

**Important: Run these commands from the project root directory (where the scripts are located):**

```bash
# Navigate to the project directory first
cd /Users/bthaile/gitrepos/opteee

# Option 1: Process ONLY the new MP3 files (Recommended)
python3 whisper_transcribe.py

# Option 2: Run the complete transcript step (processes all files)
python3 run_pipeline.py --step transcripts
```

**What these commands do:**
- **Automatically detect** new MP3 files in `audio_files/` directory
- **Run Whisper AI** to generate transcripts for files that don't have them yet
- **Create transcript files** in `transcripts/` directory
- **Skip files** that already have transcripts (won't reprocess)

### **Step 3: Verify Processing**
Check that your files were processed:
```bash
# First, make sure you're in the right directory
cd /Users/bthaile/gitrepos/opteee

# Check if transcript was created
ls transcripts/{VIDEO_ID}.txt

# Check transcript content
head transcripts/{VIDEO_ID}.txt
```

## 🚨 **Important: How the System Works**

### **What Happens Automatically:**
1. **You download:** `audio_files/oOyjSHIJSPs.mp3`
2. **You run:** `python3 whisper_transcribe.py`
3. **System detects:** "New MP3 file found: oOyjSHIJSPs.mp3"
4. **System processes:** Runs Whisper AI transcription
5. **System creates:** `transcripts/oOyjSHIJSPs.txt`
6. **System updates:** Processing progress and removes from failed list

### **You DON'T Need To:**
- ❌ Specify which files to process
- ❌ Run separate commands for each file
- ❌ Worry about reprocessing existing files
- ❌ Manually update any tracking files

### **The System Automatically:**
- ✅ Detects new MP3 files
- ✅ Skips already processed files
- ✅ Updates progress tracking
- ✅ Removes successfully processed videos from failed list

### **Real Example:**
```bash
# 1. Navigate to project directory
cd /Users/bthaile/gitrepos/opteee

# 2. You downloaded these files:
# audio_files/oOyjSHIJSPs.mp3
# audio_files/LuhAOKk3rjI.mp3
# audio_files/cbMpZUz22cQ.mp3

# 3. Run this ONE command:
python3 whisper_transcribe.py

# 4. System automatically:
# - Finds your 3 new MP3 files
# - Processes them with Whisper AI
# - Creates transcripts/oOyjSHIJSPs.txt
# - Creates transcripts/LuhAOKk3rjI.txt  
# - Creates transcripts/cbMpZUz22cQ.txt
# - Updates progress tracking
```

## 🔄 **Processing Options Explained**

### **Option 1: `python3 whisper_transcribe.py`**
**Use this when:** You've downloaded some MP3 files and want to process them
- Scans `audio_files/` directory for MP3 files
- Processes only files that don't have transcripts yet
- Fastest option for new downloads

### **Option 2: `python3 run_pipeline.py --step transcripts`**
**Use this when:** You want to run the full transcript generation step
- Does the same as Option 1 but as part of the larger pipeline
- Includes additional validation and progress tracking
- Slightly slower but more comprehensive

### **Option 3: `python3 run_pipeline.py --force-reprocess`**
**Use this when:** You want to reprocess ALL videos (rarely needed)
- Processes ALL MP3 files regardless of existing transcripts
- Takes much longer
- Only use if you want to completely rebuild everything

## 🎯 **Quick Reference**

### **I downloaded 5 MP3 files. What do I run?**
```bash
# Navigate to project directory
cd /Users/bthaile/gitrepos/opteee

# Run the processing command
python3 whisper_transcribe.py
```
**Result:** System processes your 5 new files, skips the rest

### **I downloaded 1 MP3 file. What do I run?**
```bash
# Navigate to project directory
cd /Users/bthaile/gitrepos/opteee

# Run the processing command
python3 whisper_transcribe.py
```
**Result:** System processes your 1 new file, skips the rest

### **I want to check if everything is working:**
```bash
# Navigate to project directory
cd /Users/bthaile/gitrepos/opteee

# Run the validation command
python3 run_pipeline.py --step transcripts
```
**Result:** System processes any new MP3 files and validates everything

## 📊 **Current Status**
- **Total Videos:** 502
- **Successfully Processed:** 0 (after cleanup)
- **Failed Downloads:** 502 (all need manual download)
- **Interactive Tracker:** `download_tracker.html`

##  **Troubleshooting**

### **"No new files to process"**
- Check your files are in `audio_files/` directory
- Verify filename format: `{VIDEO_ID}.mp3`
- Ensure files are > 10KB (real audio)

### **"Transcription failed"**
- Check audio file quality
- Verify MP3 format
- Ensure sufficient disk space

### **"File not found"**
- Verify exact filename matches video ID
- Check file extension is `.mp3`
- Ensure file is in `audio_files/` directory

## 📋 **Next Steps After Processing**

Once transcripts are generated, the system will automatically:
1. **Update processed transcripts** with metadata
2. **Rebuild vector store** for search
3. **Remove processed videos** from failed list
4. **Update progress tracking**

Run the complete pipeline to finish:
```bash
# Make sure you're in the project directory
cd /Users/bthaile/gitrepos/opteee

# Run the remaining pipeline steps
python3 run_pipeline.py --step preprocess
python3 run_pipeline.py --step vectors
``` 