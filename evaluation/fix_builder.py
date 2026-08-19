"""
fix_builder_paren.py — finds and fixes the missing closing paren on SRC_SYSTEMS
"""
from pathlib import Path

src = Path("build_neurips_notebook.py").read_text(encoding="utf-8")

sys_start  = src.index("SRC_SYSTEMS = (")
next_start = src.index("SRC_RETRIEVAL = (", sys_start)

tail = src[next_start - 80 : next_start]
print("Tail before SRC_RETRIEVAL:")
print(repr(tail))

if ")\n\n" in tail:
    print("Closing ) already present — builder looks OK")
else:
    print("MISSING closing ) — inserting now")
    new_src = src[:next_start] + ")\n\n" + src[next_start:]
    Path("build_neurips_notebook.py").write_text(new_src, encoding="utf-8")
    print("Fixed!")
