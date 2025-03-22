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

## Vector Database for Transcript Search

This project now includes functionality to create a vector database from the processed transcripts, enabling semantic search capabilities for finding relevant content.

### Processing Pipeline

1. **Data Collection**: Videos metadata is collected using `collect_video_metadata.py`
2. **Transcript Generation**: Transcripts are generated using Whisper and stored in the `transcripts` directory
3. **Transcript Processing**: Transcripts are cleaned, chunked, and enriched with metadata using `preprocess_transcripts.py`
4. **Vector Database Creation**: Chunks are converted to embeddings and stored in a FAISS vector database using `create_vector_store.py`
5. **Semantic Search**: Search the vector database for relevant content using `search_transcripts.py`

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