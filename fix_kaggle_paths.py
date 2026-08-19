import json

with open("CogniSync_v3_kaggle.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)

for c in nb["cells"]:
    if c["cell_type"] == "code":
        for i, line in enumerate(c["source"]):
            # Swap Colab paths to Kaggle native output paths
            if "/content/" in line:
                c["source"][i] = line.replace("/content/", "/kaggle/working/")
            elif "/content" in line:
                c["source"][i] = line.replace("/content", "/kaggle/working")
                
            # Disable Colab-specific download magic which crashes Kaggle
            if "from google.colab import files" in line:
                c["source"][i] = "# from google.colab import files (disabled for Kaggle)\n"
            if "files.download" in line:
                c["source"][i] = line.replace("files.download", "# files.download")

with open("CogniSync_v3_kaggle.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=2)

print("Patched output directories to /kaggle/working/!")
