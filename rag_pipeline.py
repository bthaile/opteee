import os
import sys
import json
import pickle
import argparse
from typing import List, Dict, Any, Tuple
import numpy as np
import faiss
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from config import VECTOR_DIR, SYSTEM_PROMPT

# LangChain imports
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda
from langchain_core.documents import Document

# OpenAI imports
from langchain_openai import ChatOpenAI

# Claude imports
from langchain_anthropic import ChatAnthropic

# Constants
VECTOR_STORE_DIR = VECTOR_DIR
TMP_VECTOR_STORE_DIR = "/tmp/vector_store"
TEXTS_PATH = os.path.join(VECTOR_STORE_DIR, "transcript_texts.pkl")
METADATA_PATH = os.path.join(VECTOR_STORE_DIR, "transcript_metadata.pkl")
INDEX_PATH = os.path.join(VECTOR_STORE_DIR, "transcript_index.faiss")

DEFAULT_TOP_K = 5
DEFAULT_LLM_MODEL = "gpt-4o-mini"
DEFAULT_CLAUDE_MODEL = "claude-3-7-sonnet-20250219"
DEFAULT_TEMPERATURE = 0.2
DEFAULT_LLM_PROVIDER = "openai"  # "openai" or "claude"

# Load environment variables
load_dotenv()

def get_available_providers() -> List[str]:
    """Get a list of available LLM providers based on API keys"""
    providers = []
    
    if os.getenv("OPENAI_API_KEY"):
        providers.append("openai")
        
    if os.getenv("CLAUDE_API_KEY") or os.getenv("ANTHROPIC_API_KEY"):
        providers.append("claude")
        
    return providers

def get_vector_store_path(filename):
    """Try both permanent and temporary vector store locations"""
    app_path = os.path.join(VECTOR_STORE_DIR, filename)
    tmp_path = os.path.join(TMP_VECTOR_STORE_DIR, filename)
    
    if os.path.exists(app_path):
        return app_path
    elif os.path.exists(tmp_path):
        return tmp_path
    else:
        raise FileNotFoundError(f"Required file '{filename}' not found in either {VECTOR_STORE_DIR} or {TMP_VECTOR_STORE_DIR}")

