import os
import textwrap
from dotenv import load_dotenv
from rag_pipeline import (
    CustomFAISSRetriever, 
    create_rag_chain, 
    run_rag_query, 
    format_result,
    get_available_providers,
    DEFAULT_TOP_K,
    DEFAULT_LLM_MODEL,
    DEFAULT_CLAUDE_MODEL,
    DEFAULT_TEMPERATURE,
    DEFAULT_LLM_PROVIDER
)

# Load environment variables
load_dotenv()

# Get available providers
available_providers = get_available_providers()
if not available_providers:
    print("❌ Error: No API keys found. Please set OPENAI_API_KEY or CLAUDE_API_KEY in .env file.")
    exit(1)

def setup_rag_pipeline(top_k=DEFAULT_TOP_K, model=None, temperature=DEFAULT_TEMPERATURE, provider=DEFAULT_LLM_PROVIDER):
    """Set up the RAG pipeline with the specified parameters"""
    # Initialize retriever
    retriever = CustomFAISSRetriever(top_k=top_k)
    
    # Create RAG chain
    retriever, chain = create_rag_chain(
        retriever, 
        llm_model=model, 
        temperature=temperature,
        provider=provider
    )
    
    return retriever, chain

def print_banner():
    """Print the application banner"""
    banner = """
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃                   OPTEEE RAG SYSTEM                   ┃
    ┃           Options Trading Education Assistant         ┃
    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    
    Ask me anything about options trading based on Outlier Trading videos!
    Type 'exit', 'quit', or 'q' to exit the application.
    Type 'config' to adjust settings.
    """
    print(banner)

def format_wrapped_text(text, width=80):
    """Format text with proper wrapping"""
    # Split the text into paragraphs
    paragraphs = text.split('\n')
    
    # Wrap each paragraph
    wrapped_paragraphs = []
    for paragraph in paragraphs:
        if paragraph.strip():
            wrapped = textwrap.fill(paragraph, width=width)
            wrapped_paragraphs.append(wrapped)
        else:
            wrapped_paragraphs.append("")
    
    # Join paragraphs back together
    return '\n'.join(wrapped_paragraphs)

def display_answer(result, show_sources=True, width=80):
    """Display the answer with proper formatting"""
    answer = result['answer']
    sources = result['sources']
    
    print("\n" + "="*width)
    print("ANSWER:")
    print("-"*width)
    print(format_wrapped_text(answer, width))
    print()
    
    if show_sources and sources:
        print("-"*width)
        print(":")
        print("-"*width)
        
        for i, source in enumerate(sources):
            print(f"{i+1}. {source['title']}")
            print(f"   Timestamp: {source['timestamp']}")
            print(f"   URL: {source['url']}")
            print()

