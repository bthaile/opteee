#!/usr/bin/env python
"""
Simple script to test a single question with the RAG pipeline,
allowing easy comparison of different providers, models, and parameters.
"""

import os
import sys
import argparse
from time import time
from dotenv import load_dotenv

# Import from rag_pipeline.py
from rag_pipeline import (
    CustomFAISSRetriever,
    create_rag_chain,
    run_rag_query,
    format_result,
    get_available_providers,
    DEFAULT_TOP_K,
    DEFAULT_TEMPERATURE
)

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Test a single question with the RAG pipeline")
    parser.add_argument("question", type=str, help="Question to test")
    parser.add_argument("--provider", type=str, choices=["openai", "claude"], 
                       help="LLM provider to use (default: use available provider)")
    parser.add_argument("--top-k", type=int, default=DEFAULT_TOP_K, 
                       help=f"Number of documents to retrieve (default: {DEFAULT_TOP_K})")
    parser.add_argument("--temperature", type=float, default=DEFAULT_TEMPERATURE,
                       help=f"Temperature for response generation (default: {DEFAULT_TEMPERATURE})")
    parser.add_argument("--model", type=str, help="Specific model to use (default: provider's default)")
    parser.add_argument("--compare", action="store_true", help="Compare results from both providers if available")
    
    args = parser.parse_args()
    
    # Load environment variables
    load_dotenv()
    
    # Check available providers
    available_providers = get_available_providers()
    if not available_providers:
        print("❌ Error: No API keys found.")
        print("   Please set OPENAI_API_KEY or CLAUDE_API_KEY in .env file.")
        sys.exit(1)
    
    # Determine providers to test
    providers_to_test = []
    
    if args.compare:
        # If comparing, try to use both providers
        providers_to_test = available_providers
        if len(providers_to_test) < 2:
            print(f"⚠️ Warning: Only {providers_to_test[0]} is available for comparison.")
            print("   To compare both providers, add API keys for both OpenAI and Claude.")
    else:
        # Use specified provider or default
        if args.provider:
            if args.provider in available_providers:
                providers_to_test = [args.provider]
            else:
                print(f"⚠️ Warning: {args.provider} is not available. Using {available_providers[0]} instead.")
                providers_to_test = [available_providers[0]]
        else:
            providers_to_test = [available_providers[0]]
    
    # Process with each provider
    for provider in providers_to_test:
        print("\n" + "="*80)
        print(f"TESTING WITH {provider.upper()}")
        print("="*80)
        
        try:
            # Initialize retriever
            retriever = CustomFAISSRetriever(top_k=args.top_k)
            
            # Create RAG chain
            _, chain = create_rag_chain(
                retriever, 
                llm_model=args.model,
                temperature=args.temperature,
                provider=provider
            )
            
            print(f"✅ RAG pipeline initialized with {provider}")
            if args.model:
                print(f"   Using model: {args.model}")
            print(f"   Using top_k: {args.top_k}, temperature: {args.temperature}")
            
            # Process the question
            print(f"\n Processing: '{args.question}'")
            start_time = time()
            result = run_rag_query(retriever, chain, args.question)
            end_time = time()
            
            # Print timing information
            print(f"\n⏱️ Processing time: {end_time - start_time:.2f} seconds")
            print(f"📊 Retrieved {len(result['sources'])} sources")
            
            # Format and print the result
            format_result(result)
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    print("\n✅ Testing complete!")

if __name__ == "__main__":
    main() 