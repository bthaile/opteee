# Setting Up Vector Store for Hugging Face Spaces

This guide explains how to handle large vector store files for your Hugging Face Space deployment.

## Problem

Hugging Face Spaces has a 10MB file size limit for regular Git storage. Our vector store files exceed this limit:
- `vector_store/transcript_index.faiss`
- `vector_store/transcript_metadata.pkl`

## Solution

Instead of including these large files in the Git repository, we'll:
1. Host them externally (Dropbox, Google Drive, etc.)
2. Download them during app startup on Hugging Face

## Step-by-Step Instructions

### 1. Create the Vector Store Archive

Run the following script to create a compressed archive of your vector store:

```bash
python prepare_vector_store.py
```

This will create a file called `vector_store.tar.gz`.

### 2. Upload to External Storage

Upload the `vector_store.tar.gz` file to an external storage service:
- **Dropbox**: Upload and create a shared link
- **Google Drive**: Upload and create a sharing link
- **Hugging Face**: You can also use the Hugging Face [datasets](https://huggingface.co/docs/hub/datasets-adding) to host large files

Make sure to:
- Get a direct download link (not just a sharing page)
- Set sharing permissions to "Anyone with the link"

### 3. Update the Download Script

Edit `download_and_setup.py` and replace the `VECTOR_STORE_URL` with your direct download link:

```python
VECTOR_STORE_URL = "https://your-direct-download-link-here"
```

### 4. Commit Changes and Push to GitHub

```bash
git add .gitignore app.py download_and_setup.py
git commit -m "Setup external vector store download"
git push
```

### 5. Deploy to Hugging Face Space

The GitHub Actions workflow will automatically deploy your code to Hugging Face Spaces.
The app will automatically download the vector store when it starts up.

## Troubleshooting

- **Download fails**: Check your download URL and make sure it's a direct download link
- **App starts without vector store**: The app will still start, but queries will fail
- **Memory issues**: If your vector store is extremely large, you may need to upgrade your Hugging Face Space hardware 