import os
import glob
from bs4 import BeautifulSoup

DATALAKE_LLM_DIR = r"c:\Users\msaur\OneDrive\Desktop\Obsidian\obsidian\Faraday\03 - Data Lake\llm_chats"
INBOX_DIR = r"c:\Users\msaur\OneDrive\Desktop\Obsidian\obsidian\Faraday\00 - Inbox"

def find_gemini_html():
    search_path = os.path.join(DATALAKE_LLM_DIR, "**", "My Activity.html")
    files = glob.glob(search_path, recursive=True)
    if not files:
        print("Could not find My Activity.html in the Data Lake")
        return None
    return files[0]

def parse_and_convert():
    activity_file = find_gemini_html()
    if not activity_file:
        return
        
    print(f"Parsing {activity_file}...")
    output_md = os.path.join(INBOX_DIR, "Gemini_History.md")
    
    try:
        with open(activity_file, 'r', encoding='utf-8', errors='ignore') as f:
            html_content = f.read()
            
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Google Takeout Activity wraps interactions in cards.
        # We will extract text from all div/p tags, filtering empty ones.
        # To avoid giant non-stop text, we split by common Google Takeout structure 'mdl-grid' or just by breaks.
        
        # Usually, outer-cell wrappers hold each query
        interaction_divs = soup.find_all('div', class_='outer-cell')
        
        if not interaction_divs:
            # Fallback if classes are missing
            print("No outer-cell divs found. Falling back to body text dump.")
            raw_text = soup.get_text(separator='\n\n', strip=True)
            with open(output_md, 'w', encoding='utf-8') as f:
                f.write("# Gemini History\n\n")
                f.write(raw_text)
            print("Saved fallback Markdown dump.")
            return

        print(f"Found {len(interaction_divs)} interaction cards.")
        markdown = "# Gemini Chat History\n\n"
        
        for idx, div in enumerate(interaction_divs):
            text = div.get_text(separator=' ', strip=True)
            # Remove giant boilerplate if present
            if text:
                markdown += f"### Interaction {idx+1}\n"
                markdown += f"{text}\n\n---\n\n"
                
        with open(output_md, 'w', encoding='utf-8') as f:
            f.write(markdown)
            
        print(f"Successfully converted Gemini history into: {output_md}")
        
    except Exception as e:
        print(f"Failed parsing: {e}")

if __name__ == "__main__":
    parse_and_convert()
