import os
import sys
import json
import pickle
import argparse
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
from typing import List, Dict, Any, Tuple
import numpy as np
import faiss
from dotenv import load_dotenv

# Set up environment variables for model caching before importing SentenceTransformer
# Use local cache paths for development, /app paths for deployment
cache_base = '/app/cache' if os.path.exists('/app') else os.path.expanduser('~/.cache')
os.environ.setdefault('TRANSFORMERS_CACHE', f'{cache_base}/huggingface')
os.environ.setdefault('SENTENCE_TRANSFORMERS_HOME', f'{cache_base}/sentence_transformers')
os.environ.setdefault('HF_HOME', f'{cache_base}/huggingface')

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

# Ollama imports
from langchain_ollama import ChatOllama

# Constants
VECTOR_STORE_DIR = VECTOR_DIR
TMP_VECTOR_STORE_DIR = "/tmp/vector_store"
TEXTS_PATH = os.path.join(VECTOR_STORE_DIR, "transcript_texts.pkl")
METADATA_PATH = os.path.join(VECTOR_STORE_DIR, "transcript_metadata.pkl")
INDEX_PATH = os.path.join(VECTOR_STORE_DIR, "transcript_index.faiss")

DEFAULT_TOP_K = 5
DEFAULT_LLM_MODEL = "gpt-5-mini"  # Current OpenAI model that supports temperature
DEFAULT_CLAUDE_MODEL = "claude-haiku-4-5"  # Latest Claude Sonnet 4 model
DEFAULT_OLLAMA_MODEL = "gemma2:2b"  # Ollama model (e.g. gemma2:2b, gemma3:270m)
# Fallback models when primary Ollama model returns 404 (not installed)
OLLAMA_FALLBACK_MODELS = ["gemma2:2b", "llama3.2", "llama3.2:3b", "mistral", "phi3", "llama2"]
DEFAULT_TEMPERATURE = 0.2

# Models that do NOT support temperature - omit temperature param to avoid API errors.
# Use substring match (e.g. "o1" matches "o1-mini", "o1-preview").
MODELS_NO_TEMPERATURE = {
    "openai": [
        "o1-preview", "o1-mini", "o1-pro", "o1",
        "o2", "o2-mini",
        "o3-mini", "o3-medium", "o3", "o3-pro",
        "o4-mini", "o4", "o4-pro",
        "gpt-4o-mini", "gpt-5-mini",
    ],
    "claude": [
        # Claude generally supports temperature; add exceptions if discovered
    ],
    "ollama": [
        "gemma3:270m", "gemma3:1b",  # Gemma 3 small models may not support temp
        # Add others as discovered
    ],
}
DEFAULT_LLM_PROVIDER = "claude"  # "openai", "claude", or "ollama"
DEFAULT_LLM_TIMEOUT_SECONDS = 60  # Timeout before falling back to next provider

# Load environment variables
load_dotenv()


def _get_timeout_seconds() -> int:
    """Timeout from env, else default."""
    try:
        return int(os.getenv("LLM_TIMEOUT_SECONDS", str(DEFAULT_LLM_TIMEOUT_SECONDS)))
    except ValueError:
        return DEFAULT_LLM_TIMEOUT_SECONDS


def _get_fallback_providers(primary_provider: str) -> List[str]:
    """Return providers to try as fallbacks after primary times out."""
    env_fallback = os.getenv("LLM_FALLBACK_PROVIDER", "").strip()
    if env_fallback:
        return [f.strip() for f in env_fallback.split(",") if f.strip() and f.strip() != primary_provider]
    available = get_available_providers()
    return [p for p in available if p != primary_provider]


def invoke_chain_with_timeout(chain, query: str, timeout: int = None) -> str:
    """
    Invoke the RAG chain with a timeout. Raises TimeoutError if the LLM
    does not respond within the given seconds.
    """
    timeout = timeout or _get_timeout_seconds()
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(chain.invoke, query)
        try:
            return future.result(timeout=timeout)
        except FuturesTimeoutError:
            raise TimeoutError(f"LLM did not respond within {timeout} seconds")