def config_menu(current_settings):
    """Display configuration menu and update settings"""
    print("\n" + "="*80)
    print("CONFIGURATION SETTINGS")
    print("="*80)
    print(f"1. Sources to retrieve (current: {current_settings['top_k']})")
    print(f"2. LLM provider (current: {current_settings['provider']})")
    print(f"3. LLM model (current: {current_settings['model'] or 'default'})")
    print(f"4. Temperature (current: {current_settings['temperature']})")
    print(f"5. Show sources (current: {current_settings['show_sources']})")
    print("6. Return to main menu")
    print("-"*80)
    
    choice = input("Enter your choice (1-6): ").strip()
    
    if choice == '1':
        try:
            top_k = int(input(f"Enter number of sources to retrieve (1-20, current: {current_settings['top_k']}): "))
            if 1 <= top_k <= 20:
                current_settings['top_k'] = top_k
                print(f" Updated to retrieve {top_k} sources")
            else:
                print("❌ Invalid input. Please enter a number between 1 and 20.")
        except ValueError:
            print("❌ Invalid input. Please enter a number.")
    
    elif choice == '2':
        if len(available_providers) == 1:
            print(f"⚠️ Only one provider available: {available_providers[0]}")
            print("   To use other providers, add the appropriate API keys to your .env file.")
            current_settings['provider'] = available_providers[0]
        else:
            print("\nAvailable providers:")
            for i, provider in enumerate(available_providers, 1):
                print(f"{i}. {provider}")
            
            provider_choice = input(f"Choose a provider (1-{len(available_providers)}): ").strip()
            
            try:
                idx = int(provider_choice) - 1
                if 0 <= idx < len(available_providers):
                    current_settings['provider'] = available_providers[idx]
                    # Reset model to None (default) when changing provider
                    current_settings['model'] = None
                    print(f" Updated provider to {current_settings['provider']}")
                else:
                    print("❌ Invalid choice. Settings not changed.")
            except ValueError:
                print("❌ Invalid input. Settings not changed.")

    elif choice == '3':
        if current_settings['provider'] == 'openai':
            print("\nAvailable OpenAI models:")
            print("1. gpt-4o (current flagship model, balanced)")
            print("2. gpt-4 (previous generation, stable)")
            print("3. gpt-4-turbo (optimized for speed)")
            print("4. gpt-3.5-turbo (legacy, faster/cheaper)")
            print("5. Use default")
            model_choice = input("Choose a model (1-5): ").strip()
            
            openai_model_map = {
                '1': 'gpt-4o',
                '2': 'gpt-4',
                '3': 'gpt-4-turbo',
                '4': 'gpt-3.5-turbo',
                '5': None
            }
            
            if model_choice in openai_model_map:
                current_settings['model'] = openai_model_map[model_choice]
                model_name = current_settings['model'] or DEFAULT_LLM_MODEL
                print(f" Updated model to {model_name}")
            else:
                print("❌ Invalid choice. Settings not changed.")
                
        elif current_settings['provider'] == 'claude':
            print("\nAvailable Claude models:")
            print("1. claude-sonnet-4 (newest flagship model, best performance)")
            print("2. claude-3-5-sonnet (previous flagship model, balanced)")
            print("3. claude-3-5-haiku (fastest, most efficient)")
            print("4. claude-3-opus (highest quality, more expensive)")
            print("5. Use default")
            model_choice = input("Choose a model (1-5): ").strip()
            
            claude_model_map = {
                '1': 'claude-sonnet-4-20250514',
                '2': 'claude-3-5-sonnet-20241022',
                '3': 'claude-3-5-haiku-20241022',
                '4': 'claude-3-opus-20240229',
                '5': None
            }
            
            if model_choice in claude_model_map:
                current_settings['model'] = claude_model_map[model_choice]
                model_name = current_settings['model'] or DEFAULT_CLAUDE_MODEL
                print(f" Updated model to {model_name}")
            else:
                print("❌ Invalid choice. Settings not changed.")
    
    elif choice == '4':
        try:
            temp = float(input(f"Enter temperature (0.0-1.0, current: {current_settings['temperature']}): "))
            if 0.0 <= temp <= 1.0:
                current_settings['temperature'] = temp
                print(f" Updated temperature to {temp}")
            else:
                print("❌ Invalid input. Please enter a number between 0.0 and 1.0.")
        except ValueError:
            print("❌ Invalid input. Please enter a number.")
    
    elif choice == '5':
        show = input(f"Show sources? (y/n, current: {'yes' if current_settings['show_sources'] else 'no'}): ").strip().lower()
        if show in ('y', 'yes'):
            current_settings['show_sources'] = True
            print(" Sources will be shown")
        elif show in ('n', 'no'):
            current_settings['show_sources'] = False
            print(" Sources will be hidden")
        else:
            print("❌ Invalid input. Settings not changed.")
    
    elif choice == '6':
        return
    
    else:
        print("❌ Invalid choice.")
    
    # After updating settings, rebuild the pipeline if needed
    if choice in ('1', '2', '3', '4'):
        try:
            current_settings['retriever'], current_settings['chain'] = setup_rag_pipeline(
                top_k=current_settings['top_k'],
                model=current_settings['model'],
                temperature=current_settings['temperature'],
                provider=current_settings['provider']
            )
            print("\n Pipeline updated with new settings")
        except Exception as e:
            print(f"\n❌ Error updating pipeline: {str(e)}")
            print("Please check your settings and API keys.")

def main():
    """Main application loop"""
    print_banner()
    
    # Initialize settings with available provider
    provider = DEFAULT_LLM_PROVIDER if DEFAULT_LLM_PROVIDER in available_providers else available_providers[0]
    
    # Initialize settings
    settings = {
        'top_k': DEFAULT_TOP_K,
        'model': None,  # Use provider default
        'temperature': DEFAULT_TEMPERATURE,
        'show_sources': True,
        'provider': provider
    }
    
    # Set up the initial RAG pipeline
    try:
        settings['retriever'], settings['chain'] = setup_rag_pipeline(
            top_k=settings['top_k'],
            model=settings['model'],
            temperature=settings['temperature'],
            provider=settings['provider']
        )
        
        model_name = settings['model'] or (DEFAULT_CLAUDE_MODEL if settings['provider'] == 'claude' else DEFAULT_LLM_MODEL)
        print(f" System ready! Using {settings['provider']} ({model_name}) with {settings['top_k']} sources")
        print(f" Ask any question about options trading...")
        
    except Exception as e:
        print(f"❌ Error initializing the RAG pipeline: {str(e)}")
        print("Please check your settings and API keys.")
        return
    
    while True:
        print("\n" + "-"*80)
        query = input("\nEnter your question (or 'exit' to quit, 'config' for settings): ").strip()
        
        if not query:
            continue
        
        if query.lower() in ('exit', 'quit', 'q'):
            print("Goodbye!")
            break
        
        if query.lower() == 'config':
            config_menu(settings)
            continue
        
        print(f"\nProcessing: '{query}'")
        print(f"Retrieving {settings['top_k']} most relevant sources...")
        
        try:
            # Run the query
            result = run_rag_query(
                settings['retriever'], 
                settings['chain'], 
                query
            )
            
            # Display the result
            display_answer(result, show_sources=settings['show_sources'])
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            print("Please try again or check your settings.")

if __name__ == "__main__":
    main() 