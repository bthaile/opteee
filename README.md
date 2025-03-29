---
title: opteee
emoji: 🔥
colorFrom: blue
colorTo: red
sdk: gradio
app_port: 7860
pinned: false
---

# Options Trading Knowledge Search

Debug version to understand Hugging Face Spaces environment.

## Features

- Semantic search using sentence-transformers
- FAISS vector database for fast retrieval
- Direct links to specific timestamps in relevant videos
- Built with Flask - not using Gradio

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

To create a comprehensive collection of metadata about all videos:

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Generate the initial JSON file with video information:
   ```
   python outlier_scraper.py
   ```
   This will create `outlier_trading_videos.json` containing basic information about all available videos.

3. Obtain a YouTube Data API key:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project
   - Enable the YouTube Data API v3
   - Create credentials (API Key)
   - Copy your API Key

4. Create a `.env` file in the project root and add your API key:
   ```
   YOUTUBE_API_KEY=your-api-key-here
   ```

5. Run the metadata collection script:
   ```
   python collect_video_metadata.py
   ```

This will create a new file called `outlier_trading_videos_metadata.json` with comprehensive information about each video, including:
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

## Vector Database for Transcript Search

This project now includes functionality to create a vector database from the processed transcripts, enabling semantic search capabilities for finding relevant content.

### Processing Pipeline

1. **Data Collection**: Initial video data is collected using `outlier_scraper.py` which generates a JSON file
2. **Metadata Enhancement**: Detailed video metadata is collected using `collect_video_metadata.py` and stored in JSON format
3. **Transcript Generation**: Transcripts are generated using Whisper and stored in the `transcripts` directory
4. **Transcript Processing**: Transcripts are cleaned, chunked, and enriched with metadata using `preprocess_transcripts.py`
5. **Vector Database Creation**: Chunks are converted to embeddings and stored in a FAISS vector database using `create_vector_store.py`
6. **Semantic Search**: Search the vector database for relevant content using `search_transcripts.py`

### Setting Up the Vector Database

1. Make sure all dependencies are installed:
   ```
   pip install -r requirements.txt
   ```

2. Run the preprocessing script to create cleaned and chunked transcripts:
   ```
   python preprocess_transcripts.py
   ```

3. Create the vector database:
   ```
   python create_vector_store.py
   ```
   
   Optional: Add `--test-search` to test the search functionality immediately:
   ```
   python create_vector_store.py --test-search
   ```

### Searching for Content

Search for relevant transcript sections using:
```
python search_transcripts.py "your search query here"
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

   **a. Command-line Interface:**
   ```
   python rag_pipeline.py "What are the best options strategies for beginners?"
   ```

   Options:
   - `--top-k 7`: Retrieve 7 sources (default is 5)
   - `--model "gpt-4"`: Use a specific OpenAI model (default is gpt-3.5-turbo)
   - `--temperature 0.2`: Set temperature for response generation (default is 0.1)
   - `--hide-sources`: Don't show source information in output

   **b. Interactive Application:**
   ```
   python opteee_app.py
   ```
   This launches an interactive application where you can:
   - Ask questions about options trading
   - Adjust settings (number of sources, model, temperature)
   - See answers with source attribution

### How It Works

1. **Retrieval**: The system uses the FAISS vector database to find the most relevant transcript chunks for your question
2. **Context Formation**: It combines these chunks into a comprehensive context
3. **Prompt Creation**: It creates a prompt that includes both the retrieved context and your question
4. **Generation**: An LLM (like GPT-3.5 or GPT-4) generates an answer based on the context
5. **Source Attribution**: The system shows which videos/timestamps the information came from

### Example Usage

```
$ python rag_pipeline.py "What is gamma in options trading?"

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
   - Select "Gradio" as the SDK
   - Connect to your GitHub repository
   
3. Configure your Space:
   - Add your API keys as secrets:
     - OPENAI_API_KEY: Your OpenAI API key
     - ANTHROPIC_API_KEY: Your Anthropic API key (optional)
   - Set the Space hardware (at least CPU + 16GB RAM recommended)

The app will automatically install the required dependencies and start the Gradio web interface.

## Using with Discord

To integrate this with Discord:
1. Create a Discord bot using the Discord Developer Portal
2. Use the Discord.py library to create a bot that calls your hosted Hugging Face API
3. Deploy the Discord bot to a server (Replit, Heroku, etc.)

## Local Development

To run this app locally:

```bash
git clone https://github.com/yourusername/opteee.git
cd opteee
pip install -r requirements.txt
python gradio_app.py
```

## Data Sources

This app uses a vector database of processed transcripts from Outlier Trading educational videos. The transcripts have been chunked, embedded, and stored in a FAISS index.

## Deployment to Hugging Face

This project is configured to deploy automatically to Hugging Face Spaces using GitHub Actions whenever changes are pushed to the main branch.

### Creating a Proper requirements.txt File

When deploying to Hugging Face, it's important to create a proper `requirements.txt` file that works across platforms. The standard `pip freeze` on macOS can include Apple-specific system package paths that will cause deployment failures.

To create a clean `requirements.txt` file on macOS that will work on Hugging Face:

```bash
# Make sure your virtual environment is activated
source venv/bin/activate

# Create a clean requirements file without paths to local system files
pip list --format=freeze | grep -v "@ file://" > requirements.txt
```

This command filters out any package that has a local file path reference (which typically happens with system packages on macOS).

Alternatively, you can manually install all required packages in your virtual environment and then use:

```bash
pip freeze --exclude-editable > requirements.txt
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
   python discord_bot.py
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
python process_outlier_videos.py
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