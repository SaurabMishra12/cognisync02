import os
import glob
import uuid
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
import database

FARADAY_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INBOX_DIR = os.path.join(FARADAY_BASE, "00 - Inbox")
WIKI_DIR = os.path.join(FARADAY_BASE, "02 - Wiki")

def load_documents():
    print("Loading Markdown logs...")
    docs = []
    
    search_paths = [
        os.path.join(WIKI_DIR, "**", "*.md"),
        os.path.join(INBOX_DIR, "**", "*.md")
    ]
    
    for pattern in search_paths:
        for file in glob.glob(pattern, recursive=True):
            if ".qdrant" in file or "faraday-server" in file:
                continue
            try:
                loader = TextLoader(file, encoding='utf-8')
                docs.extend(loader.load())
            except Exception as e:
                print(f"Failed to load {file}: {e}")
                
    return docs

def chunk_and_embed():
    docs = load_documents()
    if not docs:
        print("No documents found.")
        return

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(docs)
    
    print(f"Chunked into {len(chunks)} blocks. Feeding to Qdrant Database...")
    
    documents = [c.page_content for c in chunks]
    metadatas = [c.metadata for c in chunks]
    
    # Qdrant requires UUIDs or integers
    ids = [str(uuid.uuid4()) for _ in range(len(chunks))]
    
    database.ingest_text(documents, metadatas, ids)
    
    print("✅ Ingestion Complete! Data is now live in Qdrant.")

if __name__ == "__main__":
    chunk_and_embed()