def _get_provider() -> str:
    """Provider from env, else default."""
    return os.getenv("LLM_PROVIDER", DEFAULT_LLM_PROVIDER)


def _get_model_for_provider(provider: str) -> str:
    """Model from env or provider default. LLM_MODEL only applies to primary provider."""
    primary = _get_provider()
    env_model = os.getenv("LLM_MODEL")
    if env_model and provider == primary:
        return env_model
    if provider == "openai":
        return os.getenv("OPENAI_MODEL") or DEFAULT_LLM_MODEL
    if provider == "claude":
        return os.getenv("CLAUDE_MODEL") or DEFAULT_CLAUDE_MODEL
    if provider == "ollama":
        return os.getenv("OLLAMA_MODEL") or DEFAULT_OLLAMA_MODEL
    return DEFAULT_LLM_MODEL


def _is_model_not_found_error(exc: Exception) -> bool:
    """Detect 404 / model not found errors from LLM providers."""
    msg = str(exc).lower()
    return (
        "404" in msg
        or "not_found" in msg
        or "model:" in msg and ("not found" in msg or "not_found" in msg)
    )


def model_supports_temperature(provider: str, model: str) -> bool:
    """
    Check if a model supports the temperature parameter.
    Uses MODELS_NO_TEMPERATURE mapping - returns False for known incompatible models.
    Env override: OLLAMA_NO_TEMPERATURE_MODELS, OPENAI_NO_TEMPERATURE_MODELS, CLAUDE_NO_TEMPERATURE_MODELS
    (comma-separated) extend the built-in list.
    """
    no_temp = list(MODELS_NO_TEMPERATURE.get(provider, []))
    env_key = f"{provider.upper()}_NO_TEMPERATURE_MODELS"
    env_extra = os.getenv(env_key, "").strip()
    if env_extra:
        no_temp.extend(m.strip() for m in env_extra.split(",") if m.strip())
    model_lower = model.lower()
    if any(pat in model_lower for pat in no_temp):
        return False
    return True


def test_model_temperature_support(model_name: str, provider: str) -> bool:
    """
    Test if a model supports the temperature parameter.
    Uses MODELS_NO_TEMPERATURE mapping first; only calls API for unknown models.
    """
    if not model_supports_temperature(provider, model_name):
        return False
    try:
        if provider == "openai":
            ChatOpenAI(model_name=model_name, temperature=0.1, max_tokens=1)
            return True
        elif provider == "claude":
            ChatAnthropic(model_name=model_name, temperature=0.1, max_tokens=1)
            return True
        elif provider == "ollama":
            base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            ChatOllama(model=model_name, base_url=base_url, temperature=0.1)
            return True
    except Exception as e:
        error_msg = str(e).lower()
        if any(indicator in error_msg for indicator in ["temperature", "unsupported parameter", "invalid parameter"]):
            return False
        return True  # Unknown error - assume support, let main flow handle
    return True

def validate_model_configuration(provider: str, model: str, temperature: float) -> dict:
    """
    Validate model configuration and return compatibility info.
    """
    config = {
        "provider": provider,
        "model": model,
        "temperature": temperature,
        "supports_temperature": True,
        "recommended_temperature": temperature,
        "warnings": []
    }
    
    # Check temperature support
    supports_temp = test_model_temperature_support(model, provider)
    config["supports_temperature"] = supports_temp
    
    if not supports_temp:
        config["recommended_temperature"] = None
        config["warnings"].append(f"Model {model} doesn't support temperature parameter")
    
    # Check if model is known to be deprecated
    deprecated_models = ["gpt-3.5-turbo-0301", "gpt-4-0314", "claude-v1", "claude-instant-v1"]
    if any(deprecated in model.lower() for deprecated in deprecated_models):
        config["warnings"].append(f"Model {model} may be deprecated")
    
    return config

