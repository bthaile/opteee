---
title: opteee
emoji: 🔥
colorFrom: blue
colorTo: red
sdk: docker
app_port: 7860
pinned: false
---

# OPTEEE - Options Trading Knowledge Search

AI-powered search through Outlier Trading educational videos using RAG (Retrieval-Augmented Generation).

## 🚀 Quick Start

**Every new terminal session requires these commands:**

```bash
cd /Users/bthaile/gitrepos/opteee
source venv/bin/activate

# Run the main application
python3 app.py
# Visit: http://localhost:7860
```

## 📋 **Complete Processing Pipeline with Verification**

### **Step 1: Video Discovery & Metadata Collection**

**Run:**
```bash
python3 run_pipeline.py --step scrape
```

**Verification:**
```bash
# Check video metadata files exist
ls -la outlier_trading_videos*.json

# Verify video count
python3 -c "
import json
with open('outlier_trading_videos.json') as f:
    data = json.load(f)
print(f'✅ Discovered {len(data)} videos')
"
```

**Expected Output:**
- `outlier_trading_videos.json` - Basic video metadata
- `outlier_trading_videos_metadata.json` - Enhanced metadata (if YouTube API key available)
- ~500+ videos discovered

### **Step 2: Transcript Generation**

**Standard Processing:**
```bash
python3 run_pipeline.py --step transcripts
```

**⚡ Parallel Processing (Recommended for M1 Max/High-End Systems):**
```bash
# Use default parallel settings (8 workers, "base" model)
python3 parallel_transcribe.py

# Custom parallel configuration
python3 parallel_transcribe.py --workers 8 --model base --gpu

# Fix existing timestamps with parallel processing
python3 fix_timestamp_issue.py --parallel --workers 8
```

**Verification:**
```bash
# Check transcript files
ls transcripts/ | wc -l

# Verify transcript format has timestamps
head -5 transcripts/[VIDEO_ID].txt

# Check parallel processing progress
cat transcripts/parallel_progress.json
```

**Expected Output:**
- Files in `transcripts/` directory with format `[VIDEO_ID].txt`
- Each transcript line formatted as: `XX.XXs: transcript content`
- Progress tracking in `transcript_progress.json` or `parallel_progress.json`
- **Parallel processing**: 3-10x faster than sequential processing

### **Step 3: Transcript Processing & Chunking**

**Run:**
```bash
python3 run_pipeline.py --step preprocess
```

**Verification:**
```bash
# Check processed transcript chunks
ls processed_transcripts/ | wc -l

# Verify chunk structure
python3 -c "
import json
import glob
files = glob.glob('processed_transcripts/*.json')
if files:
    with open(files[0]) as f:
        chunk = json.load(f)
    print(f'✅ Sample chunk has {len(chunk)} fields')
    print(f'✅ Required fields: {\"start_timestamp_seconds\" in chunk}')
    print(f'✅ Video URL: {chunk.get(\"video_url_with_timestamp\", \"Missing\")}')
"
```

**Expected Output:**
- JSON files in `processed_transcripts/` directory
- Each chunk contains: `video_id`, `title`, `start_timestamp_seconds`, `video_url_with_timestamp`
- ~14,000+ chunks created

### **Step 4: Vector Store Creation**

**Run:**
```bash
python3 run_pipeline.py --step vectors
```

**Verification:**
```bash
# Check vector store files
ls -la vector_store/

# Verify vector store contents
python3 -c "
import pickle
with open('vector_store/transcript_metadata.pkl', 'rb') as f:
    metadata = pickle.load(f)
print(f'✅ Vector store contains {len(metadata)} chunks')
timestamps = sum(1 for chunk in metadata if chunk.get('start_timestamp_seconds', 0) > 0)
print(f'✅ Chunks with timestamps: {timestamps}')
"
```

**Expected Output:**
- `vector_store/transcript_embeddings.faiss` - FAISS index (~60MB)
- `vector_store/transcript_metadata.pkl` - Chunk metadata
- All chunks should have proper timestamps (not 0)

### **Step 5: System Validation**

**Run:**
```bash
python3 validate_system.py
```

