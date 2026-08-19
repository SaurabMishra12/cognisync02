from mcp.server.fastmcp import FastMCP
import database
import ingest

# Initialize the Native MCP Server Interface
mcp = FastMCP("Faraday Context Server")

@mcp.tool()
def search_faraday_brain(query: str, limit: int = 5) -> str:
    """
    Search Saurab's local personal database. 
    Use this tool whenever you need context about Saurab's past actions, history, architecture, emails, or personal projects.
    
    Args:
        query: The semantic search string (e.g. 'What was Saurab working on yesterday?')
        limit: Max results to return.
    """
    results = database.query_hybrid(query, limit)
    
    output = "=== FARADAY KNOWLEDGE BASE ===\n"
    for r in results["results"]:
        content = r.get("content", "")
        source = r.get("metadata", {}).get("source", "Unknown Source")
        output += f"--- SOURCE: {source} ---\n{content}\n\n"
        
    return output

@mcp.tool()
def sync_faraday_brain() -> str:
    """
    Ingest and sync all documents from the local Obsidian vault into the Faraday Database.
    Call this tool when Saurab asks you to sync, ingest, or update the Faraday database.
    """
    try:
        import sys
        import threading
        sys.stderr.write("Starting Faraday ingestion process in background...\n")
        
        # Dispatch to background thread so it doesn't freeze the IDE / MCP client protocol timeout
        threading.Thread(target=ingest.chunk_and_embed, daemon=True).start()
        
        return "✅ Sync has successfully started in the background! It will process and embed all documents quietly. You can seamlessly continue your work and run searches!"
    except Exception as e:
        return f"❌ Sync failed to start: {e}"

if __name__ == "__main__":
    # Running via stdio turns this into a zero-port native MCP server for Antigravity/Cursor
    mcp.run(transport="stdio")