def iso_duration_to_seconds(iso_duration: str) -> int:
    """Convert ISO 8601 duration string to seconds"""
    if not isinstance(iso_duration, str) or not iso_duration or iso_duration.startswith('P0D'):
        return 0
    
    from isodate import parse_duration
    try:
        duration = parse_duration(iso_duration)
        return int(duration.total_seconds())
    except Exception:
        return 0

def iso_duration_to_hhmmss(iso_duration: str) -> str:
    """Convert ISO 8601 duration to HH:MM:SS"""
    seconds = iso_duration_to_seconds(iso_duration)
    if seconds == 0:
        return ""
    
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes:02d}:{seconds:02d}"

def normalize_upload_date(value: Any) -> str:
    """Normalize upload/publish date to YYYYMMDD when possible."""
    if value is None:
        return ""

    if isinstance(value, (int, float)):
        value = str(int(value))

    if not isinstance(value, str):
        return ""

    value = value.strip()
    if not value or value.lower() in {"unknown", "n/a", "none", "null"}:
        return ""

    from datetime import datetime

    if len(value) == 8 and value.isdigit():
        return value

    # PDF CreationDate: D:20030901031723+02'00' or D:20030901031723
    if value.startswith("D:") and len(value) >= 10 and value[2:10].isdigit():
        return value[2:10]

    try:
        if "T" in value:
            dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
            return dt.strftime("%Y%m%d")
        dt = datetime.strptime(value.split("T")[0], "%Y-%m-%d")
        return dt.strftime("%Y%m%d")
    except ValueError:
        return ""

