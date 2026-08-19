import json

nb_path = r"c:\Users\msaur\OneDrive\Desktop\Obsidian\obsidian\Faraday\githubpush_cogniSync\CogniSync_Final_CIKM_Ablations.ipynb"
md_path = r"c:\Users\msaur\OneDrive\Desktop\Obsidian\obsidian\Faraday\githubpush_cogniSync\pseudocode_and_hyperparameters.md"

with open(nb_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

with open(md_path, "r", encoding="utf-8") as f:
    md_content = f.read()

# Prepend markdown cell with pseudocode
new_md_cell = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [line + "\n" for line in md_content.split("\n")]
}

disclaimer = {
    "cell_type": "markdown",
    "metadata": {},
    "source": ["# Code Redacted for Double-Blind Review\n\n", "The exact Python implementation has been redacted to preserve double-blind anonymity for CIKM 2026. The cell outputs below (generated during our T4 GPU execution) are preserved to demonstrate the execution trace. The architectural logic is represented by the following pseudocode and hyperparameters:\n\n"]
}

# Scrub the code cells
for cell in nb["cells"]:
    if cell["cell_type"] == "code":
        # Keep empty cells empty
        if len(cell["source"]) > 0:
            cell["source"] = ["# [REDACTED FOR DOUBLE-BLIND REVIEW]\n", "# Please refer to the pseudocode above for the exact logic implementation."]

# Insert disclaimer and pseudocode at the top
nb["cells"].insert(0, new_md_cell)
nb["cells"].insert(0, disclaimer)

with open(nb_path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1)

print("Notebook redacted successfully.")
