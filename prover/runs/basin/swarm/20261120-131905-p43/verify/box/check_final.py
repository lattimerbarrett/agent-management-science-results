from pathlib import Path
text=Path('record/finals.md').read_text()
code=text.split('```python',1)[1].split('```',1)[0]
exec(compile(code, 'record/finals.md:python', 'exec'))
