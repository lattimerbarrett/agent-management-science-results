from pathlib import Path
text=Path('record/finals.md').read_text()
code=text.split('```python\n',1)[1].split('```',1)[0]
exec(compile(code,'embedded-final','exec'),{'__name__':'__main__'})