**Verification:**
```bash
# Test the RAG pipeline
python3 rag_pipeline.py "What is gamma in options trading?" --provider claude

# Check for working video links with timestamps
python3 -c "
import re
# This should show video links with &t=XXX timestamps
"
```

**Expected Output:**
- All API keys validated
- Vector store verified
- RAG pipeline returns answers with timestamped video links

## ⚡ **Parallel Processing & Performance Optimization**

### **🚀 High-Performance Transcription**

For systems with multiple CPU cores (especially M1 Max, M2, or high-end Intel/AMD), parallel processing can dramatically speed up transcription:

```bash
# Quick system analysis
python3 parallel_transcribe.py --info

# Benchmark different models and worker counts
python3 benchmark_models.py --test-files 20 --models "tiny,base"

# Optimal parallel transcription
python3 parallel_transcribe.py --workers 8 --model base
```

### **📊 Performance Comparison**

| System | Sequential | Parallel (8 workers) | Speedup |
|--------|------------|---------------------|---------|
| M1 Max | 2-3 hours | 15-30 minutes | 4-8x faster |
| M2 Pro | 3-4 hours | 20-45 minutes | 4-6x faster |
| Intel i7 | 4-6 hours | 30-60 minutes | 3-5x faster |

### **🎯 Model Selection Guide**

**For Sequential Processing:**
- `tiny`: Fastest processing, 95% accuracy
- `base`: Good balance of speed and accuracy

**For Parallel Processing:**
- `base`: **Recommended** - Better CPU utilization
- `tiny`: May underutilize CPU cores

### **🔧 Audio File Diagnostics**

```bash
# Check for problematic audio files
python3 check_audio_files.py

# Auto-fix common audio issues
python3 check_audio_files.py --fix

# Validate specific directory
python3 check_audio_files.py --dir audio_files_processed
```

### **📈 Benchmarking Tools**

```bash
# Test your system's optimal configuration
python3 benchmark_models.py

# Compare models with different worker counts
python3 benchmark_models.py --models "tiny,base,small" --max-workers 10

# Test specific file count
python3 benchmark_models.py --test-files 50
```

## 🔧 **Key Features**

### **Multiple User Interfaces**

1. **🌐 Web Interface (Primary)**
   - `python3 app.py` → `http://localhost:7860`
   - AI-powered Q&A with source attribution

2. **💻 Command Line Interface**
   - `python3 rag_pipeline.py "your question"`
   - `python3 search_transcripts.py "search terms"`

3. **🤖 Discord Bot**
   - `cd discord/ && python3 discord_bot.py`
   - Requires `DISCORD_TOKEN` in environment

### **AI Model Support**

- **OpenAI**: `gpt-4o`, `gpt-4`, `gpt-3.5-turbo`
- **Anthropic**: `claude-sonnet-4-20250514`, `claude-3-5-sonnet-20241022`
- **Automatic temperature fallback** for models that don't support it

### **Timestamp Accuracy**

- **Exact timestamps**: Video links jump to precise content location
- **Format**: `https://youtube.com/watch?v=VIDEO_ID&t=SECONDS`
- **Chunk precision**: Each chunk maps to specific video moments

## 🛠️ **Configuration**

### **Environment Variables**
```bash
# Required (at least one)
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key

# Optional
YOUTUBE_API_KEY=your_youtube_key
DISCORD_TOKEN=your_discord_token
```

### **Additional Dependencies for Parallel Processing**
```bash
# Install additional dependencies (already in requirements.txt)
pip install psutil torch
```

### **Key Settings** (in `pipeline_config.py`)
- **Chunk Size**: 250 words
- **Overlap**: 50 words
- **Vector Model**: `all-MiniLM-L6-v2`
- **Default Temperature**: 0.2

### **Parallel Processing Settings**
- **WHISPER_MODEL**: `"tiny"` (default for sequential processing)
- **WHISPER_MODEL_PARALLEL**: `"base"` (optimized for parallel processing)
- **PARALLEL_WORKERS**: `8` (default worker count)
- **PARALLEL_ENABLE**: `True` (enable parallel processing by default)

### **Model Performance Characteristics**
- **tiny**: 39M parameters, ~32x faster than base, 95% accuracy
- **base**: 74M parameters, reference speed, 99% accuracy
- **small**: 244M parameters, ~2x slower than base, 99.5% accuracy

