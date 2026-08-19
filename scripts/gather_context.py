import os
import datetime
import json
import requests
import PyPDF2
from docx import Document
from bs4 import BeautifulSoup

# --- CONFIGURATION ---
FARADAY_INBOX = r"c:\Users\msaur\OneDrive\Desktop\Obsidian\obsidian\Faraday\00 - Inbox"
GITHUB_USERNAME = "SaurabMishra12"
MEDIUM_USERNAME = "@saurabmishra"
# We bound the local search specifically to the Inbox to keep it lightning fast.
# Any PDFs or documents you want parsed (like LinkedIn) should be dropped here.
SCAN_DIRECTORIES = [
    FARADAY_INBOX
]
KEYWORDS = ["saurab", "mishra", "resume", "cv", "profile", "linkedin", "pdf"]

def extract_pdf_text(filepath):
    text = ""
    try:
        with open(filepath, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error reading PDF {filepath}: {e}")
    return text

def extract_docx_text(filepath):
    text = ""
    try:
        doc = Document(filepath)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        print(f"Error reading DOCX {filepath}: {e}")
    return text

def scan_local_files():
    print("Scanning local files (Desktop, Documents, Inbox)...")
    found_context = []
    
    for directory in SCAN_DIRECTORIES:
        if not os.path.exists(directory):
            continue
            
        for root, _, files in os.walk(directory):
            # Limit depth or skip hidden dirs to speed up
            if any(part.startswith('.') for part in root.split(os.sep)):
                continue
                
            for file in files:
                filepath = os.path.join(root, file)
                filename_lower = file.lower()
                
                # Check if it's a file of interest
                if any(k in filename_lower for k in KEYWORDS) or "linkedin" in filename_lower:
                    if filename_lower.endswith(".pdf"):
                        print(f"Parsing PDF: {file}")
                        text = extract_pdf_text(filepath)
                        found_context.append(f"### Source: {file}\n```\n{text[:2000]}...\n```\n")
                    elif filename_lower.endswith(".docx"):
                        print(f"Parsing DOCX: {file}")
                        text = extract_docx_text(filepath)
                        found_context.append(f"### Source: {file}\n```\n{text[:2000]}...\n```\n")
                    elif filename_lower.endswith((".md", ".txt")):
                        print(f"Parsing TXT/MD: {file}")
                        try:
                            with open(filepath, 'r', encoding='utf-8') as f:
                                text = f.read()
                                found_context.append(f"### Source: {file}\n```\n{text[:2000]}...\n```\n")
                        except:
                            pass
    return "\n".join(found_context)

def get_github_context():
    print("Fetching GitHub context...")
    context = ""
    try:
        # User details
        resp = requests.get(f"https://api.github.com/users/{GITHUB_USERNAME}").json()
        if "message" not in resp:
            context += f"**Bio:** {resp.get('bio', '')}\n"
            context += f"**Public Repos:** {resp.get('public_repos', 0)}\n\n"
        
        # Repo details
        repos = requests.get(f"https://api.github.com/users/{GITHUB_USERNAME}/repos?sort=updated&per_page=5").json()
        if isinstance(repos, list):
            context += "#### Recent Repositories:\n"
            for r in repos:
                context += f"- **{r.get('name')}**: {r.get('description', 'No description')} *(Language: {r.get('language')})*\n"
    except Exception as e:
        print(f"GitHub fetch failed: {e}")
    return context

def get_medium_context():
    print("Fetching Medium context (via RSS)...")
    context = "#### Recent Medium Articles:\n"
    try:
        # Medium RSS feeds are easier to parse than their JS-heavy HTML
        resp = requests.get(f"https://medium.com/feed/{MEDIUM_USERNAME}")
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, 'xml')
            items = soup.find_all('item')
            for item in items[:5]: # Top 5 articles
                title = item.title.text if item.title else "Untitled"
                link = item.link.text if item.link else ""
                context += f"- [{title}]({link})\n"
    except Exception as e:
        print(f"Medium fetch failed: {e}")
    return context

def main():
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    output_path = os.path.join(FARADAY_INBOX, f"context_dump_{date_str}.md")
    
    print("Starting context compilation...")
    markdown_output = f"---\ntitle: Context Dump {date_str}\ntype: brain-dump\n---\n\n# Context Dump ({date_str})\n\n"
    
    markdown_output += "## 1. Local Files & LinkedIn\n"
    markdown_output += scan_local_files() + "\n\n"
    
    markdown_output += "## 2. GitHub Profile\n"
    markdown_output += get_github_context() + "\n\n"
    
    markdown_output += "## 3. Medium & Portfolio\n"
    markdown_output += get_medium_context() + "\n\n"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown_output)
        
    print(f"\n[SUCCESS] Compiled context saved to:\n{output_path}")
    print("\n[NEXT STEP] To use this: Tell Antigravity 'Ingest my latest context dump'")

if __name__ == "__main__":
    main()
