"""fix_syntax.py — patches the backslash-continuation issue in build_neurips_notebook.py"""
from pathlib import Path

p = Path("build_neurips_notebook.py")
content = p.read_text(encoding="utf-8")

# The issue: code("""\  (backslash after opening triple-quote)
# Python's parser sees this as a line continuation INSIDE the source file,
# which is NOT what we want inside a triple-quoted string of a builder script.
# Replace with plain code("""
before = 'code("""\\\n'
after  = 'code("""\n'
count  = content.count(before)
fixed  = content.replace(before, after)
p.write_text(fixed, encoding="utf-8")
print(f"Fixed {count} occurrence(s) of backslash-continuation in code() calls.")
