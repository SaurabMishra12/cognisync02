import os
import argparse
from tqdm import tqdm

from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader, UnstructuredWordDocumentLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

FARADAY_VAULT = r"c:\Users\msaur\OneDrive\Desktop\Obsidian\obsidian\Faraday"
CHROMA_DB_DIR = os.path.join(FARADAY_VAULT, ".chroma")

def get_loaders():
    # We use glob patterns to load all relevant files while skipping `.chroma/` and `scripts/`
    print("Loading documents from Faraday Vault...")
    
    # Loaders for different file types
    md_loader = DirectoryLoader(FARADAY_VAULT, glob="**/*.md", loader_cls=TextLoader, exclude=["*.chroma*", "scripts/*"])
    txt_loader = DirectoryLoader(FARADAY_VAULT, glob="**/*.txt", loader_cls=TextLoader, exclude=["*.chroma*", "scripts/*"])
    pdf_loader = DirectoryLoader(FARADAY_VAULT, glob="**/*.pdf", loader_cls=PyPDFLoader, exclude=["*.chroma*", "scripts/*"])
    
    docs = []
    for loader in [md_loader, txt_loader, pdf_loader]:
        try:
            docs.extend(loader.load())
        except Exception as e:
            print(f"Warning: Issue loading some documents - {e}")
            
    print(f"Loaded {len(docs)} documents.")
    return docs

def split_documents(docs):
    print("Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_documents(docs)
    print(f"Split down into {len(chunks)} conceptual chunks.")
    return chunks

def extract_and_embed():
    docs = get_loaders()
    if not docs:
        print("No documents found in Faraday vault.")
        return

    chunks = split_documents(docs)

    print("Initializing Local Embeddings (all-MiniLM-L6-v2) - WARNING: This might take a moment on first run to download model weights.")
    # Local open-source embeddings, no API keys necessary.
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    print(f"Building ChromaDB at {CHROMA_DB_DIR}...")
    
    # We use from_documents to ingest. For an existing DB, we can use Chroma initially.
    # To prevent massive memory spikes, Chroma is relatively efficient, but we will let LangChain handle it.
    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DB_DIR
    )
    db.persist()
    print("✅ Indexing Complete! You now have a complete Vector Brain.")

def query_brain(query: str):
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma(persist_directory=CHROMA_DB_DIR, embedding_function=embeddings)
    
    results = db.similarity_search_with_relevance_scores(query, k=5)
    
    print(f"\n🧠 Querying Vector Brain for: '{query}'\n")
    if not results:
        print("No results found.")
        return
        
    for doc, score in results:
        print(f"--- [Score: {score:.3f}] Source: {doc.metadata.get('source', 'Unknown')} ---")
        # Print a snippet
        snippet = doc.page_content.replace("\n", " ").strip()[:300]
        print(f"{snippet}...\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Faraday Vector Brain CLI")
    parser.add_argument("--build", action="store_true", help="Parse Faraday vault and build the vector database.")
    parser.add_argument("--query", type=str, help="Search the vault semantically.")
    
    args = parser.parse_args()
    
    if args.build:
        extract_and_embed()
    elif args.query:
        query_brain(args.query)
    else:
        print("Usage: python build_vector_brain.py --build  OR  python build_vector_brain.py --query \"Your search here\"")