def get_available_providers() -> List[str]:
    """Get a list of available LLM providers based on API keys and config."""
    providers = []

    if os.getenv("OPENAI_API_KEY"):
        providers.append("openai")

    if os.getenv("CLAUDE_API_KEY") or os.getenv("ANTHROPIC_API_KEY"):
        providers.append("claude")

    # Ollama: available when OLLAMA_BASE_URL is set or LLM_PROVIDER=ollama
    if os.getenv("OLLAMA_BASE_URL") or _get_provider() == "ollama":
        providers.append("ollama")

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
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2", top_k: int = DEFAULT_TOP_K, sort_by: str = "relevance"):
        """Initialize the retriever"""
        self.model_name = model_name
        self.top_k = top_k
        self.sort_by = sort_by  # Can be 'relevance', 'date', or 'combined'
        self.fetch_multiplier = 2
        self.model = None
        self.index = None
        self.texts = []
        self.metadata = []
        
        # Load the main video metadata file for enrichment
        self.video_metadata_map = {}
        try:
            metadata_path = 'outlier_trading_videos_metadata.json'
            if os.path.exists(metadata_path):
                with open(metadata_path, 'r') as f:
                    videos_data = json.load(f)
                self.video_metadata_map = {video['video_id']: video for video in videos_data}
                print(" Loaded video metadata for data enrichment.")
        except Exception as e:
            print(f"⚠️ Warning: Could not load main video metadata file: {e}")

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
        
        # Load the model with multiple fallback strategies
        self.model = None
        loading_strategies = [
            # Strategy 1: Default loading
            {"name": "default", "func": lambda: SentenceTransformer(self.model_name)},
            
            # Strategy 2: With explicit cache folder
            {"name": "explicit_cache", "func": lambda: SentenceTransformer(
                self.model_name, 
                cache_folder='/app/cache/sentence_transformers'
            )},
            
            # Strategy 3: Force download with cache
            {"name": "force_download", "func": lambda: SentenceTransformer(
                self.model_name,
                cache_folder='/app/cache/sentence_transformers',
                use_auth_token=False
            )},
            
            # Strategy 4: Direct from HuggingFace Hub (no cache)
            {"name": "no_cache", "func": lambda: SentenceTransformer(
                self.model_name,
                cache_folder=None
            )}
        ]
        
        print(f"Loading embedding model: {self.model_name}")
        
        for strategy in loading_strategies:
            try:
                print(f"💡 Attempting {strategy['name']} loading strategy...")
                
                # Set environment variables for this attempt
                if strategy['name'] in ['explicit_cache', 'force_download']:
                    os.environ['TRANSFORMERS_CACHE'] = '/app/cache/huggingface'
                    os.environ['SENTENCE_TRANSFORMERS_HOME'] = '/app/cache/sentence_transformers'
                    os.environ['HF_HOME'] = '/app/cache/huggingface'
                
                self.model = strategy['func']()
                print(f" Model loaded successfully using {strategy['name']} strategy")
                break
                
            except Exception as e:
                print(f"❌ {strategy['name']} strategy failed: {str(e)}")
                continue
        
        if self.model is None:
            print("🔧 All model loading strategies failed. Application will exit.")
            print("This might be due to network restrictions in the deployment environment.")
            sys.exit(1)
        
        # Load the index
        try:
            print("Loading vector store files...")
            self.index = faiss.read_index(get_vector_store_path("transcript_index.faiss"))
            
            with open(get_vector_store_path("transcript_texts.pkl"), 'rb') as f:
                self.texts = pickle.load(f)
            
            with open(get_vector_store_path("transcript_metadata.pkl"), 'rb') as f:
                self.metadata = pickle.load(f)
            
            print(f" Loaded {len(self.texts)} vectors")
            
        except Exception as e:
            print(f"❌ Error loading vector store: {str(e)}")
            sys.exit(1)
    
    def expand_query(self, query: str) -> str:
        """
        Expand query with common trading acronyms and related terms.
        This helps with semantic search by providing more context.
        """
        # Common options trading acronyms and their expansions
        acronym_expansions = {
            'PEAD': 'PEAD post-earnings announcement drift earnings surprise',
            'IV': 'implied volatility IV options pricing',
            'DTE': 'DTE days to expiration options time decay',
            'ITM': 'in the money ITM strike price',
            'OTM': 'out of the money OTM strike price',
            'ATM': 'at the money ATM strike price',
            'PMCC': 'PMCC poor man covered call diagonal spread',
            'CSP': 'CSP cash secured put selling puts',
            'CC': 'covered call CC writing calls',
            'LEAPS': 'LEAPS long term equity anticipation securities',
            'VIX': 'VIX volatility index fear gauge',
            'VEGA': 'vega volatility sensitivity options greeks',
            'THETA': 'theta time decay options greeks',
            'DELTA': 'delta directional risk options greeks',
            'GAMMA': 'gamma delta sensitivity options greeks',
            'RHO': 'rho interest rate sensitivity options greeks',
        }
        
        # Check if query is a known acronym (case-insensitive, whole word)
        query_upper = query.upper().strip()
        for acronym, expansion in acronym_expansions.items():
            if query_upper == acronym or query_upper == acronym.lower():
                print(f"🔍 Expanding query '{query}' → '{expansion}'")
                return expansion
        
        # If query contains an acronym, append the expansion
        words = query.upper().split()
        expansions_to_add = []
        for word in words:
            if word in acronym_expansions:
                expansions_to_add.append(acronym_expansions[word])
        
        if expansions_to_add:
            expanded = query + ' ' + ' '.join(expansions_to_add)
            print(f"🔍 Expanding query '{query}' → '{expanded}'")
            return expanded
        
        return query
    
    def get_relevant_documents(self, query: str) -> List[Document]:
        """Get relevant documents for a query"""
        if self.model is None or self.index is None:
            raise ValueError("Retriever not properly initialized")
        
        # Expand query if it contains known acronyms
        expanded_query = self.expand_query(query)
        
        # Fetch 2x the requested number of results
        fetch_k = self.top_k * self.fetch_multiplier
        
        # Encode the expanded query
        query_embedding = self.model.encode([expanded_query])[0]
        query_embedding = np.array([query_embedding]).astype('float32')
        
        # Search the index for more results than needed
        distances, indices = self.index.search(query_embedding, fetch_k)
        
        # Create documents with scores and parsed dates
        documents = []
        for i, idx in enumerate(indices[0]):
            if idx == -1:
                continue
                
            text = self.texts[idx]
            meta = self.metadata[idx].copy() # Use a copy to avoid modifying the original
            score = float(distances[0][i])
            meta['score'] = score
            
            # --- Data Enrichment Step ---
            # If duration or upload_date is missing, enrich from the main metadata file
            video_id = meta.get('video_id')
            if video_id and video_id in self.video_metadata_map:
                main_video_meta = self.video_metadata_map[video_id]
                if 'duration' not in meta or not meta['duration']:
                    meta['duration'] = main_video_meta.get('duration')
                if 'upload_date' not in meta or not meta['upload_date']:
                    meta['upload_date'] = (
                        main_video_meta.get('upload_date')
                        or main_video_meta.get('published_at')
                        or main_video_meta.get('publishedAt')
                    )
                if 'published_at' not in meta or not meta['published_at']:
                    meta['published_at'] = (
                        main_video_meta.get('published_at')
                        or main_video_meta.get('publishedAt')
                    )

            # Normalize and align dates so downstream formatting is consistent
            normalized_upload_date = normalize_upload_date(
                meta.get('upload_date')
                or meta.get('published_at')
                or meta.get('publishedAt')
            )
            meta['upload_date'] = normalized_upload_date

            # Parse upload date
            try:
                from datetime import datetime
                # Try to parse published_at first, then fallback to upload_date
                date_str = meta.get('published_at') or meta.get('upload_date') or '19700101'
                # Handle both ISO format and YYYYMMDD format
                if 'T' in date_str:  # ISO format
                    upload_date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                else:  # YYYYMMDD format
                    upload_date = datetime.strptime(date_str, '%Y%m%d')
                meta['upload_date_obj'] = upload_date
            except:
                from datetime import datetime
                meta['upload_date_obj'] = datetime(1970, 1, 1)
            
            doc = Document(page_content=text, metadata=meta)
            documents.append(doc)
        
        # Sort based on user preference
        if self.sort_by == 'date':
            # Newest first
            documents.sort(key=lambda x: (-x.metadata['upload_date_obj'].timestamp()))
        elif self.sort_by == 'combined':
            # Balance relevance and date
            documents.sort(key=lambda x: (x.metadata['score'], -x.metadata['upload_date_obj'].timestamp()))
        else:  # 'relevance' (default)
            # Sort by relevance score only
            documents.sort(key=lambda x: x.metadata['score'])
        
        return documents[:self.top_k]

