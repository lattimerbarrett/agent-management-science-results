from pathlib import Path
# Run the final submitted code verbatim (the first Python fenced block).
text = Path('record/finals.md').read_text()
code = text.split('```python\n', 1)[1].split('```', 1)[0]
exec(compile(code, 'submitted_final.py', 'exec'), {'__name__':'__main__'})
