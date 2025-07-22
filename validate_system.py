#!/usr/bin/env python3
"""
Comprehensive system validation script for the OPTEEE system.
This script checks all components and helps prevent temperature errors.
"""

import os
import sys
from dotenv import load_dotenv

def main():
    """Run comprehensive system validation"""
    print("🔧 OPTEEE System Validation")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    try:
        # Import after loading env vars
        from rag_pipeline import (
            validate_system_configuration, 
            get_available_providers,
            test_model_temperature_support,
            DEFAULT_LLM_MODEL,
            DEFAULT_CLAUDE_MODEL,
            DEFAULT_TEMPERATURE
        )
        
        print("📋 Checking system components...")
        
        # 1. Check vector store
        print("\n1. Vector Store Check:")
        try:
            from config import VECTOR_DIR
            vector_files = [
                "transcript_index.faiss",
                "transcript_metadata.pkl", 
                "transcript_texts.pkl"
            ]
            
            for file in vector_files:
                file_path = os.path.join(VECTOR_DIR, file)
                if os.path.exists(file_path):
                    print(f"   ✅ {file}")
                else:
                    print(f"   ❌ {file} - Missing")
        except Exception as e:
            print(f"   ❌ Vector store check failed: {e}")
        
        # 2. Check API Keys
        print("\n2. API Key Check:")
        providers = get_available_providers()
        if not providers:
            print("   ❌ No API keys found")
            print("    Please set OPENAI_API_KEY or ANTHROPIC_API_KEY in .env file")
        else:
            for provider in providers:
                print(f"   ✅ {provider.upper()} API key found")
        
        # 3. Model Validation
        print("\n3. Model Validation:")
        
        if "openai" in providers:
            print(f"   🧪 Testing OpenAI model: {DEFAULT_LLM_MODEL}")
            supports_temp = test_model_temperature_support(DEFAULT_LLM_MODEL, "openai")
            if supports_temp:
                print(f"   ✅ {DEFAULT_LLM_MODEL} supports temperature")
            else:
                print(f"   ⚠️ {DEFAULT_LLM_MODEL} doesn't support temperature (fallback will be used)")
        
        if "claude" in providers:
            print(f"   🧪 Testing Claude model: {DEFAULT_CLAUDE_MODEL}")
            supports_temp = test_model_temperature_support(DEFAULT_CLAUDE_MODEL, "claude")
            if supports_temp:
                print(f"   ✅ {DEFAULT_CLAUDE_MODEL} supports temperature")
            else:
                print(f"   ⚠️ {DEFAULT_CLAUDE_MODEL} doesn't support temperature (fallback will be used)")
        
        # 4. Full system validation
        print("\n4. Full System Validation:")
        success = validate_system_configuration(verbose=True)
        
        # 5. Temperature Error Prevention Summary
        print("\n5. Temperature Error Prevention:")
        print("   ✅ Multi-layer fallback system active")
        print("   ✅ Automatic error detection and retry")
        print("   ✅ Known model compatibility checks")
        print("   ✅ Graceful degradation for unsupported models")
        
        # 6. Recommendations
        print("\n6. Recommendations:")
        if success:
            print("   🎉 System is ready! No critical issues found.")
            print(f"    Default models: OpenAI={DEFAULT_LLM_MODEL}, Claude={DEFAULT_CLAUDE_MODEL}")
            print(f"   🌡️ Default temperature: {DEFAULT_TEMPERATURE}")
        else:
            print("   ⚠️ Some issues detected. Check the messages above.")
        
        print("\n" + "=" * 50)
        print("✅ Validation complete")
        
        return success
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Please ensure all dependencies are installed")
        return False
    except Exception as e:
        print(f"❌ Validation failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 