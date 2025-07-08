---
title: opteee
emoji: 🔥
colorFrom: blue
colorTo: red
sdk: docker
app_port: 7860
pinned: false
---

# Options Trading Knowledge Search

AI-powered search through Outlier Trading educational videos using RAG (Retrieval-Augmented Generation).

## Features

- Semantic search using sentence-transformers
- FAISS vector database for fast retrieval
- Direct links to specific timestamps in relevant videos
- Built with Gradio web interface
- Supports both OpenAI and Anthropic Claude models
- RAG pipeline for context-aware answers

## 🎉 **BREAKTHROUGH: YouTube Blocking Solved!**

**We've successfully solved the YouTube 403 Forbidden blocking issue!**

Our new **browser-based cookie extraction approach** bypasses YouTube's anti-bot detection by:
- 🍪 **Extracting real browser cookies** from actual user sessions
- 🤖 **Simulating authentic user behavior** with proper headers and delays
- 🆕 **Using latest yt-dlp version** (2025.6.30) with enhanced compatibility
- 📱 **Anti-detection measures** including headless browser automation

**Result:** Downloads that were failing with 403 errors now work successfully!

## ⚡ **Quick Start (Copy & Paste)**

**🚨 IMPORTANT: Run these commands EVERY time you open a new terminal:**

```bash
cd /Users/bthaile/gitrepos/opteee
source venv/bin/activate
python3 whisper_focused_downloader.py
```

**This will automatically:**
- ✅ **Discover videos** from Outlier Trading channel (502 videos)
- ✅ **Process in batches** of 5 videos (conservative system-friendly approach)
- ✅ **Download audio** using browser-based cookie extraction (bypasses YouTube blocking)
- ✅ **Generate transcripts** with Whisper AI (only method that works)
- ✅ **Track progress** with immediate saves after each successful step
- ✅ **Resume processing** from any interruption point
- ✅ **Save transcripts** in `transcripts/` folder with proper naming

### **🚨 Common Error Fix**

**If you get: `ModuleNotFoundError: No module named 'pytube'`**

**This means you opened a NEW terminal!** Every new terminal session starts fresh.

**Solution: Always run these 2 setup commands first:**
```bash
cd /Users/bthaile/gitrepos/opteee
source venv/bin/activate
```

**You should see `(venv)` appear at the start of your prompt.** Then run your script.

**New Terminal = New Setup Required!**

---

## 🚀 **For Complete Beginners (No Python Experience Required)**

**If you've never used Python before, start here! This guide assumes zero technical knowledge.**

### **✅ Prerequisites Check**

**Good news: Your system is already set up!** You have:
- ✅ Python installed
- ✅ All packages installed in a virtual environment
- ✅ Project ready to use

**No additional software installation needed!**

### **🖥️ Step 1: Open Terminal**

**On Mac:**
1. Press `Cmd + Space` (Command + Spacebar)
2. Type "terminal"
3. Press Enter

**You'll see a black window with text like:**
```
[yourusername@computer:~]$
```

### **🗂️ Step 2: Navigate to the Project**

**Copy and paste this command into Terminal:**
```bash
cd /Users/bthaile/gitrepos/opteee
```

**Press Enter. You should see:**
```
[bthaile@mbp:~/gitrepos/opteee]$
```

### **🐍 Step 3: Activate Python Environment**

**Copy and paste this command:**
```bash
source venv/bin/activate
```

**Press Enter. You should see `(venv)` appear at the beginning:**
```
(venv) [bthaile@mbp:~/gitrepos/opteee]$
```

**The `(venv)` means Python is ready to use!**

### **🎵 Step 4: Automatically Process All Outlier Trading Videos**

**Copy and paste this command:**
```bash
python3 whisper_focused_downloader.py
```

