import json

with open("CogniSync_v3_kaggle.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)

# Create a new cell to clean cache
clean_cell = {
  "cell_type": "code",
  "execution_count": None,
  "metadata": {},
  "outputs": [],
  "source": [
    "import os\n",
    "import shutil\n",
    "# Clear corrupted cache and locks from previous failed runs\n",
    "cache_dir = os.path.expanduser('~/.cache/huggingface/datasets')\n",
    "print('Cleaning corrupted HF datasets cache lock files...')\n",
    "if os.path.exists(cache_dir):\n",
    "    for root, dirs, files in os.walk(cache_dir):\n",
    "        for f in files:\n",
    "            if f.endswith('.lock'):\n",
    "                try:\n",
    "                    os.remove(os.path.join(root, f))\n",
    "                except: pass\n",
    "    nq_path = os.path.join(cache_dir, 'natural_questions')\n",
    "    if os.path.exists(nq_path):\n",
    "        shutil.rmtree(nq_path, ignore_errors=True)\n",
    "        print('Removed old natural_questions cache (freed ~50GB!)')\n",
    "else:\n",
    "    print('Cache clear ready.')\n"
  ]
}

# Insert cleanly after the imports cell (which is indexing at 2)
nb["cells"].insert(3, clean_cell)

with open("CogniSync_v3_kaggle.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=2)

print("Added cache cleaning cell to notebook.")
