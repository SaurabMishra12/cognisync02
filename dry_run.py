import json
import ast

def check_notebook(filepath):
    print(f"Checking notebook: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        nb = json.load(f)

    full_code = ""
    for c in nb.get("cells", []):
        if c.get("cell_type") == "code":
            source = "".join(c.get("source", []))
            # replace colab shell magic to prevent ast failure
            source = source.replace("!pip", "#!pip")
            full_code += source + "\n\n"
            
            try:
                ast.parse(source)
            except SyntaxError as e:
                print(f"SyntaxError in cell:\n{source}\nError: {e}")
                return False

    print("Syntax check passed. Semantic/Variable check...")
    
    try:
        compile(full_code, "notebook.py", "exec")
        print("Compilation check passed!")
    except Exception as e:
        print(f"Compilation error: {e}")
        return False
        
    return True

if __name__ == "__main__":
    if check_notebook("CogniSync_v3_strong.ipynb"):
        print("SUCCESS: Notebook is syntactically sound.")
    else:
        print("FAILED.")
