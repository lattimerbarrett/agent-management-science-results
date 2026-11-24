from pathlib import Path
s=Path('record/finals.md').read_text()
code=s.split('```python\n',1)[1].split('```',1)[0]
exec(compile(code, 'final_certificate.py', 'exec'), {'__name__':'__main__'})
