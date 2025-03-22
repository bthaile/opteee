# YouTube Transcript Processor

This project downloads and processes YouTube transcripts. If a video doesn't have a transcript, it uses Whisper to generate one from the audio.

## Setup

The project requires Python 3.11.7 for best compatibility with the Whisper library.

### Automated Setup (Recommended)

Run the setup script to automatically configure the environment:

```bash
# Make the script executable
chmod +x setup.sh

# Run the script
./setup.sh
```

The script will:
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
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Activate the virtual environment:
```bash
source venv/bin/activate
```

2. Run the main script:
```bash
python save_youtube_transcript.py
```

3. To process failed videos with Whisper:
```bash
python whisper_transcribe.py
```

## YouTube Video Metadata Collection

To create a comprehensive CSV file with metadata about all videos:

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Obtain a YouTube Data API key:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project
   - Enable the YouTube Data API v3
   - Create credentials (API Key)
   - Copy your API Key

3. Edit the `collect_video_metadata.py` script and replace `YOUR_YOUTUBE_API_KEY` with your actual API key

4. Run the metadata collection script:
   ```
   python collect_video_metadata.py
   ```

This will create a new file called `outlier_trading_videos_metadata.csv` with comprehensive information about each video, including:
- Video ID, title, and URL
- Channel name
- Upload date and duration
- View count and likes
- Description and tags
- Thumbnail URL
- Transcript information (path, creation date, method)
- Guest names (if detected)
- Content summary

Note: If you don't provide a YouTube API key, the script will still work but with limited metadata from yt-dlp.

## Important Files

- **transcript_progress.json**: Tracks which videos have been processed, failed, or processed with Whisper. **BACK UP THIS FILE** if you need to recreate the project!
- **transcripts/**: Directory where all transcripts are saved
- **requirements.txt**: Lists all required packages
- **setup.sh**: Automated setup script

## Recreating the Project

If you need to recreate the project:

1. Clone or recreate the project files
2. **Copy your backed-up transcript_progress.json file to the project directory**
3. Run the setup script: `./setup.sh`

This ensures you don't reprocess videos that have already been transcribed. 