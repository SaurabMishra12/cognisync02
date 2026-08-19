"""
fix_systems_close.py
Inserts the missing closing '}' for the SYSTEMS dict inside the
SRC_SYSTEMS block of build_neurips_notebook.py.
"""
from pathlib import Path

src = Path("build_neurips_notebook.py").read_text(encoding="utf-8")

# The last line of the SYSTEMS dict that the patch wrote
MARKER = "    \"    'CogniSync (Hybrid)':  CogniSyncHybrid,\\n\"\n"
AFTER  = "\n"   # blank line before SRC_RETRIEVAL (or before the closing paren we already inserted)

pos = src.find(MARKER)
if pos == -1:
    print("ERROR: marker not found")
    exit(1)

end_of_marker = pos + len(MARKER)
# What comes immediately after?
snippet = src[end_of_marker:end_of_marker+120]
print("After SYSTEMS dict line:")
print(repr(snippet))

# We need to insert  "\"}\"\n"  right after the marker
CLOSE_LINES = (
    "    \"}\\n\"\n"
    "    \"\\n\"\n"
    "    \"print(f'Systems: {list(SYSTEMS.keys())}')\\n\"\n"
)

if '"}"' in snippet or '"}\\"' in snippet or '\"}\n\"' in src[end_of_marker:end_of_marker+20]:
    print("Closing } already present — skipping")
else:
    new_src = src[:end_of_marker] + CLOSE_LINES + src[end_of_marker:]
    Path("build_neurips_notebook.py").write_text(new_src, encoding="utf-8")
    print("Fixed: inserted SYSTEMS dict closing }")
