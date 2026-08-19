import os
import requests
import google.generativeai as genai
import argparse

# Configuration
FARADAY_URL = "http://127.0.0.1:8000/search"
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

def get_faraday_context(query_text: str):
    """Hits your secure local Faraday Server to extract your life's context."""
    print("🧠 Querying Faraday Brain...")
    try:
        response = requests.post(FARADAY_URL, json={"query": query_text, "limit": 5})
        if response.status_code == 200:
            data = response.json()
            context_blocks = []
            for item in data.get("context", []):
                # Standardize the output, whether it's text or image references
                content = item.get("content", "No content")
                source = item.get("metadata", {}).get("source", "Unknown Source")
                if source is None:
                    source = "Unknown Source"
                context_blocks.append(f"--- SOURCE: {source} ---\n{content}\n")
                
            context_bundle = "\n".join(context_blocks)
            print(f"✅ Successfully retrieved {len(context_blocks)} chunks of local memory!")
            print(f"[Preview of Injected Context]:\n{context_bundle[:300]}...\n")
            return context_bundle
        else:
            print(f"⚠️ Faraday Server returned Error: {response.text}")
            return ""
    except requests.exceptions.ConnectionError:
        print("❌ CRITICAL ERROR: Could not connect to Faraday Server. Is it running on port 8000?")
        return ""

def call_gemini(system_context: str, user_prompt: str):
    """Sends the bundled mega-prompt securely to Gemini's API."""
    if not GEMINI_API_KEY:
        print("❌ ERROR: GEMINI_API_KEY environment variable is not set.")
        print("Please set your API key using: setx GEMINI_API_KEY 'your-key-here'")
        return

    genai.configure(api_key=GEMINI_API_KEY)
    
    # We use Gemini 1.5 Pro to handle the massive context windows we are injecting
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    
    mega_prompt = f"""
You are Saurab's highly intelligent Personal Agent. 
You are equipped with 'Faraday', a local vector database containing his exact chat history, notes, code, and career goals.

=== FARADAY CONTEXT DEEP DIVE ===
The following information was semantically matched from Saurab's local computer. Use this as absolute truth to answer his query:
{system_context}
================================

Saurab's Query: {user_prompt}
"""
    
    print("☁️ Sending context-injected prompt to Gemini Cloud...")
    try:
        response = model.generate_content(mega_prompt)
        print("\n================== GEMINI RESPONSE ==================\n")
        print(response.text)
        print("\n=====================================================\n")
    except Exception as e:
        print(f"Failed to communicate with Gemini API: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Faraday Dynamic Proxy Agent")
    parser.add_argument("query", type=str, help="Your question/prompt for Gemini")
    
    args = parser.parse_args()
    
    context = get_faraday_context(args.query)
    call_gemini(context, args.query)
