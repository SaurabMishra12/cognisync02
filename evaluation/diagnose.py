"""diagnose.py — find the real cause of SyntaxError in build_neurips_notebook.py"""
import ast, pathlib, sys

src = pathlib.Path("build_neurips_notebook.py").read_text(encoding="utf-8")
try:
    ast.parse(src)
    print("No syntax errors found!")
except SyntaxError as e:
    print(f"SyntaxError at line {e.lineno}: {e.msg}")
    lines = src.splitlines()
    for i in range(max(0, e.lineno-4), min(len(lines), e.lineno+3)):
        marker = ">>>" if i+1 == e.lineno else "   "
        print(f"{marker} {i+1:4d}: {lines[i]}")