class CustomFAISSRetriever:
    """Custom retriever using FAISS index"""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2", top_k: int = DEFAULT_TOP_K):
        """Initialize the retriever"""
        self.model_name = model_name
        self.top_k = top_k
        self.fetch_multiplier = 2  # Will fetch 2x the requested results
        self.model = None
        self.index = None
        self.texts = []
        self.metadata = []
        
        # Check if vector store exists
        if not os.path.exists(VECTOR_STORE_DIR):
            print(f"❌ Error: Vector store directory '{VECTOR_STORE_DIR}' not found.")
            sys.exit(1)
        
        # Check if all required files exist
        for path in [TEXTS_PATH, METADATA_PATH, INDEX_PATH]:
            if not os.path.exists(path):
                print(f"❌ Error: Required file '{os.path.basename(path)}' not found.")
                print("   Please run create_vector_store.py first.")
                sys.exit(1)
        
        # Load the model
        try:
            print(f"Loading embedding model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
        except Exception as e:
            print(f"❌ Error loading model: {str(e)}")
            sys.exit(1)
        
        # Load the index
        try:
            print("Loading vector store files...")
            self.index = faiss.read_index(get_vector_store_path(INDEX_PATH))
            
            with open(get_vector_store_path(TEXTS_PATH), 'rb') as f:
                self.texts = pickle.load(f)
            
            with open(get_vector_store_path(METADATA_PATH), 'rb') as f:
                self.metadata = pickle.load(f)
            
            print(f"✅ Loaded {len(self.texts)} vectors")
            
        except Exception as e:
            print(f"❌ Error loading vector store: {str(e)}")
            sys.exit(1)
    
    def get_relevant_documents(self, query: str) -> List[Document]:
        """Get relevant documents for a query"""
        if self.model is None or self.index is None:
            raise ValueError("Retriever not properly initialized")
        
        # Fetch 2x the requested number of results
        fetch_k = self.top_k * self.fetch_multiplier
        
        # Encode the query
        query_embedding = self.model.encode([query])[0]
        query_embedding = np.array([query_embedding]).astype('float32')
        
        # Search the index for more results than needed
        distances, indices = self.index.search(query_embedding, fetch_k)
        
        # Create documents with scores
        documents = []
        for i, idx in enumerate(indices[0]):
            if idx == -1:  # FAISS may return -1 if there are not enough results
                continue
                
            text = self.texts[idx]
            meta = self.metadata[idx]
            score = float(distances[0][i])
            
            # Add score to metadata
            meta['score'] = score
            
            doc = Document(page_content=text, metadata=meta)
            documents.append(doc)
        
        # Sort by score (lower distance is better) and take top_k
        documents.sort(key=lambda x: x.metadata['score'])
        return documents[:self.top_k]

def format_documents(docs: List[Document]) -> str:
    """Format documents for the prompt"""
    formatted_docs = []
    
    for i, doc in enumerate(docs):
        content = doc.page_content
        meta = doc.metadata
        
        # Format metadata including upload date
        meta_str = "\n".join([
            f"Title: {meta.get('title', 'Unknown')}",
            f"URL: {meta.get('video_url', 'Unknown')}",
            f"Timestamp: {meta.get('timestamp', 'Unknown')}",
            f"Channel: {meta.get('channel', 'Unknown')}",
            f"Upload Date: {meta.get('upload_date', 'Unknown')}"
        ])
        
        # Format document
        doc_str = f"[Document {i+1}]\n{content}\n\n{meta_str}"
        formatted_docs.append(doc_str)
    
    return "\n\n".join(formatted_docs)

def create_rag_chain(retriever, llm_model=None, temperature=DEFAULT_TEMPERATURE, provider=DEFAULT_LLM_PROVIDER):
    """Create a RAG chain with the specified parameters"""
    # Add debug print
    print("\n=== System Prompt ===")
    print(SYSTEM_PROMPT)
    print("===================\n")
    
    available_providers = get_available_providers()
    
    # Validate provider
    if provider not in available_providers:
        if not available_providers:
            print("❌ Error: No API keys found.")
            print("   Please set OPENAI_API_KEY or CLAUDE_API_KEY in .env file.")
            sys.exit(1)
        else:
            print(f"⚠️ Warning: Provider '{provider}' not available. Using {available_providers[0]} instead.")
            provider = available_providers[0]
    
    # Initialize the language model
    if provider == "openai":
        # Check for API key
        if not os.getenv("OPENAI_API_KEY"):
            print("❌ Error: OPENAI_API_KEY not found in environment variables or .env file.")
            print("   Please set your OpenAI API key in the .env file.")
            sys.exit(1)
        
        # Initialize OpenAI model
        model = llm_model or DEFAULT_LLM_MODEL
        llm = ChatOpenAI(model_name=model, temperature=temperature)
        print(f"✅ Using OpenAI model: {model}")
        
    elif provider == "claude":
        # Check for API key
        claude_key = os.getenv("CLAUDE_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
        if not claude_key:
            print("❌ Error: CLAUDE_API_KEY or ANTHROPIC_API_KEY not found in environment variables or .env file.")
            print("   Please set your Claude API key in the .env file.")
            sys.exit(1)
        
        # Initialize Claude model
        model = llm_model or DEFAULT_CLAUDE_MODEL
        os.environ["ANTHROPIC_API_KEY"] = claude_key  # Ensure the key is set for Anthropic
        llm = ChatAnthropic(model_name=model, temperature=temperature)
        print(f"✅ Using Claude model: {model}")
    
    else:
        print(f"❌ Error: Unsupported provider '{provider}'")
        sys.exit(1)
    
    # Create the prompt template with system message
    template = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("user", """Context for answering the question:
{context}

User Question: {question}""")
    ])
    
    # Create the RAG chain
    chain = (
        {"context": lambda query: format_documents(retriever.get_relevant_documents(query)), 
         "question": RunnablePassthrough()}
        | template
        | llm
        | StrOutputParser()
    )
    
    return retriever, chain