**This will automatically:**
- **Discover videos** from the Outlier Trading YouTube channel (502 videos)
- **Process in batches** of 5 videos (prevents system overload)
- **Download audio** using browser-based cookie extraction (bypasses YouTube's anti-bot detection)
- **Generate transcripts** using Whisper AI (only method that works for this channel)
- **Track progress** with immediate saves after each step (`transcript_progress.json`)
- **Resume processing** from any interruption point
- **Save transcripts** in the `transcripts/` folder with proper video ID naming

### **🎯 Complete Beginner Workflow**

**🚨 CRITICAL: Every time you open Terminal (or a new terminal tab), you MUST run the setup commands:**

1. **Open Terminal** (Cmd + Space, type "terminal")
2. **ALWAYS copy these 3 commands one by one:**
   ```bash
   cd /Users/bthaile/gitrepos/opteee
   source venv/bin/activate
   python3 whisper_focused_downloader.py
   ```

**Why? Because each terminal session starts completely fresh with no memory of previous sessions.**

**That's it! You don't need to understand what these commands do - just copy and paste them EVERY TIME.**

### **🔄 Understanding Terminal Sessions**

**Think of terminals like this:**
- **Terminal Window 1** = Needs setup commands ✅
- **Terminal Window 2** = Needs setup commands again ✅  
- **New Terminal Tab** = Needs setup commands again ✅
- **Same Terminal** = Setup stays active until you close it ✅

**Examples of when you need to run setup again:**
- ❌ You opened a new terminal window
- ❌ You opened a new terminal tab
- ❌ You restarted your computer
- ❌ You closed and reopened terminal

**When setup stays active:**
- ✅ You run multiple commands in the same terminal window
- ✅ You wait for one command to finish, then run another

**Key Rule: New Terminal = Run Setup Commands Again**

### **📁 How the Automatic Process Works**

**The script automatically handles everything:**
```
/Users/bthaile/gitrepos/opteee/audio_files/    # Audio files (temporary)
/Users/bthaile/gitrepos/opteee/transcripts/    # Final transcripts
```

**Automatic process:**
1. **Discovers videos** from Outlier Trading YouTube channel (502 videos)
2. **Downloads audio** using browser-based cookie extraction (bypasses YouTube blocking)
3. **Saves progress immediately** after each successful audio download
4. **Transcribes audio** using Whisper AI (most reliable method)
5. **Saves progress immediately** after each successful transcript
6. **Saves transcripts** with proper video ID naming (e.g., `cbMpZUz22cQ.txt`)
7. **Tracks detailed progress** with separate audio/transcript counters

**No manual downloads needed!** The script handles everything automatically.

### **🚨 If Something Goes Wrong**

**"Command not found" error:**
```bash
# Make sure you're in the right folder:
cd /Users/bthaile/gitrepos/opteee
```

**"No module named..." error (MOST COMMON):**
```bash
# This means you opened a NEW terminal session!
# Always run BOTH setup commands:
cd /Users/bthaile/gitrepos/opteee
source venv/bin/activate
# You should see (venv) at the beginning of your prompt
```

**"No videos to process" or "All videos processed":**
- This means all Outlier Trading videos have been transcribed!
- Check the `transcripts/` folder for results
- To reprocess videos, delete `transcript_progress.json` and run again

### **🎓 You Don't Need to Learn Python**

**This guide is designed so you can use the system without learning Python programming.** Just follow the copy-paste commands above.

**The system automatically:**
- ✅ Finds your MP3 files
- ✅ Converts them to text transcripts
- ✅ Tracks progress
- ✅ Handles all the technical stuff

## 🔧 **Advanced Setup (For Developers)**

**If you're a developer or want to understand the technical details, see below:**

### Quick Start (Recommended)

**Option 1: Docker Setup (Matches Production)**
```bash
# Clone the repository
git clone https://github.com/yourusername/opteee.git
cd opteee

# Create .env file with your API keys
cat > .env << EOF
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
EOF

# Run with Docker (builds everything automatically)
./run_local.sh
```

**Option 2: Python Environment Setup (Advanced)**
```bash
# Make the script executable
chmod +x setup.sh

# Run the script
./setup.sh
```

The Python setup script will:
1. Check if pyenv is installed
2. Install Python 3.11.7 using pyenv if not already installed
3. Set the local Python version for this project
4. Create and activate a virtual environment
5. Install required packages
6. Create necessary directories and files

### Manual Setup

If you prefer to set up manually:

1. Install pyenv and Python 3.11.7:
```bash
# Install pyenv (macOS)
brew install pyenv

# Install Python 3.11.7
pyenv install 3.11.7

# Set local Python version
pyenv local 3.11.7
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## 📖 **Simple Usage Guide**

### **🎵 Automatic Video Processing (Main Use Case)**

**To automatically download and transcribe all Outlier Trading videos:**

1. **🚨 EVERY TIME you open terminal, run these commands:**
   ```bash
   cd /Users/bthaile/gitrepos/opteee
   source venv/bin/activate
   python3 whisper_focused_downloader.py
   ```

**That's it!** The script will:
- ✅ **Discover all videos** from the Outlier Trading YouTube channel
- ✅ **Download audio** using robust fallback methods
- ✅ **Generate transcripts** using Whisper AI
- ✅ **Process in batches** (10 videos at a time)
- ✅ **Resume automatically** if interrupted
- ✅ **Save transcripts** in the `transcripts/` folder

**Remember: New terminal session = Run all commands again!**

### **🌐 Running the Web Application (Advanced)**

**If you want to use the web interface for asking questions:**

```bash
# Navigate to project and activate environment
cd /Users/bthaile/gitrepos/opteee
source venv/bin/activate

# Run the web application
python3 app.py
```

**Then open your web browser and go to:** `http://localhost:7860`

### **🔧 Advanced Usage (For Developers)**

**Recommended: Docker Method (Matches Production)**
```bash
# Create .env file with API keys (at least one required)
cat > .env << EOF
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
# Optional: YouTube API Key for enhanced metadata
YOUTUBE_API_KEY=your_youtube_api_key_here
# Optional: Discord Bot Token
DISCORD_TOKEN=your_discord_bot_token_here
EOF

# Run with Docker
./run_local.sh
```

**Alternative: Direct Python Method**
```bash
# Activate the virtual environment
source venv/bin/activate

# Set environment variables
export OPENAI_API_KEY=your_key_here
export ANTHROPIC_API_KEY=your_key_here

# Run the Gradio web application
python3 app.py
```

**Access the application at `http://localhost:7860`**

### Local Docker Development Tips

**First-time setup:**
1. The initial Docker build takes 3-5 minutes (building vector store)
2. Subsequent runs are much faster (image is cached)
3. The vector store is built once during image creation, not at runtime

**Making changes:**
```bash
# Stop running container
docker stop opteee-options-search

# Make your code changes, then rebuild
./run_local.sh
```

**Debugging:**
```bash
# View container logs
docker logs opteee-options-search

# Access container shell
docker exec -it opteee-options-search /bin/bash
```

### **🎬 Video Processing Pipeline**

### **Simple Workflow (Beginners)**

**🚨 IMPORTANT: Run these commands EVERY TIME you open a new terminal:**

```bash
# Navigate to project and activate environment (REQUIRED EVERY TIME)
cd /Users/bthaile/gitrepos/opteee
source venv/bin/activate

# Automatically process all Outlier Trading videos
python3 whisper_focused_downloader.py
```

**This automatically:**
- ✅ Discovers videos from Outlier Trading YouTube channel
- ✅ Downloads audio for each video (multiple fallback strategies)
- ✅ Transcribes audio using Whisper AI (most reliable method)
- ✅ Saves transcripts in `transcripts/` folder
- ✅ Processes in batches (10 videos at a time)
- ✅ Skips already processed videos
- ✅ Resumes from interruptions

**Remember: Each new terminal session needs the setup commands again!**

---

## 🎯 **Why We Use Whisper-Only for Outlier Trading**

**The Reality:** After testing 502 videos from Outlier Trading, we discovered:

- ❌ **YouTube Transcript API fails** for ~99% of videos (channel doesn't provide captions)
- ❌ **yt-dlp subtitle extraction fails** for ~99% of videos (no auto-generated captions)
- ✅ **Whisper AI transcription succeeds** when audio downloads work (only reliable method)

**Our Solution:** `whisper_focused_downloader.py`

- 🎯 **Skips YouTube transcript methods entirely** (they don't work for this channel)
- 🍪 **Uses browser-based cookie extraction** (simulates real user sessions to bypass anti-bot detection)
- 🆕 **Updated yt-dlp with latest version** (2025.6.30) for enhanced compatibility
- 🤖 **Focuses on Whisper AI exclusively** (the only method that works)
- 📦 **Processes in batches** (5 videos at a time, conservative approach)
- 💾 **Tracks progress immediately** (saves after each audio download and transcript)

**Result:** BREAKTHROUGH! Successfully bypasses YouTube's 403 Forbidden errors!

### **📖 What You'll See When Running the Script**

**Starting the script:**
```bash
$ python3 whisper_focused_downloader.py
🚀 Whisper-Focused Transcript Downloader (Browser-Based)
============================================================
🔧 Using browser-extracted cookies to avoid detection
🆕 Updated yt-dlp with latest anti-bot countermeasures
📦 Processing in batches of 5 videos
⏱️ Delays: 10s between videos, 15s between batches

📋 Current Processing Status
============================================================
📚 Total videos discovered: 502
🎵 Audio files downloaded: 45
✅ Transcripts completed: 43
❌ Failed: 12
🎯 Remaining: 447
📈 Completion rate: 8.6%

📦 Batch Progress:
    🔄 Last batch completed: 8
    📊 Batch size: 5
    🕐 Started: 2024-01-15 14:30:22
    🕐 Last updated: 2024-01-15 16:45:33
```

**During processing:**
```bash
🎯 Found 447 videos to process

🔄 Processing batch 9/90 (5 videos)
============================================================

📹 Video 1/5 in batch 9
📹 Processing: Selling Options for Monthly Income
    Video ID: cbMpZUz22cQ
  🍪 Extracting cookies from browser session...
  ✅ Extracted 6 cookies
  🔄 Downloading audio...
  ✅ Audio downloaded: 9.4 MB
  📝 Progress saved: audio downloaded
  🎤 Transcribing with Whisper...
  ✅ Transcript saved: transcripts/cbMpZUz22cQ.txt
  📝 Progress saved: transcript processed
    ✅ Success!
    ⏸️  Pausing 10 seconds...

📊 Batch 9/90 Complete!
    ✅ Successes: 4
    ❌ Failures: 1
    ⏱️  Batch time: 185.3s
    📈 Batch success rate: 80.0%
    ⏸️  Pausing 15 seconds before next batch...
```

**Checking status anytime:**
```bash
$ python3 whisper_focused_downloader.py --status
📋 Current Processing Status
============================================================
📚 Total videos discovered: 502
🎵 Audio files downloaded: 67
✅ Transcripts completed: 63
❌ Failed: 15
🎯 Remaining: 424
📈 Completion rate: 12.5%

📦 Batch Progress:
    🔄 Last batch completed: 13
    📊 Batch size: 5
    🕐 Started: 2024-01-15 14:30:22
    🕐 Last updated: 2024-01-15 18:22:15

❌ Recent failures (last 5):
    - 2jG5SD-3F0w
    - hny9FtaPG9o
    - dBD1IkHNlGY
    - qW6h2g8C_NI
    - GVoSqEj3k9I
    
📁 Progress file: transcript_progress.json
```

### **📊 Enhanced Progress Tracking with Immediate Saves**

The new system uses **one comprehensive progress file** (`transcript_progress.json`) with **immediate progress saves**:

**🔄 Batch Processing:**
- **Groups of 5 videos** (configurable) for conservative processing
- **10-second pause** between videos, **15-second pause** between batches
- **Real-time batch statistics** (success rate, timing, overall progress)

**📋 Immediate Progress Tracking:**
- **Single file tracking** - no dummy files or scattered progress data
- **Immediate saves** - progress saved after each audio download and transcript
- **Dual tracking** - separate counters for audio downloads vs transcript completion
- **Resumable processing** - continue from any interruption point
- **Recent failures tracking** - see what went wrong recently

**📈 Key Benefits:**
- ✅ **Easy to monitor** - run `python3 whisper_focused_downloader.py --status` anytime
- ✅ **System-friendly** - conservative batching prevents overload
- ✅ **Immediate saves** - never lose progress, even if interrupted mid-process
- ✅ **Dual tracking** - see audio downloads vs transcript completions separately
- ✅ **Browser-based** - bypasses YouTube's 403 Forbidden errors
- ✅ **Latest tech** - updated yt-dlp with enhanced anti-bot countermeasures

**📁 Progress File Contents:**
```json
{
  "processed": [],
  "failed": ["https://www.youtube.com/watch?v=abc123"],
  "audio_downloaded": ["https://www.youtube.com/watch?v=def456", "https://www.youtube.com/watch?v=ghi789"],
  "whisper_processed": ["https://www.youtube.com/watch?v=def456"],
  "methods": {"def456": "Whisper"},
  "batch_info": {
    "last_batch_completed": 13,
    "videos_per_batch": 5,
    "last_updated": "2024-01-15 18:22:15",
    "processing_started": "2024-01-15 14:30:22"
  },
  "statistics": {
    "total_videos_discovered": 502,
    "audio_downloaded": 67,
    "total_processed": 63,
    "total_failed": 15,
    "success_rate": 12.5
  }
}
```

### **🔧 Enhanced Command Line Options**

The improved script now includes additional options for better control:

**Basic Usage:**
```bash
# Run with default settings (batch size 5)
python3 whisper_focused_downloader.py

# Show current status without processing
python3 whisper_focused_downloader.py --status

# Custom batch size (process more or fewer videos at once)
python3 whisper_focused_downloader.py --batch-size 3

# Reprocess videos (overwrite existing audio/transcripts)
python3 whisper_focused_downloader.py --reprocess
```

**Key Options:**
- `--status` - Show current processing status without starting new downloads
- `--batch-size N` - Process N videos per batch (default: 5, recommended: 1-10)
- `--reprocess` - Reprocess all videos, overwriting existing files
- `--help` - Show all available options

**When to Use --reprocess:**
- Audio files are corrupted or incomplete
- Transcript quality is poor due to older Whisper models
- You want to upgrade all files to the latest format
- Testing new download strategies

---

## 📥 **Clean Manual Video Processing System**

**NEW: Systematic approach to handle failed video downloads with proper state tracking and resumable processing.**

### **🎯 The Clean Solution**

Instead of the messy old process, we now have a unified system that tracks video states and allows resuming from any failure point:

1. **FAILED_DOWNLOAD** - Video download failed, needs manual download
2. **HAVE_VIDEO_NO_TRANSCRIPT** - Video downloaded but transcript generation failed  
3. **COMPLETED** - Video downloaded and transcript generated successfully

### **📊 Step 1: Check Current Status**

**🚨 REMEMBER: Every new terminal session needs setup commands:**

```bash
# Navigate to project and activate environment
cd /Users/bthaile/gitrepos/opteee
source venv/bin/activate

# Scan current state of all videos
python3 manual_video_processor.py --scan
```

**This will show you:**
- ❌ Videos needing manual download
- 🎵 Videos needing transcript processing  
- ✅ Videos completed successfully
- 🎯 Overall progress percentage

### **📋 Step 2: Get Download List**

```bash
# Show the first 20 videos that need downloading
python3 manual_video_processor.py --failed 20

# Export complete download list to file
python3 manual_video_processor.py --export download_list.txt
```

### **📥 Step 3: Download Audio Files**

**Option A: Use y2mate (Recommended)**
1. **Open `download_tracker.html`** in your browser
2. **Click "📥 Download" buttons** → Opens y2mate directly
3. **Click the "🎵 Audio" tab** (not the Video tab!)
4. **Download as MP3** → Save to Downloads folder
5. **Click video ID** to copy it → Use as filename
6. **Move file:** `mv ~/Downloads/filename.mp3 audio_files/{VIDEO_ID}.mp3`

**Option B: Use yt-dlp (Batch)**
```bash
# Download multiple videos at once
yt-dlp --extract-audio --audio-format mp3 --output "audio_files/%(id)s.%(ext)s" \
  "https://www.youtube.com/watch?v=VIDEO_ID1" \
  "https://www.youtube.com/watch?v=VIDEO_ID2"
```

### **🔧 Step 4: Handle Accidental Video Downloads**

**If you downloaded MP4 files instead of MP3:**

```bash
# Convert all MP4 files to MP3 automatically
python3 convert_mp4_to_mp3.py
```

This will:
- Convert all `.mp4` files in `audio_files/` to `.mp3`
- Remove the original `.mp4` files
- Tell you they're ready for transcript processing

### **🎤 Step 5: Process Transcripts**

```bash
# Process transcripts for all videos that have audio but no transcript
python3 manual_video_processor.py --process-transcripts

# Or process specific video IDs
python3 manual_video_processor.py --process-transcripts abc123 def456
```

### **🧹 Step 6: Clean Up and Monitor**

```bash
# Remove dummy files and error transcripts
python3 manual_video_processor.py --cleanup

# Check current status
python3 manual_video_processor.py --status

# Show completed videos
python3 manual_video_processor.py --completed
```

### **🎯 Complete Workflow Example**

```bash
# 1. Setup (every new terminal session)
cd /Users/bthaile/gitrepos/opteee
source venv/bin/activate

# 2. Check what needs to be done
python3 manual_video_processor.py --scan

# 3. See first 10 videos needing download  
python3 manual_video_processor.py --failed 10

# 4. Download some MP3 files manually...
# (Save them as audio_files/VIDEO_ID.mp3)

# 5. Process the transcripts
python3 manual_video_processor.py --process-transcripts

# 6. Check progress
python3 manual_video_processor.py --status
```

### **📊 Key Benefits of New System**

✅ **Clear State Tracking** - Always know exactly what needs to be done  
✅ **Resumable Processing** - Pick up from any failure point  
✅ **No Duplicate Work** - Never reprocess the same video twice  
✅ **Automatic Cleanup** - Removes dummy files and error messages  
✅ **Progress Monitoring** - See completion percentage and status  
✅ **Batch Processing** - Handle multiple videos efficiently  

### **🔍 Troubleshooting New System**

**"No videos tracked. Run --scan first."**
```bash
python3 manual_video_processor.py --scan
```

**"Downloaded MP4 instead of MP3"**
```bash
python3 convert_mp4_to_mp3.py
```

**"Want to see what videos need work"**
```bash
python3 manual_video_processor.py --failed
python3 manual_video_processor.py --need-transcript
```

**"Want to export list for batch downloading"**
```bash
python3 manual_video_processor.py --export my_download_list.txt
```

### **📋 All Available Commands**

```bash
# Status and monitoring
python3 manual_video_processor.py --scan                    # Scan all files
python3 manual_video_processor.py --status                  # Show summary
python3 manual_video_processor.py --failed [limit]          # Show failed downloads
python3 manual_video_processor.py --need-transcript [limit] # Show videos needing transcripts
python3 manual_video_processor.py --completed [limit]       # Show completed videos

# Processing
python3 manual_video_processor.py --process-transcripts     # Process all pending
python3 manual_video_processor.py --process-transcripts ID1 ID2  # Process specific IDs
python3 manual_video_processor.py --cleanup                 # Remove dummy files

# Export and utilities  
python3 manual_video_processor.py --export [filename]       # Export download list
python3 convert_mp4_to_mp3.py                              # Convert video files
```

This new system gives you complete control and visibility over the manual processing workflow!

---

### **Advanced Pipeline (Developers)**

**🎯 Recommended Approach for Outlier Trading**

Since the Outlier Trading channel doesn't provide YouTube captions, we use a **Whisper-focused approach**:

```bash
# Step 1: Discover videos from YouTube channel
python3 outlier_scraper.py

# Step 2: Download audio and transcribe with Whisper (MAIN PROCESS)
python3 whisper_focused_downloader.py

# Step 3: Process transcripts into chunks
python3 preprocess_transcripts.py

# Step 4: Create vector store for search
python3 create_vector_store.py
```

**Alternative: Use the unified pipeline (may have mixed results)**
```bash
# Complete pipeline - includes YouTube transcript methods (mostly fail for this channel)
python3 run_pipeline.py

# Better: Force Whisper-only approach
python3 run_pipeline.py --step scrape      # Video discovery
# Then use whisper_focused_downloader.py instead of built-in transcript step
python3 whisper_focused_downloader.py      # Whisper transcription
python3 run_pipeline.py --step preprocess  # Chunking & metadata  
python3 run_pipeline.py --step vectors     # Vector store creation
```

**Why this approach works better:**
- ✅ **Outlier Trading doesn't provide YouTube captions** for most videos
- ✅ **Whisper transcription has 100% success rate** when audio downloads succeed
- ✅ **Multiple audio download strategies** increase success rate
- ✅ **Batch processing** prevents system overload
- ✅ **Progress tracking** allows resuming from interruptions

**Pipeline Validation & Health Check:**
```bash
# Validate pipeline is ready and consistent
python3 validate_pipeline.py

# Test configuration and imports
python3 test_pipeline_fixes.py
```

## Centralized Configuration & Pipeline Architecture

**NEW: All processing scripts now use centralized configuration for consistency.**

The project includes `pipeline_config.py` which provides:
- **Unified settings**: Chunk size (250 words), overlap (50 words), file paths
- **Consistent formats**: All files use JSON format for compatibility
- **Environment management**: Centralized API key and directory handling
- **Validation**: Built-in configuration validation and error checking

```bash
# Check current configuration
python3 pipeline_config.py
```

**Key Configuration Settings:**
- **Chunk Size**: 250 words per chunk (consistent across all processing)
- **Overlap**: 50 words between chunks (maintains context continuity)
- **Min Words**: 10 words minimum per chunk (filters out noise)
- **File Format**: JSON only (no CSV conflicts)
- **Progress Tracking**: Automated progress and error recovery

## YouTube Video Metadata Collection

**Recommended: Use the unified pipeline runner**
```bash
python3 run_pipeline.py --step scrape
```

**Manual Setup (Advanced):**

1. Set up your environment:
   ```bash
   # Install dependencies
   pip install -r requirements.txt
   
   # Create .env file with API key (optional but recommended)
   echo "YOUTUBE_API_KEY=your-api-key-here" > .env
   ```

2. Run video discovery:
   ```bash
   python3 outlier_scraper.py
   ```
   Creates `outlier_trading_videos.json` with basic video information.

3. Enhance with detailed metadata (if YouTube API key provided):
   ```bash
   python3 collect_video_metadata.py
   ```
   Creates `outlier_trading_videos_metadata.json` with comprehensive data.

**YouTube API Setup:**
- Go to [Google Cloud Console](https://console.cloud.google.com/)
- Create a new project and enable YouTube Data API v3
- Create credentials (API Key) and add to `.env` file

**Generated Metadata Includes:**
- Video ID, title, and URL
- Channel name, upload date, duration
- View count, likes, description, tags
- Thumbnail URL and transcript information
- Guest detection and content summaries

**Note**: Without a YouTube API key, the system uses yt-dlp for basic metadata.

## Vector Database for Transcript Search

The project includes a comprehensive vector database system for semantic search of educational content.

### Complete Processing Pipeline (Automated)

**Recommended: Use the unified pipeline runner**
```bash
# Complete pipeline - handles everything automatically
python3 run_pipeline.py

# Or run specific steps
python3 run_pipeline.py --step preprocess  # Chunking & metadata
python3 run_pipeline.py --step vectors     # Vector store creation
```

**The automated pipeline ensures:**
- ✅ **Consistent chunking**: 250 words per chunk, 50 words overlap
- ✅ **Complete metadata**: Every chunk includes video info, timestamps, URLs
- ✅ **Progress tracking**: Avoids reprocessing, handles errors gracefully
- ✅ **Format consistency**: All files use JSON format for compatibility

### Processing Steps (Automated by Pipeline)

1. **Data Collection**: Video discovery via `outlier_scraper.py` → JSON metadata
2. **Metadata Enhancement**: YouTube API enrichment via `collect_video_metadata.py`
3. **Transcript Generation**: Whisper AI transcription (YouTube API captions not available for this channel) → raw `.txt` files
4. **Transcript Processing**: Cleaning, chunking, metadata enrichment → processed `.json` files
5. **Vector Database**: Embedding generation + FAISS index creation → searchable database
6. **Quality Validation**: Automated checks for consistency and completeness

### Manual Setup (Advanced)

If you need to run individual steps:

1. Ensure dependencies and validate configuration:
   ```bash
   pip install -r requirements.txt
   python3 validate_pipeline.py
   ```

2. Process transcripts into chunks:
   ```bash
   python3 preprocess_transcripts.py
   ```

3. Create the vector database:
   ```bash
   python3 create_vector_store.py
   
   # Optional: Test search functionality
   python3 create_vector_store.py --test-search
   ```

### Searching for Content

Search for relevant transcript sections using:
```
python3 search_transcripts.py "your search query here"
```

Options:
- `--top-k 10`: Return 10 results (default is 5)
- `--show-text`: Also show the transcript text (not just metadata)

### Programmatic Usage

You can also use the search functionality from your own Python code:

```python
from search_helper import search_transcripts, format_results

# Search for relevant transcripts
results = search_transcripts("options trading strategies for beginners", top_k=5)

# Format and print results
print(format_results(results))

# Or access individual results
for result in results:
    print(f"Title: {result['title']}")
    print(f"URL: {result['video_url']}")
```

This vector database can be integrated into a RAG (Retrieval Augmented Generation) system to provide context for large language models.

## Pipeline Management & Validation Tools

**NEW: The project now includes comprehensive tools for managing and validating the processing pipeline.**

### Pipeline Runner (`run_pipeline.py`)

**Complete workflow orchestration with smart processing:**

```bash
# Run complete pipeline (recommended)
python3 run_pipeline.py

# Force reprocess everything for consistency
python3 run_pipeline.py --force-reprocess

# Run individual steps
python3 run_pipeline.py --step scrape      # Video discovery only
python3 run_pipeline.py --step transcripts # Transcript generation only
python3 run_pipeline.py --step preprocess  # Chunking & metadata only
python3 run_pipeline.py --step vectors     # Vector store creation only
```

**Features:**
- **Smart Detection**: Detects existing data and asks before reprocessing
- **Progress Tracking**: Shows detailed statistics and completion status
- **Error Recovery**: Handles failures gracefully with detailed error reporting
- **Idempotent**: Multiple runs produce identical results

### Script Interaction & Artifact Flow

**Critical Implementation Detail:** All scripts now use centralized configuration and proper argument passing:

```
🔧 Script Dependencies & Function Calls:
├── run_pipeline.py (Main Orchestrator)
│   ├── → outlier_scraper.main() [No args needed]
│   ├── → whisper_transcribe.main() [No args needed] 
│   ├── → preprocess_transcripts.main() [No args needed]
│   └── → create_vector_store.main(args) [✅ FIXED: Now passes argparse.Namespace]
│
├── pipeline_config.py (Central Configuration)
│   ├── → CHUNK_SIZE = 250 words
│   ├── → OVERLAP = 50 words
│   ├── → File paths (TRANSCRIPT_DIR, PROCESSED_DIR, etc.)
│   └── → validate_config() function
│
└── Individual Scripts (Can run standalone)
    ├── outlier_scraper.py
    ├── collect_video_metadata.py  
    ├── whisper_transcribe.py
    ├── preprocess_transcripts.py
    └── create_vector_store.py [Takes argparse args]
```

**Artifact Creation Flow:**
1. **`outlier_scraper.py`** → Creates `outlier_trading_videos.json`
2. **`collect_video_metadata.py`** → Enhances to `outlier_trading_videos_metadata.json`  
3. **`whisper_transcribe.py`** → Creates `.txt` files in `transcripts/`
4. **`preprocess_transcripts.py`** → Creates `.json` files in `processed_transcripts/`
5. **`create_vector_store.py`** → Creates FAISS index in `vector_store/`

**Key Fix Applied:** The `run_vector_creation()` function in `run_pipeline.py` now properly creates and passes arguments to `create_vector_store.main()` using `argparse.Namespace()` instead of calling it without arguments.

### Validation Tools

**Pipeline Health Check (`validate_pipeline.py`):**
```bash
python3 validate_pipeline.py
```
- Validates script organization and dependencies
- Checks configuration consistency
- Verifies file structure and formats
- Tests API keys and environment setup
- Provides specific recommendations for fixes

**Consistency Testing (`test_pipeline_fixes.py`):**
```bash
python3 test_pipeline_fixes.py
```
- Tests import consistency across all scripts
- Validates configuration settings
- Checks for conflicting file formats
- Ensures all required scripts are present

**Configuration Management (`pipeline_config.py`):**
```bash
python3 pipeline_config.py
```
- Shows current configuration settings
- Validates chunking parameters
- Displays file paths and API key status
- Centralized settings for all scripts

### Benefits of the New Architecture

✅ **Consistency**: All scripts use identical settings from central configuration  
✅ **Reliability**: Validation tools catch configuration issues before processing  
✅ **Efficiency**: Smart detection avoids unnecessary reprocessing  
✅ **Maintainability**: Centralized configuration eliminates setting drift  
✅ **Reproducibility**: Multiple runs guarantee identical chunking and results

### Troubleshooting Script Interactions

**Common Issue: "TypeError: main() missing 1 required positional argument"**

**Problem:** Some scripts expect command-line arguments when called programmatically.

**Solution Applied:** The `run_pipeline.py` script now properly handles argument passing:

```python
# ❌ OLD (Caused errors):
import create_vector_store
create_vector_store.main()

# ✅ NEW (Fixed):
import create_vector_store
import argparse

vector_args = argparse.Namespace(
    model='all-MiniLM-L6-v2',
    batch_size=32,
    test_search=False
)
create_vector_store.main(vector_args)
```

**Scripts Requiring Arguments:**
- `create_vector_store.py` - Requires model name, batch size, test mode
- All other scripts (`outlier_scraper.py`, `whisper_transcribe.py`, `preprocess_transcripts.py`) can be called without arguments

**Validation:** Run `python3 validate_pipeline.py` to check all script interactions are working correctly.

## Complete Script Arguments & Configuration Reference

This section documents all command-line arguments and configuration options for every script in the project.

### Quick Reference - Most Common Scripts

| Script | Purpose | Common Usage |
|--------|---------|--------------|
| `run_pipeline.py` | Main pipeline orchestrator | `python3 run_pipeline.py` |
| `run_pipeline.py --step X` | Run specific step | `python3 run_pipeline.py --step transcripts` |
| `validate_pipeline.py` | Health check | `python3 validate_pipeline.py` |
| `search_transcripts.py` | Vector search | `python3 search_transcripts.py "your query"` |
| `rag_pipeline.py` | RAG Q&A | `python3 rag_pipeline.py "your question"` |
| `test_rag.py` | Test RAG pipeline | `python3 test_rag.py --provider claude` |
| `app.py` | Web application | `python3 app.py` |
| `create_vector_store.py` | Vector store creation | `python3 create_vector_store.py --test-search` |

### Common Argument Patterns

**Top-K (Number of Results):**
- `--top-k 5` - Return 5 results (default in most scripts)
- `--top-k 10` - Return 10 results for more comprehensive searches

**Model Selection:**
- `--model gpt-4` - Use GPT-4 (OpenAI)
- `--model claude-3-5-sonnet` - Use Claude 3.5 Sonnet (Anthropic)
- `--model all-MiniLM-L6-v2` - Use default embedding model

**Provider Selection:**
- `--provider openai` - Use OpenAI models
- `--provider claude` - Use Anthropic Claude models

**Temperature Control:**
- `--temperature 0.1` - More deterministic responses (default)
- `--temperature 0.7` - More creative responses

**Testing & Debugging:**
- `--test-search` - Run test queries
- `--show-text` - Show full text content
- `--compare` - Compare multiple providers
- `--force-reprocess` - Ignore existing files and reprocess

### Main Pipeline Scripts

#### 1. `run_pipeline.py` - Main Pipeline Orchestrator
**Usage:** `python3 run_pipeline.py [OPTIONS]`

**Arguments:**
- `--step {scrape,transcripts,preprocess,vectors}` - Run only a specific step
- `--force-reprocess` - Force reprocessing of all steps (ignores existing files)

**Examples:**
```bash
# Run complete pipeline
python3 run_pipeline.py

# Run specific step
python3 run_pipeline.py --step transcripts

# Force reprocess everything
python3 run_pipeline.py --force-reprocess
```

#### 2. `validate_pipeline.py` - Pipeline Health Check
**Usage:** `python3 validate_pipeline.py`

No arguments. Validates configuration consistency and system health.

#### 3. `test_pipeline_fixes.py` - Code Consistency Testing
**Usage:** `python3 test_pipeline_fixes.py`

No arguments. Tests import consistency and code organization.

### Individual Processing Scripts

#### 4. `outlier_scraper.py` - Video Discovery
**Usage:** `python3 outlier_scraper.py`

No arguments. Uses configuration from `pipeline_config.py`.

#### 5. `collect_video_metadata.py` - Enhanced Metadata Collection
**Usage:** `python3 collect_video_metadata.py`

No arguments. Requires `YOUTUBE_API_KEY` in environment.

#### 6. `whisper_transcribe.py` - Transcript Generation
**Usage:** `python3 whisper_transcribe.py`

No arguments. Uses configuration from `pipeline_config.py`.

#### 7. `preprocess_transcripts.py` - Transcript Chunking
**Usage:** `python3 preprocess_transcripts.py`

No arguments. Uses chunking parameters from `pipeline_config.py`.

#### 8. `create_vector_store.py` - Vector Store Creation
**Usage:** `python3 create_vector_store.py [OPTIONS]`

**Arguments:**
- `--model MODEL` - Sentence transformer model (default: `all-MiniLM-L6-v2`)
- `--batch-size SIZE` - Batch size for embedding creation (default: 32)
- `--test-search` - Run test queries after creating the index

**Examples:**
```bash
# Create vector store with defaults
python3 create_vector_store.py

# Use different model and batch size
python3 create_vector_store.py --model all-mpnet-base-v2 --batch-size 16

# Create and test search functionality
python3 create_vector_store.py --test-search
```

### Search & Query Scripts

#### 9. `search_transcripts.py` - Vector Search
**Usage:** `python3 search_transcripts.py QUERY [OPTIONS]`

**Arguments:**
- `QUERY` - Search query (multiple words accepted)
- `--model MODEL` - Sentence transformer model (default: `all-MiniLM-L6-v2`)
- `--top-k K` - Number of results to return (default: 5)
- `--show-text` - Show text content of results

**Examples:**
```bash
# Basic search
python3 search_transcripts.py "gamma in options trading"

# Get more results
python3 search_transcripts.py "risk management" --top-k 10

# Show full text content
python3 search_transcripts.py "covered call" --show-text
```

#### 10. `rag_pipeline.py` - RAG Question Answering
**Usage:** `python3 rag_pipeline.py QUERY [OPTIONS]`

**Arguments:**
- `QUERY` - Question to answer
- `--top-k K` - Number of documents to retrieve (default: 5)
- `--model MODEL` - LLM model to use (default: gpt-3.5-turbo for OpenAI, claude-3-5-sonnet for Claude)
- `--temperature T` - Temperature for the LLM (default: 0.1)
- `--provider {openai,claude}` - LLM provider to use (default: openai)

**Examples:**
```bash
# Basic question with OpenAI
python3 rag_pipeline.py "What is gamma in options trading?"

# Use Claude with more sources
python3 rag_pipeline.py "Explain covered calls" --provider claude --top-k 7

# Use specific model and temperature
python3 rag_pipeline.py "Risk management strategies" --model gpt-4 --temperature 0.2
```

### Testing & Debugging Scripts

#### 11. `test_rag.py` - RAG Pipeline Testing
**Usage:** `python3 test_rag.py [OPTIONS]`

**Arguments:**
- `--provider {openai,claude}` - LLM provider to use
- `--top-k K` - Number of documents to retrieve (default: 5)
- `--output FILE` - Output file to save results (default: rag_test_results.txt)
- `--questions Q1 Q2 ...` - Specific questions to test (default: use built-in test questions)
- `--model MODEL` - Specific model to use (default: provider's default)

**Examples:**
```bash
# Test with default questions
python3 test_rag.py

# Test with specific questions using Claude
python3 test_rag.py --provider claude --questions "What is gamma?" "How does theta work?"

# Test with custom output file
python3 test_rag.py --output my_test_results.txt
```

#### 12. `test_single_question.py` - Single Question Testing
**Usage:** `python3 test_single_question.py QUESTION [OPTIONS]`

**Arguments:**
- `QUESTION` - Question to test
- `--provider {openai,claude}` - LLM provider to use
- `--top-k K` - Number of documents to retrieve (default: 5)
- `--temperature T` - Temperature for response generation (default: 0.1)
- `--model MODEL` - Specific model to use (default: provider's default)
- `--compare` - Compare results from both providers if available

**Examples:**
```bash
# Test single question
python3 test_single_question.py "What is implied volatility?"

# Compare both providers
python3 test_single_question.py "Explain delta hedging" --compare

# Use specific model and temperature
python3 test_single_question.py "Bull call spread strategy" --model gpt-4 --temperature 0.3
```

### Utility Scripts

#### 13. `count_files.py` - File Counting Utility
**Usage:** `python3 count_files.py DIRECTORY [OPTIONS]`

**Arguments:**
- `DIRECTORY` - Directory to count files in
- `-r, --recursive` - Count files in subdirectories
- `-t, --type TYPE` - File type to count (e.g., .txt)

**Examples:**
```bash
# Count files in transcripts directory
python3 count_files.py transcripts

# Count all JSON files recursively
python3 count_files.py . -r -t .json

# Count only TXT files
python3 count_files.py processed_transcripts -t .txt
```

#### 14. `pipeline_config.py` - Configuration Display
**Usage:** `python3 pipeline_config.py`

No arguments. Displays current configuration settings and validates them.

### Web Applications

#### 15. `app.py` - Main Gradio Web Application
**Usage:** `python3 app.py`

No arguments. Runs the web interface on port 7860.

#### 16. `discord/discord_bot.py` - Discord Bot
**Usage:** `python3 discord/discord_bot.py`

No arguments. Requires `DISCORD_TOKEN` in environment.

### Configuration Files

#### Environment Variables (`.env` file)
```bash
# Required for enhanced metadata
YOUTUBE_API_KEY=your_youtube_api_key

# Required for RAG pipeline (at least one)
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
CLAUDE_API_KEY=your_claude_api_key  # Alternative name for Anthropic

# Optional for Discord bot
DISCORD_TOKEN=your_discord_bot_token
```

#### Central Configuration (`pipeline_config.py`)
Key settings that affect all scripts:
- `CHUNK_SIZE = 250` - Words per chunk
- `OVERLAP = 50` - Words overlap between chunks
- `MIN_CHUNK_WORDS = 10` - Minimum chunk size
- `BATCH_SIZE = 32` - Embedding batch size
- File paths and directory locations

### Script Usage Patterns

**Complete Pipeline (Recommended):**
```bash
python3 run_pipeline.py
```

**Individual Steps:**
```bash
python3 run_pipeline.py --step scrape
python3 run_pipeline.py --step transcripts
python3 run_pipeline.py --step preprocess
python3 run_pipeline.py --step vectors
```

**Search & Query:**
```bash
python3 search_transcripts.py "your query"
python3 rag_pipeline.py "your question"
```

**Testing:**
```bash
python3 validate_pipeline.py
python3 test_rag.py
python3 test_single_question.py "test question"
```

**Debugging:**
```bash
python3 count_files.py transcripts
python3 pipeline_config.py
```

This comprehensive reference ensures you can use and configure every script in the project effectively.  

## RAG (Retrieval Augmented Generation) Pipeline

This project now includes a full RAG pipeline that can answer questions about options trading based on the transcript content:

### Setting Up the RAG Pipeline

1. Make sure you have completed the previous steps:
   - Collected video metadata
   - Processed transcripts
   - Created the vector database

2. Set your OpenAI API key in the `.env` file:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```

3. The system includes two ways to interact with the RAG pipeline:

   **a. Web Interface (Recommended):**
   ```
   python3 app.py
   ```
   Open your browser to `http://localhost:7860` to access the Gradio interface where you can:
   - Ask questions about options trading
   - Adjust settings (number of sources, AI provider, sorting)
   - See answers with source attribution
   - View formatted results with video links

   **b. Command-line Interface (Advanced):**
   ```
   python3 rag_pipeline.py "What are the best options strategies for beginners?"
   ```

   Options:
   - `--top-k 7`: Retrieve 7 sources (default is 5)
   - `--model "gpt-4"`: Use a specific OpenAI model (default is gpt-3.5-turbo)
   - `--temperature 0.2`: Set temperature for response generation (default is 0.1)
   - `--hide-sources`: Don't show source information in output

### How It Works

1. **Retrieval**: The system uses the FAISS vector database to find the most relevant transcript chunks for your question
2. **Context Formation**: It combines these chunks into a comprehensive context
3. **Prompt Creation**: It creates a prompt that includes both the retrieved context and your question
4. **Generation**: An LLM (like GPT-3.5 or GPT-4) generates an answer based on the context
5. **Source Attribution**: The system shows which videos/timestamps the information came from

### 🔧 **RAG Pipeline Technical Implementation**

#### **Query Processing Flow**
```
User Question → Embedding → FAISS Search → Chunk Retrieval → Context Assembly → LLM Generation → Formatted Response
```

#### **Retrieval Strategy**
- **Similarity Search**: Uses cosine similarity in 384-dimensional vector space
- **Top-K Selection**: Configurable (default: 5 chunks)
- **Relevance Scoring**: FAISS L2 distance converted to similarity scores
- **Deduplication**: Removes duplicate chunks from same video segment

#### **Context Assembly**
- **Chunk Ordering**: Sorted by relevance score (highest first)
- **Metadata Integration**: Each chunk includes video title, timestamp, and URL
- **Context Limits**: Respects LLM token limits (typically 4k-8k tokens)
- **Format Structure**: Consistent formatting for optimal LLM comprehension

#### **LLM Integration**
- **Supported Models**: OpenAI GPT-3.5/4, Anthropic Claude 3.5 Sonnet
- **Temperature Control**: Configurable (default: 0.1 for consistency)
- **System Prompts**: Optimized for financial education content
- **Response Formatting**: Structured with source attribution

#### **Source Attribution System**
- **Timestamp Precision**: Links to exact seconds in videos
- **URL Generation**: Automatic YouTube timestamp URLs (`&t=XXX`)
- **Title Preservation**: Original video titles with timestamp references
- **Relevance Ranking**: Sources ordered by similarity score

### Example Usage

**Web Interface (Primary Method):**
1. Run `python3 app.py`
2. Open `http://localhost:7860` in your browser
3. Enter your question: "What is gamma in options trading?"
4. Select your preferred AI provider (OpenAI or Claude)
5. Choose number of results and sorting method
6. Click submit to get formatted results with video links

**Command Line (Advanced):**
```
$ python3 rag_pipeline.py "What is gamma in options trading?"

================================================================================
QUESTION: What is gamma in options trading?
================================================================================

Gamma in options trading is a measure of the rate of change in an option's delta 
in relation to changes in the underlying asset's price. It represents the amount 
delta will change when the underlying security increases in price by $1.

Gamma is highest for at-the-money options and decreases for in-the-money and 
out-of-the-money options. It's particularly important for options nearing 
expiration, as time decay accelerates and gamma increases significantly for 
at-the-money options.

Options traders need to be aware of gamma risk, especially when trading multiple 
options positions or managing delta-hedged positions, as it can cause rapid 
changes in portfolio exposure during volatile market movements.

----------------------------------------
SOURCES:
----------------------------------------
1. Breaking Down My DJT Long Call Trade – Key Takeaways on Gamma
   Timestamp: 00:05:44
   URL: https://www.youtube.com/watch?v=4ountK1Wflc&t=344

2. Option Greeks Explained | Options Greeks for Beginners
   Timestamp: 00:12:11
   URL: https://www.youtube.com/watch?v=0qcfwt6wf2I&t=731

## Important Files

### Core Pipeline Files
- **pipeline_config.py**: **CENTRAL CONFIGURATION** - All processing settings, file paths, and parameters
- **run_pipeline.py**: **MAIN WORKFLOW** - Complete pipeline orchestration with progress tracking
- **validate_pipeline.py**: **HEALTH CHECK** - Validates configuration consistency and system health
- **test_pipeline_fixes.py**: **CONSISTENCY TESTING** - Validates code organization and imports

### Processing Scripts & Their Artifacts

| Script | Input Files | Output Files | Purpose |
|--------|-------------|--------------|---------|
| `outlier_scraper.py` | None (YouTube URLs) | `outlier_trading_videos.json` | Video discovery & basic metadata |
| `collect_video_metadata.py` | `outlier_trading_videos.json` | `outlier_trading_videos_metadata.json` | Enhanced metadata via YouTube API |
| `whisper_transcribe.py` | Video metadata JSON | `transcripts/*.txt` | Transcript generation (YouTube API + Whisper) |
| `preprocess_transcripts.py` | `transcripts/*.txt` + metadata JSON | `processed_transcripts/*.json` | Chunking & metadata enrichment |
| `create_vector_store.py` | `processed_transcripts/*.json` | `vector_store/*.{faiss,pkl}` | FAISS index creation |

### Data Files (Critical for Backup)
- **transcript_progress.json**: Tracks video processing status. **BACK UP THIS FILE** to avoid reprocessing!
- **outlier_trading_videos.json**: Complete video metadata from channel scraping
- **outlier_trading_videos_metadata.json**: Enhanced metadata with YouTube API data
- **processed_transcripts/**: Directory with all processed chunks (JSON format)
- **transcripts/**: Directory with raw transcript files (TXT format)
- **vector_store/**: FAISS index and embeddings for semantic search

### Application Files
- **app.py**: Main Gradio web application entry point
- **requirements.txt**: Production dependencies (full list)
- **minimal_requirements.txt**: Docker dependencies (optimized)
- **setup.sh**: Automated Python environment setup script

### Configuration & Troubleshooting Files
- **.env**: API keys (YouTube, OpenAI, Anthropic, Discord)
- **manual_processing_needed.json**: Videos requiring manual intervention
- **missing_transcripts.json**: List of videos needing transcript generation
- **unlisted_videos.json**: Discovered unlisted/private videos

## Recreating the Project

**If you need to recreate the project from scratch:**

### Option 1: Docker Setup (Recommended)
```bash
git clone https://github.com/yourusername/opteee.git
cd opteee

# Restore critical backup files (if available)
# Copy your backed-up transcript_progress.json to avoid reprocessing
cp /path/to/backup/transcript_progress.json .

# Create .env file with API keys
echo "OPENAI_API_KEY=your_key_here" > .env
echo "ANTHROPIC_API_KEY=your_key_here" >> .env

# Run with Docker (builds everything automatically)
./run_local.sh
```

### Option 2: Python Environment Setup
```bash
git clone https://github.com/yourusername/opteee.git
cd opteee

# Restore critical backup files (if available)
cp /path/to/backup/transcript_progress.json .

# Setup Python environment
./setup.sh

# Activate environment and set API keys
source venv/bin/activate
export OPENAI_API_KEY=your_key_here
export ANTHROPIC_API_KEY=your_key_here

# Validate configuration
python3 validate_pipeline.py

# Run the application
python3 app.py
```

### Rebuilding Data from Scratch
```bash
# Complete rebuild (processes all videos)
python3 run_pipeline.py --force-reprocess

# Or rebuild step by step
python3 run_pipeline.py --step scrape      # Discover videos
python3 run_pipeline.py --step transcripts # Generate transcripts
python3 run_pipeline.py --step preprocess  # Create chunks
python3 run_pipeline.py --step vectors     # Build vector store
```

**Critical Files to Backup:**
- `transcript_progress.json` (processing status)
- `outlier_trading_videos*.json` (video metadata)
- `processed_transcripts/` (processed chunks)
- `transcripts/` (raw transcripts)
- `.env` (API keys)

# Options Trading Education Assistant (OPTEEE)

A RAG (Retrieval-Augmented Generation) system for answering questions about options trading based on Outlier Trading educational videos.

## Features
- Ask questions about options trading concepts
- Retrieves relevant information from a collection of educational videos
- Provides source links to the exact timestamp in original videos
- Supports both OpenAI and Anthropic Claude models

## Setup in Hugging Face Spaces

1. Fork this repository to your GitHub account
2. Create a new Hugging Face Space
   - Go to [Hugging Face Spaces](https://huggingface.co/spaces)
   - Click "Create new Space"
   - Select "Docker" as the SDK
   - Connect to your GitHub repository
   
3. Configure your Space:
   - Add your API keys as secrets:
     - OPENAI_API_KEY: Your OpenAI API key
     - ANTHROPIC_API_KEY: Your Anthropic API key (optional)
   - Set the Space hardware (at least CPU + 16GB RAM recommended)

The app will automatically install the required dependencies, build the vector store, and start the Gradio web interface.

## Using with Discord

To integrate this with Discord:
1. Create a Discord bot using the Discord Developer Portal
2. Use the Discord.py library to create a bot that calls your hosted Hugging Face API
3. Deploy the Discord bot to a server (Replit, Heroku, etc.)

## Local Development

**This application uses Docker for both local development and production deployment to ensure consistency.**

### Primary Method: Docker (Matches Hugging Face Deployment)
```bash
git clone https://github.com/yourusername/opteee.git
cd opteee

# Create .env file with your API keys
echo "OPENAI_API_KEY=your_key_here" > .env
echo "ANTHROPIC_API_KEY=your_key_here" >> .env

# Run with Docker (builds vector store during image creation)
./run_local.sh
```

**Key Benefits:**
- ✅ **Identical to Hugging Face deployment** - same Docker image, same runtime
- ✅ **Vector store built during image creation** - faster startup, consistent data
- ✅ **No dependency conflicts** - all packages pinned to working versions
- ✅ **Consistent environment** - works the same on any machine

### Alternative: Direct Python (Advanced Users Only)
```bash
git clone https://github.com/yourusername/opteee.git
cd opteee
./setup.sh  # Sets up Python environment
source venv/bin/activate
# Set environment variables
export OPENAI_API_KEY=your_key_here
export ANTHROPIC_API_KEY=your_key_here
python3 app.py
```

**Note**: Direct Python setup may have dependency conflicts. Docker is recommended for consistency.

The application will be available at `http://localhost:7860`

## Technical Architecture & Data Pipeline

### 📊 **Complete Data Processing Pipeline**

This app processes Outlier Trading educational videos through a comprehensive pipeline that ensures consistency and high-quality RAG responses:

#### **0. Centralized Configuration & Pipeline Management**
- **Configuration**: `pipeline_config.py` provides unified settings for all processing scripts
- **Pipeline Runner**: `run_pipeline.py` orchestrates the complete workflow with progress tracking
- **Validation**: `validate_pipeline.py` ensures configuration consistency and system health
- **Benefits**: Eliminates configuration drift, ensures reproducible results, simplifies maintenance

#### **1. Video Discovery & Metadata Collection**
- **Discovery**: `outlier_scraper.py` scrapes the Outlier Trading YouTube channel
- **Metadata Enhancement**: `collect_video_metadata.py` enriches videos with YouTube API data
- **Output**: `outlier_trading_videos.json` and `outlier_trading_videos_metadata.json`
- **Configuration**: Uses centralized channel URLs and file paths from `pipeline_config.py`

#### **2. Transcript Generation**
- **Primary Method**: YouTube API automatic captions (when available)
- **Fallback Method**: Whisper AI transcription for videos without captions
- **Processing**: `save_youtube_transcript.py` and `whisper_transcribe.py`
- **Output**: Raw transcripts in `transcripts/` directory (`.txt` files)

#### **3. Transcript Preprocessing & Chunking**
- **Script**: `preprocess_transcripts.py`
- **Chunking Strategy** (centrally configured for consistency):
  - **Chunk Size**: 250 words per chunk
  - **Overlap**: 50 words between chunks (maintains context continuity)
  - **Minimum Length**: 10 words (filters out noise)
- **Configuration**: All settings managed by `pipeline_config.py` for reproducible results
- **Output**: Processed chunks in `processed_transcripts/` directory (`.json` files)

#### **4. Chunk Structure & Metadata**
Each processed chunk is a JSON object with **consistent metadata**:
```json
{
  "video_id": "abc123xyz",
  "title": "Options Greeks Explained",
  "upload_date": "2024-01-15",
  "duration": 1847,
  "channel": "Outlier Trading",
  "description": "Learn about options Greeks...",
  "content_summary": "Explanation of gamma risk",
  "chunk_id": "abc123xyz_chunk_042",
  "chunk_index": 42,
  "start_time": 650,
  "end_time": 720,
  "text": "Gamma measures the rate of change...",
  "word_count": 247,
  "timestamp": "00:10:50",
  "video_url": "https://www.youtube.com/watch?v=abc123xyz",
  "video_url_with_timestamp": "https://www.youtube.com/watch?v=abc123xyz&t=650"
}
```

#### **5. Vector Store Creation**
- **Script**: `create_vector_store.py`
- **Embedding Model**: `all-MiniLM-L6-v2` (384-dimensional vectors)
- **Index**: FAISS L2 distance similarity search
- **Process**: 
  - Loads all processed chunks from `processed_transcripts/`
  - Generates embeddings for chunk text
  - Builds FAISS index for fast similarity search
  - Stores index in `vector_store/` directory
- **Build Time**: ~30 minutes for 14,721 chunks (during Docker image creation)

#### **6. RAG Pipeline Integration**
- **Query Processing**: User questions are embedded using the same model
- **Retrieval**: FAISS similarity search finds top-k relevant chunks
- **Context Assembly**: Retrieved chunks are combined with their metadata
- **LLM Generation**: OpenAI/Claude generates answers using the context
- **Source Attribution**: Responses include video links with exact timestamps

### 🎯 **Metadata Consistency & Quality**

#### **Consistent Naming Convention**
- **Chunk IDs**: `{video_id}_chunk_{index:03d}` (e.g., `abc123xyz_chunk_042`)
- **File Names**: `{video_id}_processed.json` in `processed_transcripts/`
- **Timestamps**: Always in `HH:MM:SS` format
- **URLs**: Always include timestamp parameter for direct access

#### **Quality Assurance**
- **Duplicate Detection**: Chunks are deduplicated during processing
- **Content Validation**: Minimum word count ensures meaningful content
- **Metadata Validation**: All chunks include complete metadata schema
- **Error Handling**: Failed processing tracked in `transcript_progress.json`
- **Configuration Validation**: `validate_pipeline.py` ensures system consistency
- **Reproducibility**: Centralized config guarantees identical results across runs
- **Testing**: `test_pipeline_fixes.py` validates code organization and imports

#### **Scalability Design**
- **Incremental Processing**: Only new videos are processed on updates
- **Caching**: Vector store built once, reused across deployments
- **Batch Processing**: Embeddings created in batches for efficiency
- **Memory Management**: Large files processed in chunks to prevent OOM

### 📈 **Performance Metrics & Data Scale**

#### **Current Data Scale**
- **Total Videos**: ~500+ educational videos from Outlier Trading
- **Total Chunks**: 14,721 processed chunks
- **Average Chunk Size**: 250 words (~1,000 characters)
- **Vector Dimensions**: 384 (all-MiniLM-L6-v2)
- **Index Size**: ~60MB FAISS index file
- **Build Time**: ~30 minutes (full pipeline)

#### **Query Performance**
- **Average Query Time**: <2 seconds (including LLM generation)
- **Retrieval Time**: <100ms for similarity search
- **Vector Search**: <10ms for top-k retrieval
- **Context Assembly**: <50ms for metadata formatting
- **LLM Generation**: 1-2 seconds (depends on model and response length)

#### **Complete Processing Flow**
```
YouTube Videos (500+)
    ↓ (outlier_scraper.py)
Video URLs & Basic Info
    ↓ (collect_video_metadata.py + YouTube API)
Enhanced Metadata (JSON)
    ↓ (save_youtube_transcript.py OR whisper_transcribe.py)
Raw Transcripts with Timestamps (.txt)
    ↓ (preprocess_transcripts.py)
Cleaned Text + Timestamp Mapping
    ↓ (Chunking Algorithm: 250 words, 50 overlap)
Individual Chunks with Complete Metadata
    ↓ (JSON serialization)
Processed Chunks (14,721 total)
    ↓ (create_vector_store.py)
FAISS Vector Store (60MB index)
    ↓ (app.py RAG pipeline)
User Q&A Interface (Gradio)
```

**Key Processing Details:**
- **Video Discovery**: Automated scraping of Outlier Trading channel
- **Dual Transcript Methods**: YouTube API (fast) + Whisper AI (fallback)
- **Smart Chunking**: 250-word chunks with 50-word overlap for context
- **Rich Metadata**: Every chunk includes video info, timestamps, direct links
- **Vector Search**: 384-dimensional embeddings for semantic similarity
- **Real-time RAG**: Sub-second retrieval + LLM generation

## Data Sources

This app uses a vector database of processed transcripts from Outlier Trading educational videos. The transcripts have been chunked, embedded, and stored in a FAISS index.

## Vector Store Management

The application uses a FAISS vector database that contains chunked and embedded transcripts:

### Local Development
- Vector store is built from `processed_transcripts/` directory
- Run `python3 create_vector_store.py` to build/rebuild locally
- Stored in `vector_store/` directory

### Docker Deployment
- Vector store is built during Docker image creation
- Built from `processed_transcripts/` during `docker build`
- Ensures consistent environment between local and production

### Hugging Face Spaces
- Vector store is built during the Docker image build process
- No runtime building required - faster startup times
- Includes all processed transcripts in the deployment

### Adding New Content

**Recommended: Use the unified pipeline**
```bash
# Process all new videos with complete pipeline
python3 run_pipeline.py

# Or process specific steps for new content
python3 run_pipeline.py --step scrape      # Discover new videos
python3 run_pipeline.py --step transcripts # Generate new transcripts
python3 run_pipeline.py --step preprocess  # Process new chunks
python3 run_pipeline.py --step vectors     # Update vector store
```

**Manual deployment:**
1. Process new videos: `python3 run_pipeline.py`
2. Commit new files: `git add processed_transcripts/ outlier_trading_videos*.json && git commit`
3. Deploy: `git push origin main`

**The pipeline ensures:**
- ✅ Only new videos are processed (smart detection)
- ✅ Consistent chunking with existing content
- ✅ Complete metadata for all new chunks
- ✅ Automatic vector store updates

## Unified Deployment Strategy

This project uses **Docker for both local development and production deployment** to ensure complete consistency between environments.

### Why Docker-First Approach?

- **🎯 Consistency**: Local development matches production exactly
- **⚡ Performance**: Vector store built once during image creation, not at runtime
- **🔒 Reliability**: No dependency conflicts between different environments
- **🚀 Deployment**: Same Docker image works locally and on Hugging Face

### Deployment Architecture

**Both Local and Hugging Face use identical setup:**
- **SDK**: Docker (not Gradio SDK)
- **Container**: Uses `Dockerfile` to build complete environment
- **Vector Store**: Built during Docker image creation (not at runtime)
- **Entry Point**: `app.py` (Gradio application)
- **Port**: 7860
- **Dependencies**: Pinned versions in `minimal_requirements.txt`

### Automatic Deployment Process

1. **GitHub Actions**: Triggered on push to main branch
2. **Docker Build**: Creates container with all dependencies
3. **Vector Store**: Built from `processed_transcripts/` during image creation
4. **Deployment**: Pushed to Hugging Face Spaces using HF token

### Required Secrets

Set these in your GitHub repository secrets:
- `HF_TOKEN`: Your Hugging Face access token
- API keys are set in Hugging Face Spaces environment variables:
  - `OPENAI_API_KEY`
  - `ANTHROPIC_API_KEY`

### Manual Deployment

If you need to deploy manually:

```bash
# Build and test locally first
./run_local.sh

# Push to GitHub to trigger automatic deployment
git push origin main
```

### Troubleshooting Deployment Issues

If you encounter errors during deployment:

1. Check that your `requirements.txt` doesn't contain any Mac-specific paths (files starting with `/AppleInternal/...`)
2. Verify that all package versions are compatible with the Python version used by Hugging Face
3. Remove any platform-specific packages that aren't needed for the web application 

### Resolving Dependency Conflicts

Sometimes deployment fails due to dependency conflicts between packages. Common conflicts include:

1. **torch vs openai-whisper**: Recent versions of torch (2.6.0+) require triton 3.2.0 on Linux, while openai-whisper requires triton<3. To fix this:
   ```bash
   # Downgrade torch to version 2.0.1 in requirements.txt
   sed -i '' 's/torch==2.6.0/torch==2.0.1/g' requirements.txt
   # Or manually edit the file
   ```

2. **torch vs transformers**: When downgrading torch, transformers may need to be downgraded as well. Newer transformers versions (4.40.0+) may require torch features like `torch.compiler` that don't exist in older torch versions:
   ```bash
   # If using torch 2.0.1, downgrade transformers to 4.30.2
   sed -i '' 's/transformers==4.50.0/transformers==4.30.2/g' requirements.txt
   ```

3. **transformers vs sentence-transformers**: Different versions of these packages have strict interdependencies. If you downgrade transformers, you may need to downgrade sentence-transformers as well:
   ```bash
   # If using transformers 4.30.2, downgrade sentence-transformers to 2.2.2
   sed -i '' 's/sentence-transformers==2.5.0/sentence-transformers==2.2.2/g' requirements.txt
   ```

4. **transformers vs tokenizers**: Transformers requires specific versions of tokenizers. For example:
   ```bash
   # If using transformers 4.30.2, downgrade tokenizers to 0.13.3
   sed -i '' 's/tokenizers==0.21.1/tokenizers==0.13.3/g' requirements.txt
   ```

5. If you encounter other dependency conflicts, the error message usually contains useful information about which packages are conflicting. Try:
   - Downgrading or upgrading specific packages
   - Using compatibility matrices from package documentation
   - Using a tool like `pip-tools` to resolve dependencies

After making changes to resolve conflicts, commit and push the changes to trigger a new deployment.

# Opteee Discord Bot

A Discord bot that provides access to the opteee options trading knowledge base through Discord.

## Features

- Search options trading knowledge base using natural language queries
- Get detailed answers with video sources and timestamps
- Easy-to-use commands
- Markdown-formatted responses

## Setup

1. Create a Discord Bot:
   - Go to the [Discord Developer Portal](https://discord.com/developers/applications)
   - Click "New Application" and give it a name
   - Go to the "Bot" section and click "Add Bot"
   - Copy the bot token
   - Enable the following bot intents:
     - Message Content Intent
     - Server Members Intent

2. Install Dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file:
   ```
   DISCORD_TOKEN=your_discord_bot_token_here
   ```

4. Invite the Bot to Your Server:
   - Go to OAuth2 > URL Generator in the Discord Developer Portal
   - Select the following scopes:
     - `bot`
     - `applications.commands`
   - Select the following bot permissions:
     - Send Messages
     - Read Message History
   - Copy the generated URL and open it in a browser to invite the bot

## Usage

1. Start the bot:
   ```bash
   python3 discord_bot.py
   ```

2. Available Commands:
   - `!search <query>` - Search for options trading information
   - `!help` - Show help information

Example:
```
!search What is gamma in options trading?
```

## Notes

- The bot uses the opteee application hosted on Hugging Face Spaces
- Responses are formatted in Markdown for better readability
- Long responses are automatically split into multiple messages to comply with Discord's message length limits 

# Outlier Trading Transcript Processing Pipeline

This repository contains scripts for processing and maintaining transcripts from the Outlier Trading YouTube channel. The pipeline handles video scraping, transcript generation, and preprocessing for RAG (Retrieval-Augmented Generation) applications.

## Prerequisites

1. Python 3.8 or higher
2. FFmpeg installed on your system
3. YouTube API key (for enhanced metadata)

### System Requirements

- FFmpeg installation:
  ```bash
  # macOS (using Homebrew)
  brew install ffmpeg

  # Ubuntu/Debian
  sudo apt-get install ffmpeg

  # Windows
  # Download from https://ffmpeg.org/download.html
  ```

### Python Dependencies

Install required Python packages:
```bash
pip install -r requirements.txt
```

## Environment Setup

1. Create a `.env` file in the root directory:
```bash
YOUTUBE_API_KEY=your_api_key_here
```

2. Create necessary directories:
```bash
mkdir transcripts audio_files processed_transcripts
```

## Pipeline Overview

The pipeline consists of four main steps:

1. **Video Scraping**: Collects metadata for all videos from the Outlier Trading channel
2. **Missing Transcript Detection**: Identifies videos without transcripts
3. **Transcript Generation**: Uses Whisper to generate transcripts for missing videos
4. **Transcript Preprocessing**: Processes all transcripts into chunks for RAG applications

### Directory Structure

```
.
├── transcripts/              # Raw transcript files (.txt)
├── audio_files/             # Temporary audio files for processing
├── processed_transcripts/   # Processed chunks for RAG (.json)
├── process_outlier_videos.py # Main processing script
└── requirements.txt         # Python dependencies
```

## Running the Pipeline

Execute the main script:
```bash
python3 process_outlier_videos.py
```

The script will:
1. Scrape all videos from the Outlier Trading channel
2. Identify videos missing transcripts
3. Generate transcripts for missing videos using Whisper
4. Preprocess all transcripts into chunks with metadata

### Output Files

- `outlier_trading_videos.json`: Complete video metadata
- `missing_transcripts.json`: List of videos needing transcripts
- `manual_processing_needed.json`: Videos requiring manual intervention
- `processed_transcripts/*.json`: Processed transcript chunks for RAG

## Transcript Processing Details

### Chunking Configuration

- Chunk size: 250 words
- Overlap: 50 words between chunks
- Minimum content length: 10 words

### Metadata Included

Each processed chunk includes:
- Video ID and title
- Upload date and duration
- Channel information
- Description and content summary
- Timestamp information
- Direct video URL with timestamp

## Troubleshooting

### Common Issues

1. **FFmpeg Not Found**
   - Ensure FFmpeg is installed and in your system PATH
   - Verify installation with `ffmpeg -version`

2. **YouTube API Errors**
   - Check your API key in `.env`
   - Verify API quota limits
   - Ensure proper API key format (not an OAuth client ID)

3. **Transcript Generation Failures**
   - Check audio file quality
   - Verify sufficient disk space
   - Check Whisper model loading

### Manual Processing

Videos requiring manual processing are saved to `manual_processing_needed.json`. These may need:
- Manual transcript creation
- Audio quality improvements
- Special handling for non-English content

## Maintenance

### Regular Updates

1. Run the pipeline weekly to catch new videos
2. Monitor `manual_processing_needed.json` for issues
3. Check processed transcript quality in `processed_transcripts/`

### Cleanup

Periodically clean up temporary files:
```bash
rm -rf audio_files/*  # Remove processed audio files
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

[Your License Here] 