def create_openai_model_with_fallback(model: str, temperature: float) -> ChatOpenAI:
    """Create OpenAI model. Uses MODELS_NO_TEMPERATURE mapping to avoid temp errors."""
    if model_supports_temperature("openai", model):
        print(f" Using OpenAI model: {model} (temperature: {temperature})")
        return ChatOpenAI(model_name=model, temperature=temperature)
    print(f" Using OpenAI model: {model} (temperature not supported)")
    return ChatOpenAI(model_name=model)

def create_ollama_model_with_fallback(model: str, temperature: float):
    """Create Ollama model with base_url from env. Uses MODELS_NO_TEMPERATURE mapping."""
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")
    if model_supports_temperature("ollama", model):
        print(f" Using Ollama model: {model} at {base_url} (temperature: {temperature})")
        return ChatOllama(model=model, base_url=base_url, temperature=temperature)
    print(f" Using Ollama model: {model} at {base_url} (temperature not supported)")
    return ChatOllama(model=model, base_url=base_url)


def create_claude_model_with_fallback(model: str, temperature: float) -> ChatAnthropic:
    """Create Claude model. Uses MODELS_NO_TEMPERATURE mapping."""
    if model_supports_temperature("claude", model):
        print(f" Using Claude model: {model} (temperature: {temperature})")
        return ChatAnthropic(model_name=model, temperature=temperature)
    print(f" Using Claude model: {model} (temperature not supported)")
    return ChatAnthropic(model_name=model)