## 🎯 **Common Commands**

### **Basic Operations**
```bash
# Complete pipeline
python3 run_pipeline.py

# System validation
python3 validate_system.py

# Test RAG pipeline
python3 test_rag.py

# Search transcripts
python3 search_transcripts.py "covered calls" --top-k 5

# Ask questions
python3 rag_pipeline.py "What is theta decay?"
```

### **⚡ Parallel Processing Commands**
```bash
# High-performance parallel transcription
python3 parallel_transcribe.py

# Custom parallel configuration
python3 parallel_transcribe.py --workers 6 --model base --gpu

# Fix timestamps with parallel processing
python3 fix_timestamp_issue.py --parallel --workers 8

# System performance analysis
python3 parallel_transcribe.py --info

# Benchmark your system
python3 benchmark_models.py --test-files 10
```

### **🔧 Diagnostic Commands**
```bash
# Check audio file health
python3 check_audio_files.py

# Fix problematic audio files
python3 check_audio_files.py --fix

# Validate specific directory
python3 check_audio_files.py --dir audio_files_processed

# Resume interrupted processing
python3 parallel_transcribe.py --resume
```

## 📊 **System Stats**

- **Videos**: ~500+ from Outlier Trading
- **Chunks**: ~14,000+ processed segments
- **Vector Store**: 60MB FAISS index
- **Query Time**: <2 seconds (including LLM generation)
- **Accuracy**: Exact video timestamps for navigation

### **⚡ Performance Metrics**
- **Sequential transcription**: 2-6 hours for full dataset
- **Parallel transcription**: 15-60 minutes for full dataset (system dependent)
- **Optimal worker count**: 6-8 workers for most systems
- **Model recommendation**: `base` for parallel, `tiny` for sequential
- **Memory usage**: ~1-2GB per worker process

## 🔧 **Troubleshooting**

### **Common Issues**

1. **"ModuleNotFoundError"** → Run setup commands in every new terminal
2. **"No timestamps in results"** → Regenerate transcripts with `python3 fix_timestamp_issue.py --parallel`
3. **"API key not found"** → Check `.env` file or environment variables
4. **"Vector store not found"** → Run `python3 create_vector_store.py`
5. **"Failed to load audio"** → Check audio files with `python3 check_audio_files.py --fix`
6. **"Transcription too slow"** → Use parallel processing: `python3 parallel_transcribe.py`
7. **"Worker process crashed"** → Reduce workers: `python3 parallel_transcribe.py --workers 4`

### **Verification Commands**
```bash
# Check system health
python3 validate_system.py

# Test specific components
python3 test_single_question.py "test question"

# Check file counts
python3 count_files.py transcripts
python3 count_files.py processed_transcripts

# Check parallel processing capabilities
python3 parallel_transcribe.py --info

# Verify audio file health
python3 check_audio_files.py

# Test system performance
python3 benchmark_models.py --test-files 5
```

## 🚀 **Deployment**

### **Local Development**
```bash
# Docker (recommended)
./run_local.sh

# Python environment
source venv/bin/activate && python3 app.py
```

### **Production (Hugging Face)**
- Uses Docker for consistency
- Vector store built during image creation
- Automatic deployment via GitHub Actions

## 📚 **Architecture**

```
YouTube Videos → Video Discovery → Transcript Generation → 
Chunking & Metadata → Vector Store → RAG Pipeline → User Interface
```

**Key Components:**
- **FAISS Vector Store**: Semantic similarity search
- **Sentence Transformers**: Text embedding generation
- **OpenAI/Claude**: Answer generation
- **Gradio**: Web interface
- **Discord.py**: Bot interface

## 🎉 **Success Indicators**

✅ **Working System:**
- Video links include `&t=XXX` timestamps
- RAG answers include source attribution
- Search returns relevant results
- All validation checks pass

❌ **Issues to Fix:**
- Links go to `&t=0` (timestamp issue)
- No source attribution in answers
- Empty search results
- Validation errors

---

*For detailed troubleshooting and advanced configuration, see the development documentation in the repository.*
