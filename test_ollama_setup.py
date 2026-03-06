#!/usr/bin/env python3
"""
Diagnostic script to test Ollama connectivity and model availability.
Run from your environment (or inside Docker if that's how you deploy).
"""
import os
import sys
import json

# Load .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")
LLM_MODEL = os.getenv("LLM_MODEL", "gemma3:270m")


def fetch(url: str, timeout: int = 10) -> tuple[str | None, Exception | None]:
    """Fetch URL, return (response_text, None) or (None, error)."""
    try:
        import urllib.request
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode(), None
    except Exception as e:
        return None, e


def main():
    print("=" * 60)
    print("Ollama Setup Diagnostic")
    print("=" * 60)
    print(f"Configured OLLAMA_BASE_URL: {OLLAMA_BASE_URL}")
    print(f"Configured LLM_MODEL:       {LLM_MODEL}")
    print()

    # Test configured URL first
    print("1. Testing configured server...")
    version_txt, err = fetch(f"{OLLAMA_BASE_URL}/api/version")
    if err:
        print(f"   FAIL - Cannot reach {OLLAMA_BASE_URL}")
        print(f"   Error: {err}")
    else:
        print(f"   OK - Server reachable ({version_txt[:80]}...)")
    print()

    # Also try localhost for comparison
    if "localhost" not in OLLAMA_BASE_URL and "127.0.0.1" not in OLLAMA_BASE_URL:
        print("2. Testing localhost (for comparison)...")
        version_txt, err = fetch("http://localhost:11434/api/version")
        if err:
            print(f"   localhost:11434 - Not reachable ({err})")
        else:
            print(f"   localhost:11434 - Reachable")
        print()

    # List models from whichever server works
    print("3. Listing available models...")
    tags_txt, err = fetch(f"{OLLAMA_BASE_URL}/api/tags")
    if err:
        tags_txt, err = fetch("http://localhost:11434/api/tags")
        source = "localhost (fallback)"
    else:
        source = OLLAMA_BASE_URL

    if err:
        print(f"   FAIL - Could not list models from either server")
        return 1

    data = json.loads(tags_txt)
    models = data.get("models", [])
    names = [m.get("name", m.get("model", "?")) for m in models]
    print(f"   From {source}:")
    for n in names:
        marker = " <-- CONFIGURED" if LLM_MODEL in n or n == LLM_MODEL else ""
        print(f"     - {n}{marker}")
    print()

    # Check if configured model exists
    print("4. Checking configured model...")
    has_model = any(LLM_MODEL in m.get("name", "") or LLM_MODEL in m.get("model", "") for m in models)
    if has_model:
        print(f"   OK - {LLM_MODEL} is available")
    else:
        print(f"   FAIL - {LLM_MODEL} is NOT installed")
        print()
        print("   Fixes:")
        print("   - On the Ollama server, run: ollama pull gemma3:270m")
        if names:
            print(f"   - Or in .env use an installed model: LLM_MODEL={names[0]}")
        return 1
    print()

    # If configured URL failed but localhost worked, warn
    if "m1pro" in OLLAMA_BASE_URL or ".home" in OLLAMA_BASE_URL:
        version_txt, err = fetch(f"{OLLAMA_BASE_URL}/api/version")
        if err:
            print("NOTE: Configured remote host unreachable. If running in Docker,")
            print("      try: OLLAMA_BASE_URL=http://host.docker.internal:11434")
            print("      On m1pro.home, ensure: OLLAMA_HOST=0.0.0.0")
            print()

    print("All checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