def format_documents(docs: List[Document]) -> str:
    """Format documents for the prompt, adapting metadata to source type."""
    formatted_docs = []
    
    for i, doc in enumerate(docs):
        content = doc.page_content
        meta = doc.metadata
        source_type = meta.get('source_type', 'video')
        
        if source_type == 'pdf':
            # Format metadata for book/research paper sources
            meta_parts = [f"Title: {meta.get('title', 'Unknown')}"]
            author = meta.get('author', '')
            if author:
                meta_parts.append(f"Author: {author}")
            section = meta.get('section', '')
            if section and section != 'Document':
                meta_parts.append(f"Section: {section}")
            page_range = meta.get('page_range', '')
            page_number = meta.get('page_number', '')
            if page_range:
                meta_parts.append(f"Pages: {page_range}")
            elif page_number:
                meta_parts.append(f"Page: {page_number}")
            meta_parts.append("Type: Research Paper / Book")
            meta_str = "\n".join(meta_parts)
        else:
            # Format metadata for video transcript sources
            meta_str = "\n".join([
                f"Title: {meta.get('title', 'Unknown')}",
                f"URL: {meta.get('video_url', 'Unknown')}",
                f"Timestamp: {meta.get('timestamp', 'Unknown')}",
                f"Channel: {meta.get('channel', 'Unknown')}",
                f"Upload Date: {meta.get('upload_date', 'Unknown')}",
                "Type: Video Transcript"
            ])
        
        # Format document
        doc_str = f"[Document {i+1}]\n{content}\n\n{meta_str}"
        formatted_docs.append(doc_str)
    
    return "\n\n".join(formatted_docs)

def validate_system_configuration(verbose: bool = False) -> bool:
    """
    Validate the entire system configuration to prevent errors.
    Returns True if everything is configured correctly, False otherwise.
    """
    
    print(" Validating system configuration...")
    
    available_providers = get_available_providers()
    if not available_providers:
        print("❌ No LLM provider configured. Set OPENAI_API_KEY, CLAUDE_API_KEY, or OLLAMA_BASE_URL/LLM_PROVIDER=ollama.")
        return False
    
    print(f" Available providers: {', '.join(available_providers)}")
    
    # Test default configurations
    all_valid = True
    
    # Test OpenAI default if available
    if "openai" in available_providers:
        if verbose:
            print(f"🧪 Testing OpenAI default model: {DEFAULT_LLM_MODEL}")
        
        config = validate_model_configuration("openai", DEFAULT_LLM_MODEL, DEFAULT_TEMPERATURE)
        
        if config["warnings"]:
            print(f"⚠️ OpenAI warnings: {'; '.join(config['warnings'])}")
        
        if not config["supports_temperature"]:
            print(f"ℹ️ OpenAI model {DEFAULT_LLM_MODEL} doesn't support temperature (will use fallback)")
    
    # Test Claude default if available
    if "claude" in available_providers:
        if verbose:
            print(f"🧪 Testing Claude default model: {DEFAULT_CLAUDE_MODEL}")
        
        config = validate_model_configuration("claude", DEFAULT_CLAUDE_MODEL, DEFAULT_TEMPERATURE)
        
        if config["warnings"]:
            print(f"⚠️ Claude warnings: {'; '.join(config['warnings'])}")
        
        if not config["supports_temperature"]:
            print(f"ℹ️ Claude model {DEFAULT_CLAUDE_MODEL} doesn't support temperature (will use fallback)")

    if "ollama" in available_providers:
        ollama_model = _get_model_for_provider("ollama")
        if verbose:
            print(f"🧪 Testing Ollama default model: {ollama_model}")
        config = validate_model_configuration("ollama", ollama_model, DEFAULT_TEMPERATURE)
        if config["warnings"]:
            print(f"⚠️ Ollama warnings: {'; '.join(config['warnings'])}")
        if not config["supports_temperature"]:
            print(f"ℹ️ Ollama model {ollama_model} doesn't support temperature (will use fallback)")

    if all_valid:
        print(" System configuration validation complete - no critical issues found")
    
    return all_valid

