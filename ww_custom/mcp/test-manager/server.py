from fastmcp import FastMCP
import os
import json
import glob

# Initialize FastMCP server
mcp = FastMCP("Test Case Manager")

# Configuration paths
CONFIG_DIR = os.path.join(os.getcwd(), "ww_custom", "config")
CONFIG_FILE = os.path.join(CONFIG_DIR, "qa_config.json")

def _load_config():
    """Load the QA status configuration."""
    if not os.path.exists(CONFIG_FILE):
        return {}
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}

def _save_config(config_data):
    """Save the QA status configuration."""
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config_data, f, indent=2)

@mcp.tool()
def check_tc_config() -> str:
    """
    Checks if the Test Case (TC) repository is configured.
    Returns a status message indicating if the config is valid or missing.
    """
    config = _load_config()
    repo_path = config.get("tc_repo_path")
    
    if not repo_path:
        return "MISSING_CONFIG: TC repository path is not configured."
    
    if not os.path.exists(repo_path):
        return f"INVALID_CONFIG: The configured path '{repo_path}' does not exist on the file system."
        
    return f"OK: TC repository is configured at '{repo_path}'."

@mcp.tool()
def setup_tc_repo(path: str) -> str:
    """
    Sets up a new Test Case repository or configures an existing one.
    
    Args:
        path: The absolute path to the folder where TCs will be stored.
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(path, exist_ok=True)
        
        # Save to config
        config = _load_config()
        config["tc_repo_path"] = path
        _save_config(config)
        
        return f"SUCCESS: TC repository configured at '{path}'."
    except Exception as e:
        return f"ERROR: Failed to setup TC repo. {str(e)}"

@mcp.tool()
def search_past_tcs(query: str) -> str:
    """
    Searches for past Test Cases in the configured repository.
    Currently supports filename and simple text content search.
    
    Args:
        query: The search keyword (e.g., 'login', 'payment setup').
    """
    config = _load_config()
    repo_path = config.get("tc_repo_path")
    
    if not repo_path or not os.path.exists(repo_path):
        return "ERROR: TC repository is not valid. Please run `setup_tc_repo` first."
    
    results = []
    try:
        # Search for markdown and text files
        files = glob.glob(os.path.join(repo_path, "**/*.md"), recursive=True) + \
                glob.glob(os.path.join(repo_path, "**/*.txt"), recursive=True)
                
        for file_path in files:
            # Simple filename check
            filename = os.path.basename(file_path)
            if query.lower() in filename.lower():
                results.append(f"[FILE_MATCH] {filename}")
                continue
                
            # Content check (read first 1000 chars for efficiency)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read(1000)
                    if query.lower() in content.lower():
                        results.append(f"[CONTENT_MATCH] {filename}")
            except:
                continue
                
        if not results:
            return "No matching Test Cases found."
            
        return "Found similar Test Cases:\n" + "\n".join(results[:10]) # Limit to 10 results
        
    except Exception as e:
        return f"ERROR: Search failed. {str(e)}"

@mcp.tool()
def save_new_tc(filename: str, content: str) -> str:
    """
    Saves a new Test Case to the repository.
    
    Args:
        filename: Name of the file (e.g., 'TC_LOGIN_001.md').
        content: The full markdown content of the TC.
    """
    config = _load_config()
    repo_path = config.get("tc_repo_path")
    
    if not repo_path or not os.path.exists(repo_path):
        return "ERROR: TC repository is not valid. Please run `setup_tc_repo` first."
        
    try:
        full_path = os.path.join(repo_path, filename)
        
        # Check if file exists to prevent accidental overwrite (basic safety)
        if os.path.exists(full_path):
            return f"WARNING: File '{filename}' already exists. Please choose a different name or explicitly confirm overwrite."
            
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        return f"SUCCESS: Test case saved to '{full_path}'."
        
    except Exception as e:
        return f"ERROR: Failed to save file. {str(e)}"

if __name__ == "__main__":
    mcp.run()