def run_rag_query(retriever, chain, query: str) -> Dict[str, Any]:
    """Run a RAG query and return the result with sources"""
    # Get relevant documents (already sorted by score)
    docs = retriever.get_relevant_documents(query)
    
    if not docs:
        return {
            "answer": "I couldn't find any relevant information to answer your question.",
            "sources": []
        }
    
    # Generate answer
    answer = chain.invoke(query)
    
    # Extract sources (maintaining order)
    sources = []
    for doc in docs:
        meta = doc.metadata
        
        # Get video ID and ensure it's valid
        video_id = meta.get("video_id", "")
        
        # Fix any URL issues by reconstructing with the proper video_id
        timestamp_seconds = meta.get("start_timestamp_seconds", 0)
        if isinstance(timestamp_seconds, float) or isinstance(timestamp_seconds, int):
            timestamp_seconds = int(timestamp_seconds)
        else:
            timestamp_seconds = 0
            
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        video_url_with_timestamp = f"{video_url}&t={timestamp_seconds}" if video_id else ""
        
        source = {
            "title": meta.get("title", "Unknown"),
            "video_id": video_id,
            "url": video_url_with_timestamp or meta.get("video_url", ""),
            "timestamp": meta.get("start_timestamp", ""),
            "channel": meta.get("channel_name", meta.get("channel", "Unknown")),
            "upload_date": meta.get("upload_date", "Unknown"),
            "score": meta.get("score", 0.0)
        }
        sources.append(source)
    
    return {
        "answer": answer,
        "sources": sources
    }

def format_result(result: Dict[str, Any]) -> None:
    """Print formatted result"""
    print("\n" + "="*80)
    print("ANSWER:")
    print("-"*80)
    print(result["answer"])
    print("\n" + "="*80)
    print("SOURCES:")
    print("-"*80)
    
    for i, source in enumerate(result["sources"]):
        print(f"{i+1}. {source['title']}")
        print(f"   Timestamp: {source['timestamp']}")
        print(f"   URL: {source['url']}")
        print(f"   Score: {source['score']:.4f}")
        print()

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="RAG pipeline for options trading education")
    parser.add_argument("query", type=str, help="Query to answer")
    parser.add_argument("--top-k", type=int, default=DEFAULT_TOP_K, help=f"Number of documents to retrieve (default: {DEFAULT_TOP_K})")
    parser.add_argument("--model", type=str, default=None, help=f"LLM model to use (default: {DEFAULT_LLM_MODEL} for OpenAI, {DEFAULT_CLAUDE_MODEL} for Claude)")
    parser.add_argument("--temperature", type=float, default=DEFAULT_TEMPERATURE, help=f"Temperature for the LLM (default: {DEFAULT_TEMPERATURE})")
    parser.add_argument("--provider", type=str, default=DEFAULT_LLM_PROVIDER, choices=["openai", "claude"], help=f"LLM provider to use (default: {DEFAULT_LLM_PROVIDER})")
    
    args = parser.parse_args()
    
    # Get available providers
    available_providers = get_available_providers()
    if not available_providers:
        print("❌ Error: No API keys found. Please set OPENAI_API_KEY or CLAUDE_API_KEY in .env file.")
        sys.exit(1)
    
    # Validate provider
    if args.provider not in available_providers:
        print(f"⚠️ Warning: Provider '{args.provider}' not available. Using {available_providers[0]} instead.")
        args.provider = available_providers[0]
    
    # Initialize retriever
    retriever = CustomFAISSRetriever(top_k=args.top_k)
    
    # Create RAG chain
    retriever, chain = create_rag_chain(
        retriever, 
        llm_model=args.model, 
        temperature=args.temperature,
        provider=args.provider
    )
    
    # Run the query
    result = run_rag_query(retriever, chain, args.query)
    
    # Format and print the result
    format_result(result)

if __name__ == "__main__":
    main() 