def create_rag_chain(retriever, llm_model=None, temperature=DEFAULT_TEMPERATURE, provider=DEFAULT_LLM_PROVIDER):
    """Create a RAG chain with the specified parameters"""
    # Add debug print
    print("\n=== System Prompt ===")
    print(SYSTEM_PROMPT)
    print("===================\n")
    
    available_providers = get_available_providers()
    
    # Resolve provider and model from env when not passed
    provider = provider or _get_provider()
    if provider not in available_providers:
        if not available_providers:
            print("❌ Error: No LLM provider configured.")
            print("   Set OPENAI_API_KEY, CLAUDE_API_KEY, or OLLAMA_BASE_URL / LLM_PROVIDER=ollama in .env")
            sys.exit(1)
        print(f"⚠️ Warning: Provider '{provider}' not available. Using {available_providers[0]} instead.")
        provider = available_providers[0]

    model = llm_model or _get_model_for_provider(provider)

    # Initialize the language model
    if provider == "openai":
        # Check for API key
        if not os.getenv("OPENAI_API_KEY"):
            print("❌ Error: OPENAI_API_KEY not found in environment variables or .env file.")
            print("   Please set your OpenAI API key in the .env file.")
            sys.exit(1)
        
        # Robust temperature handling with multiple fallback layers
        llm = create_openai_model_with_fallback(model, temperature)

    elif provider == "claude":
        claude_key = os.getenv("CLAUDE_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
        if not claude_key:
            print("❌ Error: CLAUDE_API_KEY or ANTHROPIC_API_KEY not found in .env")
            sys.exit(1)
        os.environ["ANTHROPIC_API_KEY"] = claude_key
        llm = create_claude_model_with_fallback(model, temperature)

    elif provider == "ollama":
        llm = create_ollama_model_with_fallback(model, temperature)

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

def run_rag_query(retriever, chain, query: str, timeout: int = None) -> Dict[str, Any]:
    """Run a RAG query and return the result with sources. Raises TimeoutError if LLM does not respond in time."""
    # Get relevant documents (already sorted by score)
    docs = retriever.get_relevant_documents(query)

    if not docs:
        return {
            "answer": "",  # Return empty - let frontend handle no results messaging
            "sources": []
        }

    # Generate answer (with timeout)
    answer = invoke_chain_with_timeout(chain, query, timeout=timeout)
    
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
        video_url_with_timestamp = f"{video_url}&t={timestamp_seconds}" if video_id and timestamp_seconds > 0 else video_url
        
        # Convert duration to HH:MM:SS format
        duration = meta.get("duration", "")
        duration_seconds = iso_duration_to_seconds(duration)

        # Determine source type (pdf or video)
        source_type = meta.get("source_type", "video")
        
        source = {
            "title": meta.get("title", "Unknown"),
            "source_type": source_type,
            "video_id": video_id,
            "url": video_url,
            "video_url_with_timestamp": video_url_with_timestamp,
            "start_timestamp_seconds": timestamp_seconds,
            "timestamp": meta.get("start_timestamp", ""),
            "channel": meta.get("channel_name", meta.get("channel", "Unknown")),
            "upload_date": normalize_upload_date(
                meta.get("upload_date") or meta.get("published_at") or meta.get("publishedAt")
            ),
            "score": meta.get("score", 0.0),
            "content": doc.page_content,  # Include the actual transcript content
            "duration_seconds": duration_seconds,  # Pass raw seconds
        }
        
        # Add PDF-specific fields if this is a PDF source
        if source_type == "pdf":
            source["document_id"] = meta.get("document_id", "")
            source["source_file"] = meta.get("source_file", "")
            source["page_number"] = meta.get("page_number", 0)
            source["page_range"] = meta.get("page_range", "")
            source["section"] = meta.get("section", "")
            source["author"] = meta.get("author", "")
        
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
        # Format the date nicely
        try:
            from datetime import datetime
            date_str = source.get('upload_date', '')
            if 'T' in date_str:  # ISO format
                date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            else:  # YYYYMMDD format
                date = datetime.strptime(date_str, '%Y%m%d')
            # Format as "Monday, Mar 23, 2024"
            formatted_date = date.strftime("%A, %b %d, %Y")
        except:
            formatted_date = source.get('upload_date', 'Unknown')
            
        # Create video link with timestamp
        video_link = source.get('url', '')
        if video_link:
            video_link = f" [{video_link}]"
            
        print(f"• \"{source['title']}\" (Score: {source['score']:.1f}) - {formatted_date}{video_link}")
    print()

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="RAG pipeline for options trading education")
    parser.add_argument("query", type=str, nargs="?", help="Query to answer")
    parser.add_argument("--top-k", type=int, default=DEFAULT_TOP_K, help=f"Number of documents to retrieve (default: {DEFAULT_TOP_K})")
    parser.add_argument("--model", type=str, default=None, help=f"LLM model to use (default: {DEFAULT_LLM_MODEL} for OpenAI, {DEFAULT_CLAUDE_MODEL} for Claude)")
    parser.add_argument("--temperature", type=float, default=DEFAULT_TEMPERATURE, help=f"Temperature for the LLM (default: {DEFAULT_TEMPERATURE})")
    parser.add_argument("--provider", type=str, default=None, choices=["openai", "claude", "ollama"], help="LLM provider (default from LLM_PROVIDER env)")
    parser.add_argument("--validate", action="store_true", help="Validate system configuration and exit")
    parser.add_argument("--test-temp", type=str, help="Test if a specific model supports temperature")
    
    args = parser.parse_args()
    
    # Handle special commands
    if args.validate:
        validate_system_configuration(verbose=True)
        return
        
    if args.test_temp:
        provider = args.provider
        model = args.test_temp
        supports_temp = test_model_temperature_support(model, provider)
        print(f"Model {model} ({' supports' if supports_temp else '❌ does not support'}) temperature parameter")
        return
        
    if not args.query:
        print("❌ Error: Query is required unless using --validate or --test-temp")
        parser.print_help()
        return
    
    # Get available providers
    available_providers = get_available_providers()
    if not available_providers:
        print("❌ Error: No LLM provider configured. Set OPENAI_API_KEY, CLAUDE_API_KEY, or OLLAMA_BASE_URL/LLM_PROVIDER=ollama.")
        sys.exit(1)
    
    # Resolve provider from env if not passed
    provider = args.provider or _get_provider()
    if provider not in available_providers:
        print(f"⚠️ Warning: Provider '{provider}' not available. Using {available_providers[0]} instead.")
        provider = available_providers[0]
    
    # Initialize retriever
    retriever = CustomFAISSRetriever(top_k=args.top_k)
    
    # Create RAG chain
    retriever, chain = create_rag_chain(
        retriever,
        llm_model=args.model,
        temperature=args.temperature,
        provider=provider
    )
    
    # Run the query
    result = run_rag_query(retriever, chain, args.query)
    
    # Format and print the result
    format_result(result)

if __name__ == "__main__":
    main() 