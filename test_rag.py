#!/usr/bin/env python
"""
Test script for the RAG pipeline to ensure it retrieves accurate content and
generates coherent responses for questions about options trading.
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
    get_available_providers,
    DEFAULT_TOP_K
)

# Test questions covering different aspects of options trading
TEST_QUESTIONS = [
    "What is gamma in options trading?",
    "Explain what a covered call strategy is.",
    "How does implied volatility affect option prices?",
    "What is the difference between American and European options?",
    "Explain the concept of theta decay in options.",
    "What is a bull call spread strategy?",
    "How do you calculate the break-even point for a call option?",
    "What happens to options during stock splits?",
    "Explain what a put-call parity is.",
    "How can I use options to hedge my stock portfolio?"
]

def load_environment():
    """Load environment variables and check for API keys"""
    load_dotenv()
    
    # Check for API keys
    available_providers = get_available_providers()
    if not available_providers:
        print("❌ Error: No API keys found.")
        print("   Please set OPENAI_API_KEY or CLAUDE_API_KEY in .env file.")
        sys.exit(1)
    
    return available_providers

def test_pipeline(provider, top_k=DEFAULT_TOP_K, specific_questions=None, model=None):
    """Test the RAG pipeline with a set of questions"""
    print(f"🔍 Testing RAG pipeline with {provider} provider and top_k={top_k}")
    if model:
        print(f"🔍 Using model: {model}")
    
    # Initialize retriever
    try:
        retriever = CustomFAISSRetriever(top_k=top_k)
        
        # Create RAG chain
        _, chain = create_rag_chain(
            retriever, 
            provider=provider,
            llm_model=model
        )
        
        print(f"✅ Successfully initialized the RAG pipeline with {provider}")
        
    except Exception as e:
        print(f"❌ Error initializing the RAG pipeline: {e}")
        sys.exit(1)
    
    # Use specified questions or default test questions
    questions = specific_questions if specific_questions else TEST_QUESTIONS
    
    # Test each question
    results = []
    
    for i, question in enumerate(questions, 1):
        print(f"\n[{i}/{len(questions)}] Testing: '{question}'")
        
        start_time = time()
        try:
            result = run_rag_query(retriever, chain, question)
            end_time = time()
            
            # Store result with timing information
            result_with_stats = {
                "question": question,
                "answer": result["answer"],
                "sources": result["sources"],
                "time_seconds": end_time - start_time
            }
            
            results.append(result_with_stats)
            
            # Print summary
            print(f"✅ Retrieved {len(result['sources'])} sources in {end_time - start_time:.2f} seconds")
            print(f"   Answer length: {len(result['answer'])} characters")
            
            # Print a short preview of the answer
            preview = result['answer'][:100] + "..." if len(result['answer']) > 100 else result['answer']
            print(f"   Preview: {preview}")
            
        except Exception as e:
            print(f"❌ Error processing question: {e}")
            results.append({
                "question": question,
                "error": str(e)
            })
    
    # Print summary
    successful = sum(1 for r in results if "error" not in r)
    print(f"\n📊 Test Summary: {successful}/{len(questions)} questions processed successfully")
    
    avg_time = sum(r.get("time_seconds", 0) for r in results if "time_seconds" in r) / successful if successful else 0
    print(f"📊 Average processing time: {avg_time:.2f} seconds per question")
    
    return results

def save_results(results, output_file="rag_test_results.txt"):
    """Save test results to a file"""
    with open(output_file, "w") as f:
        f.write("="*80 + "\n")
        f.write("RAG PIPELINE TEST RESULTS\n")
        f.write("="*80 + "\n\n")
        
        for i, result in enumerate(results, 1):
            f.write(f"Question {i}: {result['question']}\n")
            f.write("-"*80 + "\n")
            
            if "error" in result:
                f.write(f"❌ Error: {result['error']}\n")
            else:
                f.write(f"Answer ({result['time_seconds']:.2f} seconds):\n")
                f.write(result['answer'] + "\n\n")
                
                f.write("\n")
                for j, source in enumerate(result['sources'], 1):
                    f.write(f"{j}. {source['title']}\n")
                    f.write(f"   URL: {source['url']}\n")
                    f.write(f"   Score: {source['score']:.4f}\n")
            
            f.write("\n" + "="*80 + "\n\n")
    
    print(f"✅ Results saved to {output_file}")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Test the RAG pipeline")
    parser.add_argument("--provider", type=str, help="LLM provider to use (openai or claude)")
    parser.add_argument("--top-k", type=int, default=DEFAULT_TOP_K, help=f"Number of documents to retrieve (default: {DEFAULT_TOP_K})")
    parser.add_argument("--output", type=str, default="rag_test_results.txt", help="Output file to save results (default: rag_test_results.txt)")
    parser.add_argument("--questions", type=str, nargs="+", help="Specific questions to test (default: use built-in test questions)")
    parser.add_argument("--model", type=str, help="Specific model to use (default: provider's default)")
    
    args = parser.parse_args()
    
    # Load environment variables
    available_providers = load_environment()
    
    # Determine provider to use
    provider = args.provider
    if not provider or provider not in available_providers:
        provider = available_providers[0]
        if args.provider and args.provider not in available_providers:
            print(f"⚠️ Warning: Provider '{args.provider}' not available. Using {provider} instead.")
    
    # Run tests
    results = test_pipeline(
        provider=provider,
        top_k=args.top_k,
        specific_questions=args.questions,
        model=args.model
    )
    
    # Save results
    save_results(results, args.output)

if __name__ == "__main__":
    main() 